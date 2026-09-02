import sys
import os
import shutil

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

source_dir = r'd:\26_강의자료\프로젝트'
target_dir = r'd:\26_강의자료\프로젝트\발표용 공유'

os.makedirs(target_dir, exist_ok=True)

data_files = [
    "서울시_3040_맞벌이_주거지_최종통합_마스터.csv",
    "3040_맞벌이_주거지_클러스터링_분석결과_v2연동.csv",
    "3040_맞벌이_예산별_서울최적주거지_종합랭킹.csv",
    "동네별_가격_흔들림_순위표.xlsx"
]

print("=== 분석 데이터 파일 발표용 공유 폴더에 최종 정리 ===")
copied_list = []
for fname in data_files:
    src_path = os.path.join(source_dir, fname)
    dst_path = os.path.join(target_dir, fname)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        copied_list.append(fname)
        print(f"✅ 복사 완료: {fname} -> {target_dir}")
    else:
        print(f"⚠️ 파일 없음: {fname}")

print(f"\n총 {len(copied_list)}개의 최종 데이터 파일이 정리되었습니다!")
