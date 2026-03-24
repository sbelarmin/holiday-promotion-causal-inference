# Methods Appendix  
## Identification Strategy and Estimation Framework

---

## Data Structure

- Panel data: 10,000 users × 35 days
- Observational campaign (non-random exposure)
- Exposure probability correlated with prior engagement and spend

Outcome: Margin dollars  
Treatment: Exposure during promo window

---

## Estimation Strategy

We estimated incremental impact using progressively stronger identification methods.

---

### 1. Naïve Post Comparison

Estimated difference in mean margin between exposed and unexposed users during the promo window.

Limitation:
- Biased due to baseline differences in engagement and spend.

---

### 2. Difference-in-Differences (DiD)

Model:
$$
Y_it = β (Treated_i × Post_t) + α_i + ε_it
$$
Controls for:
- Time-invariant user differences
- Common macro trends

Assumption:
Parallel trends between treated and control groups.

---

### 3. Two-Way Fixed Effects (TWFE)

Model:
$$
Y_it = β (Treated_i × Post_t) + α_i + γ_t + ε_it
$$
Controls for:
- User fixed effects (α_i)
- Date fixed effects (γ_t)

Clustered standard errors at the user level.

---

### 4. Propensity Score Weighting (IPW)

Estimated treatment probability using pre-period covariates:
- Prior 30-day spend
- Engagement score
- Tenure
- Pre-period margin

Computed stabilized inverse probability weights.

Finding:
- Propensity scores clustered near 1.0
- Severe overlap failure
- Covariate balance not materially improved

Conclusion:
IPW not credible due to positivity violation.

---

### 5. Weighted DiD

Applied IPW weights within DiD framework.

Estimate nearly identical to unweighted DiD.

Indicates:
Observable selection not driving remaining bias.

---

### 6. Event Study (Dynamic DiD)

Estimated event-time treatment effects:
$$
Y_it = Σ_k β_k (1[event_time = k] × Treated_i) + α_i + γ_t + ε_it
$$
Findings:
- Pre-period coefficients statistically insignificant.
- No strong evidence of parallel trend violation.
- Immediate and sustained negative margin effect post-promo.  
![Event Study: Dynamic Treatment Effects on Margin Dollars](../figures/event_study.png){width=100%}
---

## Identification Assumptions

1. Parallel trends (supported by event study).
2. No time-varying unobserved confounders.
3. Stable unit treatment value (no spillovers).
4. Positivity (violated for IPW).

---

## Comparison to Synthetic Ground Truth

True ATT: -6.54  
Estimated DiD: -4.60  

Residual bias likely driven by:
- Treatment effect heterogeneity
- Time-varying targeting intensity
- Structural model assumptions in data-generating process

---

## Conclusion

Difference-in-Differences with fixed effects provides the most credible estimate under observed conditions.

IPW is not reliable due to lack of overlap.

Event study diagnostics support causal interpretation of DiD results.