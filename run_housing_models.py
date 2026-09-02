import sys
import os
import pandas as pd
import numpy as np
import json

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, roc_auc_score

# 1. 데이터 로드
file_path = r'd:\26_강의자료\프로젝트\3040_맞벌이_예산별_서울최적주거지_종합랭킹.csv'
df = pd.read_csv(file_path)

print("=== [1] 데이터 로드 완료 ===")
print(f"총 분석 대상 법정동 수: {len(df)}개")

# 2. 특성(Features) 및 결측치 처리
features = [
    '최근_중앙가격_억', '평당단가_만원', '3040비중_%', '30대비중_%', '40대비중_%', 
    '자녀(10대이하)_%', '직주비', '최근1년_거래건수', 'GBD_시간(분)', 
    'YBD_시간(분)', 'CBD_시간(분)', '3대도심_평균통근시간(분)'
]

X = df[features].fillna(df[features].median())

# ==========================================
# [모델 1] 회귀 모델 (Regression): 가격방어점수 예측
# ==========================================
y_resilience = df['가격안정점수']
X_train, X_test, y_train, y_test = train_test_split(X, y_resilience, test_size=0.25, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Ridge 회귀
ridge_reg = Ridge(alpha=1.0)
ridge_reg.fit(X_train_scaled, y_train)
y_pred_ridge = ridge_reg.predict(X_test_scaled)
r2_ridge = r2_score(y_test, y_pred_ridge)
rmse_ridge = np.sqrt(mean_squared_error(y_test, y_pred_ridge))

# Random Forest 회귀
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X_train, y_train)
y_pred_rf = rf_reg.predict(X_test)
r2_rf = r2_score(y_test, y_pred_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))

print("\n==========================================")
print("📊 [회귀 모델 1] 가격 방어 점수(가격안정점수) 예측 결과")
print("==========================================")
print(f"• Ridge 회귀 R² Score: {r2_ridge:.4f} (RMSE: {rmse_ridge:.4f})")
print(f"• Random Forest 회귀 R² Score: {r2_rf:.4f} (RMSE: {rmse_rf:.4f})")

rf_importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_reg.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n[Random Forest 가격방어 영향력 Top 5]")
for idx, row in rf_importance.head(5).iterrows():
    print(f"  {row['Feature']}: {row['Importance']*100:.1f}%")

# ==========================================
# [모델 2] 회귀 모델 (Regression): 3040 종합추천점수 예측
# ==========================================
y_total = df['종합추천점수']
X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(X, y_total, test_size=0.25, random_state=42)

rf_reg_total = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg_total.fit(X_train_t, y_train_t)
y_pred_total = rf_reg_total.predict(X_test_t)

r2_total = r2_score(y_test_t, y_pred_total)
rmse_total = np.sqrt(mean_squared_error(y_test_t, y_pred_total))

print("\n==========================================")
print("📊 [회귀 모델 2] 3040 종합추천점수 예측 결과")
print("==========================================")
print(f"• Random Forest 회귀 R² Score: {r2_total:.4f} (RMSE: {rmse_total:.4f})")

rf_total_importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_reg_total.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n[종합추천점수 결정 핵심 요인 Top 5]")
for idx, row in rf_total_importance.head(5).iterrows():
    print(f"  {row['Feature']}: {row['Importance']*100:.1f}%")

# ==========================================
# [추천 모델 A] 분류 모델 (Classification): 하락장 철통방어지역 판별
# ==========================================
y_class = (df['가격안정점수'] >= df['가격안정점수'].quantile(0.67)).astype(int)

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_class, test_size=0.25, random_state=42, stratify=y_class)

rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train_c, y_train_c)
y_pred_c = rf_clf.predict(X_test_c)
acc_c = accuracy_score(y_test_c, y_pred_c)
auc_c = roc_auc_score(y_test_c, rf_clf.predict_proba(X_test_c)[:, 1])

print("\n==========================================")
print("💡 [추천 모델 A: 분류 모델] 하락장 철통방어 1등급 동네 판별기")
print("==========================================")
print(f"• Classification Accuracy (정확도): {acc_c * 100:.2f}%")
print(f"• ROC-AUC Score (분류 성능): {auc_c:.4f}")

# ==========================================
# [추천 모델 B] 다기준 의사결정 모델 (MCDM - TOPSIS)
# ==========================================
def topsis_ranking(data, weights, impact):
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

topsis_df = df[['3대도심_평균통근시간(분)', '하락기_낙폭_%', '3040비중_%', '평당단가_만원']].copy()
topsis_df['하락기_낙폭_%'] = abs(topsis_df['하락기_낙폭_%'])

weights = [0.4, 0.3, 0.2, 0.1]
impact = ['-', '-', '+', '-']

df['TOPSIS_스코어'] = topsis_ranking(topsis_df, weights, impact)

print("\n==========================================")
print("💡 [추천 모델 B: MCDM TOPSIS] 맞벌이 조건별 랭킹 Top 5")
print("==========================================")
top5 = df[['자치구', '법정동', '최근_중앙가격_억', '3대도심_평균통근시간(분)', '하락기_낙폭_%', 'TOPSIS_스코어']].sort_values('TOPSIS_스코어', ascending=False).head(5)
for idx, row in top5.iterrows():
    print(f"  {row['자치구']} {row['법정동']} | 가격: {row['최근_중앙가격_억']}억 | 통근: {row['3대도심_평균통근시간(분)']}분 | 하락낙폭: {row['하락기_낙폭_%']}% | TOPSIS점수: {row['TOPSIS_스코어']:.4f}")

# JSON 결과 저장
results = {
    "r2_ridge": r2_ridge,
    "rmse_ridge": rmse_ridge,
    "r2_rf": r2_rf,
    "rmse_rf": rmse_rf,
    "r2_total": r2_total,
    "acc_clf": acc_c,
    "auc_clf": auc_c,
    "top_features_resilience": rf_importance.head(5).to_dict(orient='records'),
    "top_features_total": rf_total_importance.head(5).to_dict(orient='records'),
    "top5_topsis": top5[['자치구', '법정동', '최근_중앙가격_억', '3대도심_평균통근시간(분)', 'TOPSIS_스코어']].to_dict(orient='records')
}

with open(r'd:\26_강의자료\프로젝트\model_execution_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n=== 모델링 실행 및 파일 저장(model_execution_results.json) 완료 ===")
