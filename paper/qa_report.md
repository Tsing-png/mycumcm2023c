# QA Report — Final Submission Audit

**Profile**: submission
**Date**: 2026-08-05
**Pre-audits**: consistency ✅, completeness ✅

---

## 1. Workflow Integrity

| Gate | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| G1 (framed) | ✅ | ✅ | ✅ | ✅ |
| G2 (screened) | ✅ | ✅ | ✅ | N/A |
| G2.5 (chosen) | ✅ HUMAN | ✅ HUMAN | ✅ HUMAN | N/A |
| G3 (coded+reviewed) | ✅ | ✅ | ✅ | N/A |
| G4 (results verified) | ✅ | ✅ | ✅ | N/A |
| G5 (paper ready) | ⏳ paper sections pending | ⏳ | ⏳ | ⏳ |

**Human judgments**: 10 decisions in `planning/framing_decisions.jsonl` — method choices, framing, assumptions. All traceable.

**Scope compliance**: M1+M2 implemented for all Q. M3 fallbacks (Q2, Q3) not activated — correctly not implemented.

**Verdict**: ✅ PASS (G5 expected next-step)

## 2. Evidence Integrity

**Fabrication check**: All 14 frozen claims resolved to on-disk sources:
- 13 from `run_summary.json` (machine-generated during code execution)
- 1 from robustness script output
- 0 from hand-edited sources ✅

**Provenance**: Every numerical claim in solution package has `source_file` + `locator` in frozen_numbers.json. Writer can verify independently.

**Uncertainty visibility**: 
- k sensitivity ranges reported alongside point estimates
- Elasticity estimation R² documented (0.011–0.144 — transparent about low explanatory power)
- Cross-year correlation instability in Q1 explained (not hidden)
- Q_max bound noted as non-binding (transparent about model behavior)

**Verdict**: ✅ PASS

## 3. Method Quality

| Criterion | Evidence |
|---|---|
| Baseline usable | M2 produces directly comparable profit figures (same formula, same data, same evaluation period) |
| Assumptions coherent | 20 assumptions in model_assumptions.md — 6 human-confirmed types, all sourced |
| Constraints enforced | Q_max bound, ≥2.5kg minimum, [27,33] range — all in code |
| Output not degenerate | All markup std > 0.01, all profit diverse across categories/SKUs |
| Fallback triggers defined | Q2: Prophet RMSE > ARIMA for 3+ cats; Q3: any γ < 50% — both evaluated and not triggered |
| Robustness covers key risks | k, elasticity, loss rate, filter threshold, Q_max bound |

**Verdict**: ✅ PASS

## 4. Paper Quality

| Criterion | Status |
|---|---|
| Problem-method-results aligned | ✅ Final method explanations cover problem→method→results pipeline |
| Claims proportional to evidence | ✅ All claims cite run_summary or robustness summary |
| Method rationale human-owned | ✅ decision_ids in all method choices |
| Physical interpretation | ⏳ To be provided by human in paper drafting |
| Limitations documented | ✅ Each final method explanation has limitations section |

**Verdict**: ⏳ PASS (physical interpretation pending human writer)

## 5. Presentation

| Criterion | Status |
|---|---|
| Type 3 figures exist | ✅ 7 paper figures generated (150 DPI, Chinese fonts, academic sizing) |
| Type 2 figures exist | ✅ 4 comparison figures |
| Type 1 diagnostics excluded from paper | ✅ 6 diagnostic figures correctly classified in figure-table-plan |
| Tables sourced | ✅ All CSV tables exist with correct rows/columns |
| References (refs.bib) | ⚠️ MISSING — next skill: reference-manager |
| AI-use disclosure | ⚠️ To be drafted per contest rules |
| Figure render verification | ⚠️ Not yet run — next skill: math-figure-generator render checks |

**Verdict**: ⚠️ CONDITIONAL — refs.bib and render checks pending

---

## Verdict: PASSED (with 3 next-step items)

| # | Blocker | Owner |
|---|---|---|
| 1 | Paper sections not written | `paper-section-writer` |
| 2 | refs.bib not created | `reference-manager` |
| 3 | Figure render verification not run | `math-figure-generator` render checks |

All G1-G4 artifacts pass workflow, evidence, and method quality checks. Paper-stage items are the expected remaining work. Ready for paper drafting handoff.
