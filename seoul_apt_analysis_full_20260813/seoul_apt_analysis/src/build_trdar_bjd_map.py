"""
상권 -> 법정동 공간조인 매핑 생성기
====================================

영역-상권 폴리곤과 법정동(읍면동) 경계 폴리곤을 면적 기준으로 겹쳐,
각 상권이 어느 법정동에 얼마나 걸쳐 있는지 계산한다.

이름 규칙 매칭(개포1동 -> 개포동)이나 연결요소 클러스터 방식은 모두 실패했다.
    - 이름 매칭: 400개 중 83개만 일치, 거래 커버리지 84%
    - 연결요소: 일부 행정동이 두 법정동에 걸쳐 연쇄적으로 묶여
               중구 전체(6행정동x56법정동)가 한 덩어리가 됨
공간중첩은 배분 가정 없이 실제 겹치는 면적으로 나눈다.

산출물 (data/output/)
    trdar_bjd_map.csv        상권별 대표 법정동 (참고용)
    trdar_bjd_fragments.csv  전체 중첩 조각 + 겹침비율  <- build_panel.py 가 사용
"""

import sys
import geopandas as gpd

from paths import TRDAR_DIR, BJD_DIR, OUT, find_one

# 경계 파일의 컬럼명은 출처마다 다르므로 후보를 순서대로 탐색
CODE_HINTS = ['EMD_CD', 'ADM_CD', 'BJD_CD', 'LEGALCD', '법정동코드']
NAME_HINTS = ['EMD_KOR_NM', 'EMD_NM', 'ADM_NM', 'BJD_NM', '법정동명']

# 법정동 경계 파일에 .prj 가 없을 때 가정할 좌표계.
# GIS Developer 등에서 배포하는 전국 행정구역 SHP는 관례적으로 UTM-K를 쓴다.
ASSUMED_CRS = 5179


def pick_col(cols, hints, kind):
    for h in hints:
        for c in cols:
            if c.upper() == h.upper():
                return c
    for h in hints:
        for c in cols:
            if h.upper() in c.upper():
                return c
    raise KeyError(f'{kind} 컬럼을 찾지 못했습니다. 실제 컬럼: {list(cols)}')


def read_shp(path):
    """국내 경계자료는 대개 CP949. UTF-8로 저장된 것도 있어 순서대로 시도한다."""
    for enc in ('cp949', 'utf-8'):
        try:
            return gpd.read_file(path, encoding=enc), enc
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f'인코딩 판별 실패: {path}')


def fix_invalid(gdf, label):
    """자기교차 등 불량 폴리곤이 있으면 overlay가 실패하므로 먼저 보정."""
    bad = ~gdf.is_valid
    if bad.any():
        print(f'  {label} 불량 폴리곤 {bad.sum()}개 보정')
        gdf.loc[bad, 'geometry'] = gdf.loc[bad, 'geometry'].make_valid()
        still = ~gdf.is_valid
        if still.any():
            gdf.loc[still, 'geometry'] = gdf.loc[still, 'geometry'].buffer(0)
    return gdf


def main():
    print('[1] 상권 폴리곤')
    trdar, _ = read_shp(find_one(TRDAR_DIR, '*.shp'))
    print(f'  {len(trdar):,}개, CRS={trdar.crs}')

    print('\n[2] 법정동 경계')
    bjd_path = sys.argv[1] if len(sys.argv) > 1 else find_one(BJD_DIR, '*.shp')
    bjd, enc = read_shp(bjd_path)
    print(f'  {bjd_path.name if hasattr(bjd_path, "name") else bjd_path}  '
          f'{len(bjd):,}개, CRS={bjd.crs}, 인코딩={enc}')

    code_col = pick_col(bjd.columns, CODE_HINTS, '법정동코드')
    name_col = pick_col(bjd.columns, NAME_HINTS, '법정동명')
    print(f'  코드="{code_col}", 이름="{name_col}"')

    if bjd.crs is None:
        print(f'  ! CRS 정보 없음 -> EPSG:{ASSUMED_CRS} 로 가정')
        bjd = bjd.set_crs(ASSUMED_CRS)
    if bjd.crs != trdar.crs:
        print(f'  좌표계 변환: {bjd.crs} -> {trdar.crs}')
        bjd = bjd.to_crs(trdar.crs)

    bjd[code_col] = bjd[code_col].astype(str)
    bjd = bjd[bjd[code_col].str.startswith('11')]        # 서울만
    print(f'  서울 필터 후 {len(bjd):,}개')

    print('\n[3] 면적 중첩')
    t = trdar[['TRDAR_CD', 'TRDAR_CD_N', 'SIGNGU_CD_', 'ADSTRD_CD_', 'geometry']].copy()
    t.columns = ['상권_코드', '상권_코드_명', '자치구_코드_명', '행정동_코드_명', 'geometry']
    b = bjd[[code_col, name_col, 'geometry']].copy()
    b.columns = ['법정동코드', '법정동명', 'geometry']

    t, b = fix_invalid(t, '상권'), fix_invalid(b, '법정동')

    ov = gpd.overlay(t, b, how='intersection', keep_geom_type=False)
    ov['겹침면적'] = ov.geometry.area
    ov['겹침비율'] = (ov['겹침면적'] / ov.groupby('상권_코드')['겹침면적'].transform('sum')).round(4)
    print(f'  조각 {len(ov):,}개')

    frag = ov[['상권_코드', '법정동코드', '법정동명', '겹침면적', '겹침비율']]
    frag.to_csv(OUT / 'trdar_bjd_fragments.csv', index=False, encoding='utf-8-sig')

    best = (ov.sort_values('겹침면적', ascending=False)
              .drop_duplicates('상권_코드')
              [['상권_코드', '상권_코드_명', '자치구_코드_명', '행정동_코드_명',
                '법정동코드', '법정동명', '겹침면적', '겹침비율']]
              .sort_values('상권_코드'))
    best.to_csv(OUT / 'trdar_bjd_map.csv', index=False, encoding='utf-8-sig')

    print('\n[4] 결과')
    print(f'  매핑된 상권 {len(best):,}/{len(trdar):,} ({len(best)/len(trdar)*100:.1f}%)')
    print(f'  고유 법정동 {best["법정동명"].nunique()}개')
    print(f'  겹침비율 중앙값 {best["겹침비율"].median():.3f}  '
          f'(여러 법정동에 걸친 상권 {(best["겹침비율"] < 0.5).sum()}개)')
    print(f'  저장 -> {OUT.name}/trdar_bjd_fragments.csv, trdar_bjd_map.csv')


if __name__ == '__main__':
    main()
