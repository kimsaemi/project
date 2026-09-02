import os
import sys
import numpy as np
import pandas as pd
import duckdb
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, silhouette_score

def main():
    print(">>> 1. 데이터 로드 및 결합...")
    df_admdong = pd.read_csv('final_admdong_table_설명포함_1.csv')
    
    kik_path = 'seoul_apt_analysis 3/data/raw/code_map/KIKmix.20260720(말소코드포함).xlsx'
    df_kik = pd.read_excel(kik_path)
    df_kik_seoul = df_kik[(df_kik['시도명'] == '서울특별시') & (df_kik['말소일자'].isna())].copy()
    df_kik_seoul['adm_cd8'] = df_kik_seoul['행정동코드'].astype(str).str[:8].astype(int)
    
    adm_map = df_kik_seoul[['시군구명', '읍면동명', 'adm_cd8']].drop_duplicates(subset=['시군구명', '읍면동명'])
    adm_map.rename(columns={'시군구명': '자치구명', '읍면동명': '행정동명'}, inplace=True)
    
    df_merged = pd.merge(df_admdong, adm_map, on=['자치구명', '행정동명'], how='left')
    
    name_fix = {
        ('종로구', '창신제1동'): 11110680,
        ('종로구', '창신제2동'): 11110690,
        ('종로구', '창신제3동'): 11110700,
        ('종로구', '숭인제1동'): 11110710,
        ('종로구', '숭인제2동'): 11110720,
    }
    for (gu, dong), cd in name_fix.items():
        mask = (df_merged['자치구명'] == gu) & (df_merged['행정동명'] == dong) & (df_merged['adm_cd8'].isna())
        df_merged.loc[mask, 'adm_cd8'] = cd
        
    unmapped = df_merged[df_merged['adm_cd8'].isna()]
    if len(unmapped) > 0:
        for idx, row in unmapped.iterrows():
            cand = adm_map[(adm_map['자치구명'] == row['자치구명']) & (adm_map['행정동명'].str.contains(row['행정동명'][:2], na=False))]
            if len(cand) > 0:
                df_merged.loc[idx, 'adm_cd8'] = cand.iloc[0]['adm_cd8']
                
    profile_path = '수도권 생활이동 (연령별, 출발-도착지 기준)-6-7월/03_서울시 427개 출발 행정동별 통합 프로파일_06_07.csv'
    df_prof = pd.read_csv(profile_path)
    df_prof.rename(columns={'o_admdong_cd': 'adm_cd8'}, inplace=True)
    
    df_merged['adm_cd8'] = df_merged['adm_cd8'].fillna(0).astype(int)
    df_mart = pd.merge(df_merged, df_prof, on='adm_cd8', how='left')
    
    print(">>> 2. 4대 업무지구(GBD, CBD, YBD, 판교) 접근성 쿼리...")
    con = duckdb.connect()
    parquet_path = '수도권 생활이동 (연령별, 출발-도착지 기준)-6-7월/01_서울 출발,아침 이동의 출발도착누적 2050_06_07.parquet'
    
    query = f"""
    SELECT 
        CAST(o_admdong_cd AS BIGINT) as adm_cd8,
        AVG(CASE WHEN d_admdong_cd LIKE '11680%' OR d_admdong_cd LIKE '11650%' THEN weighted_avg_move_time END) as time_to_gbd,
        SUM(CASE WHEN d_admdong_cd LIKE '11680%' OR d_admdong_cd LIKE '11650%' THEN morning_move_2050 ELSE 0 END) as move_to_gbd,
        
        AVG(CASE WHEN d_admdong_cd LIKE '11110%' OR d_admdong_cd LIKE '11140%' THEN weighted_avg_move_time END) as time_to_cbd,
        SUM(CASE WHEN d_admdong_cd LIKE '11110%' OR d_admdong_cd LIKE '11140%' THEN morning_move_2050 ELSE 0 END) as move_to_cbd,
        
        AVG(CASE WHEN d_admdong_cd LIKE '11560%' OR d_admdong_cd LIKE '11440%' THEN weighted_avg_move_time END) as time_to_ybd,
        SUM(CASE WHEN d_admdong_cd LIKE '11560%' OR d_admdong_cd LIKE '11440%' THEN morning_move_2050 ELSE 0 END) as move_to_ybd,
        
        AVG(CASE WHEN d_admdong_cd LIKE '41135%' THEN weighted_avg_move_time END) as time_to_pangyo,
        SUM(CASE WHEN d_admdong_cd LIKE '41135%' THEN morning_move_2050 ELSE 0 END) as move_to_pangyo
    FROM '{parquet_path}'
    GROUP BY CAST(o_admdong_cd AS BIGINT)
    """
    df_hubs = con.execute(query).df()
    df_mart = pd.merge(df_mart, df_hubs, on='adm_cd8', how='left')
    
    for col in ['time_to_gbd', 'time_to_cbd', 'time_to_ybd', 'time_to_pangyo', 'weighted_avg_move_time', 'weighted_avg_move_dist']:
        df_mart[col] = df_mart[col].fillna(df_mart[col].median())
    for col in ['move_to_gbd', 'move_to_cbd', 'move_to_ybd', 'move_to_pangyo', 'morning_move_2030', 'morning_move_4050', 'morning_move_2050']:
        df_mart[col] = df_mart[col].fillna(0)
        
    print(">>> 3. 파생변수 생성...")
    df_mart['단가_평당만원'] = (df_mart['최근1년_평균가격(㎡당_만원)'] * 3.30578).round(1)
    df_mart['추정_전용59_가격_억'] = ((df_mart['최근1년_평균가격(㎡당_만원)'] * 59) / 10000).round(2)
    df_mart['추정_전용84_가격_억'] = ((df_mart['최근1년_평균가격(㎡당_만원)'] * 84) / 10000).round(2)
    df_mart['추정_평균매매가_억'] = ((df_mart['최근1년_평균가격(㎡당_만원)'] * df_mart['평균_전용면적(㎡)']) / 10000).round(2)
    
    df_mart['직주_유입비율'] = (df_mart['평일_출근으로_도착한_사람수'] / (df_mart['평일_귀가로_도착한_사람수'] + 1)).round(2)
    df_mart['3대도심_평균통근시간'] = ((df_mart['time_to_gbd'] + df_mart['time_to_cbd'] + df_mart['time_to_ybd']) / 3.0).round(1)
    df_mart['가성비_접근성지수'] = ((100.0 / df_mart['3대도심_평균통근시간']) / (df_mart['단가_평당만원'] + 1) * 10000).round(2)
    
    bins = [0, 6, 9, 12, 15, 999]
    labels = ['6억 이하(실속형)', '6~9억(가성비 패밀리)', '9~12억(중위 주거타운)', '12~15억(준상급지)', '15억 초과(핵심 상급지)']
    df_mart['예산구간_전용59'] = pd.cut(df_mart['추정_전용59_가격_억'], bins=bins, labels=labels)
    
    print(">>> 4. 머신러닝 회귀 및 기여도 분석...")
    feature_cols = [
        'weighted_avg_move_time', 'weighted_avg_move_dist', '3대도심_평균통근시간',
        'time_to_gbd', 'time_to_cbd', 'time_to_ybd', 'time_to_pangyo',
        '직주_유입비율', '평일_출근으로_도착한_사람수', '평일_귀가로_도착한_사람수',
        'morning_move_2050', 'destination_diversity', '최근1년_거래건수'
    ]
    
    X = df_mart[feature_cols].copy()
    y = df_mart['단가_평당만원']
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    r2_rf = r2_score(y, rf.predict(X))
    
    ridge = Ridge(alpha=1.0)
    scaler_x = StandardScaler()
    X_s = scaler_x.fit_transform(X)
    ridge.fit(X_s, y)
    r2_ridge = r2_score(y, ridge.predict(X_s))
    
    importances = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': rf.feature_importances_,
        'Std_Coef': ridge.coef_
    }).sort_values(by='Importance', ascending=False)
    print("=== Feature Importances & Coefs ===")
    print(importances)
    
    print(">>> 5. K-Means 군집 분석 및 정교한 라벨링...")
    cluster_features = [
        '단가_평당만원', '3대도심_평균통근시간', '직주_유입비율',
        '평일_귀가로_도착한_사람수', 'destination_diversity', 'time_to_gbd'
    ]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_mart[cluster_features])
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_mart['cluster_id'] = kmeans.fit_predict(X_scaled)
    
    # 각 군집의 평균 단가 기준으로 정렬하여 명칭 부여
    cluster_means = df_mart.groupby('cluster_id')['단가_평당만원'].mean().sort_values()
    # 0: 최저단가 -> 외곽 실속 주거타운
    # 1: 2순위단가 -> 가성비 스마트 주거타운
    # 2: 3순위단가 -> 준상급 교통요충지
    # 3: 최고단가 -> 초고가 핵심 프리미엄지
    id_to_name = {
        cluster_means.index[0]: '외곽 실속 주거타운',
        cluster_means.index[1]: '가성비 스마트 주거타운',
        cluster_means.index[2]: '준상급 교통/주거요충지',
        cluster_means.index[3]: '핵심 프리미엄 상급지'
    }
    df_mart['cluster_name'] = df_mart['cluster_id'].map(id_to_name)
    
    print(">>> 6. 3040 맞벌이 다기준 추천 점수 산출...")
    def min_max_norm(series, invert=False):
        min_v, max_v = series.min(), series.max()
        if max_v == min_v:
            return pd.Series(50, index=series.index)
        norm = (series - min_v) / (max_v - min_v) * 100
        return (100 - norm) if invert else norm

    score_price = min_max_norm(df_mart['단가_평당만원'], invert=True)
    score_livability = min_max_norm(df_mart['평일_귀가로_도착한_사람수']) * 0.6 + min_max_norm(df_mart['최근1년_거래건수']) * 0.4
    score_commute_overall = min_max_norm(df_mart['3대도심_평균통근시간'], invert=True)
    
    score_gbd = min_max_norm(df_mart['time_to_gbd'], invert=True)
    score_cbd = min_max_norm(df_mart['time_to_cbd'], invert=True)
    score_ybd = min_max_norm(df_mart['time_to_ybd'], invert=True)
    score_pangyo = min_max_norm(df_mart['time_to_pangyo'], invert=True)
    
    df_mart['score_price'] = score_price.round(1)
    df_mart['score_livability'] = score_livability.round(1)
    df_mart['score_commute_overall'] = score_commute_overall.round(1)
    df_mart['score_gbd'] = score_gbd.round(1)
    df_mart['score_cbd'] = score_cbd.round(1)
    df_mart['score_ybd'] = score_ybd.round(1)
    df_mart['score_pangyo'] = score_pangyo.round(1)
    
    # 맞벌이 조합별 종합 점수 (통근 50% + 가성비 30% + 주거환경 20%)
    df_mart['추천점수_강남_광화문'] = (
        (score_gbd * 0.25 + score_cbd * 0.25) + 
        score_price * 0.30 + 
        score_livability * 0.20
    ).round(1)
    
    df_mart['추천점수_강남_여의도'] = (
        (score_gbd * 0.25 + score_ybd * 0.25) + 
        score_price * 0.30 + 
        score_livability * 0.20
    ).round(1)

    df_mart['추천점수_여의도_광화문'] = (
        (score_ybd * 0.25 + score_cbd * 0.25) + 
        score_price * 0.30 + 
        score_livability * 0.20
    ).round(1)

    df_mart['추천점수_강남_판교'] = (
        (score_gbd * 0.25 + score_pangyo * 0.25) + 
        score_price * 0.30 + 
        score_livability * 0.20
    ).round(1)
    
    df_mart['종합_3040_추천점수'] = (
        score_commute_overall * 0.50 + 
        score_price * 0.30 + 
        score_livability * 0.20
    ).round(1)
    
    # 소수점 포맷 정리
    df_mart['time_to_gbd'] = df_mart['time_to_gbd'].round(1)
    df_mart['time_to_cbd'] = df_mart['time_to_cbd'].round(1)
    df_mart['time_to_ybd'] = df_mart['time_to_ybd'].round(1)
    df_mart['time_to_pangyo'] = df_mart['time_to_pangyo'].round(1)
    df_mart['weighted_avg_move_time'] = df_mart['weighted_avg_move_time'].round(1)
    
    output_path = 'final_recommendation_mart.csv'
    df_mart.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    json_path = 'recommendation_data.json'
    df_mart.to_json(json_path, orient='records', force_ascii=False, indent=2)
    print(">>> 7. CSV & JSON 저장 완료!")

if __name__ == '__main__':
    main()
