"""
파생변수 생성 + 강건성 진단 유틸
=================================

분석 과정에서 합의된 기준을 코드로 고정한 모듈이다. 왜 이런 기준인지는
ANALYSIS.md 를 볼 것. 요약하면:

  1. 분석 단위는 법정동이 주력, 자치구는 설명용.
     자치구는 n=25 라 강남구·중구 2~3개가 상관계수를 좌우한다.
  2. 40대 비중 단독 대신 '핵심생애주기비중'(30대+40대)을 쓴다.
  3. 직주비(비율) 대신 log(직장인구)를 기본으로 쓴다.
  4. 상관계수는 Pearson·Spearman·이상치제거값을 항상 함께 본다.

사용:
    from features import add_features, robust_corr, collapse

    panel = add_features(pd.read_csv(OUT / 'panel_dong.csv'))
    print(robust_corr(collapse(panel, '코드8'), '핵심생애주기비중', '단가_중앙값'))
"""

import numpy as np
import pandas as pd
from scipy import stats

# 자치구 단위에서 상관계수를 좌우하는 것으로 확인된 구.
#   강남구  : 단가 1위 + 40대비중 1위 + 직주비 2위  -> 모든 상관을 혼자 끌어올린다
#   중구·종로구: 직주비 9.96 / 3.31 로 최상위인데 가격은 중위권 -> 직주비 상관을 혼자 끌어내린다
# 어느 쪽을 빼느냐에 따라 직주비 상관이 0.19~0.78 로 요동쳤다.
LEVERAGE_GU = ['강남구', '중구', '종로구']

# 이상치 제거 강건성 검사에서 잘라낼 상·하위 비율
TRIM_Q = 0.02

# 직주비는 상주인구가 분모라, 상주인구 수백 명짜리 법정동에서 값이 폭발한다
# (문래동4가 직주비 20.7, 수서동 37.1). 이 동들은 관계를 만드는 게 아니라 가린다:
# 상주인구 하한을 올릴수록 log직주비~단가 상관이 0.394 -> 0.479 -> 0.637 -> 0.783 으로 강해졌다.
# 1,000명은 법정동 82%(222/272)를 남기면서 퇴화 사례만 걷어내는 지점.
MIN_RESIDENTS = 1000

# 패널 전체의 직장인구 합 ÷ 상주인구 합. 서울 '평균' 기준선이다.
# 실제 서울은 0.56(종사자 530만 / 인구 940만)인데 패널은 1.01 로 약 1.8배 부풀려져 있다.
# 상권 반경 내 인구만 집계해 직장은 71%, 주거는 40% 만 잡히기 때문이다.
# 그래서 직주비 절대값은 발표하면 안 되고, 이 값으로 나눈 '서울 평균 대비 배율'을 쓴다
# (분자·분모의 부풀림이 약분된다).
SEOUL_JOB_RATIO = 1.01

# 발표용 범주. 순위만 쓰므로 위 편향과 무관하다.
# 경계는 0.5(주민 2명당 출근자 1명)와 3(주민 1명당 3명) — 해석이 쉬운 지점으로 잡았다.
JOB_RATIO_BINS = [0, 0.5, 3, np.inf]
JOB_RATIO_LABELS = ['주거지', '혼합', '업무중심']


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """panel_dong / panel_gu 에 합의된 파생변수를 붙인다."""
    out = df.copy()

    # ── 인구 구성 ──────────────────────────────────────────
    # 40대 단독은 Pearson 0.70 / Spearman 0.39 로 격차가 커 레버리지 신호였다.
    # 30대와 합치면 개별 잡음(자녀 유무, 전월세 전환시점)이 상쇄되고
    # 이상치를 빼도 0.75 -> 0.64 -> 0.56 으로 완만하게만 줄어든다.
    out['핵심생애주기비중'] = out['상주비중_30'] + out['상주비중_40']

    # 고령 비중은 가격과 가장 강한 음의 상관(-0.71)을 보인 변수라 대조군으로 남긴다.
    out['고령비중'] = out['상주비중_60_이상']

    # ── 직주 성격 ──────────────────────────────────────────
    # 직주비 원값은 중구 9.96 ~ 중랑구 0.112 로 두 자릿수 배율 차이라 선형상관이 깨진다.
    # 법정동 단위에서 Pearson 0.177 / Spearman 0.407 로 격차가 컸는데,
    # 로그를 씌우자 0.391 / 0.407 로 붙고 이상치를 빼도 0.36~0.43 을 유지했다.
    # -> 직주근접 지표는 log(직주비)를 쓴다. 원값은 쓰지 말 것.
    out['log직주비'] = np.log(out['직주비'].where(out['직주비'] > 0))

    # log(직장인구)는 자치구에서만 강했고(0.688) 법정동에서는 0.087 로 무너졌다.
    # '직장이 몇 개냐'보다 '주거 대비 얼마나 직장 중심이냐'가 실제 신호다.
    out['log직장인구'] = np.log(out['직장인구'].where(out['직장인구'] > 0))
    out['log상주인구'] = np.log(out['상주인구'].where(out['상주인구'] > 0))

    # ── 발표용 (절대값 대신 쓸 것) ─────────────────────────
    # 직주비 절대값은 실제보다 1.8배 부풀려져 있다(ANALYSIS.md 1-3 참고).
    # 아래 세 가지는 배율 편향이 약분되거나 순위만 쓰므로 안전하다.

    # log2: 1 단위 = 2배. "2배가 될 때마다 가격 +N%" 로 바로 읽힌다.
    out['log2직주비'] = np.log2(out['직주비'].where(out['직주비'] > 0))

    # 서울 평균 대비 배율. 분자·분모의 부풀림이 약분된다.
    out['직주비_서울평균대비'] = (out['직주비'] / SEOUL_JOB_RATIO).round(2)

    # 범주. 순위만 쓰므로 편향과 무관하고, 통계 없이도 계단이 보인다.
    out['지역유형'] = pd.cut(out['직주비'], JOB_RATIO_BINS, labels=JOB_RATIO_LABELS)

    # ── 종속변수 ──────────────────────────────────────────
    out['log단가'] = np.log(out['단가_중앙값'].where(out['단가_중앙값'] > 0))

    return out


def collapse(df: pd.DataFrame, unit: str, sample_ok_only: bool = True,
             min_residents: int = 0) -> pd.DataFrame:
    """패널을 단위별 시계열 평균으로 접는다(횡단면 분석용).

    인구 변수는 연 1회만 갱신돼 분기 변동이 2.7~6.4% 에 불과하므로,
    횡단면 상관을 볼 때는 시계열 평균으로 접는 편이 노이즈가 적다.

    sample_ok_only : panel_dong 의 거래 5건 미만 행(중앙값이 불안정)을 제외
    min_residents  : 상주인구 하한. 직주비 계열을 볼 때는 MIN_RESIDENTS 를 줄 것.
                     기본 0 은 '거르지 않음'(다른 변수와 표본을 맞춰야 할 때).
    """
    d = df
    if sample_ok_only and '표본충분' in d.columns:
        d = d[d['표본충분']]
    if min_residents:
        d = d[d['상주인구'] >= min_residents]

    # 코드8은 숫자로 읽히지만 식별자이므로 평균 대상에서 뺀다
    num = d.select_dtypes(include=[np.number]).columns.difference(['분기', unit, '코드8'])
    g = d.groupby(unit)[list(num)].mean()

    # 자치구명은 이상치 진단에 필요하므로 살려둔다
    if unit != '자치구명' and '자치구명' in d.columns:
        g = g.join(d.groupby(unit)['자치구명'].first())
    if '법정동명' in d.columns and unit == '코드8':
        g = g.join(d.groupby(unit)['법정동명'].first())
    g = g.reset_index()

    # 범주형은 평균이 안 되므로 접은 뒤의 직주비로 다시 매긴다
    # (분기별 유형의 최빈값이 아니라 기간 평균 기준이라야 일관된다)
    if '직주비' in g.columns:
        g['지역유형'] = pd.cut(g['직주비'], JOB_RATIO_BINS, labels=JOB_RATIO_LABELS)
    return g


def robust_corr(df: pd.DataFrame, x: str, y: str = '단가_중앙값') -> pd.Series:
    """Pearson·Spearman·이상치제거 상관을 한 번에 낸다.

    Pearson 과 Spearman 의 격차가 크거나, trim/leverage 제거 후 값이
    크게 무너지면 '진짜 관계'가 아니라 소수 관측치가 만든 착시다.
    """
    d = df[[x, y] + (['자치구명'] if '자치구명' in df.columns else [])].dropna(subset=[x, y])
    if len(d) < 5:
        raise ValueError(f'표본이 너무 적다: n={len(d)}')

    res = {
        'n': len(d),
        'pearson': np.corrcoef(d[x], d[y])[0, 1],
        'spearman': stats.spearmanr(d[x], d[y]).correlation,
    }

    # 종속변수 상·하위 TRIM_Q 를 자른 뒤에도 관계가 남는가
    lo, hi = d[y].quantile([TRIM_Q, 1 - TRIM_Q])
    t = d[(d[y] >= lo) & (d[y] <= hi)]
    res[f'trim{int(TRIM_Q*100)}%'] = np.corrcoef(t[x], t[y])[0, 1] if len(t) >= 5 else np.nan

    # 레버리지 자치구를 뺀 뒤에도 남는가 (자치구 단위에서만 의미 있다)
    if '자치구명' in d.columns:
        s = d[~d['자치구명'].isin(LEVERAGE_GU)]
        res['no_leverage'] = np.corrcoef(s[x], s[y])[0, 1] if len(s) >= 5 else np.nan

    res['verdict'] = _verdict(res)
    return pd.Series(res, name=x)


def _verdict(r: dict) -> str:
    """상관이 강건한지 한 단어로 판정한다."""
    vals = [abs(v) for k, v in r.items()
            if k not in ('n', 'verdict') and isinstance(v, float) and not np.isnan(v)]
    if not vals:
        return '판정불가'
    if min(vals) < 0.15:
        return '취약 (일부 관측치 의존)'
    if max(vals) - min(vals) > 0.25:
        return '불안정 (기준별 편차 큼)'
    if min(vals) >= 0.30:
        return '강건'
    return '약함'


def diagnose(df: pd.DataFrame, xs: list, y: str = '단가_중앙값') -> pd.DataFrame:
    """여러 변수를 한 표로 진단한다."""
    return pd.DataFrame([robust_corr(df, x, y) for x in xs])


if __name__ == '__main__':
    from paths import OUT

    XS = ['핵심생애주기비중', '상주비중_40', 'log직주비', '직주비',
          'log직장인구', '고령비중', '면적_중앙값', '인구밀도', 'log상주인구']

    for name, unit in [('panel_gu.csv', '자치구명'), ('panel_dong.csv', '코드8')]:
        panel = add_features(pd.read_csv(OUT / name))
        cs = collapse(panel, unit)
        print(f'\n{"="*72}\n{name}  (단위 {unit}, n={len(cs)})\n{"="*72}')
        print(diagnose(cs, XS).round(3).to_string())

    # 직주비 계열은 분모가 작은 법정동을 걸러야 제 모습이 나온다
    dong = add_features(pd.read_csv(OUT / 'panel_dong.csv'))
    cs = collapse(dong, '코드8', min_residents=MIN_RESIDENTS)
    print(f'\n{"="*72}\npanel_dong.csv  상주인구 {MIN_RESIDENTS:,}명 이상만  (n={len(cs)})\n{"="*72}')
    print(diagnose(cs, ['log직주비', '핵심생애주기비중', '면적_중앙값']).round(3).to_string())
