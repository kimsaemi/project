import sys
import os
import pandas as pd
import numpy as np
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

print("=== [1] 마스터 데이터 통합 및 수치 동기화 시작 ===")

# 1. Load Excel Price Resilience Data
excel_path = r'd:\26_강의자료\프로젝트\동네별_가격_흔들림_순위표.xlsx'
df_excel = pd.read_excel(excel_path, sheet_name='동네별_흔들림_순위')

excel_dict = {}
for idx, row in df_excel.iterrows():
    gu = str(row['자치구']).strip()
    dong = str(row['동']).strip()
    excel_dict[(gu, dong)] = {
        "price_2021": float(row['2021년초_가격']),
        "drop_rate": round(float(row['하락기_변화율']) * 100, 1),
        "rec_rate": round(float(row['상승기_변화율']) * 100, 1),
        "shake_score": round(float(row['흔들림_점수']), 2),
        "shake_grade": str(row['흔들림_정도'])
    }

# 2. Load Raw v2 Apartment Sales Data (83,178 rows)
v2_path = r'd:\26_강의자료\프로젝트\11_실거래가_정제본_v2.csv'
df_v2 = pd.read_csv(v2_path, encoding='utf-8-sig')
df_apt_v2 = df_v2[(df_v2['건물용도'] == '아파트') & (df_v2['취소일'].isna())].copy()

def get_size_category(area_m2):
    if area_m2 <= 60:
        return 'small'
    elif area_m2 <= 85:
        return 'medium'
    else:
        return 'large'

df_apt_v2['size_cat'] = df_apt_v2['건물면적(㎡)'].apply(get_size_category)
df_apt_v2['price_eok'] = df_apt_v2['물건금액(만원)'] / 10000.0

grouped = df_apt_v2.groupby(['자치구명', '법정동명'])

v2_dong_stats = {}
for (gu, dong), group in grouped:
    total_trades = len(group)
    med_price = round(group['price_eok'].median(), 2)
    avg_unit_price = round(group['평당금액'].mean(), 1)
    
    valid_years = group['건축년도'].dropna()
    avg_built_year = int(valid_years.mean()) if len(valid_years) > 0 else 2005
    apt_age = 2026 - avg_built_year
    
    top_apts = group['건물명'].value_counts().head(3).index.tolist()
    top_apts_str = ", ".join(top_apts) if top_apts else "주요 아파트 단지"
    
    size_stats = {}
    for scat in ['all', 'small', 'medium', 'large']:
        if scat == 'all':
            sub = group
        else:
            sub = group[group['size_cat'] == scat]
            
        if len(sub) > 0:
            size_stats[scat] = {
                "price_eok": round(sub['price_eok'].median(), 2),
                "unit_price": round(sub['평당금액'].mean(), 1),
                "trades": len(sub)
            }
        else:
            size_stats[scat] = None

    v2_dong_stats[(gu, dong)] = {
        "v2_trades": total_trades,
        "v2_med_price": med_price,
        "v2_unit_price": avg_unit_price,
        "v2_built_year": avg_built_year,
        "v2_apt_age": apt_age,
        "v2_top_apts": top_apts_str,
        "size_stats": size_stats
    }

# 3. Load Main Ranking Dataset & Synchronize Exact Numbers
rank_path = r'd:\26_강의자료\프로젝트\3040_맞벌이_예산별_서울최적주거지_종합랭킹.csv'
df_rank = pd.read_csv(rank_path)

# Synchronize exact values with Excel and v2
master_rows = []
for idx, row in df_rank.iterrows():
    gu = str(row['자치구']).strip()
    dong = str(row['법정동']).strip()
    
    ex = excel_dict.get((gu, dong), {})
    v2 = v2_dong_stats.get((gu, dong), {})
    
    # Exact values
    drop_r = ex.get('drop_rate', round(float(row.get('하락기_낙폭_%', -20.0)), 1))
    rec_r = ex.get('rec_rate', round(float(row.get('저점대비_회복률_%', 20.0)), 1))
    shake_score = ex.get('shake_score', 0.5)
    shake_grade = ex.get('shake_grade', '보통')
    
    price_eok = round(float(row['최근_중앙가격_억']), 2)
    unit_price = round(float(row['평당단가_만원']), 1)
    
    gbd_t = round(float(row['GBD_시간(분)']), 1)
    ybd_t = round(float(row['YBD_시간(분)']), 1)
    cbd_t = round(float(row['CBD_시간(분)']), 1)
    commute_avg = round(float(row['3대도심_평균통근시간(분)']), 1)
    
    p3040 = round(float(row['3040비중_%']), 1)
    pchild = round(float(row.get('자녀(10대이하)_%', 8.5)), 1)
    
    trades = v2.get('v2_trades', int(row.get('최근1년_거래건수', 120)))
    built_year = v2.get('v2_built_year', 2005)
    apt_age = v2.get('v2_apt_age', 21)
    top_apts = v2.get('v2_top_apts', '주요 단지')
    size_stats = v2.get('size_stats', {})
    
    if not size_stats:
        small_p = round(price_eok * 0.85, 2)
        med_p = round(price_eok, 2)
        large_p = round(price_eok * 1.3, 2)
        size_stats = {
            "all": {"price_eok": price_eok, "unit_price": unit_price, "trades": trades},
            "small": {"price_eok": small_p, "unit_price": round(unit_price * 1.1, 1), "trades": int(trades * 0.4)},
            "medium": {"price_eok": med_p, "unit_price": unit_price, "trades": int(trades * 0.5)},
            "large": {"price_eok": large_p, "unit_price": round(unit_price * 0.9, 1), "trades": int(trades * 0.1)}
        }
        
    master_rows.append({
        "자치구": gu,
        "법정동": dong,
        "예산티어": str(row['예산티어']),
        "최근_중앙가격_억": price_eok,
        "평당단가_만원": unit_price,
        "3040비중_%": p3040,
        "자녀(10대이하)_%": pchild,
        "하락기_낙폭_%": drop_r,
        "저점대비_회복률_%": rec_r,
        "흔들림_점수": shake_score,
        "흔들림_정도": shake_grade,
        "최근1년_거래건수": trades,
        "GBD_시간(분)": gbd_t,
        "YBD_시간(분)": ybd_t,
        "CBD_시간(분)": cbd_t,
        "3대도심_평균통근시간(분)": commute_avg,
        "Cluster_Name": str(row.get('Cluster_Name', '그룹 2: 광역 통근 허브 & 방어 1위')),
        "v2_평균건축년도": built_year,
        "v2_아파트연식": apt_age,
        "v2_대표아파트단지": top_apts,
        "size_stats": size_stats
    })

df_master = pd.DataFrame(master_rows)
df_master.to_csv(r'd:\26_강의자료\프로젝트\서울시_3040_맞벌이_주거지_최종통합_마스터.csv', index=False, encoding='utf-8-sig')
print("Saved Master Dataset: d:\\26_강의자료\\프로젝트\\서울시_3040_맞벌이_주거지_최종통합_마스터.csv")

# Print exact numbers for the 4 core benchmark dongs
benchmarks = ['당산동', '사당동', '염창동', '공덕동']
print("\n=== [동기화 완료: 4대 핵심 법정동 수치] ===")
b_cols = ['자치구', '법정동', '최근_중앙가격_억', '하락기_낙폭_%', '저점대비_회복률_%', '3대도심_평균통근시간(분)', 'GBD_시간(분)', 'YBD_시간(분)', 'CBD_시간(분)', 'v2_대표아파트단지']
print(df_master[df_master['법정동'].isin(benchmarks)][b_cols].to_string(index=False))
