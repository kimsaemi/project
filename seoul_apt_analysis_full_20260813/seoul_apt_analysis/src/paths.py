"""
프로젝트 경로 및 공용 유틸
==========================

모든 경로는 이 파일 위치를 기준으로 계산되므로,
프로젝트 폴더를 통째로 어디에 옮겨도(다른 PC, 다른 사용자명) 그대로 동작한다.
절대경로를 스크립트에 직접 쓰지 말고 항상 여기의 상수를 쓸 것.
"""

import unicodedata
from fnmatch import fnmatch
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'data' / 'output'

MOLIT_DIR = RAW / 'molit_price'      # 국토교통부 아파트 매매 실거래가 2021~2023
SEOUL_DIR = RAW / 'seoul_price'      # 서울시 부동산 실거래가 2024~2026
POP_DIR   = RAW / 'population'       # 상권분석서비스 상주/길단위/직장인구
TRDAR_DIR = RAW / 'trdar_area'       # 영역-상권 shapefile
BJD_DIR   = RAW / 'bjd_boundary'     # 법정동(읍면동) 경계 shapefile
CODE_DIR  = RAW / 'code_map'         # 행정안전부 KIKmix 크로스워크

OUT.mkdir(parents=True, exist_ok=True)

# 파일별 인코딩이 제각각이다.
#   서울시 열린데이터광장 = UTF-8-SIG,  국토부/행안부/GIS 자료 = CP949
ENCODINGS = ('utf-8-sig', 'cp949', 'utf-8')


def smart_read(path, **kw):
    """인코딩을 자동 판별해 CSV를 읽는다."""
    last = None
    for enc in ENCODINGS:
        try:
            return pd.read_csv(path, encoding=enc, low_memory=False, **kw)
        except UnicodeDecodeError as e:
            last = e
    raise RuntimeError(f'인코딩 판별 실패: {path}') from last


def _glob_nfc(directory: Path, pattern: str) -> list:
    """한글 파일명을 정규화해서 매칭한다.

    macOS는 파일명을 NFD(자모 분해형)로 저장하는데 소스의 패턴은 NFC(조합형)라
    '아파트*.csv' 가 '아파트(매매)....csv' 를 못 찾는다. Windows에서 만든
    파이프라인을 macOS에서 돌릴 때 반드시 걸린다. 양쪽을 NFC로 맞춰 비교한다.
    """
    if not directory.exists():
        return []
    pat = unicodedata.normalize('NFC', pattern)
    hits = [p for p in directory.iterdir()
            if p.is_file() and fnmatch(unicodedata.normalize('NFC', p.name), pat)]
    return sorted(hits, key=lambda p: unicodedata.normalize('NFC', p.name))


def find_one(directory: Path, pattern: str) -> Path:
    """디렉터리에서 패턴에 맞는 파일 하나를 찾는다. 없으면 안내와 함께 실패."""
    hits = _glob_nfc(directory, pattern)
    if not hits:
        raise FileNotFoundError(
            f'파일을 찾을 수 없습니다: {directory.name}/{pattern}\n'
            f'  확인할 위치: {directory}\n'
            f'  README.md 의 "데이터 원본" 절을 참고해 내려받아 넣어주세요.')
    return hits[0]


def find_all(directory: Path, pattern: str) -> list:
    hits = _glob_nfc(directory, pattern)
    if not hits:
        raise FileNotFoundError(f'파일이 하나도 없습니다: {directory.name}/{pattern}')
    return hits


if __name__ == '__main__':
    print(f'ROOT = {ROOT}\n')
    for name, d in [('국토부 실거래가', MOLIT_DIR), ('서울시 실거래가', SEOUL_DIR),
                    ('상권 인구', POP_DIR), ('영역-상권', TRDAR_DIR),
                    ('법정동 경계', BJD_DIR), ('코드 매핑', CODE_DIR),
                    ('산출물', OUT)]:
        files = sorted(p for p in d.glob('*') if p.is_file()) if d.exists() else []
        mark = 'OK ' if files else '없음'
        print(f'[{mark}] {name:14s} {len(files)}개  ({d.relative_to(ROOT)})')
        for f in files:
            print(f'         - {f.name}  ({f.stat().st_size/1e6:.1f} MB)')
