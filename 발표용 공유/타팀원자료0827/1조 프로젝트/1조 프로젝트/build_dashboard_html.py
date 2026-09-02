import json

def build_html():
    with open('recommendation_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    json_str = json.dumps(data, ensure_ascii=False)
    
    html_template = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3040 맞벌이 주거지 AI 추천 & 머신러닝 종합 대시보드</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-base: #0b0f19;
            --bg-card: rgba(18, 24, 38, 0.85);
            --bg-card-hover: rgba(28, 38, 58, 0.95);
            --border-color: rgba(255, 255, 255, 0.08);
            --border-accent: rgba(59, 130, 246, 0.4);
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --text-dim: #64748b;
            --primary: #3b82f6;
            --primary-glow: rgba(59, 130, 246, 0.25);
            --success: #10b981;
            --warning: #f59e0b;
            --purple: #8b5cf6;
            --rose: #f43f5e;
            --cyan: #06b6d4;
            --radius-lg: 16px;
            --radius-md: 12px;
            --radius-sm: 8px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
        }}

        body {{
            background-color: var(--bg-base);
            color: var(--text-main);
            min-height: 100vh;
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            overflow-x: hidden;
            padding-bottom: 60px;
        }}

        /* Header */
        header {{
            border-bottom: 1px solid var(--border-color);
            backdrop-filter: blur(20px);
            background: rgba(11, 15, 25, 0.75);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 16px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo-area {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .badge-1team {{
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            font-weight: 800;
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 20px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}

        .header-title {{
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.5px;
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .header-meta {{
            font-size: 13px;
            color: var(--text-sub);
        }}

        /* Container */
        .container {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 24px 32px;
        }}

        /* KPI Row */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: var(--border-accent);
            box-shadow: 0 12px 24px -10px var(--primary-glow);
        }}

        .kpi-title {{
            font-size: 13px;
            color: var(--text-sub);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .kpi-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 4px;
        }}

        .kpi-sub {{
            font-size: 12px;
            color: var(--text-dim);
        }}

        /* Main Grid */
        .main-layout {{
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 24px;
            align-items: start;
        }}

        /* Simulator Sidebar */
        .simulator-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px;
            position: sticky;
            top: 88px;
        }}

        .panel-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .form-group {{
            margin-bottom: 20px;
        }}

        .form-label {{
            font-size: 13px;
            font-weight: 600;
            color: var(--text-sub);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }}

        .form-select, .form-range {{
            width: 100%;
        }}

        .form-select {{
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: var(--text-main);
            padding: 10px 14px;
            border-radius: var(--radius-sm);
            font-size: 14px;
            outline: none;
            cursor: pointer;
            transition: border-color 0.2s;
        }}

        .form-select:focus {{
            border-color: var(--primary);
        }}

        .range-slider-wrap {{
            padding: 4px 0;
        }}

        .slider-val-badge {{
            color: var(--primary);
            font-weight: 700;
            font-size: 14px;
        }}

        .preset-buttons {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-top: 8px;
        }}

        .btn-preset {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-sub);
            padding: 8px 4px;
            border-radius: var(--radius-sm);
            font-size: 12px;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s;
        }}

        .btn-preset.active, .btn-preset:hover {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}

        /* Content Area */
        .content-area {{
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}

        .section-box {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px;
        }}

        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}

        .section-title {{
            font-size: 18px;
            font-weight: 700;
        }}

        /* Ranking Cards */
        .ranking-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .rank-card {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 16px 20px;
            display: grid;
            grid-template-columns: 48px 1.4fr 1fr 1fr 1fr 100px;
            align-items: center;
            gap: 16px;
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .rank-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border-accent);
            transform: translateX(4px);
        }}

        .rank-num {{
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: var(--text-dim);
            text-align: center;
        }}

        .rank-card:nth-child(1) .rank-num {{ color: #fbbf24; }}
        .rank-card:nth-child(2) .rank-num {{ color: #94a3b8; }}
        .rank-card:nth-child(3) .rank-num {{ color: #d97706; }}

        .dong-info-name {{
            font-size: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .dong-info-gu {{
            font-size: 12px;
            color: var(--text-sub);
            font-weight: 400;
        }}

        .cluster-tag {{
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 600;
        }}

        .tag-cluster-0 {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
        .tag-cluster-1 {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
        .tag-cluster-2 {{ background: rgba(139, 92, 246, 0.15); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.3); }}
        .tag-cluster-3 {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }}

        .metric-cell {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .metric-cell .label {{
            font-size: 11px;
            color: var(--text-dim);
        }}

        .metric-cell .val {{
            font-size: 14px;
            font-weight: 600;
        }}

        .score-badge {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
            border: 1px solid var(--border-accent);
            border-radius: var(--radius-sm);
            padding: 6px 10px;
            text-align: center;
        }}

        .score-badge .score-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 800;
            color: #60a5fa;
        }}

        .score-badge .score-lbl {{
            font-size: 10px;
            color: var(--text-sub);
        }}

        /* Chart Area */
        .chart-grid {{
            display: grid;
            grid-template-columns: 1.3fr 1fr;
            gap: 20px;
        }}

        .chart-box {{
            height: 380px;
            position: relative;
        }}

        /* Modal */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(8px);
            z-index: 1000;
            display: none;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .modal-content {{
            background: #131b2e;
            border: 1px solid var(--border-accent);
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 680px;
            padding: 28px;
            position: relative;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: modalFade 0.2s ease-out;
        }}

        @keyframes modalFade {{
            from {{ opacity: 0; transform: scale(0.96); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}

        .modal-close {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: transparent;
            border: none;
            color: var(--text-sub);
            font-size: 24px;
            cursor: pointer;
        }}

        .modal-header {{
            margin-bottom: 20px;
        }}

        .modal-title {{
            font-size: 22px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .modal-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 20px;
        }}

        .modal-stat-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 14px;
        }}

        .modal-stat-title {{
            font-size: 12px;
            color: var(--text-sub);
            margin-bottom: 4px;
        }}

        .modal-stat-value {{
            font-size: 18px;
            font-weight: 700;
            color: var(--text-main);
        }}

        @media (max-width: 1024px) {{
            .main-layout {{
                grid-template-columns: 1fr;
            }}
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>

    <header>
        <div class="logo-area">
            <span class="badge-1team">1조 BigData Lab</span>
            <h1 class="header-title">3040 맞벌이 주거지 AI 추천 & 머신러닝 대시보드</h1>
        </div>
        <div class="header-meta">
            서울시 418개 행정동 × 23.5만 건 실거래가 × 수도권 출퇴근 생활이동 결합
        </div>
    </header>

    <div class="container">
        <!-- KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">분석 대상 행정동 <span>📍</span></div>
                <div class="kpi-val">418<span style="font-size:16px;font-weight:400;color:var(--text-sub);">개 동</span></div>
                <div class="kpi-sub">서울 25개 자치구 전수 분석</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">머신러닝 단가 설명력 (R²) <span>🤖</span></div>
                <div class="kpi-val" style="color:var(--success);">95.4%</div>
                <div class="kpi-sub">Random Forest Regressor 검증</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">강남(GBD) 통근시간 가격 기여도 <span>⚡</span></div>
                <div class="kpi-val" style="color:var(--primary);">50.6%</div>
                <div class="kpi-sub">서울 아파트 가격 지배 요인 1위</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">3040 가성비 1위 추천지 <span>🏆</span></div>
                <div class="kpi-val" style="color:var(--warning);">강서 염창동</div>
                <div class="kpi-sub">9호선 급행 / 전용59 7.7억대</div>
            </div>
        </div>

        <!-- Main Workspace -->
        <div class="main-layout">
            <!-- Left: Simulator Controls -->
            <div class="simulator-panel">
                <h2 class="panel-title">🎯 맞벌이 조건 시뮬레이터</h2>
                
                <div class="form-group">
                    <label class="form-label">남편 직장 권역</label>
                    <select id="hub-husband" class="form-select" onchange="runSimulation()">
                        <option value="gbd" selected>강남 / 서초 (GBD)</option>
                        <option value="cbd">광화문 / 종로 (CBD)</option>
                        <option value="ybd">여의도 / 마포 (YBD)</option>
                        <option value="pangyo">판교 / 분당</option>
                        <option value="overall">3대 도심 통합</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">아내 직장 권역</label>
                    <select id="hub-wife" class="form-select" onchange="runSimulation()">
                        <option value="cbd" selected>광화문 / 종로 (CBD)</option>
                        <option value="gbd">강남 / 서초 (GBD)</option>
                        <option value="ybd">여의도 / 마포 (YBD)</option>
                        <option value="pangyo">판교 / 분당</option>
                        <option value="overall">3대 도심 통합</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">희망 평형대</label>
                    <select id="flat-type" class="form-select" onchange="runSimulation()">
                        <option value="59" selected>전용 59㎡ (약 24~25평형)</option>
                        <option value="84">전용 84㎡ (약 32~34평형)</option>
                    </select>
                </div>

                <div class="form-group">
                    <div class="form-label">
                        <span>최대 가용 예산</span>
                        <span id="budget-val" class="slider-val-badge">12.0억원</span>
                    </div>
                    <div class="range-slider-wrap">
                        <input type="range" id="budget-slider" class="form-range" min="4" max="25" step="0.5" value="12" oninput="updateBudgetVal(this.value)">
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">가중치 성향 선택</label>
                    <div class="preset-buttons">
                        <button class="btn-preset" onclick="setPreset('commute', this)">통근우선</button>
                        <button class="btn-preset active" onclick="setPreset('balanced', this)">균형형</button>
                        <button class="btn-preset" onclick="setPreset('price', this)">가성비우선</button>
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">자치구 필터</label>
                    <select id="gu-filter" class="form-select" onchange="runSimulation()">
                        <option value="all">서울시 전체 (25개구)</option>
                    </select>
                </div>
            </div>

            <!-- Right: Results & Visualizations -->
            <div class="content-area">
                <!-- Recommendations Section -->
                <div class="section-box">
                    <div class="section-header">
                        <div>
                            <h2 class="section-title">✨ 맞춤 추천 주거지 Top 10</h2>
                            <p style="font-size: 13px; color: var(--text-sub); margin-top: 4px;">선택하신 맞벌이 직장 및 예산 조건에 최적화된 동네 랭킹입니다. (카드를 클릭하면 상세 프로파일을 확인하실 수 있습니다.)</p>
                        </div>
                        <span id="match-count-badge" style="font-size: 12px; background: rgba(59, 130, 246, 0.1); color: #60a5fa; padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(59, 130, 246, 0.2);">418개 중 10개 표시</span>
                    </div>

                    <div id="ranking-container" class="ranking-list">
                        <!-- Dynamic items -->
                    </div>
                </div>

                <!-- Charts Section -->
                <div class="section-box">
                    <div class="section-header">
                        <h2 class="section-title">📊 서울시 418개 행정동 가격 vs 통근시간 상관 분석</h2>
                    </div>
                    <div class="chart-grid">
                        <div class="chart-box">
                            <canvas id="scatterChart"></canvas>
                        </div>
                        <div class="chart-box">
                            <canvas id="clusterPieChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Detail Modal -->
    <div id="detail-modal" class="modal-overlay" onclick="closeModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <div class="modal-header">
                <div id="modal-dong-name" class="modal-title">동네명</div>
                <div id="modal-cluster-tag" style="margin-top: 6px;"></div>
            </div>
            <div class="modal-grid">
                <div class="modal-stat-card">
                    <div class="modal-stat-title">평당 단가 / 추정 전용 59㎡</div>
                    <div id="modal-price" class="modal-stat-value">-</div>
                </div>
                <div class="modal-stat-card">
                    <div class="modal-stat-title">남편 통근 소요시간</div>
                    <div id="modal-husband-time" class="modal-stat-value">-</div>
                </div>
                <div class="modal-stat-card">
                    <div class="modal-stat-title">아내 통근 소요시간</div>
                    <div id="modal-wife-time" class="modal-stat-value">-</div>
                </div>
                <div class="modal-stat-card">
                    <div class="modal-stat-title">최근 1년 거래건수 / 유동성</div>
                    <div id="modal-tx-count" class="modal-stat-value">-</div>
                </div>
            </div>
            <div style="height: 240px; margin-top: 12px;">
                <canvas id="radarChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        const rawData = {json_str};

        let currentPreset = 'balanced';
        let scatterChartInstance = null;
        let clusterPieInstance = null;
        let radarChartInstance = null;

        // Init
        document.addEventListener('DOMContentLoaded', () => {{
            populateGuFilter();
            initCharts();
            runSimulation();
        }});

        function populateGuFilter() {{
            const guSet = new Set(rawData.map(d => d.자치구명));
            const select = document.getElementById('gu-filter');
            Array.from(guSet).sort().forEach(gu => {{
                const opt = document.createElement('option');
                opt.value = gu;
                opt.textContent = gu;
                select.appendChild(opt);
            }});
        }}

        function updateBudgetVal(val) {{
            document.getElementById('budget-val').textContent = parseFloat(val).toFixed(1) + '억원';
            runSimulation();
        }}

        function setPreset(preset, btn) {{
            currentPreset = preset;
            document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            runSimulation();
        }}

        function getTimeField(hub) {{
            if (hub === 'gbd') return 'time_to_gbd';
            if (hub === 'cbd') return 'time_to_cbd';
            if (hub === 'ybd') return 'time_to_ybd';
            if (hub === 'pangyo') return 'time_to_pangyo';
            return '3대도심_평균통근시간';
        }}

        function runSimulation() {{
            const hubH = document.getElementById('hub-husband').value;
            const hubW = document.getElementById('hub-wife').value;
            const flatType = document.getElementById('flat-type').value;
            const maxBudget = parseFloat(document.getElementById('budget-slider').value);
            const guFilter = document.getElementById('gu-filter').value;

            const timeColH = getTimeField(hubH);
            const timeColW = getTimeField(hubW);
            const priceCol = flatType === '59' ? '추정_전용59_가격_억' : '추정_전용84_가격_억';

            // Filter by budget & gu
            let filtered = rawData.filter(d => {{
                const price = d[priceCol];
                if (price > maxBudget) return false;
                if (guFilter !== 'all' && d.자치구명 !== guFilter) return false;
                return true;
            }});

            // Weights
            let w_commute = 0.5, w_price = 0.3, w_env = 0.2;
            if (currentPreset === 'commute') {{
                w_commute = 0.7; w_price = 0.15; w_env = 0.15;
            }} else if (currentPreset === 'price') {{
                w_commute = 0.3; w_price = 0.55; w_env = 0.15;
            }}

            // Dynamic Scoring
            filtered.forEach(d => {{
                const tH = d[timeColH] || 50;
                const tW = d[timeColW] || 50;
                const avgCommute = (tH + tW) / 2.0;
                
                // Commute score: lower time -> higher score (range approx 25~80 min)
                const commuteScore = Math.max(0, Math.min(100, 100 - (avgCommute - 25) * (100 / 55)));
                const priceScore = d.score_price;
                const envScore = d.score_livability;

                d.sim_score = (commuteScore * w_commute + priceScore * w_price + envScore * w_env);
                d.current_tH = tH;
                d.current_tW = tW;
                d.current_price = d[priceCol];
            }});

            filtered.sort((a, b) => b.sim_score - a.sim_score);
            const top10 = filtered.slice(0, 10);

            renderRankings(top10, flatType, hubH, hubW);
            updateScatterChart(filtered);
        }}

        function getClusterClass(name) {{
            if (name.includes('프리미엄')) return 'tag-cluster-3';
            if (name.includes('가성비')) return 'tag-cluster-1';
            if (name.includes('요충지')) return 'tag-cluster-2';
            return 'tag-cluster-0';
        }}

        function renderRankings(items, flatType, hubH, hubW) {{
            const container = document.getElementById('ranking-container');
            container.innerHTML = '';

            if (items.length === 0) {{
                container.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-dim);">해당 예산 및 조건에 부합하는 동네가 없습니다. 예산 슬라이더를 올려보세요.</div>';
                return;
            }}

            items.forEach((d, idx) => {{
                const card = document.createElement('div');
                card.className = 'rank-card';
                card.onclick = () => openDetail(d);

                card.innerHTML = `
                    <div class="rank-num">#${{idx + 1}}</div>
                    <div>
                        <div class="dong-info-name">
                            ${{d.행정동명}}
                            <span class="dong-info-gu">${{d.자치구명}}</span>
                        </div>
                        <div style="margin-top: 4px;">
                            <span class="cluster-tag ${{getClusterClass(d.cluster_name)}}">${{d.cluster_name}}</span>
                        </div>
                    </div>
                    <div class="metric-cell">
                        <span class="label">예상 매매가 (전용${{flatType}}㎡)</span>
                        <span class="val" style="color:#60a5fa;">${{d.current_price.toFixed(2)}}억원</span>
                    </div>
                    <div class="metric-cell">
                        <span class="label">남편 통근 / 아내 통근</span>
                        <span class="val">${{d.current_tH.toFixed(1)}}분 / ${{d.current_tW.toFixed(1)}}분</span>
                    </div>
                    <div class="metric-cell">
                        <span class="label">평당 단가</span>
                        <span class="val">${{d.단가_평당만원.toLocaleString()}}만원</span>
                    </div>
                    <div class="score-badge">
                        <div class="score-val">${{d.sim_score.toFixed(1)}}</div>
                        <div class="score-lbl">AI 추천점수</div>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function initCharts() {{
            // 1. Scatter Chart
            const ctxScatter = document.getElementById('scatterChart').getContext('2d');
            scatterChartInstance = new Chart(ctxScatter, {{
                type: 'scatter',
                data: {{
                    datasets: [
                        {{
                            label: '핵심 프리미엄',
                            data: [],
                            backgroundColor: 'rgba(244, 63, 94, 0.7)',
                            borderColor: '#f43f5e'
                        }},
                        {{
                            label: '가성비 스마트타운',
                            data: [],
                            backgroundColor: 'rgba(16, 185, 129, 0.7)',
                            borderColor: '#10b981'
                        }},
                        {{
                            label: '준상급 교통요충지',
                            data: [],
                            backgroundColor: 'rgba(139, 92, 246, 0.7)',
                            borderColor: '#8b5cf6'
                        }},
                        {{
                            label: '외곽 실속주거지',
                            data: [],
                            backgroundColor: 'rgba(59, 130, 246, 0.7)',
                            borderColor: '#3b82f6'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ labels: {{ color: '#94a3b8' }} }},
                        tooltip: {{
                            callbacks: {{
                                label: function(ctx) {{
                                    const raw = ctx.raw;
                                    return `${{raw.dong}} (${{raw.gu}}): 통근 ${{raw.x}}분, 평당 ${{raw.y}}만원`;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            title: {{ display: true, text: '3대 도심 평균 통근시간 (분)', color: '#94a3b8' }},
                            grid: {{ color: 'rgba(255,255,255,0.05)' }},
                            ticks: {{ color: '#64748b' }}
                        }},
                        y: {{
                            title: {{ display: true, text: '평당 단가 (만원)', color: '#94a3b8' }},
                            grid: {{ color: 'rgba(255,255,255,0.05)' }},
                            ticks: {{ color: '#64748b' }}
                        }}
                    }}
                }}
            }});

            // 2. Cluster Pie Chart
            const ctxPie = document.getElementById('clusterPieChart').getContext('2d');
            const counts = {{
                '핵심 프리미엄 상급지': 0,
                '가성비 스마트 주거타운': 0,
                '준상급 교통/주거요충지': 0,
                '외곽 실속 주거타운': 0
            }};
            rawData.forEach(d => {{
                if (counts[d.cluster_name] !== undefined) counts[d.cluster_name]++;
            }});

            clusterPieInstance = new Chart(ctxPie, {{
                type: 'doughnut',
                data: {{
                    labels: Object.keys(counts),
                    datasets: [{{
                        data: Object.values(counts),
                        backgroundColor: ['#f43f5e', '#10b981', '#8b5cf6', '#3b82f6'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', boxWidth: 12, padding: 16 }} }},
                        title: {{ display: true, text: '서울시 418개 행정동 군집 분포', color: '#f8fafc', font: {{ size: 14 }} }}
                    }}
                }}
            }});
        }}

        function updateScatterChart(filteredData) {{
            if (!scatterChartInstance) return;

            const d0 = [], d1 = [], d2 = [], d3 = [];
            filteredData.forEach(d => {{
                const pt = {{
                    x: d['3대도심_평균통근시간'],
                    y: d['단가_평당만원'],
                    dong: d.행정동명,
                    gu: d.자치구명
                }};
                if (d.cluster_name.includes('프리미엄')) d0.push(pt);
                else if (d.cluster_name.includes('가성비')) d1.push(pt);
                else if (d.cluster_name.includes('요충지')) d2.push(pt);
                else d3.push(pt);
            }});

            scatterChartInstance.data.datasets[0].data = d0;
            scatterChartInstance.data.datasets[1].data = d1;
            scatterChartInstance.data.datasets[2].data = d2;
            scatterChartInstance.data.datasets[3].data = d3;
            scatterChartInstance.update();
        }}

        function openDetail(d) {{
            document.getElementById('modal-dong-name').textContent = `${{d.행정동명}} (${{d.자치구명}})`;
            document.getElementById('modal-cluster-tag').innerHTML = `<span class="cluster-tag ${{getClusterClass(d.cluster_name)}}">${{d.cluster_name}}</span>`;
            document.getElementById('modal-price').textContent = `${{d.단가_평당만원.toLocaleString()}}만원 / ${{d.추정_전용59_가격_억.toFixed(2)}}억 (59㎡)`;
            document.getElementById('modal-husband-time').textContent = `${{d.current_tH.toFixed(1)}}분 소요`;
            document.getElementById('modal-wife-time').textContent = `${{d.current_tW.toFixed(1)}}분 소요`;
            document.getElementById('modal-tx-count').textContent = `${{d.최근1년_거래건수}}건 (상위 ${{Math.round(100 - d.score_livability)}}%)`;

            // Radar Chart
            const ctxRadar = document.getElementById('radarChart').getContext('2d');
            if (radarChartInstance) radarChartInstance.destroy();

            radarChartInstance = new Chart(ctxRadar, {{
                type: 'radar',
                data: {{
                    labels: ['가격 가성비', '주거 쾌적성', '강남 접근성', '도심 접근성', '여의도 접근성', '판교 접근성'],
                    datasets: [{{
                        label: d.행정동명 + ' 프로파일',
                        data: [d.score_price, d.score_livability, d.score_gbd, d.score_cbd, d.score_ybd, d.score_pangyo],
                        backgroundColor: 'rgba(59, 130, 246, 0.25)',
                        borderColor: '#3b82f6',
                        pointBackgroundColor: '#60a5fa'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        r: {{
                            angleLines: {{ color: 'rgba(255,255,255,0.08)' }},
                            grid: {{ color: 'rgba(255,255,255,0.08)' }},
                            pointLabels: {{ color: '#94a3b8', font: {{ size: 11 }} }},
                            ticks: {{ display: false, min: 0, max: 100 }}
                        }}
                    }}
                }}
            }});

            document.getElementById('detail-modal').style.display = 'flex';
        }}

        function closeModal(e) {{
            if (!e || e.target.id === 'detail-modal' || e.target.className === 'modal-close') {{
                document.getElementById('detail-modal').style.display = 'none';
            }}
        }}
    </script>
</body>
</html>
'''
    with open('3040_맞벌이_주거지_종합_대시보드.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(">>> 3040_맞벌이_주거지_종합_대시보드.html 생성 완료!")

if __name__ == '__main__':
    build_html()
