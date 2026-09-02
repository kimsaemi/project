# Report source notes

- Reporting question: `final_recommendation_mart_v2.csv`를 1조 프로젝트의 최종 데이터로 사용해도 되는가?
- Audience: product stakeholders (팀원·강사·발표 청중)
- Delivery mode: portable HTML
- Assessment standard: `Needs revision`

## Delivery blocker

The canonical portable report builder was invoked, but `node` is not installed or callable in this environment. Therefore `artifact.json` could not pass the packaged `validate_artifact` and browser/structural delivery command, and no `report.html` is claimed. The readable fallback is `검토보고서.md`; `artifact.json` is retained as an unvalidated report payload for a future environment with Node.js.

## Evidence inventory

1. `final_recommendation_mart_v2.csv`
2. `final_recommendation_mart.csv`
3. `final_admdong_table_설명포함_1.csv`
4. `run_comprehensive_analysis.py`
5. `DATASET_SPECIFICATION.md`
6. `COMPREHENSIVE_ANALYSIS_REPORT.md`
7. `0826_팀회의_근거메모.md`
8. `프로젝트_진행현황_작성본_20260827.md`
9. `02_commute_to_3centers.csv`
10. `03_price_stability_by_dong.csv`
11. `05_candidate_master.csv`
12. `validation_evidence.json`

## Checks performed

- Row and column count, key uniqueness, exact duplicates, null rates, categorical coverage, and numeric ranges
- Recalculation of every price, commute, component score, and recommendation-score formula stored in v2
- Column-level comparison with `final_recommendation_mart.csv`
- Administrative-dong key reconciliation with `final_admdong_table_설명포함_1.csv`
- Commute-time reconciliation against the 8/27 agreed hub pipeline
- Price-defense coverage, source legal-dong coverage, and missing required reliability flags
- Exact-name diagnostic comparison of v2's estimated 59㎡ price against 2026 actual 59㎡ median prices
- Meeting-decision alignment for grain, metrics, weights, confidence fields, and intended question
- Reproducibility review of the available generation code and data dictionary

## Report structure mapping

- Title: exact report title block
- Executive summary: visible `Executive Summary` block immediately after title
- Key findings with evidence: validation, price, commute, and meeting-alignment sections plus four audit tables
- Recommended next steps: mandatory-fix section and target-schema table
- Further questions: explicit open-question section
- Caveats and assumptions: explicit final section

## Visualization decision

No chart was used. This is a pass/fail data-governance review where exact counts, rates, definitions, and side-by-side mappings are more decision-useful than a plotted trend. Small audit tables preserve the evidence without implying temporal or causal structure.

## Reproducibility note

The local `python`, `py`, and `python3` commands resolve only to Microsoft Store stubs and cannot execute. A Jupyter notebook could therefore not be executed or truthfully handed off as validated. The reproducible companion is `validate_final_recommendation_mart_v2.ps1`, which completed successfully and generated `validation_evidence.json`.

## Important interpretation caveats

- The 59㎡ price comparison uses only 67 rows where the administrative-dong name and legal-dong name match exactly within the same district. It compares different spatial grains and partially different time windows, so it is a diagnostic of budget-filter risk, not a full replacement price table.
- The 8/27 commute file is also a proxy for weekday morning movement because the OD data does not contain a confirmed trip-purpose field.
- The review does not certify the alternative `05_candidate_master.csv` as final-ready; that file still needs sensitivity analysis, 1:N mapping disclosure, and explicit treatment of missing or untested price-defense rows.
