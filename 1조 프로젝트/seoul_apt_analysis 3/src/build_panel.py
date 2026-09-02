"""
아파트 실거래가 x 상권 인구 통합 패널 생성기
=============================================

가격  국토부 실거래가 2021~2023  +  서울시 실거래가 2024~2026
인구  상권분석서비스 상주인구 / 길단위(유동)인구 / 직장인구
공간  build_trdar_bjd_map.py 가 만든 중첩 조각으로 상권 인구를 법정동에 면적 비례배분
조인  법정동코드 8자리 (서울시는 코드 조립, 국토부는 KIKmix로 이름 역조회)

산출물 (data/output/)
    panel_dong.csv   법정동 x 분기
    panel_gu.csv     자치구 x 분기

실행:  python build_panel.py
"""

import numpy as np
import pandas as pd

from paths import (MOLIT_DIR, SEOUL_DIR, POP_DIR, CODE_DIR, OUT,
                   smart_read, find_one, find_all)

QUARTERS = [int(f'{y}{q}') for y in range(2021, 2027) for q in range(1, 5)][:21]

# 국토부는 이 분기 '미만', 서울시는 '이상'만 쓴다.
#   국토부 파일은 계약일 기준으로 받아 2021~2023 계약분이 완전하고,
#   서울시 파일은 '접수연도' 기준이라 2024년 파일에 2023년 계약분이 일부만 섞인다.
#   연도로 중복제거하면 국토부 2023년치가 통째로 사라지므로 반드시 분기로 자를 것.
CUTOFF_Q = 20241

# 이보다 거래가 적은 법정동-분기는 중앙값이 불안정하다. 삭제하지 않고 플래그만 남긴다.
MIN_DEALS = 5


def to_quarter(ym):
    ym = pd.to_numeric(ym, errors='coerce')
    return (ym // 100 * 10 + (ym % 100 - 1) // 3 + 1).astype('Int64')


# ────────────────────────────────────────────────────────────
def load_bjd_ref():
    """행정안전부 KIKmix -> 법정동코드8 기준정보 + (자치구명, 법정동명) 역조회표"""
    mix = pd.read_excel(find_one(CODE_DIR, 'KIKmix*.xlsx'), dtype=str)
    mix = mix[(mix['시도명'] == '서울특별시') & mix['동리명'].notna()].copy()
    mix['코드8'] = mix['법정동코드'].str[:8]

    # 현재 유효한 매핑만 (말소된 행정동이 섞이면 중복 집계)
    ref = (mix[mix['말소일자'].isna()]
           .drop_duplicates('코드8')[['코드8', '시군구명', '동리명']]
           .rename(columns={'시군구명': '자치구명', '동리명': '법정동명'}))

    # 이름->코드는 말소분까지 포함해야 과거(2021년) 거래도 붙는다. 최신 코드 우선.
    name2code = (mix.sort_values('말소일자', na_position='first')
                    .drop_duplicates(['시군구명', '동리명'], keep='last')
                    .set_index(['시군구명', '동리명'])['코드8'])
    return ref, name2code


# ────────────────────────────────────────────────────────────
def load_molit(name2code):
    """국토부 파일: 안내문 15줄이 앞에 붙어 있고 코드 컬럼이 없다."""
    out = []
    for p in find_all(MOLIT_DIR, '아파트*.csv'):
        for enc in ('cp949', 'utf-8-sig'):
            try:
                lines = p.read_text(encoding=enc).splitlines(keepends=True)
                break
            except UnicodeDecodeError:
                continue
        hdr = next((i for i, l in enumerate(lines) if l.lstrip('﻿').startswith('"NO"')), 0)
        df = pd.read_csv(p, encoding=enc, skiprows=hdr, dtype=str)

        parts = df['시군구'].str.split(' ', n=2, expand=True)
        keep = parts[0] == '서울특별시'
        df, parts = df[keep], parts[keep]

        std = pd.DataFrame({
            '자치구명': parts[1].values,
            '법정동명': parts[2].values,
            '면적': pd.to_numeric(df['전용면적(㎡)'], errors='coerce').values,
            '금액': pd.to_numeric(df['거래금액(만원)'].str.replace(',', ''), errors='coerce').values,
            '계약년월': df['계약년월'].values,
            '건축년도': pd.to_numeric(df['건축년도'], errors='coerce').values,
            '취소': df['해제사유발생일'].replace('-', np.nan).values,
        })
        std['코드8'] = pd.MultiIndex.from_arrays([std['자치구명'], std['법정동명']]).map(name2code)
        out.append(std)
        print(f'  [국토부] {p.name:42s} {len(std):>7,}건  '
              f'{sorted(std["계약년월"].str[:4].unique())}  코드결측 {std["코드8"].isna().sum()}')
    return pd.concat(out, ignore_index=True)


def load_seoul():
    """서울시 파일: 자치구코드+법정동코드로 코드8을 직접 만든다."""
    out = []
    for p in find_all(SEOUL_DIR, '서울시 부동산 실거래가 정보*.csv'):
        df = smart_read(p, dtype={'자치구코드': str, '법정동코드': str})
        df = df[df['건물용도'] == '아파트']
        std = pd.DataFrame({
            '자치구명': df['자치구명'].values,
            '법정동명': df['법정동명'].values,
            '면적': pd.to_numeric(df['건물면적(㎡)'], errors='coerce').values,
            '금액': pd.to_numeric(df['물건금액(만원)'].astype(str).str.replace(',', ''),
                                errors='coerce').values,
            '계약년월': df['계약일'].astype(str).str[:6].values,
            '건축년도': pd.to_numeric(df['건축년도'], errors='coerce').values,
            '취소': df['취소일'].values,
            '코드8': (df['자치구코드'].str.zfill(5) + df['법정동코드'].str.zfill(5)).str[:8].values,
        })
        out.append(std)
        print(f'  [서울시] {p.name:42s} {len(std):>7,}건  '
              f'{sorted(std["계약년월"].str[:4].unique())}  코드결측 {std["코드8"].isna().sum()}')
    return pd.concat(out, ignore_index=True)


def load_prices(name2code):
    print('\n[1] 실거래가')
    molit, seoul = load_molit(name2code), load_seoul()
    molit['분기'], seoul['분기'] = to_quarter(molit['계약년월']), to_quarter(seoul['계약년월'])

    df = pd.concat([molit[molit['분기'] < CUTOFF_Q],
                    seoul[seoul['분기'] >= CUTOFF_Q]], ignore_index=True)
    n0 = len(df)
    df = df[df['취소'].isna()]                                   # 취소/해제 제외
    df = df[(df['면적'] > 0) & (df['금액'] > 0) & df['코드8'].notna()]
    df = df[df['분기'].isin(QUARTERS)]
    df['㎡당_만원'] = df['금액'] / df['면적']
    print(f'  컷오프 {CUTOFF_Q} 적용 후 {n0:,}건 -> 유효 {len(df):,}건')
    return df


# ────────────────────────────────────────────────────────────
POP_SPECS = [
    ('상주인구', '*상주인구-상권*.csv',   '총_상주인구_수',  '상주', '상주인구'),
    ('유동인구', '*길단위인구-상권*.csv', '총_유동인구_수',  '유동', '유동인구'),
    ('직장인구', '*직장인구-상권*.csv',   '총_직장_인구_수', '직장', '직장_인구'),
]


def load_population(frag):
    print('\n[2] 인구 (상권 -> 법정동 면적 비례배분)')
    parts = []
    for label, pattern, total_col, prefix, agepat in POP_SPECS:
        df = smart_read(find_one(POP_DIR, pattern), dtype={'상권_코드': str})
        df['상권_코드'] = df['상권_코드'].str.strip()

        cols = {f'{prefix}인구': total_col}
        for age in ['10', '20', '30', '40', '50', '60_이상']:
            c = f'연령대_{age}_{agepat}_수'
            if c in df.columns:
                cols[f'{prefix}_{age}'] = c
        if '총_가구_수' in df.columns:
            cols['가구수'] = '총_가구_수'

        sub = df[['상권_코드', '기준_년분기_코드'] + list(cols.values())].rename(
            columns={v: k for k, v in cols.items()})

        m = sub.merge(frag, on='상권_코드', how='inner')
        for c in cols:                                # 겹치는 면적 비율만큼만 배분
            m[c] = m[c] * m['겹침비율']
        m['상권면적'] = m['겹침면적']                  # 분모도 같은 비율로 나눠야 밀도가 맞다

        g = m.groupby(['코드8', '기준_년분기_코드'])[list(cols) + ['상권면적']].sum().reset_index()
        if prefix != '상주':
            g = g.drop(columns='상권면적')
        parts.append(g)
        print(f'  {label}: {len(df):,}행 -> 법정동 {g["코드8"].nunique()}개 x '
              f'분기 {g["기준_년분기_코드"].nunique()}개')

    pop = parts[0]
    for p in parts[1:]:
        pop = pop.merge(p, on=['코드8', '기준_년분기_코드'], how='outer')
    return pop.rename(columns={'기준_년분기_코드': '분기'})


# ────────────────────────────────────────────────────────────
def agg_price(df, keys):
    return df.groupby(keys).agg(
        거래건수=('금액', 'size'),
        단가_중앙값=('㎡당_만원', 'median'),      # 평균은 그 분기 평형 구성에 휘둘린다
        단가_평균=('㎡당_만원', 'mean'),
        가격_중앙값_만원=('금액', 'median'),
        면적_중앙값=('면적', 'median'),
        건축년도_중앙값=('건축년도', 'median'),
    ).reset_index().round(2)


def add_derived(out):
    out['인구밀도'] = (out['상주인구'] / (out['상권면적'] / 1e6)).round(1)
    out['가구당인구'] = (out['상주인구'] / out['가구수']).round(3)
    out['직주비'] = (out['직장인구'] / out['상주인구']).round(3)
    for prefix in ('상주', '유동', '직장'):
        for c in [c for c in out.columns if c.startswith(f'{prefix}_')]:
            out[c.replace(f'{prefix}_', f'{prefix}비중_')] = (out[c] / out[f'{prefix}인구']).round(4)
    out['표본충분'] = out['거래건수'] >= MIN_DEALS
    return out


def main():
    ref, name2code = load_bjd_ref()
    price = load_prices(name2code)

    frag = smart_read(OUT / 'trdar_bjd_fragments.csv',
                      dtype={'상권_코드': str, '법정동코드': str})
    frag['코드8'] = frag['법정동코드'].str[:8]
    frag = frag[['상권_코드', '코드8', '겹침면적', '겹침비율']]
    pop = load_population(frag)

    print('\n[3] 패널 생성')
    dong = (agg_price(price, ['코드8', '분기'])
            .merge(pop, on=['코드8', '분기'], how='inner')
            .merge(ref, on='코드8', how='left'))
    dong = add_derived(dong)
    front = ['자치구명', '법정동명', '코드8', '분기', '거래건수', '단가_중앙값', '표본충분']
    dong = dong[front + [c for c in dong.columns if c not in front]]
    dong.sort_values(['자치구명', '법정동명', '분기']).to_csv(
        OUT / 'panel_dong.csv', index=False, encoding='utf-8-sig')

    price_gu = price.merge(ref[['코드8', '자치구명']].rename(columns={'자치구명': '구'}),
                           on='코드8', how='left')
    gu_price = agg_price(price_gu, ['구', '분기']).rename(columns={'구': '자치구명'})
    pop_gu = pop.merge(ref[['코드8', '자치구명']], on='코드8', how='left')
    num = [c for c in pop_gu.columns if c not in ('코드8', '분기', '자치구명')]
    pop_gu = pop_gu.groupby(['자치구명', '분기'])[num].sum().reset_index()
    gu = add_derived(gu_price.merge(pop_gu, on=['자치구명', '분기'], how='inner'))
    gu.to_csv(OUT / 'panel_gu.csv', index=False, encoding='utf-8-sig')

    print(f'  panel_gu.csv     {len(gu):>6,}행  (자치구 {gu["자치구명"].nunique()}개 x '
          f'분기 {gu["분기"].nunique()}개)  거래 {gu["거래건수"].sum():,}건')
    print(f'  panel_dong.csv   {len(dong):>6,}행  (법정동 {dong["코드8"].nunique()}개 x '
          f'분기 {dong["분기"].nunique()}개)  거래 {dong["거래건수"].sum():,}건')
    print(f'    거래 {MIN_DEALS}건 이상: {dong["표본충분"].sum():,}행 '
          f'({dong["표본충분"].mean()*100:.1f}%)')

    matched = price['코드8'].isin(set(dong['코드8'])).sum()
    print(f'\n[4] 커버리지  {matched:,}/{len(price):,} ({matched/len(price)*100:.1f}%)')
    lost = (price[~price['코드8'].isin(set(dong['코드8']))]
            .groupby(['자치구명', '법정동명']).size().sort_values(ascending=False))
    if len(lost):
        print(f'  미포함 법정동 {len(lost)}개 (상권 자체가 설정되지 않은 지역): '
              + ', '.join(f'{g} {d}({v:,})' for (g, d), v in lost.head(6).items()))


if __name__ == '__main__':
    main()
