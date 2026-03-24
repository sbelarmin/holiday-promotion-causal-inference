---
title: "Promo Causal Evaluation"
author: "Scott Belarmino"
date: "March 2026"
---

## Causal Evaluation Summary: 40% Promotion

### Objective

Estimate the incremental margin impact of a 40% promotional campaign using observational data where treatment was targeted (not randomized).

The primary outcome is **margin dollars**.  
The secondary outcome is **revenue**.

---

## Causal Ladder Summary

We estimate the treatment effect using progressively stronger identification strategies, moving from simple observational comparisons toward designs that better address selection bias.

---

### 1. Naïve Post-Period Comparison

**Method:** Compare exposed vs. non-exposed users during the promo window.

**Result:** -5.61

**Issue:** Estimates are biased due to non-random treatment assignment.  
Exposed users had higher prior spend and engagement before the promotion.

---

### 2. Difference-in-Differences (DiD)

**Method:** Compare pre-to-post outcome changes for treated versus control users.

**Result:** -4.60

**Interpretation:** Adjusts for time-invariant differences between groups.

This approach removes baseline selection bias but relies on the **parallel trends assumption**.

---

### 3. Two-Way Fixed Effects (TWFE)

**Method:** Difference-in-Differences with user and date fixed effects.

**Result:** -4.60

**Interpretation:** Controls for:

- Time-invariant user heterogeneity
- Daily macro shocks affecting all users

The estimate remains unchanged relative to the basic DiD specification.

---

### 4. Propensity Score Weighting (IPW)

**Goal:** Rebalance treated and control users based on observable characteristics.

**Findings:**

- Propensity scores clustered near **1.0**
- Severe overlap failure between treated and control groups
- Covariate balance did not improve after weighting

**Conclusion:** IPW estimates are not credible due to a lack of **common support**.

---

### 5. Weighted DiD

**Method:** Difference-in-Differences with inverse probability weights.

**Result:** -4.59

**Interpretation:** Nearly identical to the unweighted DiD estimate.

Weighting does not materially alter results because overlap between groups is poor.

---

### 6. Event Study (Two-Way Fixed Effects)

**Purpose:** Evaluate the parallel trends assumption and examine dynamic treatment effects.

**Findings:**

- Pre-period coefficients are small and statistically insignificant
- No strong pre-treatment trend violations detected
- Margin drops sharply at the start of the promotion (evt_0 ≈ -7.9)
- Post-period effects remain consistently negative (approximately -5 to -6)

**Conclusion:** Event study diagnostics provide no strong evidence of violations of the parallel trends assumption.

---

### Event Study Diagnostics

![Event Study: Dynamic Treatment Effects on Margin Dollars](../figures/event_study.png){width=100%}

Pre-treatment coefficients are centered near zero and statistically insignificant, providing visual support for the parallel trends assumption.

---

## Comparison to Ground Truth (Synthetic Data)

| Estimator    | Estimate |
| ------------ | -------- |
| True ATT     | -6.54    |
| Naïve        | -5.61    |
| DiD          | -4.60    |
| TWFE         | -4.60    |
| Weighted DiD | -4.59    |

Remaining bias relative to the true ATT likely reflects:

- Treatment effect heterogeneity
- Time-varying structural differences
- Imperfect identification in observational settings

---

## Business Interpretation

The 40% promotion:

- Increased unit sales
- Reduced margins significantly
- Produced an incremental margin impact of approximately **-$4.6 per exposed user-day**

Results remain consistent across multiple identification strategies.

Event study diagnostics support the credibility of the Difference-in-Differences framework.

---

## Key Takeaways

1. Selection bias arises when marketing targets high-value users.
2. Difference-in-Differences meaningfully reduces bias relative to naïve comparisons.
3. Propensity score weighting fails when overlap assumptions are violated.
4. Event study diagnostics support the causal interpretation of DiD.
5. Strong targeting structures limit the effectiveness of reweighting approaches.

---

## Final Assessment

Under standard Difference-in-Differences assumptions, the promotion appears economically destructive in the short term.

Long-term value effects (customer acquisition, retention, or lifetime value) would be required to justify the observed margin loss.