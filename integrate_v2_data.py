import sys
import os
import pandas as pd
import numpy as np
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 1. Load Raw v2 Real Estate Transactions (83,178 rows)
v2_path = r'd:\26_강의자료\프로젝트\11_실거래가_정제본_v2.csv'
print(f"Loading {v2_path}...")
df_v2 = pd.read_csv(v2_path, encoding='utf-8-sig')

# Filter for Apartments & Valid Sales
df_apt_v2 = df_v2[df_v2['건물용도'] == '아파트'].copy()
df_apt_v2 = df_apt_v2[df_apt_v2['취소일'].isna()]  # Remove cancelled transactions

print(f"Total Raw Transactions: {len(df_v2)}건")
print(f"Filtered Apartment Sales (Valid): {len(df_apt_v2)}건")

# Calculate Size Categories
def get_size_category(area_m2):
    if area_m2 <= 60:
        return 'small'    # ~25평형 (59㎡)
    elif area_m2 <= 85:
        return 'medium'   # 25~34평형 (84㎡)
    else:
        return 'large'    # 35평형+ (84㎡超)

df_apt_v2['size_cat'] = df_apt_v2['건물면적(㎡)'].apply(get_size_category)
df_apt_v2['price_eok'] = df_apt_v2['물건금액(만원)'] / 10000.0

# Group by 자치구명 + 법정동명 to calculate real v2 statistics
grouped = df_apt_v2.groupby(['자치구명', '법정동명'])

v2_dong_stats = {}
for (gu, dong), group in grouped:
    total_trades = len(group)
    med_price = round(group['price_eok'].median(), 2)
    avg_unit_price = round(group['평당금액'].mean(), 1)
    
    # Average Construction Year
    valid_years = group['건축년도'].dropna()
    avg_built_year = int(valid_years.mean()) if len(valid_years) > 0 else 2005
    apt_age = 2026 - avg_built_year
    
    # Top 3 Popular Apartment Complex Names by Transaction Count
    top_apts = group['건물명'].value_counts().head(3).index.tolist()
    top_apts_str = ", ".join(top_apts) if top_apts else "주요 단지"
    
    # Size breakdown stats
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

print(f"Aggregated {len(v2_dong_stats)} distinct legal dongs from v2 dataset!")

# Merge with our existing clustering & ranking CSV
rank_path = r'd:\26_강의자료\프로젝트\3040_맞벌이_주거지_클러스터링_분석결과.csv'
df_rank = pd.read_csv(rank_path)

# Add v2 columns
df_rank['v2_실거래건수'] = df_rank.apply(lambda r: v2_dong_stats.get((r['자치구'], r['법정동']), {}).get('v2_trades', r['최근1년_거래건수']), axis=1)
df_rank['v2_평균건축년도'] = df_rank.apply(lambda r: v2_dong_stats.get((r['자치구'], r['법정동']), {}).get('v2_built_year', 2005), axis=1)
df_rank['v2_아파트연식'] = df_rank.apply(lambda r: v2_dong_stats.get((r['자치구'], r['법정동']), {}).get('v2_apt_age', 21), axis=1)
df_rank['v2_대표아파트단지'] = df_rank.apply(lambda r: v2_dong_stats.get((r['자치구'], r['법정동']), {}).get('v2_top_apts', '주요 대단지'), axis=1)

# Save updated dataset CSV
df_rank.to_csv(r'd:\26_강의자료\프로젝트\3040_맞벌이_주거지_클러스터링_분석결과_v2연동.csv', index=False, encoding='utf-8-sig')
print("Saved updated v2 dataset to 3040_맞벌이_주거지_클러스터링_분석결과_v2연동.csv")

# Print top 5 samples
print("\n[v2 데이터 연동 대표 5개 동 샘플]")
sample_cols = ['자치구', '법정동', '최근_중앙가격_억', 'v2_실거래건수', 'v2_평균건축년도', 'v2_아파트연식', 'v2_대표아파트단지']
print(df_rank[sample_cols].head(5).to_string(index=False))
