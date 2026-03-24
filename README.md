# Promo Causal Inference Project  
Estimating the true impact of a targeted 40% promotion on margin

---

## TL;DR

- The promotion **increases sales but destroys margin**
- Estimated causal impact: **~-$4.6 per exposed user-day**
- Results are **robust across methods (DiD, TWFE)**
- **Recommendation:**  
  → Do not scale without clear evidence of long-term value (LTV)

---

## Business Problem

A 40% promotion was deployed using **targeted (non-randomized) exposure**.

The key question:
> What is the *incremental* impact of the promotion on margin, accounting for selection bias?

---

## Approach

Causal inference ladder from biased → credible estimates:

- **Naïve comparison**
  - Biased (treated users already higher value)

- **Difference-in-Differences (DiD)**
  - Primary estimate; removes baseline bias

- **Two-Way Fixed Effects (TWFE)**
  - Adds user + time controls; confirms stability

- **Propensity Weighting (IPW)**
  - Attempted rebalancing; fails due to poor overlap

- **Event Study**
  - Validates assumptions; shows persistent negative impact

---

## Results

| Method       | Estimate |
| ------------ | -------- |
| Naïve        | -5.61    |
| DiD          | -4.60    |
| TWFE         | -4.60    |
| Weighted DiD | -4.59    |
| True ATT*    | -6.54    |

\*Synthetic benchmark for validation

---

## Key Insights

- **Selection bias is material**  
  Targeting high-value users inflates naïve performance

- **DiD provides a stable, credible estimate**  
  Consistent across specifications

- **Overlap failure limits reweighting methods**  
  IPW not reliable in highly targeted systems

- **Diagnostics support identification**  
  No meaningful pre-trends in event study

---

## Business Interpretation

- Promotion increases **units and engagement**
- But produces **negative incremental margin**

### Decision Framework

- If **short-term profitability is the goal** → Do not launch  
- If **customer acquisition / LTV is the goal** → Requires further validation

---

## What This Demonstrates

- Translating business questions into causal estimands  
- Diagnosing and correcting selection bias  
- Applying production-relevant methods (DiD, TWFE, IPW, event study)  
- Communicating results in decision-ready terms  

---

## Limitations

- Observational setting → residual bias vs. true effect  
- Strong targeting → limited overlap  
- Long-term effects (LTV, retention) not modeled  

---

## Author

Scott Belarmino  
Data Scientist | Decision Science | Causal Inference  

---

## Notes

This project was independently developed as part of a data science portfolio.  

Large Language Models (LLMs) were used to assist with code organization, documentation clarity, and readability. All modeling, analysis, and interpretations were designed and validated by the author.