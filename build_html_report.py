import sys
import pandas as pd
import numpy as np
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Read CSV data
csv_path = r'd:\26_강의자료\프로젝트\3040_맞벌이_주거지_클러스터링_분석결과.csv'
df = pd.read_csv(csv_path)

records = []
for idx, row in df.iterrows():
    records.append({
        "gu": str(row['자치구']),
        "dong": str(row['법정동']),
        "tier": str(row['예산티어']),
        "price": float(row['최근_중앙가격_억']),
        "unit_price": float(row['평당단가_만원']),
        "p3040": float(row['3040비중_%']),
        "drop": float(row['하락기_낙폭_%']),
        "commute": float(row['3대도심_평균통근시간(분)']),
        "cluster": str(row['Cluster_Name']),
        "top_newlywed": round(float(row['TOPSIS_신혼부부']), 4),
        "top_defense": round(float(row['TOPSIS_자산방어']), 4),
        "top_growth": round(float(row['TOPSIS_도심성장']), 4)
    })

json_data_str = json.dumps(records, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>3040 맞벌이를 위한 서울 최적 아파트 주거지 분석 및 모델링 종합 리포트</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Gothic+A1:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
  :root {{
    --paper: #F7F2E9;
    --paper-dim: #EDE5D4;
    --paper-line: #DCD2BC;
    --ink: #1B2436;
    --ink-soft: #4B5163;
    --line: #8A8065;
    --teal: #1F7A6C;
    --teal-soft: #DCEEE9;
    --terracotta: #C8663F;
    --terracotta-soft: #F4E1D5;
    --mix: #8A8065;
    --mix-soft: #EDE7D8;
    --gold: #B5842A;
    --gold-soft: #F2E4C4;
    --purple: #6B21A8;
    --purple-soft: #F3E8FF;
    --surface: #FFFFFF;
    --shadow: 0 1px 2px rgba(27,36,54,0.06), 0 8px 24px -12px rgba(27,36,54,0.18);
  }}

  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --paper: #171B24;
      --paper-dim: #1E232E;
      --paper-line: #323847;
      --ink: #EDE9DD;
      --ink-soft: #B9BECB;
      --line: #8D93A3;
      --teal: #4FBBA6;
      --teal-soft: #1C3733;
      --terracotta: #E58A61;
      --terracotta-soft: #3A2A22;
      --mix: #9DA3B3;
      --mix-soft: #282C36;
      --gold: #E0B458;
      --gold-soft: #332A15;
      --purple: #C084FC;
      --purple-soft: #3B0764;
      --surface: #1E232E;
      --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 8px 24px -12px rgba(0,0,0,0.5);
    }}
  }}

  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: "Gothic A1", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
  }}

  h1, h2, h3 {{ font-family: "Gowun Batang", "Noto Serif KR", serif; font-weight: 700; text-wrap: balance; color: var(--ink); margin: 0; }}
  .mono {{ font-family: "IBM Plex Mono", ui-monospace, monospace; font-variant-numeric: tabular-nums; }}

  a {{ color: inherit; }}

  .wrap {{ max-width: 860px; margin: 0 auto; padding: 0 24px; }}
  .wrap-wide {{ max-width: 1100px; margin: 0 auto; padding: 0 24px; }}

  /* Topbar */
  .topbar {{
    position: sticky; top: 0; z-index: 50;
    background: color-mix(in srgb, var(--paper) 90%, transparent);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--paper-line);
  }}
  .topbar-inner {{
    max-width: 1100px; margin: 0 auto; padding: 14px 24px;
    display: flex; align-items: center; justify-content: space-between; gap: 16px;
  }}
  .topbar-title {{ font-family: "Gowun Batang", serif; font-size: 16px; font-weight: 700; white-space: nowrap; }}
  .topbar-nav {{ display: flex; gap: 18px; font-size: 13px; color: var(--ink-soft); flex-wrap: wrap; }}
  .topbar-nav a {{ text-decoration: none; border-bottom: 1px solid transparent; padding-bottom: 2px; transition: all 0.2s; }}
  .topbar-nav a:hover {{ border-bottom-color: var(--terracotta); color: var(--ink); }}

  /* Hero */
  .hero {{ padding: 56px 0 36px; }}
  .eyebrow {{
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 12.5px; letter-spacing: 0.08em; color: var(--line);
    text-transform: uppercase; margin-bottom: 16px;
  }}
  .eyebrow .dot {{ width: 7px; height: 7px; border-radius: 50%; background: var(--terracotta); }}
  .hero h1 {{ font-size: clamp(28px, 4.5vw, 40px); line-height: 1.3; }}
  .hero h1 em {{ font-style: normal; color: var(--terracotta); }}
  .hero p.lede {{ font-size: 16.5px; color: var(--ink-soft); max-width: 60ch; margin-top: 16px; }}

  .stat-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: var(--paper-line); border: 1px solid var(--paper-line); border-radius: 12px; overflow: hidden; margin-top: 32px; }}
  .stat {{ background: var(--surface); padding: 18px 16px; }}
  .stat .n {{ font-size: 26px; font-weight: 600; color: var(--teal); }}
  .stat .l {{ font-size: 12px; color: var(--ink-soft); margin-top: 4px; line-height: 1.4; }}
  @media (max-width: 768px){{ .stat-row {{ grid-template-columns: repeat(2, 1fr); }} }}

  /* Sections */
  section {{ padding: 52px 0; border-top: 1px solid var(--paper-line); scroll-margin-top: 60px; }}
  .section-head {{ display: flex; align-items: baseline; gap: 14px; margin-bottom: 24px; }}
  .section-num {{ font-family: "IBM Plex Mono", monospace; font-size: 13px; color: var(--terracotta); border: 1px solid var(--terracotta); border-radius: 99px; padding: 2px 10px; flex: none; }}
  .section-head h2 {{ font-size: clamp(22px, 3vw, 28px); }}
  .section-sub {{ color: var(--ink-soft); font-size: 14.5px; margin: -14px 0 24px; max-width: 64ch; }}

  /* Cards Grid */
  .cards3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
  @media (max-width: 800px){{ .cards3 {{ grid-template-columns: 1fr; }} }}
  .card {{ background: var(--surface); border: 1px solid var(--paper-line); border-radius: 14px; padding: 22px 20px; box-shadow: var(--shadow); }}
  .card .tag {{ font-size: 12px; letter-spacing: 0.06em; text-transform: uppercase; font-weight: 700; margin-bottom: 10px; }}
  .card p {{ font-size: 13.5px; color: var(--ink-soft); margin: 0; }}
  .card.cause .tag {{ color: var(--terracotta); }}
  .card.target .tag {{ color: var(--ink); }}
  .card.effect .tag {{ color: var(--teal); }}

  /* Personas Grid */
  .persona-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 20px; }}
  @media (max-width: 850px){{ .persona-grid {{ grid-template-columns: 1fr; }} }}
  .p-card {{ background: var(--surface); border: 1.5px solid var(--paper-line); border-radius: 14px; padding: 20px; box-shadow: var(--shadow); position: relative; }}
  .p-card.p1 {{ border-top: 4px solid var(--teal); }}
  .p-card.p2 {{ border-top: 4px solid var(--terracotta); }}
  .p-card.p3 {{ border-top: 4px solid var(--gold); }}
  .p-card h3 {{ font-size: 16px; font-weight: 700; margin-bottom: 6px; }}
  .p-card .weights {{ font-size: 12px; color: var(--ink-soft); font-family: "IBM Plex Mono", monospace; background: var(--paper-dim); padding: 4px 8px; border-radius: 6px; display: inline-block; margin-bottom: 12px; }}
  .p-card ul {{ margin: 0; padding-left: 18px; font-size: 13px; color: var(--ink-soft); }}
  .p-card li {{ margin-bottom: 6px; }}

  /* Cluster Grid */
  .cluster-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 20px; }}
  @media (max-width: 750px){{ .cluster-grid {{ grid-template-columns: 1fr; }} }}
  .c-card {{ background: var(--surface); border: 1px solid var(--paper-line); border-radius: 14px; padding: 20px; box-shadow: var(--shadow); }}
  .c-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid var(--paper-line); padding-bottom: 8px; }}
  .c-title {{ font-size: 15px; font-weight: 700; }}
  .c-badge {{ font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; }}
  .c1 .c-badge {{ background: var(--teal-soft); color: var(--teal); }}
  .c2 .c-badge {{ background: var(--terracotta-soft); color: var(--terracotta); }}
  .c3 .c-badge {{ background: var(--gold-soft); color: var(--gold); }}
  .c4 .c-badge {{ background: var(--purple-soft); color: var(--purple); }}
  .c-metrics {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12.5px; color: var(--ink-soft); margin-bottom: 12px; }}
  .c-metrics b {{ color: var(--ink); font-family: "IBM Plex Mono", monospace; }}

  /* Finder Tool */
  .tool {{ background: var(--surface); border: 1px solid var(--paper-line); border-radius: 16px; box-shadow: var(--shadow); overflow: hidden; }}
  .tool-controls {{ background: var(--paper-dim); padding: 20px 24px; display: flex; flex-wrap: wrap; gap: 18px; align-items: flex-end; border-bottom: 1px solid var(--paper-line); }}
  .field label {{ display: block; font-size: 11.5px; font-weight: 700; color: var(--ink-soft); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px; }}
  .budget-input {{ display: flex; align-items: center; gap: 6px; background: var(--surface); border: 1.5px solid var(--paper-line); border-radius: 10px; padding: 7px 12px; }}
  .budget-input input {{ width: 80px; border: none; background: transparent; font-family: "IBM Plex Mono", monospace; font-size: 17px; font-weight: 600; color: var(--ink); outline: none; }}
  .budget-input span {{ color: var(--ink-soft); font-size: 13.5px; }}
  .chip-row {{ display: flex; gap: 6px; flex-wrap: wrap; }}
  .chip {{ font-size: 12.5px; padding: 6px 12px; border-radius: 99px; border: 1.5px solid var(--paper-line); background: var(--surface); color: var(--ink-soft); cursor: pointer; font-family: "Gothic A1", sans-serif; transition: all 0.15s; }}
  .chip:hover {{ border-color: var(--line); }}
  .chip.active {{ background: var(--ink); border-color: var(--ink); color: var(--paper); }}
  .field.search input {{ border: 1.5px solid var(--paper-line); border-radius: 10px; padding: 8px 12px; font-family: "Gothic A1", sans-serif; font-size: 13.5px; background: var(--surface); color: var(--ink); outline: none; width: 170px; }}
  .field.search input:focus, .budget-input:focus-within {{ border-color: var(--terracotta); }}

  .tool-summary {{ padding: 14px 24px; font-size: 13.5px; color: var(--ink-soft); border-bottom: 1px solid var(--paper-line); display: flex; justify-content: space-between; align-items: center; }}
  .tool-summary b {{ color: var(--ink); font-family: "IBM Plex Mono", monospace; }}

  .table-scroll {{ overflow: auto; max-height: 520px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; min-width: 850px; }}
  thead th {{ position: sticky; top: 0; z-index: 2; background: var(--paper-dim); text-align: left; font-weight: 700; font-size: 11.5px; color: var(--ink-soft); padding: 10px 14px; border-bottom: 1px solid var(--paper-line); cursor: pointer; user-select: none; white-space: nowrap; }}
  thead th:hover {{ color: var(--ink); }}
  thead th.num, td.num {{ text-align: right; }}
  tbody td {{ padding: 9px 14px; border-bottom: 1px solid var(--paper-line); white-space: nowrap; }}
  tbody tr:hover {{ background: var(--paper-dim); }}
  tbody td.num {{ font-family: "IBM Plex Mono", monospace; }}

  .badge {{ display: inline-block; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 4px; }}
  .badge.g1 {{ background: var(--teal-soft); color: var(--teal); }}
  .badge.g2 {{ background: var(--terracotta-soft); color: var(--terracotta); }}
  .badge.g3 {{ background: var(--gold-soft); color: var(--gold); }}
  .badge.g4 {{ background: var(--purple-soft); color: var(--purple); }}

  footer {{ padding: 48px 0; border-top: 1px solid var(--paper-line); font-size: 12.5px; color: var(--line); }}
  footer .cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  @media (max-width: 600px){{ footer .cols {{ grid-template-columns: 1fr; }} }}
  footer h5 {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ink-soft); margin-bottom: 8px; font-weight: 700; font-family: "Gothic A1", sans-serif; }}
</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-inner">
    <div class="topbar-title">3040 주거지 최적화 모델링 리포트</div>
    <nav class="topbar-nav">
      <a href="#problem">문제정의</a>
      <a href="#topsis">TOPSIS 맞춤모델</a>
      <a href="#cluster">4대 군집분석</a>
      <a href="#finder">동네 검색 도구</a>
      <a href="#pipeline">데이터 파이프라인</a>
    </nav>
  </div>
</div>

<div class="wrap">
  <div class="hero">
    <div class="eyebrow"><span class="dot"></span>서울 아파트 실수요 & 자산방어 융합 모델링</div>
    <h1>3040 맞벌이를 위한 <em>서울 최적 주거지</em> 종합 리포트</h1>
    <p class="lede">실거래가 + 3040 실측 통근 이동량 + 금리사이클 가격 변동성을 융합하여, 예산대별 출퇴근도 편하고 집값 방어력이 우수한 서울 최적 법정동을 모델링했습니다.</p>

    <div class="stat-row">
      <div class="stat"><div class="n mono">137</div><div class="l">분석 대상 서울 주요 법정동 패널</div></div>
      <div class="stat"><div class="n mono">83.8%</div><div class="l">3040 주거선호 회귀모델 설명력 (R²)</div></div>
      <div class="stat"><div class="n mono">64.5%</div><div class="l">주거 만족도 1위 결정요인 (통근시간)</div></div>
      <div class="stat"><div class="n mono">-7.1%</div><div class="l">하락장 가격 방어 1위 낙폭율 (사당동)</div></div>
    </div>
  </div>
</div>

<section id="problem">
  <div class="wrap">
    <div class="section-head"><span class="section-num">01</span><h2>문제정의 & 핵심 목적</h2></div>
    <p class="section-sub">3040 맞벌이 가구가 주거지를 선택할 때 직면하는 3가지 핵심 과제 해결</p>
    <div class="cards3">
      <div class="card cause">
        <div class="tag">01. 예산 제약</div>
        <p>가용 가능한 예산대(6~8억 / 9~11억 / 12~15억) 내에서 선택 가능한 법정동 필터링 필요.</p>
      </div>
      <div class="card target">
        <div class="tag">02. 출퇴근 접근성</div>
        <p>맞벌이 부부의 3대 업무지구(GBD, YBD, CBD) 20분대 도달 실측 이동시간 검증.</p>
      </div>
      <div class="card effect">
        <div class="tag">03. 가격 방어력</div>
        <p>금리 인상기 하락장에 집값이 덜 떨어지고, 금리 인하기에 빠르게 반등하는 자산 안전성 포착.</p>
      </div>
    </div>
  </div>
</section>

<section id="topsis">
  <div class="wrap">
    <div class="section-head"><span class="section-num">02</span><h2>[추천 1] MCDM TOPSIS 개인 맞춤형 모델</h2></div>
    <p class="section-sub">사용자(맞벌이 부부)의 개인 가치관 및 조건 가중치(Weights)를 반영한 실시간 최적 입지 랭킹 알고리즘</p>

    <div class="persona-grid">
      <div class="p-card p1">
        <h3>A. 신혼 & 첫 집 (가성비형)</h3>
        <div class="weights">통근 50% | 예산 30% | 방어 10% | 3040 10%</div>
        <ul>
          <li><strong>1위: 영등포구 영등포동2가</strong> (7.35억 / 통근 41분)</li>
          <li><strong>2위: 종로구 숭인동</strong> (5.20억 / 통근 46분)</li>
          <li><strong>3위: 관악구 남현동</strong> (7.22억 / 통근 45분)</li>
        </ul>
      </div>

      <div class="p-card p2">
        <h3>B. 자산방어형 (하락장 안정)</h3>
        <div class="weights">방어 50% | 통근 30% | 3040 10% | 예산 10%</div>
        <ul>
          <li><strong>1위: 영등포구 영등포동2가</strong> (하락낙폭 +1.5%)</li>
          <li><strong>2위: 종로구 숭인동</strong> (하락낙폭 +1.3%)</li>
          <li><strong>3위: 구로구 구로동</strong> (하락낙폭 -2.4%)</li>
        </ul>
      </div>

      <div class="p-card p3">
        <h3>C. 직주근접 & 도심성장형</h3>
        <div class="weights">통근 40% | 3040 30% | 방어 20% | 예산 10%</div>
        <ul>
          <li><strong>1위: 강서구 염창동</strong> (3040비중 43.3%)</li>
          <li><strong>2위: 강서구 가양동</strong> (3040비중 43.3%)</li>
          <li><strong>3위: 영등포구 당산동</strong> (3040비중 38.5%)</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section id="cluster">
  <div class="wrap">
    <div class="section-head"><span class="section-num">03</span><h2>[추천 2] K-Means 4대 주거지 세그먼트 군집 분석</h2></div>
    <p class="section-sub">서울 주요 법정동의 시세, 통근시간, 방어율, 인구구조 특성에 따른 4개 대표 군집 분류</p>

    <div class="cluster-grid">
      <div class="c-card c1">
        <div class="c-header">
          <div class="c-title">그룹 1: 가성비 실속 & 실수요 밀집</div>
          <div class="c-badge">6.0억 ~ 8.3억</div>
        </div>
        <div class="c-metrics">
          <div>평균통근: <b>20~25분</b></div>
          <div>3040비중: <b>43.3% (서울 1위)</b></div>
          <div>대표동네: <b>염창동, 등촌동, 봉천동</b></div>
          <div>핵심특징: <b>9호선 급행 / 신림선 직결</b></div>
        </div>
      </div>

      <div class="c-card c2">
        <div class="c-header">
          <div class="c-title">그룹 2: 광역 허브 & 철통 방어선 ★</div>
          <div class="c-badge">9.6억 ~ 11.5억</div>
        </div>
        <div class="c-metrics">
          <div>평균통근: <b>15~20분</b></div>
          <div>하락낙폭: <b>-7.1% ~ -12.0% (최저)</b></div>
          <div>대표동네: <b>당산동, 사당동, 신도림동</b></div>
          <div>핵심특징: <b>2·9호선/2·4·7호선 환승 거점</b></div>
        </div>
      </div>

      <div class="c-card c3">
        <div class="c-header">
          <div class="c-title">그룹 3: 쿼드러플 & 도심 거점</div>
          <div class="c-badge">12.1억 ~ 15.4억</div>
        </div>
        <div class="c-metrics">
          <div>평균통근: <b>5~10분 (초근접)</b></div>
          <div>반등탄력: <b>상승기 +40.9% 폭발</b></div>
          <div>대표동네: <b>공덕동, 도화동, 문정동</b></div>
          <div>핵심특징: <b>4개 노선 환승 직주근접</b></div>
        </div>
      </div>

      <div class="c-card c4">
        <div class="c-header">
          <div class="c-title">그룹 4: 자녀 보육 & 학군 배후</div>
          <div class="c-badge">7.5억 ~ 10.5억</div>
        </div>
        <div class="c-metrics">
          <div>평균통근: <b>30~40분</b></div>
          <div>주간인구: <b>70%대 (조용한 주거)</b></div>
          <div>대표동네: <b>중계동(은행사거리), 고덕동</b></div>
          <div>핵심특징: <b>서울 3대 명문 학군</b></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="finder" class="wide">
  <div class="wrap-wide">
    <div class="section-head"><span class="section-num">04</span><h2>내 예산 및 조건으로 서울 동네 직접 찾아보기</h2></div>
    <p class="section-sub">예산, 군집 세그먼트, 페르소나 정렬 기준 및 자치구/동 이름으로 137개 분석 대상 법정동 탐색</p>

    <div class="tool">
      <div class="tool-controls">
        <div class="field">
          <label for="budget">내 가용 예산</label>
          <div class="budget-input">
            <input type="number" id="budget" min="0" step="0.5" placeholder="예: 10" />
            <span>억원 이하</span>
          </div>
        </div>

        <div class="field">
          <label>주거지 군집 세그먼트</label>
          <div class="chip-row" id="cluster-chips">
            <button class="chip active" data-cls="전체">전체</button>
            <button class="chip" data-cls="그룹 1">그룹 1 (가성비/실속)</button>
            <button class="chip" data-cls="그룹 2">그룹 2 (광역/방어1위)</button>
            <button class="chip" data-cls="그룹 3">그룹 3 (쿼드러플/도심)</button>
            <button class="chip" data-cls="그룹 4">그룹 4 (학군/보육)</button>
          </div>
        </div>

        <div class="field search">
          <label for="search">자치구 · 동 이름</label>
          <input type="text" id="search" placeholder="예: 영등포구 또는 당산" />
        </div>
      </div>

      <div class="tool-summary">
        <div>조건 만족 동네: <b id="result-count">137</b>곳 <span style="color:var(--line)">(전체 137곳 중)</span></div>
        <div style="font-size: 12px; color: var(--ink-soft);">* 열 제목 클릭 시 해당 항목으로 정렬 가능</div>
      </div>

      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th data-key="gu">자치구</th>
              <th data-key="dong">법정동</th>
              <th data-key="price" class="num">중앙 매매가</th>
              <th data-key="unit_price" class="num">평당 단가</th>
              <th data-key="commute" class="num">3대도심 통근시간</th>
              <th data-key="drop" class="num">하락기 낙폭</th>
              <th data-key="p3040" class="num">3040 비중</th>
              <th data-key="cluster">군집 구분</th>
              <th data-key="top_defense" class="num">TOPSIS 점수</th>
            </tr>
          </thead>
          <tbody id="table-body"></tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<section id="pipeline">
  <div class="wrap">
    <div class="section-head"><span class="section-num">05</span><h2>팀원 공유용 데이터 통합 및 정제 명세서</h2></div>
    <div class="cards3">
      <div class="card cause">
        <div class="tag">1. 통합 결합 키</div>
        <p>국토부 실거래가 + 수도권 07~09시 생활이동 O-D 통근 데이터 + 금리사이클 가격 흔들림 순위표를 <code>법정동코드</code>로 결합.</p>
      </div>
      <div class="card target">
        <div class="tag">2. 삭제 대상 데이터</div>
        <p>상권 길단위인구/점포수 노이즈 데이터 삭제, 빌라/단독/오피스텔 비주거 주택 제거, 30억 초과 초고가 단지 및 나홀로 아파트 제외.</p>
      </div>
      <div class="card effect">
        <div class="tag">3. 다음 단계를 위한 제안</div>
        <p>웹 대시보드(HTML) 내 가중치 동적 슬라이더 구현 및 파이썬 파이프라인 자동화 모듈(run_clustering_topsis.py) 유지 관리.</p>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <h5>데이터 출처 및 라이선스</h5>
        부동산 실거래가: 국토교통부 · 서울시 실거래가 데이터 패널<br/>
        통근 이동량: 서울 열린데이터광장 수도권 생활이동 데이터 (07~09시 피크 타임)
      </div>
      <div>
        <h5>팀원 공유용 관련 분석 파일</h5>
        [보고서] <a href="file:///d:/26_%EA%B0%95%EC%9D%98%EC%9E%90%EB%A3%8C/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/3040_%EB%A7%9E%EB%B2%8C%EC%9D%B4_%EC%A3%BC%EA%B1%B0%EC%A7%80_%EB%B6%84%EC%84%9D_%EB%B0%8F_%EB%AA%A8%EB%8D%B8%EB%A7%81_%ED%8C%80%EA%B3%B5%EC%9C%A0%EB%A6%AC%ED%8F%AC%ED%8A%B8.md">3040_맞벌이_주거지_분석_및_모델링_팀공유리포트.md</a><br/>
        [데이터] <a href="file:///d:/26_%EA%B0%95%EC%9D%98%EC%9E%90%EB%A3%8C/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/3040_%EB%A7%9E%EB%B2%8C%EC%9D%B4_%EC%A3%BC%EA%B1%B0%EC%A7%80_%ED%80%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%A9%9D_%EB%B6%84%EC%84%9D%EA%B2%B0%EA%B3%BC.csv">3040_맞벌이_주거지_클러스터링_분석결과.csv</a>
      </div>
    </div>
  </div>
</footer>

<script>
const DONG_DATA = {json_data_str};

(function(){{
  const budgetEl = document.getElementById('budget');
  const searchEl = document.getElementById('search');
  const chips = Array.from(document.querySelectorAll('#cluster-chips .chip'));
  const tbody = document.getElementById('table-body');
  const countEl = document.getElementById('result-count');
  const ths = Array.from(document.querySelectorAll('th[data-key]'));

  let activeCluster = '전체';
  let sortKey = 'top_defense';
  let sortDir = -1;

  function getBadgeClass(clsName){{
    if(clsName.includes('그룹 1')) return 'g1';
    if(clsName.includes('그룹 2')) return 'g2';
    if(clsName.includes('그룹 3')) return 'g3';
    return 'g4';
  }}

  function render(){{
    const budget = parseFloat(budgetEl.value);
    const hasBudget = !isNaN(budget) && budget > 0;
    const q = searchEl.value.trim().toLowerCase();

    let rows = DONG_DATA.filter(d => {{
      if(hasBudget && d.price > budget) return false;
      if(activeCluster !== '전체' && !d.cluster.includes(activeCluster)) return false;
      if(q && !(d.gu.toLowerCase().includes(q) || d.dong.toLowerCase().includes(q))) return false;
      return true;
    }});

    rows.sort((a,b) => {{
      let valA = a[sortKey];
      let valB = b[sortKey];
      if(typeof valA === 'string') {{
        return valA.localeCompare(valB, 'ko') * sortDir;
      }}
      return (valA > valB ? 1 : valA < valB ? -1 : 0) * sortDir;
    }});

    countEl.textContent = rows.length;

    if(rows.length === 0){{
      tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding:30px; color:var(--ink-soft);">조건에 부합하는 동네가 없습니다. 예산이나 검색 조건을 조정해 보세요.</td></tr>`;
      return;
    }}

    tbody.innerHTML = rows.map(d => `
      <tr>
        <td>${{d.gu}}</td>
        <td><strong>${{d.dong}}</strong></td>
        <td class="num mono">${{d.price.toFixed(2)}}억</td>
        <td class="num mono">${{d.unit_price.toLocaleString()}}만</td>
        <td class="num mono">${{d.commute.toFixed(1)}}분</td>
        <td class="num mono" style="color:${{d.drop > -10 ? 'var(--teal)' : 'var(--terracotta)'}}">${{d.drop.toFixed(1)}}%</td>
        <td class="num mono">${{d.p3040.toFixed(1)}}%</td>
        <td><span class="badge ${{getBadgeClass(d.cluster)}}">${{d.cluster.split(':')[0]}}</span></td>
        <td class="num mono" style="font-weight:bold; color:var(--teal);">${{d.top_defense.toFixed(4)}}</td>
      </tr>
    `).join('');
  }}

  budgetEl.addEventListener('input', render);
  searchEl.addEventListener('input', render);

  chips.forEach(chip => {{
    chip.addEventListener('click', () => {{
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCluster = chip.dataset.cls;
      render();
    }});
  }});

  ths.forEach(th => {{
    th.addEventListener('click', () => {{
      const key = th.dataset.key;
      if(sortKey === key){{
        sortDir *= -1;
      }} else {{
        sortKey = key;
        sortDir = -1;
      }}
      ths.forEach(t => t.style.fontWeight = 'normal');
      th.style.fontWeight = 'bold';
      render();
    }});
  }});

  render();
}})();
</script>

</body>
</html>
"""

output_path = r'd:\26_강의자료\프로젝트\3040_맞벌이_주거지_분석_및_모델링_팀공유리포트.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML report successfully generated at:", output_path)
