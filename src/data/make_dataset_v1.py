import numpy as np
import pandas as pd


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def generate_panel_synth(
    n_users: int = 10_000,
    n_pre_days: int = 30,
    n_promo_days: int = 5,
    seed: int = 42,
    promo_discount: float = 0.40,
) -> pd.DataFrame:
    """
    Research-grade synthetic panel dataset for Project Google.
    - 10k users by default
    - pre-period + promo-period daily rows
    - treatment = exposed to promo banner during promo period
    - outcomes include units, net_revenue, margin_dollars, margin_rate
    - ground truth includes baseline_units + true_treatment_effect + counterfactual financials
    """

    rng = np.random.default_rng(seed)

    # -----------------------------
    # 1) Dates / time features
    # -----------------------------
    # Use a synthetic date range. (Exact calendar dates don't matter for the DGP.)
    # Pre: day 0..n_pre_days-1, Promo: next n_promo_days
    total_days = n_pre_days + n_promo_days
    dates = pd.date_range("2025-11-01", periods=total_days, freq="D")
    post = np.zeros(total_days, dtype=int)
    post[n_pre_days:] = 1
    dow = np.array([d.weekday() for d in dates], dtype=int)  # 0=Mon

    # Holiday uplift curve (shared across users)
    # modest ramp + promo bump
    t = np.arange(total_days)
    ramp = 0.10 * (t / max(total_days - 1, 1))  # up to +10%
    promo_bump = np.where(post == 1, 0.25, 0.0)  # +25% organic uplift in promo window
    seasonality_effect = 1.0 + ramp + promo_bump  # multiplier

    # -----------------------------
    # 2) User covariates (one-time)
    # -----------------------------
    regions = np.array(["West", "Midwest", "South", "Northeast"])
    devices = np.array(["Mobile", "Desktop", "Tablet"])
    sources = np.array(["Direct", "Search", "Email", "Social", "Affiliates"])
    segments = np.array(["New", "Returning", "Loyal", "DealSeeker", "Premium"])

    region = rng.choice(regions, size=n_users, p=[0.28, 0.22, 0.30, 0.20])
    device_type = rng.choice(devices, size=n_users, p=[0.62, 0.33, 0.05])
    traffic_source = rng.choice(sources, size=n_users, p=[0.35, 0.28, 0.15, 0.12, 0.10])
    customer_segment = rng.choice(segments, size=n_users, p=[0.18, 0.34, 0.20, 0.18, 0.10])

    tenure_days = rng.lognormal(mean=np.log(180), sigma=0.7, size=n_users).astype(int)
    tenure_days = np.clip(tenure_days, 1, 5000)

    engagement_score = rng.normal(loc=0.0, scale=1.0, size=n_users)
    engagement_score = np.clip(engagement_score, -3.0, 3.0)

    prior_30d_spend = rng.lognormal(mean=np.log(45), sigma=1.0, size=n_users)
    prior_30d_spend = np.clip(prior_30d_spend, 0.0, 600.0)

    # -----------------------------
    # 3) Pricing + cost structure (per user)
    # -----------------------------
    # Segment-driven list prices
    seg_price_mu = {
        "New": 22,
        "Returning": 28,
        "Loyal": 30,
        "DealSeeker": 20,
        "Premium": 40,
    }
    base_price = np.array([seg_price_mu[s] for s in customer_segment], dtype=float)
    list_price = base_price * rng.lognormal(mean=0.0, sigma=0.18, size=n_users)
    list_price = np.clip(list_price, 8.0, 120.0)

    # Cost ratio varies by segment (premium tends to have better gross margin)
    seg_cost_ratio_mu = {
        "New": 0.68,
        "Returning": 0.64,
        "Loyal": 0.60,
        "DealSeeker": 0.72,
        "Premium": 0.52,
    }
    cost_ratio = np.array([seg_cost_ratio_mu[s] for s in customer_segment], dtype=float)
    cost_ratio = cost_ratio + rng.normal(0.0, 0.04, size=n_users)
    cost_ratio = np.clip(cost_ratio, 0.35, 0.85)
    unit_cost = list_price * cost_ratio

    # -----------------------------
    # 4) Treated group (propensity segment)
    # -----------------------------
    # Flag users more likely to be targeted (e.g., Loyal + Email, high engagement/spend)
    treated_group = (
        (customer_segment == "Loyal")
        | ((traffic_source == "Email") & (engagement_score > 0.2))
        | (prior_30d_spend > 120)
    ).astype(int)

    # -----------------------------
    # 5) Demand model: baseline units (counterfactual)
    # -----------------------------
    # Build user-level log-rate, then apply day-level seasonality in log-space
    seg_demand = {
        "New": -0.35,
        "Returning": -0.15,
        "Loyal": 0.05,
        "DealSeeker": -0.05,
        "Premium": -0.20,
    }
    src_demand = {"Direct": 0.10, "Search": 0.05, "Email": 0.12, "Social": -0.02, "Affiliates": 0.00}
    dev_demand = {"Mobile": -0.03, "Desktop": 0.03, "Tablet": -0.01}

    seg_term = np.array([seg_demand[s] for s in customer_segment], dtype=float)
    src_term = np.array([src_demand[s] for s in traffic_source], dtype=float)
    dev_term = np.array([dev_demand[d] for d in device_type], dtype=float)

    # user baseline intensity
    user_log_lambda = (
        -2.25
        + 0.30 * engagement_score
        + 0.22 * np.log1p(prior_30d_spend)
        + 0.10 * np.log1p(tenure_days)
        + seg_term
        + src_term
        + dev_term
    )

    # Negative binomial via Gamma-Poisson mixture
    # Larger k => less overdispersion. Choose moderate.
    k_disp = 1.8

    # Expand to user-day
    user_ids = np.arange(n_users)
    user_id_rep = np.repeat(user_ids, total_days)
    date_rep = np.tile(dates.values, n_users)
    post_rep = np.tile(post, n_users)
    dow_rep = np.tile(dow, n_users)
    season_rep = np.tile(seasonality_effect, n_users)

    # baseline mean per user-day
    base_mean = np.exp(np.repeat(user_log_lambda, total_days)) * season_rep

    # Gamma-Poisson mixture draw:
    # lambda_draw ~ Gamma(shape=k, scale=mean/k); units ~ Poisson(lambda_draw)
    lam_draw = rng.gamma(shape=k_disp, scale=base_mean / k_disp)
    baseline_units = rng.poisson(lam_draw).astype(int)

    # -----------------------------
    # 6) Exposure model (treatment assignment during promo)
    # -----------------------------
    # Only allow exposure during promo window for clean interpretation
    treated_group_rep = np.repeat(treated_group, total_days)
    engagement_rep = np.repeat(engagement_score, total_days)
    prior_spend_rep = np.repeat(prior_30d_spend, total_days)
    tenure_rep = np.repeat(tenure_days, total_days)

    seg_is_dealseeker = (np.repeat(customer_segment, total_days) == "DealSeeker").astype(int)
    src_is_email = (np.repeat(traffic_source, total_days) == "Email").astype(int)

    exposure_score = (
        -1.1
        + 0.55 * treated_group_rep
        + 0.25 * engagement_rep
        + 0.20 * np.log1p(prior_spend_rep)
        + 0.05 * np.log1p(tenure_rep)
        + 0.20 * src_is_email
        + 0.10 * seg_is_dealseeker
        + 0.85 * post_rep
    )
    p_expose = _sigmoid(exposure_score)

    exposed = rng.binomial(1, p_expose).astype(int)
    exposed = exposed * post_rep  # force 0 during pre-period

    # -----------------------------
    # 7) Treatment effect on units (heterogeneous promo lift)
    # -----------------------------
    # "Price sensitivity" proxy: deal seekers + lower prior spend are more sensitive
    prior_scaled = (np.log1p(prior_spend_rep) - np.log1p(np.median(prior_30d_spend))) / 1.0
    price_sensitivity = 0.35 * seg_is_dealseeker - 0.10 * prior_scaled

    # expected lift in units (mean of Poisson) during promo for exposed
    lift_mean = (
        exposed
        * (0.18 + 0.22 * price_sensitivity + 0.06 * np.maximum(engagement_rep, 0))
    )
    lift_mean = np.clip(lift_mean, 0.0, 1.25)  # cap

    true_treatment_effect = rng.poisson(lift_mean).astype(int)

    units = baseline_units + true_treatment_effect

    # -----------------------------
    # 8) Financials (revenue/cost/margin)
    # -----------------------------
    list_price_rep = np.repeat(list_price, total_days)
    unit_cost_rep = np.repeat(unit_cost, total_days)

    discount_pct = np.where((post_rep == 1) & (exposed == 1), promo_discount, 0.0)

    gross_sales_pre_discount = units * list_price_rep
    net_revenue = units * list_price_rep * (1.0 - discount_pct)

    total_cost = units * unit_cost_rep
    margin_dollars = net_revenue - total_cost
    margin_rate = np.where(net_revenue > 0, margin_dollars / net_revenue, 0.0)

    # -----------------------------
    # 9) Counterfactual financials (no promo)
    # -----------------------------
    counterfactual_units = baseline_units
    counterfactual_revenue = counterfactual_units * list_price_rep  # no discount
    counterfactual_margin_dollars = counterfactual_revenue - (counterfactual_units * unit_cost_rep)

    # -----------------------------
    # 10) Build DataFrame
    # -----------------------------
    df = pd.DataFrame(
        {
            "user_id": user_id_rep,
            "date": pd.to_datetime(date_rep),
            "dow": dow_rep,
            "post": post_rep,
            "exposed": exposed,
            "treated_group": treated_group_rep,
            "discount_pct": discount_pct,

            "region": np.repeat(region, total_days),
            "device_type": np.repeat(device_type, total_days),
            "traffic_source": np.repeat(traffic_source, total_days),
            "customer_segment": np.repeat(customer_segment, total_days),
            "tenure_days": tenure_rep,
            "prior_30d_spend": prior_spend_rep,
            "engagement_score": engagement_rep,

            "seasonality_effect": season_rep,
            "baseline_units": baseline_units,
            "true_treatment_effect": true_treatment_effect,
            "units": units,

            "list_price": list_price_rep,
            "gross_sales_pre_discount": gross_sales_pre_discount,
            "net_revenue": net_revenue,

            "unit_cost": unit_cost_rep,
            "total_cost": total_cost,
            "margin_dollars": margin_dollars,
            "margin_rate": margin_rate,

            "counterfactual_units": counterfactual_units,
            "counterfactual_revenue": counterfactual_revenue,
            "counterfactual_margin_dollars": counterfactual_margin_dollars,
        }
    )

    return df


def quick_sanity_checks(df: pd.DataFrame) -> dict:
    """
    Returns a small dictionary of sanity metrics you can print/log.
    """
    promo = df[df["post"] == 1]
    pre = df[df["post"] == 0]

    out = {
        "rows": len(df),
        "unique_users": df["user_id"].nunique(),
        "promo_exposure_rate": float(promo["exposed"].mean()),
        "pre_exposure_rate": float(pre["exposed"].mean()),
        "avg_units_pre": float(pre["units"].mean()),
        "avg_units_promo_exposed": float(promo.loc[promo["exposed"] == 1, "units"].mean()),
        "avg_units_promo_unexposed": float(promo.loc[promo["exposed"] == 0, "units"].mean()),
        "avg_margin_rate_pre": float(pre.loc[pre["net_revenue"] > 0, "margin_rate"].mean()),
        "avg_margin_rate_promo_exposed": float(promo.loc[(promo["exposed"] == 1) & (promo["net_revenue"] > 0), "margin_rate"].mean()),
        "avg_margin_rate_promo_unexposed": float(promo.loc[(promo["exposed"] == 0) & (promo["net_revenue"] > 0), "margin_rate"].mean()),
    }

    # selection bias check
    out["avg_prior_spend_promo_exposed"] = float(promo.loc[promo["exposed"] == 1, "prior_30d_spend"].mean())
    out["avg_prior_spend_promo_unexposed"] = float(promo.loc[promo["exposed"] == 0, "prior_30d_spend"].mean())

    return out


if __name__ == "__main__":
    df = generate_panel_synth(n_users=10_000, n_pre_days=30, n_promo_days=5, seed=42)
    metrics = quick_sanity_checks(df)
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # Save output
    df.to_csv("data/raw/holiday_promotion_panel.csv", index=False)
    print("Saved: holiday_promotion_panel.csv")