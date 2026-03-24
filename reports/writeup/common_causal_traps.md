# Common Causal Inference Traps in Product Analytics

When evaluating whether a feature, campaign, or product change caused an outcome, several common pitfalls can lead to incorrect conclusions. Recognizing these traps is a core skill for senior data scientists.

---

# 1. Selection Bias (Self-Selection)

This is one of the most common causal inference traps.

Users who **choose to adopt a product or feature** are often fundamentally different from users who do not.

### Example

A company launches a **premium membership program**.

Observed data:

| Group           | Avg Orders     |
| --------------- | -------------- |
| Premium Members | 8 orders/month |
| Non-Members     | 3 orders/month |

Naive conclusion:

> Premium membership causes users to order more.

Reality:

People who subscribe may already be:

- heavier users
- more price sensitive
- more loyal customers

In this case, **user behavior causes subscription**, not the other way around.

---

# 2. Pre/Post Illusion (Time Confounding)

Metrics often change naturally over time due to external factors.

### Example

A company launches a **new recommendation algorithm**.

| Period        | Orders  |
| ------------- | ------- |
| Before Launch | 100,000 |
| After Launch  | 110,000 |

Naive conclusion:

> The recommendation system increased orders by 10%.

Possible reality:

- overall demand increased
- seasonal effects
- macroeconomic shifts
- platform growth

Without a proper control group, it is difficult to attribute the increase to the feature.

---

# 3. Concurrent Changes (Multiple Interventions)

Companies frequently launch **multiple initiatives simultaneously**.

Example:

During the same period:

- a new delivery feature launches
- a marketing campaign begins
- pricing changes are introduced

If orders increase, it becomes unclear which change caused the effect.

Example question:

> Did same-day delivery increase orders, or did the **$10 promotional coupon** drive the change?

---

# 4. Regression to the Mean

Extreme values tend to move toward the average over time.

### Example

A company identifies the **lowest-performing stores** and introduces a performance improvement program.

Next quarter, these stores improve.

Naive conclusion:

> The improvement program worked.

Possible reality:

Poor performers often improve naturally due to normal variation, even without intervention.

This effect commonly appears in:

- churn reduction programs
- performance coaching
- targeted interventions on struggling segments

---

# 5. Survivorship Bias

Analysis may only include **units that remain visible**, ignoring those that failed or disappeared.

### Example

A platform analyzes **top-performing sellers** and observes that they:

- respond quickly to customer messages
- upload many product photos

Naive conclusion:

> Uploading more photos causes higher sales.

Possible reality:

Successful sellers remain active on the platform, while unsuccessful sellers exit. Observing only survivors can distort causal interpretation.

---

# A Practical Mental Checklist for Data Scientists

When a stakeholder claims that a feature or intervention caused a metric change, experienced data scientists typically check for the following:

1. **Selection Bias** – Are treated users systematically different from untreated users?
2. **Time Confounding** – Could the change be explained by broader trends or seasonality?
3. **Concurrent Interventions** – Were other initiatives launched at the same time?
4. **Regression to the Mean** – Are extreme observations naturally reverting to average?
5. **Survivorship Bias** – Are we only observing successful cases?

Recognizing these patterns helps prevent incorrect causal conclusions and leads to more reliable experimental design and analysis.