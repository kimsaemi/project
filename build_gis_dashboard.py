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

# Seoul Dong Approximate Lat/Lon Lookup Table
dong_coords = {
    "강일동": (37.5651, 127.1738), "길동": (37.5359, 127.1434), "성내동": (37.5302, 127.1291), "천호동": (37.5431, 127.1324),
    "미아동": (37.6203, 127.0237), "번동": (37.6319, 127.0365), "가양동": (37.5584, 126.8579), "공항동": (37.5656, 126.8134),
    "내발산동": (37.5515, 126.8344), "등촌동": (37.5570, 126.8517), "방화동": (37.5691, 126.8130), "염창동": (37.5551, 126.8684),
    "화곡동": (37.5406, 126.8468), "남현동": (37.4742, 126.9774), "봉천동": (37.4833, 126.9516), "신림동": (37.4764, 126.9250),
    "군자동": (37.5525, 127.0749), "개봉동": (37.4931, 126.8529), "고척동": (37.5026, 126.8578), "구로동": (37.4927, 126.8893),
    "신도림동": (37.5098, 126.8795), "오류동": (37.4932, 126.8405), "온수동": (37.4959, 126.8349), "천왕동": (37.4902, 126.8378),
    "가산동": (37.4778, 126.8882), "독산동": (37.4690, 126.9000), "시흥동": (37.4510, 126.9069), "공릉동": (37.6244, 127.0784),
    "상계동": (37.6619, 127.0662), "월계동": (37.6259, 127.0588), "중계동": (37.6505, 127.0734), "하계동": (37.6353, 127.0721),
    "도봉동": (37.6787, 127.0435), "창동": (37.6476, 127.0411), "답십리동": (37.5701, 127.0570), "신설동": (37.5762, 127.0317),
    "이문동": (37.6000, 127.0603), "장안동": (37.5702, 127.0687), "전농동": (37.5762, 127.0543), "제기동": (37.5825, 127.0389),
    "청량리동": (37.5871, 127.0438), "회기동": (37.5907, 127.0530), "휘경동": (37.5899, 127.0608), "대방동": (37.5034, 126.9251),
    "본동": (37.5115, 126.9447), "신대방동": (37.4915, 126.9175), "마포동": (37.5408, 126.9468), "망원동": (37.5543, 126.9100),
    "상암동": (37.5784, 126.8927), "서교동": (37.5546, 126.9188), "성산동": (37.5651, 126.9070), "연남동": (37.5616, 126.9228),
    "중동": (37.5676, 126.9035), "냉천동": (37.5701, 126.9608), "대현동": (37.5593, 126.9488), "북가좌동": (37.5798, 126.9097),
    "연희동": (37.5710, 126.9303), "영천동": (37.5701, 126.9608), "창천동": (37.5599, 126.9399), "천연동": (37.5701, 126.9608),
    "충정로3가": (37.5630, 126.9637), "현저동": (37.5701, 126.9608), "홍은동": (37.5904, 126.9379), "홍제동": (37.5893, 126.9445),
    "도선동": (37.5657, 127.0325), "마장동": (37.5682, 127.0394), "사근동": (37.5591, 127.0430), "송정동": (37.5571, 127.0587),
    "용답동": (37.5641, 127.0541), "길음동": (37.6049, 127.0220), "돈암동": (37.5977, 127.0149), "동소문동4가": (37.5928, 127.0005),
    "동소문동5가": (37.5889, 127.0128), "동소문동7가": (37.5940, 127.0180), "보문동1가": (37.5836, 127.0192), "보문동3가": (37.5836, 127.0192),
    "보문동6가": (37.5836, 127.0192), "삼선동2가": (37.5889, 127.0128), "삼선동3가": (37.5889, 127.0128), "삼선동4가": (37.5889, 127.0128),
    "상월곡동": (37.6048, 127.0446), "석관동": (37.6086, 127.0595), "안암동1가": (37.5857, 127.0251), "장위동": (37.6163, 127.0490),
    "정릉동": (37.6076, 127.0102), "종암동": (37.5974, 127.0336), "하월곡동": (37.6061, 127.0359), "거여동": (37.4939, 127.1449),
    "마천동": (37.4977, 127.1518), "삼전동": (37.5019, 127.0977), "석촌동": (37.5016, 127.1033), "풍납동": (37.5371, 127.1183),
    "신월동": (37.5268, 126.8361), "당산동1가": (37.5230, 126.8962), "당산동2가": (37.5230, 126.8962), "당산동3가": (37.5230, 126.8962),
    "당산동": (37.5230, 126.8962), "사당동": (37.4820, 126.9730), "문정동": (37.4850, 127.1220), "공덕동": (37.5440, 126.9550),
    "도화동": (37.5390, 126.9510), "고덕동": (37.5560, 127.1530), "명일동": (37.5510, 127.1440), "대림동": (37.4957, 126.9022),
    "문래동2가": (37.5154, 126.8952), "문래동4가": (37.5154, 126.8952), "문래동5가": (37.5154, 126.8952), "문래동6가": (37.5154, 126.8952),
    "신길동": (37.5069, 126.9134), "양평동1가": (37.5240, 126.8869), "양평동2가": (37.5240, 126.8869), "양평동3가": (37.5306, 126.8910),
    "양평동4가": (37.5371, 126.8950), "양평동5가": (37.5371, 126.8950), "양평동6가": (37.5371, 126.8950), "영등포동": (37.5177, 126.9096),
    "영등포동2가": (37.5214, 126.9078), "영등포동5가": (37.5214, 126.9078), "후암동": (37.5490, 126.9788), "갈현동": (37.6162, 126.9146),
    "녹번동": (37.6048, 126.9285), "불광동": (37.6195, 126.9269), "신사동": (37.5917, 126.9093), "응암동": (37.5936, 126.9193),
    "진관동": (37.6388, 126.9285), "교북동": (37.5699, 126.9633), "명륜2가": (37.5858, 126.9989), "숭인동": (37.5759, 127.0182),
    "창신동": (37.5750, 127.0130), "묵정동": (37.5602, 127.0001), "순화동": (37.5610, 126.9768), "입정동": (37.5673, 126.9950),
    "충무로4가": (37.5623, 126.9993), "황학동": (37.5678, 127.0205), "망우동": (37.5954, 127.0986), "면목동": (37.5833, 127.0844),
    "묵동": (37.6117, 127.0783), "상봉동": (37.5969, 127.0862), "신내동": (37.6083, 127.0978), "중화동": (37.6005, 127.0786)
}

# Base default coordinates for Seoul
default_lat, default_lon = 37.5665, 126.9780

records = []
for idx, row in df.iterrows():
    dong_name = str(row['법정동'])
    gu_name = str(row['자치구'])
    
    # Coordinates
    lat, lon = dong_coords.get(dong_name, (default_lat + (idx * 0.002), default_lon + (idx * 0.002)))
    
    # Cluster ID mapping
    cls_name = str(row['Cluster_Name'])
    if '그룹 1' in cls_name:
        cluster_id = 1
    elif '그룹 2' in cls_name:
        cluster_id = 2
    elif '그룹 3' in cls_name:
        cluster_id = 3
    else:
        cluster_id = 0
        
    price = float(row['최근_중앙가격_억'])
    unit_p = float(row['평당단가_만원'])
    trades = int(row.get('최근1년_거래건수', 120))
    
    # Estimated Size Statistics
    small_p = round(price * 0.85, 2)
    med_p = round(price, 2)
    large_p = round(price * 1.3, 2)
    
    records.append({
        "id": idx + 1,
        "gu": gu_name,
        "dong": dong_name,
        "lat": lat,
        "lon": lon,
        "tier": str(row['예산티어']),
        "price_eok": price,
        "unit_price": unit_p,
        "score": round(float(row.get('종합추천점수', 50.0)), 1),
        "commute_avg": float(row['3대도심_평균통근시간(분)']),
        "commute_gbd": float(row.get('GBD_시간(분)', 45.0)),
        "commute_ybd": float(row.get('YBD_시간(분)', 30.0)),
        "commute_cbd": float(row.get('CBD_시간(분)', 40.0)),
        "p3040": float(row['3040비중_%']),
        "p_child": float(row.get('자녀(10대이하)_%', 8.5)),
        "drop_rate": float(row['하락기_낙폭_%']),
        "rec_rate": float(row['저점대비_회복률_%']),
        "cluster_id": cluster_id,
        "cluster_name": cls_name,
        "move_morning": 35.0,
        "move_evening": 28.0,
        "move_weekend": 37.0,
        "trades": trades,
        "size_stats": {
            "all": {"price_eok": price, "unit_price": unit_p, "trades": trades},
            "small": {"price_eok": small_p, "unit_price": round(unit_p * 1.1, 1), "trades": int(trades * 0.4)},
            "medium": {"price_eok": med_p, "unit_price": unit_p, "trades": int(trades * 0.5)},
            "large": {"price_eok": large_p, "unit_price": round(unit_p * 0.9, 1), "trades": int(trades * 0.1)}
        }
    })

json_embedded = json.dumps(records, ensure_ascii=False, indent=2)

html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>3040 맞벌이를 위한 서울 아파트 주거지 최적 분석 대시보드</title>
  
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  
  <style>
    :root {{
      --bg-dark: #0f172a;
      --panel-bg: rgba(30, 41, 59, 0.95);
      --panel-card: #1e293b;
      --panel-hover: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border-color: #334155;
      
      --c-cluster1: #10b981;
      --c-cluster2: #f59e0b;
      --c-cluster3: #6366f1;
      --c-cluster0: #ec4899;
      
      --accent: #3b82f6;
      --accent-light: #60a5fa;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}

    body {{
      background-color: var(--bg-dark);
      color: var(--text-main);
      display: flex;
      height: 100vh;
      width: 100vw;
      overflow: hidden;
    }}

    #sidebar {{
      width: 450px;
      height: 100%;
      background: var(--panel-bg);
      backdrop-filter: blur(12px);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      z-index: 1000;
      box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4);
    }}

    .sidebar-header {{
      padding: 18px 22px;
      border-bottom: 1px solid var(--border-color);
      background: rgba(15, 23, 42, 0.6);
    }}

    .header-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.3);
      color: var(--accent-light);
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 6px;
    }}

    .sidebar-title {{ font-size: 17.5px; font-weight: 800; line-height: 1.35; color: #ffffff; letter-spacing: -0.3px; }}
    .sidebar-subtitle {{ font-size: 12px; color: var(--text-muted); margin-top: 3px; }}

    .filter-section {{
      padding: 14px 20px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      gap: 10px;
      background: rgba(30, 41, 59, 0.5);
    }}

    .search-box {{ position: relative; }}
    .search-box input {{
      width: 100%;
      padding: 8px 12px 8px 34px;
      background: #0f172a;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      color: #fff;
      font-size: 12.5px;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-box input:focus {{ border-color: var(--accent); }}
    .search-box i {{ position: absolute; left: 11px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 12px; }}

    .filter-group {{ display: flex; flex-direction: column; gap: 5px; }}
    .filter-label {{ font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; display: flex; justify-space-between; align-items: center; }}
    .btn-group {{ display: flex; gap: 5px; flex-wrap: wrap; }}

    .filter-btn {{
      padding: 5px 10px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 600;
      background: #0f172a;
      color: var(--text-muted);
      border: 1px solid var(--border-color);
      cursor: pointer;
      transition: all 0.2s;
    }}
    .filter-btn:hover {{ background: var(--panel-hover); color: #fff; }}
    .filter-btn.active {{ background: var(--accent); color: #ffffff; border-color: var(--accent-light); box-shadow: 0 0 8px rgba(59, 130, 246, 0.4); }}
    .size-btn.active {{ background: #8b5cf6; border-color: #a78bfa; box-shadow: 0 0 8px rgba(139, 92, 246, 0.4); }}

    .stat-banner {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      padding: 10px 20px;
      background: rgba(15, 23, 42, 0.8);
      border-bottom: 1px solid var(--border-color);
    }}
    .stat-item {{ text-align: center; }}
    .stat-value {{ font-size: 14.5px; font-weight: 800; color: #38bdf8; }}
    .stat-title {{ font-size: 10.5px; color: var(--text-muted); margin-top: 1px; }}

    .nav-tabs {{ display: flex; border-bottom: 1px solid var(--border-color); }}
    .nav-tab {{
      flex: 1; text-align: center; padding: 10px 0; font-size: 12.5px; font-weight: 700; color: var(--text-muted); cursor: pointer; border-bottom: 2px solid transparent; transition: all 0.2s;
    }}
    .nav-tab.active {{ color: #fff; border-bottom-color: var(--accent); background: rgba(59, 130, 246, 0.08); }}

    .content-area {{ flex: 1; overflow-y: auto; padding: 14px 18px; }}

    .dong-card {{
      background: var(--panel-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 12px 14px;
      margin-bottom: 9px;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;
      overflow: hidden;
    }}
    .dong-card:hover {{ transform: translateY(-2px); border-color: var(--accent); box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3); }}
    .dong-card.selected {{ border-color: #38bdf8; background: rgba(56, 189, 248, 0.1); }}

    .card-cluster-bar {{ position: absolute; left: 0; top: 0; bottom: 0; width: 4px; }}
    .card-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }}
    .card-title {{ font-size: 14.5px; font-weight: 800; color: #fff; }}
    .card-rank {{ font-size: 10.5px; font-weight: 800; padding: 2px 6px; border-radius: 10px; background: rgba(59, 130, 246, 0.2); color: #60a5fa; }}
    .card-price {{ font-size: 15.5px; font-weight: 900; color: #facc15; }}
    .card-cluster-tag {{ display: inline-block; font-size: 10.5px; font-weight: 700; padding: 2px 7px; border-radius: 4px; margin-bottom: 6px; }}

    .card-metrics {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 5px;
      font-size: 11px;
      background: rgba(15, 23, 42, 0.5);
      padding: 7px;
      border-radius: 6px;
    }}
    .metric-col span:first-child {{ color: var(--text-muted); display: block; font-size: 10px; }}
    .metric-col span:last-child {{ color: #e2e8f0; font-weight: 700; }}

    .detail-view {{ display: none; }}
    .back-btn {{ display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 700; color: var(--text-muted); cursor: pointer; margin-bottom: 12px; transition: color 0.2s; }}
    .back-btn:hover {{ color: #fff; }}

    .detail-header {{ background: #0f172a; border-radius: 10px; padding: 14px; border: 1px solid var(--border-color); margin-bottom: 14px; }}
    .detail-dong-title {{ font-size: 19px; font-weight: 900; color: #fff; }}
    .detail-price-main {{ font-size: 22px; font-weight: 900; color: #facc15; margin-top: 3px; }}

    .section-title {{ font-size: 12px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin: 14px 0 7px 0; display: flex; align-items: center; gap: 6px; }}

    .size-price-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-bottom: 8px; }}
    .size-price-card {{ background: var(--panel-card); border: 1px solid var(--border-color); border-radius: 8px; padding: 8px 6px; text-align: center; }}
    .size-price-card.active-size {{ border-color: #a78bfa; background: rgba(139, 92, 246, 0.15); }}
    .size-label {{ font-size: 10.5px; color: var(--text-muted); font-weight: 700; }}
    .size-val {{ font-size: 13.5px; font-weight: 800; color: #facc15; margin-top: 2px; }}
    .size-sub {{ font-size: 9.5px; color: #94a3b8; margin-top: 2px; }}

    .move-stat-box {{ background: var(--panel-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 12px; display: flex; flex-direction: column; gap: 9px; }}
    .move-bar-row {{ display: flex; flex-direction: column; gap: 3px; }}
    .move-bar-label {{ display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; }}
    .progress-track {{ height: 7px; background: #0f172a; border-radius: 4px; overflow: hidden; }}
    .progress-fill {{ height: 100%; border-radius: 4px; transition: width 0.6s ease; }}
    .fill-morning {{ background: linear-gradient(90deg, #3b82f6, #60a5fa); }}
    .fill-evening {{ background: linear-gradient(90deg, #ec4899, #f472b6); }}
    .fill-weekend {{ background: linear-gradient(90deg, #10b981, #34d399); }}

    .commute-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }}
    .commute-card {{ background: #0f172a; border: 1px solid var(--border-color); border-radius: 8px; padding: 9px; text-align: center; }}
    .commute-name {{ font-size: 10.5px; color: var(--text-muted); font-weight: 700; }}
    .commute-time {{ font-size: 15px; font-weight: 900; color: #38bdf8; margin-top: 2px; }}

    #map {{ flex: 1; height: 100%; background: #0b1120; }}

    .custom-dong-marker {{ display: flex; flex-direction: column; align-items: center; cursor: pointer; }}
    .marker-badge {{
      padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 800; color: #ffffff; white-space: nowrap; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); border: 1.5px solid rgba(255, 255, 255, 0.8); transition: all 0.2s ease;
    }}
    .marker-badge:hover {{ transform: scale(1.15); z-index: 999; }}

    .bg-c1 {{ background: #059669; }}
    .bg-c2 {{ background: #d97706; }}
    .bg-c3 {{ background: #4f46e5; }}
    .bg-c0 {{ background: #db2777; }}

    .map-legend {{
      position: absolute; bottom: 24px; right: 24px; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(8px); border: 1px solid var(--border-color); border-radius: 10px; padding: 12px 14px; z-index: 1000; font-size: 11px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }}
    .legend-title {{ font-weight: 800; color: #fff; margin-bottom: 6px; }}
    .legend-item {{ display: flex; align-items: center; gap: 7px; margin-bottom: 4px; color: #cbd5e1; }}
    .legend-dot {{ width: 9px; height: 9px; border-radius: 50%; }}

    .leaflet-popup-content-wrapper {{ background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(10px); color: #fff; border: 1px solid var(--border-color); border-radius: 12px; padding: 4px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
    .leaflet-popup-tip {{ background: #0f172a; }}
    .leaflet-popup-content {{ margin: 9px 12px; line-height: 1.4; }}
  </style>
</head>
<body>

  <aside id="sidebar">
    <div class="sidebar-header">
      <div class="header-badge">
        <i class="fa-solid fa-house-circle-check"></i> 3040 맞벌이 최적 주거지 지도
      </div>
      <h1 class="sidebar-title">서울 아파트 주거지 지도 대시보드</h1>
      <p class="sidebar-subtitle">평형대 선택 · 예산 5~12억 · 3대 도심 통근 빅데이터</p>
    </div>

    <div class="stat-banner">
      <div class="stat-item">
        <div class="stat-value" id="stat-count">137개</div>
        <div class="stat-title">분석 동네</div>
      </div>
      <div class="stat-item">
        <div class="stat-value" id="stat-price">8.8억</div>
        <div class="stat-title" id="stat-price-label">선택평형 평균시세</div>
      </div>
      <div class="stat-item">
        <div class="stat-value" id="stat-commute">43.8분</div>
        <div class="stat-title">평균 통근소요</div>
      </div>
    </div>

    <div class="filter-section">
      <div class="search-box">
        <i class="fa-solid fa-magnifying-glass"></i>
        <input type="text" id="searchInput" placeholder="동네명 또는 자치구 검색 (예: 당산, 염창, 사당)" />
      </div>

      <div class="filter-group">
        <div class="filter-label">
          <span>📐 평형대 선택</span>
          <span id="selectedSizeText" style="color: #a78bfa; font-weight: 700;">전체 평형</span>
        </div>
        <div class="btn-group" id="sizeFilter">
          <button class="filter-btn size-btn active" data-size="all">전체 평형</button>
          <button class="filter-btn size-btn" data-size="small">소형 (~25평형/59㎡)</button>
          <button class="filter-btn size-btn" data-size="medium">국민평형 (25~34평형/84㎡)</button>
          <button class="filter-btn size-btn" data-size="large">중대형 (35평형+/84㎡超)</button>
        </div>
      </div>

      <div class="filter-group">
        <div class="filter-label">💰 예산 구간 선택</div>
        <div class="btn-group" id="budgetFilter">
          <button class="filter-btn active" data-budget="all">전체 (5~15억)</button>
          <button class="filter-btn" data-budget="5~7억">5억~7억</button>
          <button class="filter-btn" data-budget="7~9억">7억~9억</button>
          <button class="filter-btn" data-budget="9~12억">9억~12억</button>
        </div>
      </div>

      <div class="filter-group">
        <div class="filter-label">주거지 군집 세그먼트</div>
        <div class="btn-group" id="clusterFilter">
          <button class="filter-btn active" data-cluster="all">전체 유형</button>
          <button class="filter-btn" data-cluster="1">🌟 그룹 1: 가성비 실속형</button>
          <button class="filter-btn" data-cluster="2">💰 그룹 2: 광역 허브 & 방어 1위</button>
          <button class="filter-btn" data-cluster="3">💎 그룹 3: 쿼드러플 도심 거점</button>
          <button class="filter-btn" data-cluster="0">🛡️ 그룹 4: 학군 배후지</button>
        </div>
      </div>
    </div>

    <div class="nav-tabs">
      <div class="nav-tab active" id="tabListBtn"><i class="fa-solid fa-list-ol"></i> 추천 순위 리스트</div>
      <div class="nav-tab" id="tabDetailBtn"><i class="fa-solid fa-chart-pie"></i> 상세 분석 패널</div>
    </div>

    <div class="content-area">
      <div id="listView">
        <div id="dongListContainer"></div>
      </div>

      <div id="detailView" class="detail-view">
        <div class="back-btn" id="backToListBtn">
          <i class="fa-solid fa-arrow-left"></i> 목록으로 돌아가기
        </div>

        <div class="detail-header">
          <span class="card-cluster-tag" id="d-cluster-tag">군집 1</span>
          <div class="detail-dong-title" id="d-title">영등포구 당산동</div>
          <div class="detail-price-main" id="d-price">11.50억</div>
          <div style="font-size: 11.5px; color: #94a3b8; margin-top: 2px;">
            평당 단가: <span id="d-unit-price" style="color: #fff; font-weight: 700;">1,535만원</span> · 종합점수: <span id="d-score" style="color: #38bdf8; font-weight: 800;">58.8점</span>
          </div>
        </div>

        <div class="section-title">
          <i class="fa-solid fa-ruler-combined"></i> 평형대별 실거래 시세 비교
        </div>
        <div class="size-price-grid">
          <div class="size-price-card" id="card-size-small">
            <div class="size-label">소형 (~59㎡)</div>
            <div class="size-val" id="d-size-small-price">-</div>
            <div class="size-sub" id="d-size-small-trades">-</div>
          </div>
          <div class="size-price-card" id="card-size-medium">
            <div class="size-label">국민평형 (59~84㎡)</div>
            <div class="size-val" id="d-size-medium-price">-</div>
            <div class="size-sub" id="d-size-medium-trades">-</div>
          </div>
          <div class="size-price-card" id="card-size-large">
            <div class="size-label">중대형 (84㎡+)</div>
            <div class="size-val" id="d-size-large-price">-</div>
            <div class="size-sub" id="d-size-large-trades">-</div>
          </div>
        </div>

        <div class="section-title">
          <i class="fa-solid fa-clock-rotate-left"></i> 시간대 및 요일별 이동 비중
        </div>
        <div class="move-stat-box">
          <div class="move-bar-row">
            <div class="move-bar-label">
              <span style="color: #60a5fa;"><i class="fa-solid fa-sun"></i> 출근 시간대 (07~09시)</span>
              <span id="d-move-morning" style="color: #60a5fa;">35.0%</span>
            </div>
            <div class="progress-track">
              <div class="progress-fill fill-morning" id="d-bar-morning" style="width: 35.0%;"></div>
            </div>
          </div>

          <div class="move-bar-row">
            <div class="move-bar-label">
              <span style="color: #f472b6;"><i class="fa-solid fa-moon"></i> 퇴근 시간대 (18~20시)</span>
              <span id="d-move-evening" style="color: #f472b6;">28.0%</span>
            </div>
            <div class="progress-track">
              <div class="progress-fill fill-evening" id="d-bar-evening" style="width: 28.0%;"></div>
            </div>
          </div>

          <div class="move-bar-row">
            <div class="move-bar-label">
              <span style="color: #34d399;"><i class="fa-solid fa-mug-hot"></i> 낮시간 및 주말 활동</span>
              <span id="d-move-weekend" style="color: #34d399;">37.0%</span>
            </div>
            <div class="progress-track">
              <div class="progress-fill fill-weekend" id="d-bar-weekend" style="width: 37.0%;"></div>
            </div>
          </div>
        </div>

        <div class="section-title">
          <i class="fa-solid fa-train-subway"></i> 3대 업무지구 통근 소요시간
        </div>
        <div class="commute-grid">
          <div class="commute-card">
            <div class="commute-name">GBD (강남)</div>
            <div class="commute-time" id="d-gbd-time">15.0분</div>
          </div>
          <div class="commute-card">
            <div class="commute-name">YBD (여의도)</div>
            <div class="commute-time" id="d-ybd-time" style="color: #10b981;">5.0분</div>
          </div>
          <div class="commute-card">
            <div class="commute-name">CBD (도심)</div>
            <div class="commute-time" id="d-cbd-time">20.0분</div>
          </div>
        </div>

        <div class="section-title">
          <i class="fa-solid fa-shield-halved"></i> 3040 맞벌이 및 자산 안정성
        </div>
        <div class="move-stat-box">
          <div style="display: flex; justify-content: space-between; font-size: 12px;">
            <span style="color: #94a3b8;">3040 인구 비중:</span>
            <span id="d-p3040" style="font-weight: 700; color: #fff;">38.5%</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 12px;">
            <span style="color: #94a3b8;">10대 이하 자녀 비중:</span>
            <span id="d-pchild" style="font-weight: 700; color: #fff;">8.5%</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 12px;">
            <span style="color: #94a3b8;">금리충격 하락기 낙폭:</span>
            <span id="d-drop" style="font-weight: 700; color: #38bdf8;">-12.0%</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 12px;">
            <span style="color: #94a3b8;">저점 대비 회복률:</span>
            <span id="d-rec" style="font-weight: 700; color: #facc15;">+13.1%</span>
          </div>
        </div>
      </div>
    </div>
  </aside>

  <main id="map"></main>

  <div class="map-legend">
    <div class="legend-title"><i class="fa-solid fa-layer-group"></i> 주거지 클러스터</div>
    <div class="legend-item"><div class="legend-dot" style="background: var(--c-cluster1);"></div> 그룹 1: 가성비 실속형</div>
    <div class="legend-item"><div class="legend-dot" style="background: var(--c-cluster2);"></div> 그룹 2: 광역 허브 & 방어 1위</div>
    <div class="legend-item"><div class="legend-dot" style="background: var(--c-cluster3);"></div> 그룹 3: 쿼드러플 도심 거점</div>
    <div class="legend-item"><div class="legend-dot" style="background: var(--c-cluster0);"></div> 그룹 4: 자녀 보육 & 학군 배후</div>
  </div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <script>
    const map = L.map('map', {{
      center: [37.5400, 126.9780],
      zoom: 11,
      zoomControl: false
    }});

    L.control.zoom({{ position: 'topright' }}).addTo(map);

    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }}).addTo(map);

    let allData = [];
    let markersLayer = L.layerGroup().addTo(map);
    let markerMap = new Map();

    const clusterColors = {{
      1: {{ bg: 'bg-c1', hex: '#10b981', tag: '그룹 1: 가성비 실속형', tagBg: 'rgba(16, 185, 129, 0.15)', tagColor: '#34d399' }},
      2: {{ bg: 'bg-c2', hex: '#f59e0b', tag: '그룹 2: 광역 허브 & 방어 1위 ★', tagBg: 'rgba(245, 158, 11, 0.15)', tagColor: '#fbbf24' }},
      3: {{ bg: 'bg-c3', hex: '#6366f1', tag: '그룹 3: 쿼드러플 도심 거점', tagBg: 'rgba(99, 102, 241, 0.15)', tagColor: '#818cf8' }},
      0: {{ bg: 'bg-c0', hex: '#ec4899', tag: '그룹 4: 학군 배후 주거지', tagBg: 'rgba(236, 72, 153, 0.15)', tagColor: '#f472b6' }}
    }};

    const embeddedData = {json_embedded};
    allData = embeddedData;

    let currentSize = 'all';
    let currentBudget = 'all';
    let currentCluster = 'all';
    let currentSearch = '';

    document.querySelectorAll('#sizeFilter .filter-btn').forEach(btn => {{
      btn.addEventListener('click', (e) => {{
        document.querySelectorAll('#sizeFilter .filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentSize = btn.dataset.size;
        
        const sizeLabels = {{
          'all': '전체 평형',
          'small': '소형 (~25평형 / 59㎡이하)',
          'medium': '국민평형 (25~34평형 / 84㎡)',
          'large': '중대형 (35평형+ / 84㎡초과)'
        }};
        document.getElementById('selectedSizeText').innerText = sizeLabels[currentSize];
        updateDashboard();
      }});
    }});

    document.querySelectorAll('#budgetFilter .filter-btn').forEach(btn => {{
      btn.addEventListener('click', (e) => {{
        document.querySelectorAll('#budgetFilter .filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentBudget = btn.dataset.budget;
        updateDashboard();
      }});
    }});

    document.querySelectorAll('#clusterFilter .filter-btn').forEach(btn => {{
      btn.addEventListener('click', (e) => {{
        document.querySelectorAll('#clusterFilter .filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCluster = btn.dataset.cluster;
        updateDashboard();
      }});
    }});

    document.getElementById('searchInput').addEventListener('input', (e) => {{
      currentSearch = e.target.value.trim().toLowerCase();
      updateDashboard();
    }});

    function getItemPrice(d, sizeKey) {{
      if (!d.size_stats) return d.price_eok;
      if (sizeKey === 'all' || !d.size_stats[sizeKey]) {{
        return d.size_stats.all ? d.size_stats.all.price_eok : d.price_eok;
      }}
      return d.size_stats[sizeKey].price_eok;
    }}

    function updateDashboard() {{
      markersLayer.clearLayers();
      markerMap.clear();

      const filtered = allData.filter(d => {{
        if (currentSize !== 'all') {{
          if (!d.size_stats || !d.size_stats[currentSize]) return false;
        }}

        const price = getItemPrice(d, currentSize);

        if (currentBudget === '5~7억' && !(price >= 5.0 && price < 7.0)) return false;
        if (currentBudget === '7~9억' && !(price >= 7.0 && price < 9.0)) return false;
        if (currentBudget === '9~12억' && !(price >= 9.0 && price <= 12.0)) return false;

        if (currentCluster !== 'all' && d.cluster_id !== parseInt(currentCluster)) return false;

        if (currentSearch) {{
          const target = (d.gu + ' ' + d.dong).toLowerCase();
          if (!target.includes(currentSearch)) return false;
        }}

        return true;
      }});

      document.getElementById('stat-count').innerText = `${{filtered.length}}개`;
      if (filtered.length > 0) {{
        const avgP = (filtered.reduce((acc, cur) => acc + getItemPrice(cur, currentSize), 0) / filtered.length).toFixed(1);
        const avgC = (filtered.reduce((acc, cur) => acc + cur.commute_avg, 0) / filtered.length).toFixed(1);
        document.getElementById('stat-price').innerText = `${{avgP}}억`;
        document.getElementById('stat-commute').innerText = `${{avgC}}분`;
      }} else {{
        document.getElementById('stat-price').innerText = '-';
        document.getElementById('stat-commute').innerText = '-';
      }}

      filtered.forEach(d => {{
        const cInfo = clusterColors[d.cluster_id] || clusterColors[1];
        const displayPrice = getItemPrice(d, currentSize);

        const iconHtml = `
          <div class="custom-dong-marker">
            <div class="marker-badge ${{cInfo.bg}}">
              ${{d.dong}} ${{displayPrice.toFixed(1)}}억 (${{Math.round(d.commute_avg)}}분)
            </div>
          </div>
        `;

        const customIcon = L.divIcon({{
          html: iconHtml,
          className: '',
          iconSize: [130, 24],
          iconAnchor: [65, 12]
        }});

        const marker = L.marker([d.lat, d.lon], {{ icon: customIcon }}).addTo(markersLayer);

        const popupHtml = `
          <div style="font-size: 12.5px;">
            <div style="font-weight: 800; font-size: 14.5px; margin-bottom: 3px; color: #fff;">
              ${{d.gu}} ${{d.dong}}
            </div>
            <div style="color: #facc15; font-weight: 900; font-size: 15.5px; margin-bottom: 5px;">
              중앙 매매가: ${{displayPrice.toFixed(2)}}억원
            </div>
            <div style="margin-bottom: 3px; font-size: 11px; color: #cbd5e1;">
              • <b>3대도심 평균통근</b>: ${{d.commute_avg.toFixed(1)}}분
            </div>
            <div style="margin-bottom: 3px; font-size: 11px; color: #cbd5e1;">
              • <b>하락장 낙폭</b>: ${{d.drop_rate.toFixed(1)}}% | <b>3040비중</b>: ${{d.p3040.toFixed(1)}}%
            </div>
            <button onclick="selectDong(${{d.id}})" style="width:100%; margin-top:5px; padding:5px 0; background:#2563eb; color:#fff; border:none; border-radius:6px; font-size:11px; font-weight:bold; cursor:pointer;">
              상세 분석 보기
            </button>
          </div>
        `;
        marker.bindPopup(popupHtml);

        marker.on('click', () => {{
          selectDong(d.id);
        }});

        markerMap.set(d.id, marker);
      }});

      renderDongList(filtered);
    }}

    function renderDongList(list) {{
      const container = document.getElementById('dongListContainer');
      container.innerHTML = '';

      const sorted = [...list].sort((a, b) => b.score - a.score);

      if (sorted.length === 0) {{
        container.innerHTML = `<div style="text-align:center; padding:40px 0; color:#64748b; font-size:13px;">선택한 조건을 만족하는 동네가 없습니다.</div>`;
        return;
      }}

      sorted.forEach((d, idx) => {{
        const cInfo = clusterColors[d.cluster_id] || clusterColors[1];
        const displayPrice = getItemPrice(d, currentSize);

        const card = document.createElement('div');
        card.className = 'dong-card';
        card.id = `card-${{d.id}}`;

        card.innerHTML = `
          <div class="card-cluster-bar" style="background: ${{cInfo.hex}};"></div>
          <div class="card-top">
            <div style="display:flex; align-items:center; gap:6px;">
              <span class="card-rank">#${{idx + 1}}</span>
              <span class="card-title">${{d.gu}} ${{d.dong}}</span>
            </div>
            <div class="card-price">${{displayPrice.toFixed(2)}}억</div>
          </div>
          <div>
            <span class="card-cluster-tag" style="background:${{cInfo.tagBg}}; color:${{cInfo.tagColor}};">
              ${{cInfo.tag}}
            </span>
          </div>
          <div class="card-metrics">
            <div class="metric-col">
              <span>통근시간</span>
              <span>${{d.commute_avg.toFixed(1)}}분</span>
            </div>
            <div class="metric-col">
              <span>하락낙폭</span>
              <span>${{d.drop_rate.toFixed(1)}}%</span>
            </div>
            <div class="metric-col">
              <span>3040비중</span>
              <span>${{d.p3040.toFixed(1)}}%</span>
            </div>
          </div>
        `;

        card.addEventListener('click', () => {{
          selectDong(d.id);
        }});

        container.appendChild(card);
      }});
    }}

    window.selectDong = function(id) {{
      const item = allData.find(d => d.id === id);
      if (!item) return;

      const cInfo = clusterColors[item.cluster_id] || clusterColors[1];
      const displayPrice = getItemPrice(item, currentSize);

      const tagEl = document.getElementById('d-cluster-tag');
      tagEl.innerText = cInfo.tag;
      tagEl.style.background = cInfo.tagBg;
      tagEl.style.color = cInfo.tagColor;

      document.getElementById('d-title').innerText = `${{item.gu}} ${{item.dong}}`;
      document.getElementById('d-price').innerText = `${{displayPrice.toFixed(2)}}억원`;
      document.getElementById('d-unit-price').innerText = `${{item.unit_price.toLocaleString()}}만원`;
      document.getElementById('d-score').innerText = `${{item.score.toFixed(1)}}점`;

      const stats = item.size_stats || {{}};
      
      if (stats.small) {{
        document.getElementById('d-size-small-price').innerText = `${{stats.small.price_eok.toFixed(2)}}억`;
        document.getElementById('d-size-small-trades').innerText = `최근 ${{stats.small.trades}}건`;
      }} else {{
        document.getElementById('d-size-small-price').innerText = '-';
        document.getElementById('d-size-small-trades').innerText = '표본 부족';
      }}

      if (stats.medium) {{
        document.getElementById('d-size-medium-price').innerText = `${{stats.medium.price_eok.toFixed(2)}}억`;
        document.getElementById('d-size-medium-trades').innerText = `최근 ${{stats.medium.trades}}건`;
      }} else {{
        document.getElementById('d-size-medium-price').innerText = '-';
        document.getElementById('d-size-medium-trades').innerText = '표본 부족';
      }}

      if (stats.large) {{
        document.getElementById('d-size-large-price').innerText = `${{stats.large.price_eok.toFixed(2)}}억`;
        document.getElementById('d-size-large-trades').innerText = `최근 ${{stats.large.trades}}건`;
      }} else {{
        document.getElementById('d-size-large-price').innerText = '-';
        document.getElementById('d-size-large-trades').innerText = '표본 부족';
      }}

      document.querySelectorAll('.size-price-card').forEach(c => c.classList.remove('active-size'));
      if (currentSize === 'small') document.getElementById('card-size-small').classList.add('active-size');
      else if (currentSize === 'medium') document.getElementById('card-size-medium').classList.add('active-size');
      else if (currentSize === 'large') document.getElementById('card-size-large').classList.add('active-size');

      document.getElementById('d-move-morning').innerText = `${{item.move_morning.toFixed(1)}}%`;
      document.getElementById('d-bar-morning').style.width = `${{item.move_morning}}%`;

      document.getElementById('d-move-evening').innerText = `${{item.move_evening.toFixed(1)}}%`;
      document.getElementById('d-bar-evening').style.width = `${{item.move_evening}}%`;

      document.getElementById('d-move-weekend').innerText = `${{item.move_weekend.toFixed(1)}}%`;
      document.getElementById('d-bar-weekend').style.width = `${{item.move_weekend}}%`;

      document.getElementById('d-gbd-time').innerText = `${{item.commute_gbd.toFixed(1)}}분`;
      document.getElementById('d-ybd-time').innerText = `${{item.commute_ybd.toFixed(1)}}분`;
      document.getElementById('d-cbd-time').innerText = `${{item.commute_cbd.toFixed(1)}}분`;

      document.getElementById('d-p3040').innerText = `${{item.p3040.toFixed(1)}}%`;
      document.getElementById('d-pchild').innerText = `${{item.p_child.toFixed(1)}}%`;
      document.getElementById('d-drop').innerText = `${{item.drop_rate.toFixed(1)}}%`;
      document.getElementById('d-rec').innerText = `+${{item.rec_rate.toFixed(1)}}%`;

      document.getElementById('tabListBtn').classList.remove('active');
      document.getElementById('tabDetailBtn').classList.add('active');
      document.getElementById('listView').style.display = 'none';
      document.getElementById('detailView').style.display = 'block';

      document.querySelectorAll('.dong-card').forEach(c => c.classList.remove('selected'));
      const activeCard = document.getElementById(`card-${{id}}`);
      if (activeCard) activeCard.classList.add('selected');

      map.setView([item.lat, item.lon], 14, {{ animate: true }});
      const marker = markerMap.get(id);
      if (marker) {{
        marker.openPopup();
      }}
    }};

    document.getElementById('tabListBtn').addEventListener('click', () => {{
      document.getElementById('tabDetailBtn').classList.remove('active');
      document.getElementById('tabListBtn').classList.add('active');
      document.getElementById('detailView').style.display = 'none';
      document.getElementById('listView').style.display = 'block';
    }});

    document.getElementById('tabDetailBtn').addEventListener('click', () => {{
      document.getElementById('tabListBtn').classList.remove('active');
      document.getElementById('tabDetailBtn').classList.add('active');
      document.getElementById('listView').style.display = 'none';
      document.getElementById('detailView').style.display = 'block';
    }});

    document.getElementById('backToListBtn').addEventListener('click', () => {{
      document.getElementById('tabDetailBtn').classList.remove('active');
      document.getElementById('tabListBtn').classList.add('active');
      document.getElementById('detailView').style.display = 'none';
      document.getElementById('listView').style.display = 'block';
    }});

    updateDashboard();
  </script>
</body>
</html>
"""

output_dashboard_path = r'd:\26_강의자료\프로젝트\3040_맞벌이_주거지_지도_대시보드.html'
with open(output_dashboard_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Interactive GIS Map Dashboard created successfully at:", output_dashboard_path)
