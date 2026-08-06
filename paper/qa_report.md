# QA Report — Final Submission Audit

**Profile**: submission | **Date**: 2026-08-05 | **Re-run**: post paper-polish

---

## 1. Workflow Integrity

| Gate | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| G1 (framed) | ✅ | ✅ | ✅ | ✅ |
| G2 (screened) | ✅ | ✅ | ✅ | N/A |
| G2.5 (human choice) | ✅ | ✅ | ✅ | N/A |
| G3 (coded+reviewed) | ✅ PASSED | ✅ PASSED | ✅ PASSED | N/A |
| G4 (results+frozen) | ✅ | ✅ | ✅ | ✅ |
| G5 (paper written) | ✅ | ✅ | ✅ | ✅ |
| G6 (audited) | ✅ | ✅ | ✅ | ✅ |

10 human decisions in `planning/framing_decisions.jsonl`. All gates passed per manifest. ✅

## 2. Evidence Integrity

- **Fabrication check**: All 14 frozen claims trace to machine-generated `run_summary.json`. 0 hand-edited values.
- **Paper numbers**: 10/10 claims verified in cross-media consistency audit. ✅
- **Uncertainty visible**: k sensitivity ranges, elasticity R², cross-year correlation instability, Q_max non-binding — all transparently reported. ✅
- **No fabricated references**: All 17 refs.bib entries trace to PDFs on disk or standard textbooks. ✅

## 3. Method Quality

| Criterion | Evidence |
|---|---|
| Usable baseline | M2 ARIMA (Q2) and fixed markup (Q3) produce directly comparable profit on same data/cost function |
| Assumptions coherent | 7 assumptions in paper; necessary/simplifying types confirmed by human |
| Constraints enforced | $Q_{\max}$, $d_{\min}=2.5$, $N\in[27,33]$ — all in code and paper |
| Output not degenerate | Markup std 0.082 (Q2), 0.311 (Q3); profit varies 4× across categories |
| Fallback evaluated | Q2 M3 (LSTM) and Q3 M3 (quota) not triggered — correctly absent from paper |
| Robustness covers key risks | $k$, elasticity, loss rate, filter threshold — all tested |

✅

## 4. Paper Quality

| Criterion | Status |
|---|---|
| Problem→method→results coherence | ✅ Each Q section follows problem→method→result→contrast structure |
| Claims proportional to evidence | ✅ "优化" used only in grid-search context; k sensitivity reported as interval |
| AI-味 cleared | ✅ "显著的实际意义""明确的业务含义" removed during polish |
| Overclaim downgrade applied | ✅ "所有结论" → "关键结论" in abstract |
| Limitations documented | ✅ 7 limitations in section 08 |
| Baseline comparison present | ✅ Q2 +304%, Q3 +185% |
| M1 advantage decomposed | ✅ Q2: better forecasting + markup optimization (two components identified) |

✅

## 5. Presentation

| Criterion | Status |
|---|---|
| 5 Type 3 figures, 300dpi | ✅ paper/figures/ — all exist |
| 1 Type 3 table (Q2策略表) | ✅ inline in section 05 |
| Figure references in order | ✅ Fig1→Fig5 sequential in text |
| refs.bib valid syntax | ✅ 17 entries, all have author/title/year |
| Reference audit | ✅ paper/reference_audit.md — 0 fabrication risks |
| Polish change log | ✅ paper/polish_changes.md |
| Chinese academic style | ✅ 连贯自然表达，避免空泛套话和AI味表述 |

✅

---

## Final Verdict: PASSED

All five audit dimensions evaluated. 0 blocking issues. Consistency and completeness audits also PASSED.

**Paper is ready for final assembly and submission.**
