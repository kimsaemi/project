import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

target_dir = r'd:\26_강의자료\프로젝트\발표용 공유'

# 1. Generate Markdown Script for Data Analysis Beginners
script_md = """# 💻 [데이터 공부용/기술 발표] 3040 맞벌이 주거지 분석 파이프라인 발표 스크립트

> 💡 **대상 청중**: 데이터 분석/머신러닝을 공부하기 시작한 스터디 팀원 및 입문자  
> ⏱️ **소요 시간**: 약 8분 ~ 12분  
> 🎯 **발표 핵심**: 결과 중심이 아닌 **'데이터 결합(Merge) → 노이즈 제거(Preprocessing) → 모델링(Regression/TOPSIS/K-Means) → 데이터 검증(QA)'**의 프로세스 스토리라인

---

### 1. 발표 구조 비교 (일반 청중 vs 데이터 학습자)

| 구분 | 일반 청중 대상 발표 | 💻 데이터 공부/학습자 대상 발표 |
| :--- | :--- | :--- |
| **핵심 질문** | "어느 동네가 제일 좋고 집값이 안 떨어지나요?" | **"어떤 데이터셋을 어떻게 합치고, 노이즈를 어떻게 버렸는가?"** |
| **강조 영역** | 결론 동네 목록 및 가성비 1등 동네 강조 | **전처리(Cleaning), 머신러닝 프로세스, 다공선성/재현성 검증** |
| **기술적 깊이** | 쉬운 구어체 설명 (용어 배제) | **회귀($R^2$, RMSE), TOPSIS, K-Means, Ridge 정규화 개념 언급** |

---

### [슬라이드 1] 표지 — 프로젝트 소개 및 분석 프레임워크
* **화면**: 3040 맞벌이를 위한 서울 최적 아파트 주거지 분석 및 모델링
* **🗣️ 발표 멘트**:
  > "안녕하십니까, 오늘 발표를 맡은 ○○○입니다.  
  > 
  > 오늘 발표는 단순한 부동산 추천에 그치지 않고, **'실제 공공 빅데이터와 실거래가 파이프라인을 구축하여 현실의 의사결정 문제를 머신러닝으로 어떻게 해결했는가'**라는 데이터 프로젝트 탐구 과정 위주로 설명해 드리겠습니다."

---

### [슬라이드 2] 문제 정의 — 도메인 문제의 데이터 지표화
* **화면**: 01. 예산의 한계 / 02. 맞벌이 출퇴근 / 03. 자산 하락 위험
* **🗣️ 발표 멘트**:
  > *(다음 슬라이드로 이동)*  
  > "데이터 분석의 첫 단추는 **'현실의 문제를 측정 가능한 변수(Feature)로 정의하는 것'**입니다.  
  > 
  > 저희는 3040 맞벌이 가구의 3대 고충을 세 가지 데이터 지표로 정의했습니다.  
  > 첫째, 예산 한계는 국토부 실거래가 `가격_중앙값_만원`으로,  
  > 둘째, 맞벌이 출퇴근 부담은 07~09시 아침 피크타임 실측 이동량 O-D `3대도심 평균통근시간(분)`으로,  
  > 셋째, 자산 하락 위험은 금리 인상기 충격 데이터의 `하락기_낙폭_%` 변수로 수치화했습니다."

---

### [슬라이드 3] 데이터 통합 & 노이즈 처리 — Data Preprocessing
* **화면**: 83,178건 v2 실거래 데이터 결합 및 노이즈 제거 기준
* **🗣️ 발표 멘트**:
  > *(다음 슬라이드로 이동)*  
  > "데이터 학습자분들이 가장 관심 있어 하실 전처리(Cleaning) 과정입니다. 저희는 `11_실거래가_정제본_v2.csv` 총 83,178건 중에서 아파트 유효 매매 46,644건을 필터링했습니다.  
  > 
  > 여기서 중요한 도메인 전처리 노하우 두 가지가 있습니다.  
  > 첫째, **'왜 상권 분석 점포수 데이터를 버렸는가?'** 입니다. 주거지 적합도를 평가할 때 상권 점포수 데이터는 도심 상업지역에 착시를 일으키는 심각한 변수 노이즈(Noise)가 되기 때문에 전량 삭제했습니다.  
  > 둘째, **'평단가 × 면적'**으로 계산하면 거래 면적 분포에 따라 왜곡이 발생하므로, 국토부 실거래가 `가격_중앙값`을 직접 활용해 데이터 왜곡을 방지했습니다."

---

### [슬라이드 4] 회귀 모델링 — Feature Importance & Multicollinearity
* **화면**: Random Forest 회귀 R² = 83.8% & 특성 중요도 1위 (64.5%)
* **🗣️ 발표 멘트**:
  > *(다음 슬라이드로 이동)*  
  > "다음은 머신러닝 회귀(Regression) 모델링 단계입니다.  
  > 137개 법정동 패널 데이터로 **Random Forest Regressor**를 학습시킨 결과, 예측 설명력 **$R^2 = 83.8\%$**, RMSE 오차 3.55점을 달성했습니다.  
  > 
  > 머신러닝의 특성 중요도(Feature Importance) 분석 결과, 주거 만족도의 64.5%를 결정짓는 요인은 '3대 도심 평균 통근시간'이었습니다.  
  > 여기서 다공선성(Multicollinearity) 이슈가 발생했는데요. GBD, YBD, CBD 통근시간 변수 간의 다공선성을 해결하기 위해 L2 정규화를 적용한 **Ridge Regression** 모델을 함께 교차 검증하여 안정적인 계수를 도출했습니다."

---

### [슬라이드 5] 추천 1: MCDM TOPSIS 다기준 의사결정 모델
* **화면**: 페르소나별 TOPSIS 랭킹 알고리즘
* **🗣️ 발표 멘트**:
  > *(다음 슬라이드로 이동)*  
  > "단순한 회귀 모델은 모든 사용자에게 동일한 획일적 순위만 줍니다. 그래서 저희는 다기준 의사결정 기법인 **TOPSIS(Technique for Order Preference by Similarity to Ideal Solution)** 알고리즘을 도입했습니다.  
  > 
  > TOPSIS는 사용자가 설정한 가중치(예: 출퇴근 40%, 방어율 30%)에 따라 **이상적 최상 조건(Ideal Best)과 최악 조건(Ideal Worst)과의 림피크 거리를 계산**해 사용자 맞춤 랭킹을 실시간으로 갱신해 주는 알고리즘입니다."

---

### [슬라이드 6] 추천 2: K-Means 비지도 군집 분석
* **화면**: K-Means k=4 군집 세그먼트 (그룹 1~4)
* **🗣️ 발표 멘트**:
  > *(다음 슬라이드로 이동)*  
  > "다음으로 동네들의 숨은 특징 패턴을 그룹화하기 위해 비지도 학습(Unsupervised Learning)인 **K-Means Clustering (k=4)**을 적용했습니다.  
  > 
  > 5차원 특성 공간(시세, 평당단가, 3040비중, 낙폭률, 통근시간)을 StandardScaler로 표준화한 후 군집화한 결과,  
  > 강서 염창·등촌의 '가성비 실속형(그룹 1)', 영등포 당산과 동작 사당의 '광역 허브 & 방어 1위(그룹 2)', 마포 공덕의 '쿼드러플 도심 거점(그룹 3)', 노원 중계의 '학군 배후지(그룹 4)'라는 4개의 정교한 주거 세그먼트 프로필이 도출되었습니다."

---

### [슬라이드 7] 대표 동네 TOP 4 매트릭스 비교
* **화면**: 실측 수치 비교표 (당산, 사당, 염창, 공덕)
* **🗣️ 발표 멘트**:
  > *(다음 슬라이드로 이동)*  
  > "모델링 결과를 실측 수치 매트릭스로 정리한 화면입니다.  
  > 하락장 낙폭이 -7.1%로 최저였던 사당동과 2·9호선 환승으로 YBD 5분 컷인 당산동의 데이터 수치 차이를 명확히 비교할 수 있습니다."

---

### [슬라이드 8] 데이터 QA & 재현성 고정
* **화면**: 수치 검증 및 전처리 체크리스트
* **🗣️ 발표 멘트**:
  > *(다음 슬라이드로 이동)*  
  > "데이터 분석에서 가장 중요한 것은 **'재현성(Reproducibility)'**입니다.  
  > K-Means 및 Random Forest 실행 시 `random_state=42`로 시드값을 고정하여 스크립트를 재실행해도 언제나 동일한 모델 결과가 산출되도록 설계했습니다."

---

### [슬라이드 9] 대시보드 서빙 & 파이프라인 연동
* **화면**: Leaflet GIS 웹 대시보드 및 공유 폴더
* **🗣️ 발표 멘트**:
  > *(다음 슬라이드로 이동)*  
  > "마지막으로 분석 결과를 사용자가 쉽게 탐색할 수 있도록 **Leaflet GIS 데이터 시각화 웹 대시보드**를 구축했습니다.  
  > 137개 법정동의 데이터 구조를 단일 HTML 파일 내에 JSON으로 임베딩(Embedding)하여, 서버 없이도 평형별 실거래 시세와 통근시간을 경량화하여 서빙할 수 있도록 파이프라인을 완성했습니다."

---

### [슬라이드 10] 결론 & Q&A
* **화면**: 결론 및 질의응답
* **🗣️ 발표 멘트**:
  > "이상으로 도메인 문제 정의부터 전처리, 회귀/군집/TOPSIS 모델링, 웹 서빙까지의 데이터 프로젝트 발표를 마치겠습니다. 질문이나 피드백이 있으시면 감사히 받겠습니다."

---

## ❓ 데이터 스터디원/학습자 예상 질문 & 기술 답변 가이드

#### Q1. "GBD, YBD, CBD 통근시간 간의 다공선성(Multicollinearity) 문제는 없었나요?"
* **🗣️ 기술 답변**:  
  > "좋은 지적이십니다. 서울 3대 도심 소요시간 간 상관계수가 높아서 다중선형회귀 시 OLS 변수 계수가 흔들리는 문제가 있었습니다. 그래서 L2 정규화가 적용된 **Ridge Regression(alpha=1.0)** 모델을 활용해 과적합을 방지하고 계수 추정을 안정화시켰습니다."

#### Q2. "K-Means의 군집 개수(k=4)는 어떻게 결정하셨나요?"
* **🗣️ 기술 답변**:  
  > "군집 내 유클리드 거리의 제곱합(WCSS)을 측정하는 Elbow Method와 실루엣 계수(Silhouette Coefficient)를 검토했습니다. k=4일 때 군집 간 해석 가능성(Interpretability)과 세그먼트 분리도가 가장 균형을 이루었기 때문에 k=4로 최종 설정했습니다."

#### Q3. "TOPSIS 알고리즘의 정규화(Normalization) 방식은 무엇을 썼나요?"
* **🗣️ 기술 답변**:  
  > "각 변수의 단위(억원, %, 분)가 다르기 때문에 **벡터 정규화(Vector Normalization)** 방식인 $r_{ij} = \frac{x_{ij}}{\sqrt{\sum x_{ij}^2}}$를 사용했습니다. 이를 통해 가중치를 정확하게 가산할 수 있었습니다."
"""

md_path = os.path.join(target_dir, "3040_맞벌이_주거지_분석_데이터입문자용_발표대본.md")
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(script_md)

print(f"Data Student Markdown Script created at: {md_path}")

# 2. Generate HTML Printable Script File for Data Learners
html_script = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[기술 발표 대본] 3040 맞벌이 서울 주거지 분석 파이프라인 (데이터 학습자용)</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&family=IBM+Plex+Mono:wght@500;700&display=swap" rel="stylesheet">

<style>
  :root {{
    --bg: #F4F7FB;
    --paper: #FFFFFF;
    --border: #DCE4EF;
    --ink: #172033;
    --muted: #5F6B7A;
    --blue: #2855D9;
    --blue-soft: #EAF0FF;
    --green: #1D7950;
    --green-soft: #E9F8F0;
    --purple: #6B21A8;
    --purple-soft: #F3E8FF;
  }}

  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #101522;
      --paper: #171E2C;
      --border: #303A4D;
      --ink: #EDF2FB;
      --muted: #A7B2C4;
      --blue: #91ADFF;
      --blue-soft: #1B2A50;
      --green: #85DBAF;
      --green-soft: #173728;
      --purple: #C084FC;
      --purple-soft: #3B0764;
    }}
  }}

  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 24px;
    background-color: var(--bg);
    color: var(--ink);
    font-family: "Pretendard", -apple-system, sans-serif;
    line-height: 1.7;
  }}

  .wrap {{ max-width: 920px; margin: 0 auto; }}

  header {{
    background: linear-gradient(135deg, #18356F 0%, #2855D9 100%);
    color: white;
    padding: 28px 32px;
    border-radius: 18px;
    margin-bottom: 24px;
  }}
  .eyebrow {{ font-size: 13px; font-weight: 800; opacity: 0.9; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px; }}
  h1 {{ font-size: 26px; font-weight: 900; margin: 0 0 8px; line-height: 1.3; }}
  .lead {{ font-size: 15px; opacity: 0.92; margin: 0; line-height: 1.5; }}

  .slide-box {{
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
  }}

  .slide-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 10px;
    margin-bottom: 14px;
  }}

  .slide-num {{
    font-size: 12px;
    font-weight: 800;
    color: var(--blue);
    background: var(--blue-soft);
    padding: 3px 10px;
    border-radius: 99px;
  }}

  .slide-title {{
    font-size: 16.5px;
    font-weight: 800;
    color: var(--ink);
  }}

  .speech-box {{
    background: var(--blue-soft);
    border-left: 4px solid var(--blue);
    border-radius: 0 10px 10px 0;
    padding: 16px 18px;
    font-size: 15px;
    color: var(--ink);
    line-height: 1.7;
  }}

  .speech-box b {{ color: var(--blue); }}
  .speech-box code {{ background: rgba(40, 85, 217, 0.15); color: var(--blue); padding: 2px 6px; border-radius: 4px; font-family: ui-monospace, monospace; }}

  .qa-card {{
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 12px;
  }}
  .qa-q {{ font-weight: 800; color: var(--blue); font-size: 15px; margin-bottom: 6px; }}
  .qa-a {{ font-size: 14px; color: var(--muted); margin: 0; line-height: 1.6; }}

  .btn-print {{
    position: fixed;
    top: 24px; right: 24px;
    background: #0F172A;
    color: white;
    border: none;
    padding: 9px 18px;
    border-radius: 99px;
    font-weight: 800;
    font-size: 13px;
    cursor: pointer;
    z-index: 999;
  }}
  @media print {{ .btn-print {{ display: none; }} body {{ padding: 0; background: white; }} .slide-box {{ box-shadow: none; }} }}
</style>
</head>
<body>

<button class="btn-print" onclick="window.print()">🖨️ 대본 인쇄 / PDF 저장</button>

<div class="wrap">
  <header>
    <div class="eyebrow">DATA ANALYSIS & ML PIPELINE SCRIPT</div>
    <h1>3040 맞벌이 주거지 분석 파이프라인 발표 대본 (데이터 입문자용)</h1>
    <p class="lead">데이터 결합(Merge), 전처리 노이즈 삭제, 회귀/TOPSIS/K-Means 모델링 및 알고리즘 검증 과정 위주로 기술된 발표 대본입니다.</p>
  </header>

  <!-- Slide 1 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 1. 표지 (프로젝트 소개 및 분석 프레임워크)</div>
      <div class="slide-num">SLIDE 01 / 10</div>
    </div>
    <div class="speech-box">
      "안녕하십니까, 오늘 발표를 맡은 ○○○입니다.<br><br>
      오늘 발표는 단순한 부동산 추천에 그치지 않고, <b>'실제 공공 빅데이터와 실거래가 파이프라인을 구축하여 현실의 의사결정 문제를 머신러닝으로 어떻게 해결했는가'</b>라는 데이터 프로젝트 탐구 과정 위주로 설명해 드리겠습니다."
    </div>
  </div>

  <!-- Slide 2 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 2. 문제 정의 (도메인 문제의 데이터 지표화)</div>
      <div class="slide-num">SLIDE 02 / 10</div>
    </div>
    <div class="speech-box">
      <i>(다음 슬라이드로 이동)</i><br>
      "데이터 분석의 첫 단추는 <b>'현실의 문제를 측정 가능한 변수(Feature)로 정의하는 것'</b>입니다.<br><br>
      저희는 3040 맞벌이 가구의 3대 고충을 세 가지 데이터 지표로 정의했습니다.<br>
      첫째, 예산 한계는 국토부 실거래가 <code>가격_중앙값_만원</code>으로,<br>
      둘째, 맞벌이 출퇴근 부담은 07~09시 아침 피크타임 실측 이동량 O-D <code>3대도심 평균통근시간(분)</code>으로,<br>
      셋째, 자산 하락 위험은 금리 인상기 충격 데이터의 <code>하락기_낙폭_%</code> 변수로 수치화했습니다."
    </div>
  </div>

  <!-- Slide 3 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 3. 데이터 통합 & 노이즈 처리 (Data Preprocessing)</div>
      <div class="slide-num">SLIDE 03 / 10</div>
    </div>
    <div class="speech-box">
      <i>(다음 슬라이드로 이동)</i><br>
      "데이터 학습자분들이 가장 관심 있어 하실 전처리(Cleaning) 과정입니다. 저희는 <code>11_실거래가_정제본_v2.csv</code> 총 83,178건 중에서 아파트 유효 매매 46,644건을 필터링했습니다.<br><br>
      여기서 중요한 도메인 전처리 노하우 두 가지가 있습니다.<br>
      첫째, <b>'왜 상권 분석 점포수 데이터를 버렸는가?'</b> 입니다. 주거지 적합도를 평가할 때 상권 점포수 데이터는 도심 상업지역에 착시를 일으키는 심각한 변수 노이즈(Noise)가 되기 때문에 전량 삭제했습니다.<br>
      둘째, <b>'평단가 × 면적'</b>으로 계산하면 거래 면적 분포에 따라 왜곡이 발생하므로, 국토부 실거래가 <code>가격_중앙값</code>을 직접 활용해 데이터 왜곡을 방지했습니다."
    </div>
  </div>

  <!-- Slide 4 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 4. 회귀 모델링 (Feature Importance & Multicollinearity)</div>
      <div class="slide-num">SLIDE 04 / 10</div>
    </div>
    <div class="speech-box">
      <i>(다음 슬라이드로 이동)</i><br>
      "다음은 머신러닝 회귀(Regression) 모델링 단계입니다.<br>
      137개 법정동 패널 데이터로 <b>Random Forest Regressor</b>를 학습시킨 결과, 예측 설명력 <b>R² = 83.8%</b>, RMSE 오차 3.55점을 달성했습니다.<br><br>
      머신러닝의 특성 중요도(Feature Importance) 분석 결과, 주거 만족도의 64.5%를 결정짓는 요인은 '3대 도심 평균 통근시간'이었습니다.<br>
      여기서 다공선성(Multicollinearity) 이슈가 발생했는데요. GBD, YBD, CBD 통근시간 변수 간의 다공선성을 해결하기 위해 L2 정규화를 적용한 <b>Ridge Regression</b> 모델을 함께 교차 검증하여 안정적인 계수를 도출했습니다."
    </div>
  </div>

  <!-- Slide 5 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 5. 추천 1: MCDM TOPSIS 다기준 의사결정 모델</div>
      <div class="slide-num">SLIDE 05 / 10</div>
    </div>
    <div class="speech-box">
      <i>(다음 슬라이드로 이동)</i><br>
      "단순한 회귀 모델은 모든 사용자에게 동일한 획일적 순위만 줍니다. 그래서 저희는 다기준 의사결정 기법인 <b>TOPSIS(Technique for Order Preference by Similarity to Ideal Solution)</b> 알고리즘을 도입했습니다.<br><br>
      TOPSIS는 사용자가 설정한 가중치(예: 출퇴근 40%, 방어율 30%)에 따라 <b>이상적 최상 조건(Ideal Best)과 최악 조건(Ideal Worst)과의 림피크 거리를 계산</b>해 사용자 맞춤 랭킹을 실시간으로 갱신해 주는 알고리즘입니다."
    </div>
  </div>

  <!-- Slide 6 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 6. 추천 2: K-Means 비지도 군집 분석</div>
      <div class="slide-num">SLIDE 06 / 10</div>
    </div>
    <div class="speech-box">
      <i>(다음 슬라이드로 이동)</i><br>
      "다음으로 동네들의 숨은 특징 패턴을 그룹화하기 위해 비지도 학습(Unsupervised Learning)인 <b>K-Means Clustering (k=4)</b>을 적용했습니다.<br><br>
      5차원 특성 공간(시세, 평당단가, 3040비중, 낙폭률, 통근시간)을 StandardScaler로 표준화한 후 군집화한 결과,<br>
      강서 염창·등촌의 '가성비 실속형(그룹 1)', 영등포 당산과 동작 사당의 '광역 허브 & 방어 1위(그룹 2)', 마포 공덕의 '쿼드러플 도심 거점(그룹 3)', 노원 중계의 '학군 배후지(그룹 4)'라는 4개의 정교한 주거 세그먼트 프로필이 도출되었습니다."
    </div>
  </div>

  <!-- Slide 7 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 7. 대표 동네 TOP 4 매트릭스 비교</div>
      <div class="slide-num">SLIDE 07 / 10</div>
    </div>
    <div class="speech-box">
      <i>(다음 슬라이드로 이동)</i><br>
      "모델링 결과를 실측 수치 매트릭스로 정리한 화면입니다.<br>
      하락장 낙폭이 -7.1%로 최저였던 사당동과 2·9호선 환승으로 YBD 5분 컷인 당산동의 데이터 수치 차이를 명확히 비교할 수 있습니다."
    </div>
  </div>

  <!-- Slide 8 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 8. 데이터 QA & 재현성 고정</div>
      <div class="slide-num">SLIDE 08 / 10</div>
    </div>
    <div class="speech-box">
      <i>(다음 슬라이드로 이동)</i><br>
      "데이터 분석에서 가장 중요한 것은 <b>'재현성(Reproducibility)'</b>입니다.<br>
      K-Means 및 Random Forest 실행 시 <code>random_state=42</code>로 시드값을 고정하여 스크립트를 재실행해도 언제나 동일한 모델 결과가 산출되도록 설계했습니다."
    </div>
  </div>

  <!-- Slide 9 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 9. 대시보드 서빙 & 파이프라인 연동</div>
      <div class="slide-num">SLIDE 09 / 10</div>
    </div>
    <div class="speech-box">
      <i>(다음 슬라이드로 이동)</i><br>
      "마지막으로 분석 결과를 사용자가 쉽게 탐색할 수 있도록 <b>Leaflet GIS 데이터 시각화 웹 대시보드</b>를 구축했습니다.<br>
      137개 법정동의 데이터 구조를 단일 HTML 파일 내에 JSON으로 임베딩(Embedding)하여, 서버 없이도 평형별 실거래 시세와 통근시간을 경량화하여 서빙할 수 있도록 파이프라인을 완성했습니다."
    </div>
  </div>

  <!-- Slide 10 -->
  <div class="slide-box">
    <div class="slide-header">
      <div class="slide-title">슬라이드 10. 결론 & Q&A</div>
      <div class="slide-num">SLIDE 10 / 10</div>
    </div>
    <div class="speech-box">
      "이상으로 도메인 문제 정의부터 전처리, 회귀/군집/TOPSIS 모델링, 웹 서빙까지의 데이터 프로젝트 발표를 마치겠습니다. 질문이나 피드백이 있으시면 감사히 받겠습니다."
    </div>
  </div>

  <!-- Q&A Defense -->
  <h2 style="margin-top: 30px; font-size: 20px;">❓ 데이터 스터디원/학습자 예상 질문 & 기술 답변 가이드</h2>
  
  <div class="qa-card">
    <div class="qa-q">Q1. "GBD, YBD, CBD 통근시간 간의 다공선성(Multicollinearity) 문제는 없었나요?"</div>
    <div class="qa-a">"좋은 지적이십니다. 서울 3대 도심 소요시간 간 상관계수가 높아서 다중선형회귀 시 OLS 변수 계수가 흔들리는 문제가 있었습니다. 그래서 L2 정규화가 적용된 <b>Ridge Regression(alpha=1.0)</b> 모델을 활용해 과적합을 방지하고 계수 추정을 안정화시켰습니다."</div>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q2. "K-Means의 군집 개수(k=4)는 어떻게 결정하셨나요?"</div>
    <div class="qa-a">"군집 내 유클리드 거리의 제곱합(WCSS)을 측정하는 Elbow Method와 실루엣 계수(Silhouette Coefficient)를 검토했습니다. k=4일 때 군집 간 해석 가능성(Interpretability)과 세그먼트 분리도가 가장 균형을 이루었기 때문에 k=4로 최종 설정했습니다."</div>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q3. "TOPSIS 알고리즘의 정규화(Normalization) 방식은 무엇을 썼나요?"</div>
    <div class="qa-a">"각 변수의 단위(억원, %, 분)가 다르기 때문에 <b>벡터 정규화(Vector Normalization)</b> 방식인 $r_{{ij}} = \\frac{{x_{{ij}}}}{{\\sqrt{{\\sum x_{{ij}}^2}}}}$를 사용했습니다. 이를 통해 가중치를 정확하게 가산할 수 있었습니다."</div>
  </div>

</div>

</body>
</html>
"""

html_path = os.path.join(target_dir, "3040_맞벌이_주거지_분석_데이터입문자용_발표대본.html")
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_script)

print(f"Data Learner HTML Script created at: {html_path}")
