"""
영역-상권 Shapefile의 속성테이블(.dbf) 로더
============================================

상권_코드 <-> 자치구/행정동 매핑과 중심좌표·영역면적을 제공한다.
지오메트리가 필요 없으므로 geopandas 없이 순수 파이썬으로 .dbf를 직접 읽는다.

주의: 같은 폴더의 CSV 버전(영역-상권.csv)은 CP949로 저장되어
      '종로1·2·3·4가동'의 가운뎃점이 '?'로 깨진다. .dbf(UTF-8)가 원본에 가깝다.
"""

import struct
import pandas as pd

from paths import TRDAR_DIR, find_one

FIELD_RENAME = {
    'TRDAR_SE_C': '상권_구분_코드',
    'TRDAR_SE_1': '상권_구분_코드_명',
    'TRDAR_CD':   '상권_코드',
    'TRDAR_CD_N': '상권_코드_명',
    'XCNTS_VALU': '엑스좌표_값',
    'YDNTS_VALU': '와이좌표_값',
    'SIGNGU_CD':  '자치구_코드',
    'SIGNGU_CD_': '자치구_코드_명',
    'ADSTRD_CD':  '행정동_코드',
    'ADSTRD_CD_': '행정동_코드_명',
    'RELM_AR':    '영역_면적',
}


def read_dbf(dbf_path, encoding='utf-8') -> pd.DataFrame:
    """DBF(dBase III/IV) 파일을 DataFrame으로 읽는다."""
    raw = dbf_path.read_bytes() if hasattr(dbf_path, 'read_bytes') else open(dbf_path, 'rb').read()
    num_records, header_len, record_len = struct.unpack('<IHH', raw[4:12])

    fields, off = [], 32                       # 32바이트 헤더 뒤 32바이트씩, 0x0D로 종료
    while raw[off] != 0x0D:
        name = raw[off:off + 11].split(b'\x00')[0].decode('ascii')
        fields.append((name, chr(raw[off + 11]), raw[off + 16]))
        off += 32

    rows = []
    for i in range(num_records):
        rec = raw[header_len + i * record_len: header_len + (i + 1) * record_len]
        if not rec or rec[0:1] == b'*':        # 삭제 표시된 레코드
            continue
        pos, row = 1, {}
        for name, ftype, flen in fields:
            val = rec[pos:pos + flen].decode(encoding, errors='replace').strip()
            pos += flen
            row[name] = (pd.to_numeric(val, errors='coerce') if val else None) if ftype == 'N' else val
        rows.append(row)

    return pd.DataFrame(rows, columns=[f[0] for f in fields])


def load_trdar_area() -> pd.DataFrame:
    """영역-상권 매핑 테이블을 한글 컬럼명으로 로드한다."""
    df = read_dbf(find_one(TRDAR_DIR, '*.dbf')).rename(columns=FIELD_RENAME)
    df['상권_코드'] = df['상권_코드'].astype(str).str.strip()
    df['행정동_코드'] = df['행정동_코드'].astype(str).str.strip()
    df['영역_면적_km2'] = df['영역_면적'] / 1_000_000
    return df


if __name__ == '__main__':
    area = load_trdar_area()
    print('=== 영역-상권 매핑 테이블 ===')
    print(f'행 수 {len(area):,} / 상권 {area["상권_코드"].nunique():,}개 / '
          f'자치구 {area["자치구_코드_명"].nunique()}개 / 행정동 {area["행정동_코드_명"].nunique()}개')
    print()
    print(area[['상권_코드', '상권_코드_명', '자치구_코드_명',
                '행정동_코드_명', '영역_면적']].head(5).to_string(index=False))
