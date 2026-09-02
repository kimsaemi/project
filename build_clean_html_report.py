import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

html_content = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="color-scheme" content="light dark" />
  <title>3040 맞벌이를 위한 서울 최적 아파트 주거지 분석 및 모델링 리포트</title>
  <style>
    :root {
      color-scheme: light dark;
      --bg: #f4f7fb;
      --paper: #ffffff;
      --ink: #172033;
      --muted: #5f6b7a;
      --line: #dce4ef;
      --blue: #2855d9;
      --blue-soft: #eaf0ff;
      --gold: #a86f00;
      --gold-soft: #fff4d6;
      --red: #a83838;
      --red-soft: #fff0f0;
      --green: #1d7950;
      --green-soft: #e9f8f0;
      --purple: #6b21a8;
      --purple-soft: #f3e8ff;
      --shadow: 0 14px 36px rgba(32, 49, 82, .10);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: "Pretendard", "Noto Sans KR", "Malgun Gothic", system-ui, sans-serif;
      line-height: 1.65;
    }
    a { color: var(--blue); }
    .wrap { width: min(1080px, calc(100% - 32px)); margin: 0 auto; }
    header {
      padding: 56px 0 38px;
      background: linear-gradient(135deg, #18356f 0%, #2855d9 66%, #3f76ee 100%);
      color: white;
    }
    .eyebrow { margin: 0 0 10px; font-weight: 800; letter-spacing: .08em; opacity: .88; font-size: 14px; text-transform: uppercase; }
    h1 { margin: 0; font-size: clamp(30px, 5.5vw, 54px); line-height: 1.15; letter-spacing: -.03em; font-weight: 800; }
    .lead { max-width: 780px; margin: 16px 0 0; font-size: 18px; opacity: .92; line-height: 1.6; }
    .meta { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 24px; }
    .meta span { padding: 6px 14px; border: 1px solid rgba(255,255,255,.35); border-radius: 999px; font-size: 13.5px; font-weight: 600; }
    
    nav { position: sticky; top: 0; z-index: 50; background: color-mix(in srgb, var(--paper) 92%, transparent); border-bottom: 1px solid var(--line); backdrop-filter: blur(10px); }
    nav .wrap { display: flex; gap: 18px; overflow-x: auto; padding-block: 12px; }
    nav a { color: var(--ink); text-decoration: none; white-space: nowrap; font-weight: 750; font-size: 14px; }
    nav a:hover { color: var(--blue); }
    
    main { padding: 30px 0 64px; }
    section { margin: 20px 0; padding: 30px; background: var(--paper); border: 1px solid var(--line); border-radius: 20px; box-shadow: var(--shadow); }
    h2 { margin: 0 0 16px; font-size: clamp(22px, 3vw, 32px); line-height: 1.25; letter-spacing: -.025em; font-weight: 800; }
    h3 { margin: 22px 0 10px; font-size: 18px; font-weight: 750; }
    p { margin: 8px 0; font-size: 15px; color: var(--ink); }
    
    .summary { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
    .card { padding: 18px; border: 1px solid var(--line); border-radius: 16px; background: linear-gradient(180deg, var(--paper), color-mix(in srgb, var(--paper) 85%, var(--blue-soft))); }
    .card strong { display: block; margin-bottom: 6px; font-size: 17px; color: var(--blue); }
    .card p { font-size: 14px; color: var(--muted); margin: 0; }
    
    .statement { padding: 22px 24px; border-left: 6px solid var(--blue); border-radius: 14px; background: var(--blue-soft); font-size: clamp(17px, 2.2vw, 22px); font-weight: 800; line-height: 1.55; color: #17316f; }
    
    .pea { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 18px; }
    .pea article { padding: 18px; border: 1px solid var(--line); border-radius: 14px; background: var(--paper); }
    .pea b { display: block; color: var(--blue); margin-bottom: 6px; font-size: 15px; }
    .pea p { font-size: 13.5px; color: var(--muted); margin: 0; }
    
    .flow { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; align-items: stretch; margin-top: 14px; }
    .flow div { position: relative; padding: 16px 10px; border: 1px solid var(--line); border-radius: 14px; text-align: center; font-weight: 800; background: var(--paper); font-size: 14.5px; }
    .flow div:not(:last-child)::after { content: "→"; position: absolute; right: -14px; top: 50%; transform: translateY(-50%); color: var(--blue); font-weight: 900; z-index: 2; }
    .flow small { display: block; color: var(--muted); margin-top: 4px; font-weight: 600; font-size: 12px; }
    
    .table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 14px; margin-top: 14px; }
    table { width: 100%; border-collapse: collapse; min-width: 760px; font-size: 14px; }
    th, td { padding: 12px 14px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: middle; }
    th { background: var(--blue-soft); color: #17316f; font-size: 13.5px; font-weight: 800; }
    tr:last-child td { border-bottom: 0; }
    
    .tag { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 800; white-space: nowrap; }
    .main { background: var(--blue-soft); color: var(--blue); }
    .support { background: var(--green-soft); color: var(--green); }
    .later { background: var(--gold-soft); color: var(--gold); }
    .stop { background: var(--red-soft); color: var(--red); }
    .purple { background: var(--purple-soft); color: var(--purple); }
    
    .persona-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 14px; }
    .persona-card { padding: 18px; border: 1px solid var(--line); border-radius: 16px; background: var(--paper); }
    .persona-card.p1 { border-top: 4px solid var(--blue); }
    .persona-card.p2 { border-top: 4px solid var(--green); }
    .persona-card.p3 { border-top: 4px solid var(--gold); }
    .persona-card h4 { margin: 0 0 6px; font-size: 16px; font-weight: 800; }
    .persona-card .w { font-size: 12px; font-family: ui-monospace, monospace; color: var(--muted); background: var(--bg); padding: 3px 8px; border-radius: 6px; display: inline-block; margin-bottom: 10px; }
    .persona-card ul { margin: 0; padding-left: 18px; font-size: 13.5px; color: var(--muted); }
    .persona-card li { margin-bottom: 4px; }
    
    .checklist { display: grid; gap: 10px; padding: 0; list-style: none; margin-top: 14px; }
    .checklist li { padding: 14px 16px 14px 46px; border: 1px solid var(--line); border-radius: 13px; position: relative; font-size: 14px; background: var(--paper); }
    .checklist li::before { content: "✓"; position: absolute; left: 16px; top: 12px; color: var(--blue); font-size: 18px; font-weight: 900; }
    
    .timeline { display: grid; gap: 10px; counter-reset: step; margin-top: 14px; }
    .timeline article { position: relative; padding: 16px 16px 16px 58px; border-left: 4px solid var(--blue); background: var(--blue-soft); border-radius: 10px; font-size: 14px; }
    .timeline article::before { counter-increment: step; content: counter(step); position: absolute; left: 16px; top: 14px; width: 26px; height: 26px; display: grid; place-items: center; border-radius: 50%; background: var(--blue); color: white; font-weight: 900; font-size: 13px; }
    
    .warning { padding: 18px; border: 1px solid #f1cf80; border-radius: 14px; background: var(--gold-soft); font-size: 14px; margin-top: 16px; }
    
    footer { padding: 30px 0 50px; color: var(--muted); text-align: center; font-size: 13px; }
    code { padding: 2px 6px; border-radius: 6px; background: color-mix(in srgb, var(--blue-soft) 78%, var(--paper)); color: var(--blue); font-family: ui-monospace, monospace; font-size: 13px; }
    
    @media (max-width: 780px) {
      .summary, .pea, .persona-grid { grid-template-columns: 1fr; }
      .flow { grid-template-columns: 1fr; }
      .flow div:not(:last-child)::after { content: "↓"; right: auto; left: 50%; top: auto; bottom: -18px; transform: translateX(-50%); }
      section { padding: 22px 18px; border-radius: 16px; }
    }
  </style>
</head>
<body>

  <header>
    <div class="wrap">
      <p class="eyebrow">3040 실수요 주거지 최적화 프로젝트 · 팀 공유용 통합 진행안</p>
      <h1>내 예산으로,<br />출퇴근도 편하고 집값도 덜 떨어지는 서울 동네 찾기</h1>
      <p class="lead">부동산 실거래가, 3040 실측 통근 이동량, 금리사이클 변동성 데이터를 합쳐 30~40대 맞벌이 부부를 위한 최적 주거지 알고리즘 및 4대 군집 세그먼트를 정리한 최종 리포트입니다.</p>
      <div class="meta">
        <span>137개 분석 법정동</span>
        <span>회귀 설명력 R² 83.8%</span>
        <span>MCDM TOPSIS 맞춤 모델</span>
        <span>K-Means 4대 군집 분석</span>
      </div>
    </div>
  </header>

  <nav aria-label="문서 목차">
    <div class="wrap">
      <a href="#summary">한눈에 보는 결론</a>
      <a href="#problem">문제 정의</a>
      <a href="#data">데이터 결합 & 노이즈 정리</a>
      <a href="#topsis">TOPSIS 맞춤 모델</a>
      <a href="#cluster">4대 주거지 세그먼트</a>
      <a href="#check">검증 체크리스트</a>
      <a href="#plan">진행 순서</a>
    </div>
  </nav>

  <main class="wrap">

    <!-- 1. 한눈에 보는 결론 -->
    <section id="summary">
      <h2>1. 한눈에 보는 결론</h2>
      <div class="summary">
        <div class="card">
          <strong>🎯 타깃 사용자</strong>
          <p>서울 아파트 내 집 마련을 준비하는 30~40대. 대표 사용 시나리오는 서로 다른 직장으로 출퇴근하는 맞벌이 부부입니다.</p>
        </div>
        <div class="card">
          <strong>❓ 핵심 질문</strong>
          <p>“내 가용 예산(6~8억/9~11억/12~15억) 안에서 두 사람 출퇴근 부담과 가격 하락 위험이 가장 적은 서울 동네는 어디일까?”</p>
        </div>
        <div class="card">
          <strong>🔗 융합 데이터</strong>
          <p>국토부 아파트 실거래가(예산/단가) + 3040 실측 통근 이동량(직주근접) + 가격 흔들림 순위표(하락장 방어력) 결합.</p>
        </div>
        <div class="card">
          <strong>💡 최종 결과물</strong>
          <p>획일적인 서울 1위가 아닌, 사용자의 예산과 개인 우선순위(가중치)에 맞춘 ‘최적 동네 5~10곳’ 및 4대 세그먼트 제시.</p>
        </div>
      </div>
    </section>

    <!-- 2. 문제 정의 -->
    <section id="problem">
      <h2>2. 우리 팀의 문제 정의 한 문장</h2>
      <div class="statement">
        서울 아파트 구매를 고민하는 30·40대 맞벌이 부부가 가용 예산 안에서 두 사람의 출퇴근 시간과 하락장 집값 방어율을 한 번에 비교하여, 자산 손실 위험이 적은 최적 동네 5~10곳을 빠르게 선별하도록 돕는다.
      </div>
      <div class="pea">
        <article>
          <b>📌 원인</b>
          <p>기존 부동산 정보는 집값 시세나 단순 교통 호재에만 쏠려 있어 "내 예산으로 출퇴근도 편하고 안전한 동네"가 어디인지 알기 어렵습니다.</p>
        </article>
        <article>
          <b>🎯 대상</b>
          <p>6억~15억 원대 예산을 가진 3040 실수요자 및 신혼부부/학부모 가정을 핵심 분석 대상으로 정의합니다.</p>
        </article>
        <article>
          <b>🚀 기대효과</b>
          <p>예산, 직무지구 통근 소요시간, 하락기 가격 방어율을 통합 지표로 제공하여 최적 입지 결정 시간을 대폭 단축시킵니다.</p>
        </article>
      </div>
    </section>

    <!-- 3. 데이터 결합 및 노이즈 정리 -->
    <section id="data">
      <h2>3. 어떤 데이터를 합치고, 필요없는 데이터는 삭제했는가?</h2>
      <p>부동산 가격만으로는 알 수 없는 "출퇴근 편의성"과 "하락장 자산 방어력"을 5개 핵심 데이터셋 융합을 통해 완성했습니다.</p>
      
      <div class="flow" aria-label="데이터 결합 흐름">
        <div>예산 필터<small>매매가 중앙값</small></div>
        <div>직주근접<small>07~09시 통근량</small></div>
        <div>가격 방어력<small>하락장 낙폭율</small></div>
        <div>3040 밀집도<small>상주/주간 인구</small></div>
        <div>최적 후보<small>개인 맞춤 랭킹</small></div>
      </div>

      <h3>데이터셋별 역할 및 정제 기준</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>데이터 구분의 축</th>
              <th>핵심 변수 (Features)</th>
              <th>프로젝트 내 역할 및 삭제/정제 기준</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>1. 부동산 실거래가</strong></td>
              <td><code>가격_중앙값_만원</code>, <code>평당단가_만원</code></td>
              <td><span class="tag main">필수 결합</span> 6~8억/9~11억/12~15억 예산 필터링. 30억 초과 초고가 및 100세대 미만 나홀로 단지 <strong>삭제</strong>.</td>
            </tr>
            <tr>
              <td><strong>2. 실측 통근 이동량</strong></td>
              <td><code>d_admdong_cd</code>, 07~09시 3040 이동량</td>
              <td><span class="tag main">필수 결합</span> GBD/YBD/CBD 3대 업무지구 20분대 도달 측정. 주말/심야 비통근 이동 데이터 <strong>삭제</strong>.</td>
            </tr>
            <tr>
              <td><strong>3. 가격 흔들림 순위표</strong></td>
              <td><code>하락기_낙폭_%</code>, <code>가격안정점수</code></td>
              <td><span class="tag main">필수 결합</span> 금리 인상기 하락장 가격 방어력 측정. 단순 반등률과 하락 방어율을 분리 평가.</td>
            </tr>
            <tr>
              <td><strong>4. 인구 및 주간인구</strong></td>
              <td><code>3040 상주비중_%</code>, <code>주간인구지수</code></td>
              <td><span class="tag support">보조 지표</span> pure 베드타운 vs 직주복합지 판별. 60대 이상 특화 데이터 <strong>삭제</strong>.</td>
            </tr>
            <tr>
              <td><strong>5. 상권 분석 서비스</strong></td>
              <td><code>길단위인구</code>, <code>점포수</code></td>
              <td><span class="tag stop">전량 삭제</span> 아파트 주거지 평가 시 상권 점포수 데이터는 큰 노이즈를 유발하므로 <strong>삭제</strong>.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 4. TOPSIS 맞춤 모델 -->
    <section id="topsis">
      <h2>4. [추천 1] 개인 맞춤형 TOPSIS 의사결정 모델</h2>
      <p>사용자(맞벌이 부부)마다 우선시하는 조건(출퇴근 vs 집값방어 vs 예산)이 다를 때, 가중치(Weights)를 입력받아 실시간 최적 동네 순위를 산출하는 알고리즘입니다.</p>

      <div class="persona-grid">
        <div class="persona-card p1">
          <h4>A. 신혼 & 첫 집 (가성비형)</h4>
          <div class="w">통근 50% | 예산 30% | 방어 10% | 3040 10%</div>
          <ul>
            <li><strong>1위: 영등포구 영등포동2가</strong> (7.35억 / 통근 41분)</li>
            <li><strong>2위: 종로구 숭인동</strong> (5.20억 / 통근 46분)</li>
            <li><strong>3위: 관악구 남현동</strong> (7.22억 / 통근 45분)</li>
          </ul>
        </div>

        <div class="persona-card p2">
          <h4>B. 자산방어형 (하락장 안정성)</h4>
          <div class="w">방어 50% | 통근 30% | 3040 10% | 예산 10%</div>
          <ul>
            <li><strong>1위: 영등포구 영등포동2가</strong> (하락낙폭 +1.5%)</li>
            <li><strong>2위: 종로구 숭인동</strong> (하락낙폭 +1.3%)</li>
            <li><strong>3위: 구로구 구로동</strong> (하락낙폭 -2.4%)</li>
          </ul>
        </div>

        <div class="persona-card p3">
          <h4>C. 직주근접 & 도심성장형</h4>
          <div class="w">통근 40% | 3040 30% | 방어 20% | 예산 10%</div>
          <ul>
            <li><strong>1위: 강서구 염창동</strong> (3040비중 43.3%)</li>
            <li><strong>2위: 강서구 가양동</strong> (3040비중 43.3%)</li>
            <li><strong>3위: 영등포구 당산동</strong> (3040비중 38.5%)</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 5. K-Means 4대 주거지 세그먼트 -->
    <section id="cluster">
      <h2>5. [추천 2] K-Means 4대 주거지 세그먼트 (군집 분석)</h2>
      <p>서울 주요 137개 법정동을 5차원 특성(시세, 통근시간, 낙폭율, 3040비중)으로 군집화한 결과입니다.</p>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>군집 세그먼트</th>
              <th>평균 매매시세</th>
              <th>평균 통근시간</th>
              <th>하락장 방어력</th>
              <th>대표 동네</th>
              <th>핵심 추천 가치 및 자산 전략</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>그룹 1: 가성비 실속 & 실수요 밀집</strong></td>
              <td>6.0억 ~ 8.3억</td>
              <td>20~25분</td>
              <td>-21.7% ~ -29.1%</td>
              <td>강서 염창·등촌<br>관악 봉천</td>
              <td><span class="tag main">30대 신혼부부 1순위</span> 9호선 급행/신림선으로 여의도·강남 15~25분 진입. 3040 거주비중 서울 1위(43.3%).</td>
            </tr>
            <tr>
              <td><strong>그룹 2: 광역 허브 & 철통 방어선 ★</strong></td>
              <td>9.6억 ~ 11.5억</td>
              <td>15~20분</td>
              <td><span class="tag support">-7.1% ~ -12.0%</span></td>
              <td>영등포 당산<br>동작 사당·신도림</td>
              <td><span class="tag support">실수요 추천 1위 🏆</span> 2·9호선/2·4·7호선 요충지. 금리 인상기 하락장 낙폭이 서울 최저 수준으로 자산 방어력 최강.</td>
            </tr>
            <tr>
              <td><strong>그룹 3: 쿼드러플 & 도심 거점</strong></td>
              <td>12.1억 ~ 15.4억</td>
              <td>5~10분</td>
              <td>상승기 +40.9%</td>
              <td>마포 공덕·도화<br>송파 문정·가락</td>
              <td><span class="tag later">고탄력 성장형 🚀</span> 4개 노선 환승 직주근접 종결지. 금리 인하기에 가장 폭발적인 시세 반등 탄력 보유.</td>
            </tr>
            <tr>
              <td><strong>그룹 4: 자녀 보육 & 학군 배후</strong></td>
              <td>7.5억 ~ 10.5억</td>
              <td>30~40분</td>
              <td>-22.8% ~ -29.5%</td>
              <td>노원 중계<br>강동 고덕·명일</td>
              <td><span class="tag purple">학군 정주형 🎓</span> 서울 3대 명문 학원가 인근. 출퇴근 30분 감수 대신 쾌적한 숲세권 및 넓은 평형 확보.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 6. 데이터 검증 체크리스트 -->
    <section id="check">
      <h2>6. 분석 전 반드시 검증한 10가지 데이터 체크리스트</h2>
      <ul class="checklist">
        <li><strong>매매가 지표:</strong> <code>단가 × 면적</code>의 계산값 대신 국토부 실거래가 <code>가격_중앙값_만원</code>을 직접 사용하여 착시 제거.</li>
        <li><strong>통근 시간대:</strong> 07:00~09:59 아침 피크 타임 통근 데이터를 필터링하여 실제 출퇴근 부담 반영.</li>
        <li><strong>다공선성 검정:</strong> GBD, YBD, CBD 통근시간 간 공선성 해결을 위해 <code>Ridge Regression</code> 정규화 모델 적용.</li>
        <li><strong>인코딩 예외 처리:</strong> Windows 콘솔 CP949 인코딩 오류 방지를 위해 `sys.stdout.reconfigure(encoding='utf-8')` 적용.</li>
        <li><strong>이상치 필터링:</strong> 30억 초과 초고가 단지 및 100세대 미만 나홀로 아파트를 전처리 단계에서 제거.</li>
        <li><strong>공간 매핑:</strong> 법정동 실거래가와 행정동 이동 데이터를 1:1 매핑 테이블로 정상 결합.</li>
        <li><strong>하락 방어 지표:</strong> 단순 변동성이 아닌 하락기 낙폭율(2021~2022)을 별도 지표로 분리 정의.</li>
        <li><strong>상권 데이터 분리:</strong> 주거지 분석 시 상권 점포수 및 길단위 인구 데이터를 노이즈로 분류하여 삭제.</li>
        <li><strong>재현성 고정:</strong> K-Means 군집화 시 <code>random_state=42</code>로 고정하여 결과 재현성 확보.</li>
        <li><strong>회귀 모델 평가:</strong> Random Forest 회귀 모델 설명력 $R^2 = 0.8382$ (83.8%) 달성 검증 완료.</li>
      </ul>
    </section>

    <!-- 7. 진행 순서 -->
    <section id="plan">
      <h2>7. 팀원 협업 진행 순서 (5단계)</h2>
      <div class="timeline">
        <article>
          <strong>1단계 — 문제 정의 확정</strong><br />
          3040 맞벌이 부부를 핵심 타깃으로 지정하고 가용 예산대(6~15억)와 하락장 방어의 의미를 최종 명확화합니다.
        </article>
        <article>
          <strong>2단계 — 데이터 결합 및 노이즈 제거</strong><br />
          국토부 실거래가 + 3040 통근 O-D + 가격 흔들림 순위표를 법정동 코드 기준으로 통합하고 상권 노이즈 데이터를 제거합니다.
        </article>
        <article>
          <strong>3단계 — 회귀 및 TOPSIS 모델링 구현</strong><br />
          파이썬(`run_housing_models.py`, `run_clustering_topsis.py`) 스크립트로 회귀 예측 및 TOPSIS 맞춤형 알고리즘을 구축합니다.
        </article>
        <article>
          <strong>4단계 — 인터랙티브 HTML 웹 리포트 제작</strong><br />
          137개 법정동 데이터를 사용자가 직접 예산과 키워드로 실시간 검색하고 정렬할 수 있는 단일 HTML 페이지를 만듭니다.
        </article>
        <article>
          <strong>5단계 — 팀원 공유 및 서비스 탑재</strong><br />
          단일 HTML 파일(`3040_맞벌이_주거지_분석_및_모델링_팀공유리포트.html`)을 팀 내 공유하여 의사결정을 완료합니다.
        </article>
      </div>

      <div class="warning">
        <strong>💡 핵심 공유 팁:</strong> 생성된 <code>3040_맞벌이_주거지_분석_및_모델링_팀공유리포트.html</code> 파일 하나만 팀원들에게 공유하면, 별도 프로그램 설치 없이 브라우저에서 즉시 열어 대시보드와 보고서를 확인하실 수 있습니다.
      </div>
    </section>

  </main>

  <footer class="wrap">
    3040 맞벌이 주거지 최적화 프로젝트 · 팀 공유용 통합 리포트 · 2026
  </footer>

</body>
</html>
"""

output_path = r'd:\26_강의자료\프로젝트\3040_맞벌이_주거지_분석_및_모델링_팀공유리포트.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated HTML report successfully generated at:", output_path)
