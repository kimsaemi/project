"""단일 숫자형 컬럼의 분포를 히스토그램·박스플롯으로 그린다.

기본 대상은 panel_dong.csv의 주 종속변수 `단가_중앙값`(㎡당 만원).
pandas 없이 표준 라이브러리 + matplotlib만 쓴다.

    python src/plot_dist.py                 # 단가_중앙값
    python src/plot_dist.py 인구밀도         # 다른 컬럼
"""

import csv
import statistics as st
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from paths import OUT

# ── 색·잉크 (dataviz 기준 팔레트, light surface) ──────────────────────────
SURFACE = "#fcfcfb"
SERIES = "#2a78d6"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"

for family in ("AppleGothic", "Apple SD Gothic Neo", "Malgun Gothic", "NanumGothic"):
    if any(f.name == family for f in matplotlib.font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = family
        break
plt.rcParams.update({
    "axes.unicode_minus": False,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.size": 10,
})

COMMA = FuncFormatter(lambda x, _: f"{x:,.0f}")


def quantile(v, p):
    """선형보간 분위수 (numpy·pandas 기본 방식)."""
    if p <= 0:
        return v[0]
    if p >= 1:
        return v[-1]
    h = (len(v) - 1) * p
    lo = int(h)
    return v[lo] + (h - lo) * (v[lo + 1] - v[lo])


def load(col):
    path = OUT / "panel_dong.csv"
    with open(path, encoding="utf-8-sig") as fh:
        vals = [r[col] for r in csv.DictReader(fh)]
    kept = sorted(float(v) for v in vals if v.strip() != "")
    return kept, len(vals) - len(kept)


def bare(ax, spines=("left", "bottom")):
    """상·우 스핀 제거, 축은 후퇴시킨다."""
    for side, sp in ax.spines.items():
        sp.set_visible(side in spines)
        sp.set_color(AXIS)
        sp.set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelcolor=INK_2, length=3, width=0.8)


def stats(v):
    q1, q2, q3 = quantile(v, 0.25), quantile(v, 0.5), quantile(v, 0.75)
    iqr = q3 - q1
    hi = q3 + 1.5 * iqr
    lo = q1 - 1.5 * iqr
    return {
        "n": len(v), "min": v[0], "q1": q1, "q2": q2, "q3": q3, "max": v[-1],
        "mean": st.mean(v), "iqr": iqr,
        "whi_hi": max(x for x in v if x <= hi),
        "whi_lo": min(x for x in v if x >= lo),
        "out_hi": sum(1 for x in v if x > hi),
        "out_lo": sum(1 for x in v if x < lo),
        "below_mean": sum(1 for x in v if x < st.mean(v)),
    }


def histogram(v, s, col, unit, out):
    # Freedman–Diaconis 로 구간 폭 결정
    width = 2 * s["iqr"] / len(v) ** (1 / 3)
    bins = max(10, round((s["max"] - s["min"]) / width))

    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=200)
    ax.hist(v, bins=bins, color=SERIES, edgecolor=SURFACE, linewidth=0.6, zorder=3)

    # 두 선이 가까워도 라벨이 겹치지 않도록 좌우·상하로 갈라놓는다
    for x, label, style, ha, dx, dy in (
        (s["q2"], f"중위수 {s['q2']:,.0f}", "-", "right", -7, -13),
        (s["mean"], f"평균 {s['mean']:,.0f}", "--", "left", 7, -31),
    ):
        ax.axvline(x, color=INK, linewidth=1.4, linestyle=style, zorder=4)
        ax.annotate(label, (x, 1), xytext=(dx, dy), textcoords="offset points",
                    xycoords=("data", "axes fraction"), color=INK, ha=ha,
                    fontsize=9, fontweight="bold" if style == "-" else "normal")

    ax.set_title(f"{col} 분포 — 서울 법정동×분기 패널 (2021Q1–2026Q1)",
                 color=INK, fontsize=13, fontweight="bold", loc="left", pad=14)
    ax.set_xlabel(unit, color=INK_2)
    ax.set_ylabel("법정동×분기 건수", color=INK_2)
    ax.xaxis.set_major_formatter(COMMA)
    ax.yaxis.set_major_formatter(COMMA)
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    bare(ax)
    ax.annotate(
        f"n={s['n']:,}  ·  구간 폭 {width:,.0f} (Freedman–Diaconis, {bins}개)  ·  "
        f"평균 미만 {s['below_mean'] / s['n'] * 100:.1f}%",
        (0, -0.22), xycoords="axes fraction", color=MUTED, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


def boxplot(v, s, col, unit, out):
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=200)
    ax.boxplot(
        v, orientation="horizontal", widths=0.42, whis=1.5, patch_artist=True,
        boxprops=dict(facecolor=SERIES, edgecolor=SURFACE, linewidth=1.2),
        medianprops=dict(color=SURFACE, linewidth=2),
        whiskerprops=dict(color=INK_2, linewidth=1.4),
        capprops=dict(color=INK_2, linewidth=1.4),
        flierprops=dict(marker="o", markersize=3.5, markerfacecolor=SERIES,
                        markeredgecolor="none", alpha=0.28),
        zorder=3,
    )

    # 오른쪽 끝 라벨이 잘리지 않도록 여유를, 위쪽에 라벨 자리를 만든다
    ax.set_xlim(min(0, s["min"]), s["max"] * 1.04)
    ax.set_ylim(0.62, 1.72)
    # 라벨은 전부 박스 위에, 서로 겹치지 않게 2행으로 엇갈려 놓는다
    for x, label, dy, ha in (
        (s["whi_lo"], f"Min {s['whi_lo']:,.0f}", 26, "left"),
        (s["q1"], f"Q1 {s['q1']:,.0f}", 4, "center"),
        (s["q2"], f"Q2 {s['q2']:,.0f}", 26, "center"),
        (s["q3"], f"Q3 {s['q3']:,.0f}", 4, "center"),
        (s["whi_hi"], f"울타리 {s['whi_hi']:,.0f}", 26, "center"),
        (s["max"], f"Max {s['max']:,.0f}", 4, "right"),
    ):
        ax.annotate(label, (x, 1.24), xytext=(0, dy), textcoords="offset points",
                    ha=ha, color=INK, fontsize=8.5)

    ax.set_title(f"{col} — 사분위·이상치", color=INK, fontsize=13,
                 fontweight="bold", loc="left", pad=16)
    ax.set_xlabel(unit, color=INK_2, labelpad=6)
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(COMMA)
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    bare(ax, spines=("bottom",))
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.text(
        0.012, 0.03,
        f"n={s['n']:,}  ·  IQR {s['iqr']:,.0f}  ·  "
        f"수염은 1.5×IQR  ·  상단 이상치 {s['out_hi']}건 "
        f"({s['out_hi'] / s['n'] * 100:.1f}%), 하단 {s['out_lo']}건",
        color=MUTED, fontsize=8.5)
    fig.savefig(out)
    plt.close(fig)


def main():
    col = sys.argv[1] if len(sys.argv) > 1 else "단가_중앙값"
    unit = "㎡당 만원" if col.startswith("단가") else col
    v, missing = load(col)
    s = stats(v)

    fig_dir = OUT / "figures"
    fig_dir.mkdir(exist_ok=True)
    h = fig_dir / f"hist_{col}.png"
    b = fig_dir / f"box_{col}.png"
    histogram(v, s, col, unit, h)
    boxplot(v, s, col, unit, b)

    print(f"{col}: n={s['n']:,} 결측={missing} 평균={s['mean']:,.2f}")
    print(f"  Min {s['min']:,.2f} / Q1 {s['q1']:,.2f} / Q2 {s['q2']:,.2f} / "
          f"Q3 {s['q3']:,.2f} / Max {s['max']:,.2f}")
    print(f"  저장: {h}\n        {b}")


if __name__ == "__main__":
    main()
