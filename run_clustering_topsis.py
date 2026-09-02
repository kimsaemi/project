import sys
import pandas as pd
import numpy as np
import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# 1. Load Data
df = pd.read_csv(r'd:\26_강의자료\프로젝트\3040_맞벌이_예산별_서울최적주거지_종합랭킹.csv')

# Features for Clustering
cluster_features = ['최근_중앙가격_억', '평당단가_만원', '3040비중_%', '하락기_낙폭_%', '저점대비_회복률_%', '3대도심_평균통근시간(분)']
X_cls = df[cluster_features].fillna(df[cluster_features].median())

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cls)

# K-Means Clustering (k=4)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Characterize Clusters
cluster_summary = df.groupby('Cluster')[cluster_features].mean()
cluster_summary['동개수'] = df.groupby('Cluster').size()

# Assign human-readable cluster names based on traits
# Let's inspect cluster traits
cluster_names = {}
for c in range(4):
    avg_price = cluster_summary.loc[c, '최근_중앙가격_억']
    avg_commute = cluster_summary.loc[c, '3대도심_평균통근시간(분)']
    avg_drop = cluster_summary.loc[c, '하락기_낙폭_%']
    avg_3040 = cluster_summary.loc[c, '3040비중_%']
    
    if avg_price > 12.0:
        name = "그룹 3: 쿼드러플 & 자산 고탄력 성장의 도심 거점"
    elif avg_drop > -15.0 and avg_commute < 55.0:
        name = "그룹 2: 광역 통근 허브 & 하락장 철통 방어선"
    elif avg_price < 8.5 and avg_3040 > 32.0:
        name = "그룹 1: 가성비 실속 & 9호선/신림선 실수요 밀집지"
    else:
        name = "그룹 4: 학군 & 자녀 보육 배후 주거지"
    cluster_names[c] = name

df['Cluster_Name'] = df['Cluster'].map(cluster_names)

print("=== [K-Means 군집 분석 결과] ===")
for c in range(4):
    c_df = df[df['Cluster'] == c]
    sample_dongs = ", ".join(c_df['법정동'].head(5).tolist())
    print(f"\n[{cluster_names[c]}] (총 {len(c_df)}개 동)")
    print(f"  • 평균 매매가: {c_df['최근_중앙가격_억'].mean():.2f}억 원 (평당 {c_df['평당단가_만원'].mean():.0f}만 원)")
    print(f"  • 평균 통근시간: {c_df['3대도심_평균통근시간(분)'].mean():.1f}분")
    print(f"  • 하락기 평균 낙폭: {c_df['하락기_낙폭_%'].mean():.1f}%")
    print(f"  • 3040 상주비중: {c_df['3040비중_%'].mean():.1f}%")
    print(f"  • 대표 동네: {sample_dongs}")

# TOPSIS Function for 3 Buyer Personas
def topsis(data, weights, impact):
    norm_data = data / np.sqrt((data**2).sum(axis=0))
    weighted_data = norm_data * weights
    ideal_best = np.zeros(data.shape[1])
    ideal_worst = np.zeros(data.shape[1])
    for j in range(data.shape[1]):
        if impact[j] == '+':
            ideal_best[j] = weighted_data.iloc[:, j].max()
            ideal_worst[j] = weighted_data.iloc[:, j].min()
        else:
            ideal_best[j] = weighted_data.iloc[:, j].min()
            ideal_worst[j] = weighted_data.iloc[:, j].max()
    d_best = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
    d_worst = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))
    return d_worst / (d_best + d_worst)

topsis_cols = ['3대도심_평균통근시간(분)', '하락기_낙폭_%', '3040비중_%', '최근_중앙가격_억']
tdf = df[topsis_cols].copy()
tdf['하락기_낙폭_%'] = abs(tdf['하락기_낙폭_%'])

# Persona 1: 신혼부부 (통근 50%, 예산/가격 30%, 방어 10%, 3040 10%)
df['TOPSIS_신혼부부'] = topsis(tdf, [0.5, 0.1, 0.1, 0.3], ['-', '-', '+', '-'])

# Persona 2: 자산방어형 맞벌이 (하락방어 50%, 통근 30%, 3040 10%, 예산 10%)
df['TOPSIS_자산방어'] = topsis(tdf, [0.3, 0.5, 0.1, 0.1], ['-', '-', '+', '-'])

# Persona 3: 자산성장/도심형 (통근 40%, 3040비중 30%, 하락방어 20%, 예산 10%)
df['TOPSIS_도심성장'] = topsis(tdf, [0.4, 0.2, 0.3, 0.1], ['-', '-', '+', '-'])

print("\n=== [페르소나별 TOPSIS 추천 Top 3] ===")
print("\n1. 신혼/가성비 추천 Top 3:")
print(df.sort_values('TOPSIS_신혼부부', ascending=False)[['자치구', '법정동', '최근_중앙가격_억', '3대도심_평균통근시간(분)']].head(3).to_string(index=False))

print("\n2. 자산방어형 맞벌이 추천 Top 3:")
print(df.sort_values('TOPSIS_자산방어', ascending=False)[['자치구', '법정동', '최근_중앙가격_억', '하락기_낙폭_%', '3대도심_평균통근시간(분)']].head(3).to_string(index=False))

# Export cluster & topsis dataset
df.to_csv(r'd:\26_강의자료\프로젝트\3040_맞벌이_주거지_클러스터링_분석결과.csv', index=False, encoding='utf-8-sig')
print("\n[3040_맞벌이_주거지_클러스터링_분석결과.csv] 저장 완료!")
