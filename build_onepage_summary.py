import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

html_onepage = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[한눈에 보는 요약 SHEET] 3040 맞벌이를 위한 서울 최적 아파트 주거지 분석</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&family=IBM+Plex+Mono:wght@500;700&display=swap" rel="stylesheet">

<style>
  :root {
    --bg: #F8FAFC;
    --paper: #FFFFFF;
    --border: #E2E8F0;
    --text-main: #0F172A;
    --text-sub: #475569;
    --blue-dark: #1E3A8A;
    --blue: #2563EB;
    --blue-soft: #EFF6FF;
    --green: #059669;
    --green-soft: #ECFDF5;
    --amber: #D97706;
    --amber-soft: #FFFBEB;
    --purple: #7C3AED;
    --purple-soft: #F5F3FF;
    --red: #DC2626;
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0F172A;
      --paper: #1E293B;
      --border: #334155;
      --text-main: #F8FAFC;
      --text-sub: #94A3B8;
      --blue-dark: #3B82F6;
      --blue: #60A5FA;
      --blue-soft: #1E3A8A;
      --green: #34D399;
      --green-soft: #064E3B;
      --amber: #FBBF24;
      --amber-soft: #451A03;
      --purple: #C084FC;
      --purple-soft: #3B0764;
      --red: #F87171;
    }
  }

  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 24px;
    background-color: var(--bg);
    color: var(--text-main);
    font-family: "Pretendard", -apple-system, sans-serif;
    line-height: 1.5;
  }

  .mono { font-family: "IBM Plex Mono", monospace; }

  .wrap { max-width: 1200px; margin: 0 auto; }

  /* Header Banner */
  header {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
    color: white;
    padding: 28px 32px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.2);
  }
  .eyebrow { font-size: 13px; font-weight: 800; letter-spacing: 0.1em; opacity: 0.85; text-transform: uppercase; }
  h1 { font-size: 28px; font-weight: 900; margin: 6px 0 10px; line-height: 1.25; }
  .lead { font-size: 15px; opacity: 0.92; max-width: 900px; margin: 0; }

  /* Top Stat Row */
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 20px;
  }
  .stat-card {
    background: var(--paper);
    border: 1px solid var(--border);
    padding: 16px 20px;
    border-radius: 14px;
    text-align: center;
  }
  .stat-val { font-size: 26px; font-weight: 900; color: var(--blue); }
  .stat-lbl { font-size: 12.5px; color: var(--text-sub); margin-top: 2px; }

  /* Main Bento Dashboard Grid */
  .bento-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 16px;
  }

  .box {
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
  }

  .col-4 { grid-column: span 4; }
  .col-6 { grid-column: span 6; }
  .col-8 { grid-column: span 8; }
  .col-12 { grid-column: span 12; }

  @media (max-width: 900px) {
    .col-4, .col-6, .col-8, .col-12 { grid-column: span 12; }
    .stat-grid { grid-template-columns: repeat(2, 1fr); }
  }

  .box-title {
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .box-title::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 16px;
    background: var(--blue);
    border-radius: 2px;
  }

  /* Table Style */
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { background: var(--bg); color: var(--text-main); font-weight: 800; padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); }
  td { padding: 8px 10px; border-bottom: 1px solid var(--border); color: var(--text-sub); }
  tr:last-child td { border-bottom: 0; }

  .badge { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 700; }
  .badge-blue { background: var(--blue-soft); color: var(--blue); }
  .badge-green { background: var(--green-soft); color: var(--green); }
  .badge-amber { background: var(--amber-soft); color: var(--amber); }
  .badge-purple { background: var(--purple-soft); color: var(--purple); }

  /* Print Button */
  .print-btn {
    position: fixed;
    top: 24px;
    right: 24px;
    background: #0F172A;
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 999;
  }
  @media print {
    .print-btn { display: none; }
    body { padding: 0; background: white; }
    .box, header, .stat-card { box-shadow: none; }
  }
</style>
</head>
<body>

<button class="print-btn" onclick="window.print()">🖨️ 인쇄 / PDF 저장</button>

<div class="wrap">
  <!-- Header Banner -->
  <header>
    <div class="eyebrow">EXECUTIVE SUMMARY DASHBOARD</div>
    <h1>3040 맞벌이를 위한 서울 최적 아파트 주거지 분석 (한눈에 보는 요약)</h1>
    <p class="lead">부동산 실거래가 + 3040 실측 통근 이동량 + 금리사이클 가격 변동성을 융합하여 3040 맞벌이 가구를 위해 설계된 1-Page 종합 요약 대시보드입니다.</p>
  </header>

  <!-- Top Stat Row -->
  <div class="stat-grid">
    <div class="stat-card">
      <div class="stat-val mono">137개</div>
      <div class="stat-lbl">서울 주요 분석 법정동 패널</div>
    </div>
    <div class="stat-card">
      <div class="stat-val mono">R² = 83.8%</div>
      <div class="stat-lbl">회귀 모델 예측 설명력</div>
    </div>
    <div class="stat-card">
      <div class="stat-val mono">64.5%</div>
      <div class="stat-lbl">주거 만족도 1위 요인 (통근시간)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val mono">-7.1%</div>
      <div class="stat-lbl">하락장 자산 방어 1위 낙폭율 (사당동)</div>
    </div>
  </div>

  <!-- Bento Grid -->
  <div class="bento-grid">
    
    <!-- Box 1: 핵심 문제 정의 -->
    <div class="box col-4">
      <div class="box-title">1. 프로젝트 핵심 목표</div>
      <p style="font-size:13.5px; color:var(--text-sub); margin-bottom:10px;">
        3040 맞벌이 가구가 가용 예산 안에서 <b>[두 부부의 출퇴근 시간 단축]</b>과 <b>[금리 하락장 가격 방어율]</b>을 한눈에 비교하여 자산 안전성이 높은 최적 동네 5~10곳을 선별.
      </p>
      <div style="background:var(--blue-soft); padding:10px 12px; border-radius:8px; font-size:12.5px; color:var(--blue); font-weight:700;">
        💡 핵심 타깃: 6억~15억 원대 예산의 3040 실수요자 & 신혼부부/학부모
      </div>
    </div>

    <!-- Box 2: 융합 데이터 및 노이즈 정리 -->
    <div class="box col-8">
      <div class="box-title">2. 융합 데이터셋 & 노이즈 전처리 명세</div>
      <table>
        <thead>
          <tr><th>구분</th><th>활용 데이터셋</th><th>분석 역할 및 정제/삭제 기준</th></tr>
        </thead>
        <tbody>
          <tr><td><b>부동산 시세</b></td><td>국토부 실거래가 패널</td><td>예산(6~8억/9~11억/12~15억) 필터링. 30억 초과 & 나홀로 아파트 <b>삭제</b>.</td></tr>
          <tr><td><b>통근 이동량</b></td><td>07~09시 실측 이동량 O-D</td><td>GBD/YBD/CBD 3대 업무지구 20분대 도달 측정. 주말/심야 데이터 <b>삭제</b>.</td></tr>
          <tr><td><b>가격 방어력</b></td><td>금리 사이클 충격 데이터</td><td>금리 인상기 하락장 낙폭률 (2021~2022) 산출. 자산 방어선 평가.</td></tr>
          <tr><td><b>상권 데이터</b></td><td>상권분석서비스 (점포수 등)</td><td>아파트 주거지 평가 시 상권 점포수 데이터는 노이즈이므로 <b>전량 삭제</b>.</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Box 3: 추천 1 - TOPSIS 개인맞춤 모델 -->
    <div class="box col-6">
      <div class="box-title">3. [추천 1] MCDM TOPSIS 개인 맞춤형 랭킹</div>
      <p style="font-size:12.5px; color:var(--text-sub); margin-bottom:8px;">사용자 가중치(출퇴근/자산방어/예산/3040밀집도) 입력에 따른 실시간 최적 입지</p>
      <table>
        <thead>
          <tr><th>페르소나 유형</th><th>가중치 설정</th><th>1위 추천 동네</th><th>2위 추천 동네</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="badge badge-blue">A. 신혼가성비</span></td>
            <td>통근50% / 예산30%</td>
            <td><b>영등포동2가</b> (7.35억)</td>
            <td><b>종로구 숭인동</b> (5.20억)</td>
          </tr>
          <tr>
            <td><span class="badge badge-green">B. 자산방어형</span></td>
            <td>방어50% / 통근30%</td>
            <td><b>영등포동2가</b> (+1.5%)</td>
            <td><b>구로구 구로동</b> (-2.4%)</td>
          </tr>
          <tr>
            <td><span class="badge badge-amber">C. 도심성장형</span></td>
            <td>통근40% / 3040 30%</td>
            <td><b>강서구 염창동</b> (43.3%)</td>
            <td><b>영등포구 당산동</b> (38.5%)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Box 4: 추천 2 - K-Means 4대 군집 분석 -->
    <div class="box col-6">
      <div class="box-title">4. [추천 2] K-Means 4대 주거 세그먼트</div>
      <table>
        <thead>
          <tr><th>군집 세그먼트</th><th>시세 대역</th><th>하락장 방어율</th><th>대표 동네 & 추천 특징</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="badge badge-blue">그룹 1 (실속)</span></td>
            <td>6.0~8.3억</td>
            <td>-21.7% ~ -29.1%</td>
            <td><b>강서 염창·등촌</b> (9호선급행/3040 1위)</td>
          </tr>
          <tr>
            <td><span class="badge badge-green">그룹 2 (방어1위)★</span></td>
            <td>9.6~11.5억</td>
            <td><b>-7.1% ~ -12.0%</b></td>
            <td><b>영등포 당산, 동작 사당</b> (방어력 1위)</td>
          </tr>
          <tr>
            <td><span class="badge badge-amber">그룹 3 (도심거점)</span></td>
            <td>12.1~15.4억</td>
            <td>상승기 +40.9%</td>
            <td><b>마포 공덕, 송파 문정</b> (쿼드러플/반등탄력)</td>
          </tr>
          <tr>
            <td><span class="badge badge-purple">그룹 4 (학군배후)</span></td>
            <td>7.5~10.5억</td>
            <td>-22.8% ~ -29.5%</td>
            <td><b>노원 중계, 강동 고덕</b> (서울3대 학군)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Box 5: TOP 4 법정동 종합 비교 -->
    <div class="box col-12">
      <div class="box-title">5. 서울 핵심 추천 법정동 TOP 4 실측 데이터 매트릭스</div>
      <table>
        <thead>
          <tr><th>자치구 / 법정동</th><th>중앙 매매가</th><th>평당 단가</th><th>3대도심 통근시간</th><th>하락장 낙폭</th><th>3040 비중</th><th>핵심 전략 및 타깃 추천</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><b>영등포구 당산동</b></td>
            <td><b>11.5억 원</b></td>
            <td>1,535만 원</td>
            <td>YBD 5분 / GBD 15분</td>
            <td style="color:var(--green); font-weight:bold;">-12.0% (방어 1위)</td>
            <td>38.5%</td>
            <td><b>[실수요 1위]</b> 2·9호선 환승 요충지, 맞벌이 직장 다를 때 최고 절충지</td>
          </tr>
          <tr>
            <td><b>동작구 사당동</b></td>
            <td><b>10.7억 원</b></td>
            <td>1,397만 원</td>
            <td>GBD 10분 / CBD 20분</td>
            <td style="color:var(--green); font-weight:bold;">-7.1% (방어 1위)</td>
            <td>33.0%</td>
            <td><b>[자산방어 1위]</b> 하락장 낙폭 서울 최저, 강남/도심 사통팔달 교통망</td>
          </tr>
          <tr>
            <td><b>강서구 염창동</b></td>
            <td><b>8.3억 원</b></td>
            <td>1,175만 원</td>
            <td>YBD 10분 / GBD 25분</td>
            <td>-29.1%</td>
            <td style="color:var(--blue); font-weight:bold;">43.3% (서울 1위)</td>
            <td><b>[가성비 1위]</b> 6~8억대 30대 첫 집 및 신혼부부 최적, 9호선 급행역</td>
          </tr>
          <tr>
            <td><b>마포구 공덕동</b></td>
            <td><b>14.1억 원</b></td>
            <td>1,894만 원</td>
            <td>YBD 5분 / CBD 10분</td>
            <td style="color:var(--amber); font-weight:bold;">상승기 +40.9%</td>
            <td>32.9%</td>
            <td><b>[자산성장 1위]</b> 4개 노선 쿼드러플 환승, 직주근접 종결지 및 고탄력</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</div>

</body>
</html>
"""

onepage_html_path = r'd:\26_강의자료\프로젝트\3040_맞벌이_주거지_분석_한눈에보는_발표요약.html'
with open(onepage_html_path, 'w', encoding='utf-8') as f:
    f.write(html_onepage)

print("One-Page Summary HTML Dashboard created at:", onepage_html_path)

# Generate Markdown Summary File
onepage_md = """# 📊 [한눈에 보는 요약 SHEET] 3040 맞벌이를 위한 서울 최적 아파트 주거지 분석

---

## Ⅰ. 프로젝트 핵심 요약 (Executive Summary)

* **핵심 질문**: *"내 예산으로 출퇴근도 편하고, 하락장에도 집값이 덜 떨어지는 서울 동네는 어디일까?"*
* **분석 대상**: 서울시 주요 137개 법정동 패널 데이터 (실거래가 + 3040 실측 통근량 + 금리사이클 낙폭율)
* **핵심 성능**: 머신러닝 Random Forest 회귀 모델 **$R^2 = 83.8\%$** 달성 (3대 도심 통근시간 기여도 **64.5%**)
* **한눈에 보는 요약 HTML 파일**: [3040_맞벌이_주거지_분석_한눈에보는_발표요약.html](file:///d:/26_%EA%B0%95%EC%9D%98%EC%9E%90%EB%A3%8C/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/3040_%EB%A7%9E%EB%B2%8C%EC%9D%B4_%EC%A3%BC%EA%B1%B0%EC%A7%80_%EB%B6%84%EC%84%9D_%ED%95%9C%EB%88%88%EC%97%90%EB%B3%B4%EB%8A%94_%EB%B0%9C%ED%91%9C%EC%90%84%EC%95%BD.html)

---

## Ⅱ. 핵심 데이터 매트릭스 (4대 대표 법정동 비교)

| 구분 | 자치구 / 법정동 | 중앙 매매가 | 평당 단가 | 3대도심 통근시간 | 하락장 방어율 | 3040 거주비중 | 핵심 추천 포인트 및 타깃 |
| :--- | :--- | :---: | :---: | :--- | :---: | :---: | :--- |
| **실수요 1위** | **영등포구 당산동** | **11.5억 원** | 1,535만 원 | YBD 5분 / GBD 15분 | **-12.0% (방어 1위)** | 38.5% | 2·9호선 환승 요충지, 맞벌이 부부 직장 다를 때 최고 절충지 |
| **자산방어 1위** | **동작구 사당동** | **10.7억 원** | 1,397만 원 | GBD 10분 / CBD 20분 | **-7.1% (서울 최저)** | 33.0% | 하락장 낙폭 서울 최저 수준, 강남/도심 20분대 사통팔달 |
| **가성비 1위** | **강서구 염창동** | **8.3억 원** | 1,175만 원 | YBD 10분 / GBD 25분 | -29.1% | **43.3% (서울 1위)** | 6~8억대 30대 첫 집 및 신혼부부 1순위, 9호선 급행 역세권 |
| **자산성장 1위** | **마포구 공덕동** | **14.1억 원** | 1,894만 원 | YBD 5분 / CBD 10분 | **상승기 +40.9%** | 32.9% | 4개 노선 쿼드러플 환승, 직주근접 종결지 및 금리인하기 반등 폭발 |

---

## Ⅲ. 2대 핵심 추천 모델링 구성

### 1. [추천 1] MCDM TOPSIS 개인 맞춤형 알고리즘
* **개념**: 사용자 가중치(출퇴근 40% + 방어력 30% + 3040비중 20% + 예산 10%)에 따른 실시간 맞춤 랭킹.
* **결과**: 신혼부부 1위(`영등포동2가 7.35억`), 자산방어 1위(`영등포동2가 +1.5%`), 도심성장 1위(`강서구 염창동 43.3%`).

### 2. [추천 2] K-Means 4대 주거 세그먼트 (군집 분석)
* **그룹 1 (가성비 실속)**: 6.0~8.3억 원 | 강서 염창·등촌, 관악 봉천 (3040비중 43.3% 서울 1위)
* **그룹 2 (광역 허브 & 방어 1위)**: 9.6~11.5억 원 | 영등포 당산, 동작 사당, 구로 신도림 (하락장 낙폭 -7~-12%)
* **그룹 3 (쿼드러플 & 도심 거점)**: 12.1~15.4억 원 | 마포 공덕·도화, 송파 문정·가락 (상승기 +40.9% 반등 탄력)
* **그룹 4 (자녀 보육 & 학군 배후)**: 7.5~10.5억 원 | 노원 중계, 강동 고덕·명일 (서울 3대 명문 학군)

---

## Ⅳ. 데이터 검증 및 삭제 노이즈 명세

1. **사용 지표**: `단가 × 면적` 착시 대신 국토부 실거래가 `가격_중앙값_만원`을 직접 사용하여 수치 왜곡 방지.
2. **시간대 필터링**: 07:00~09:59 아침 피크 타임 실측 이동량만 정밀 추출.
3. **전량 삭제 노이즈**: `상권분석서비스(점포수 등)` 주거 평가 노이즈 제거, 빌라/단독/오피스텔 비주거 주택 삭제, 30억 초과 및 나홀로 아파트 제거.
"""

onepage_md_path = r'd:\26_강의자료\프로젝트\3040_맞벌이_주거지_분석_한눈에보는_요약.md'
with open(onepage_md_path, 'w', encoding='utf-8') as f:
    f.write(onepage_md)

print("One-Page Summary Markdown created at:", onepage_md_path)
