---
trigger: always_on
glob: "**/*.{ipynb,py,md}"
description: "Rules for data modeling and machine learning model selection and implementation."
---

# Rule: NYC Taxi Data Modeling & Machine Learning Strategy

This rule defines the rationale behind the chosen architectural and analytical models for the NYC Taxi project. The Agent MUST adhere to these choices and understand the reasoning when proposing changes or implementing new features.

## 1. Data Architecture: Hybrid Multi-Fact Schema

**Decision:** The analytical data is structured using a **Hybrid Multi-Fact Schema**. Instead of a single fact table, we utilize 4 specialized virtual Fact Views (`v_FACT_YELLOW_TRIPS`, `v_FACT_GREEN_TRIPS`, `v_FACT_HVFHS_TRIPS`, `v_FACT_FHV_TRIPS`) and 1 lightweight overview view (`v_MARKET_OVERVIEW`). These are connected to shared `DIM_` tables.

**Rationale:**

- **Data Integrity (No Sparse Data):** By separating the fact tables by service type, we avoid forcing incompatible schemas together. For example, Uber/Lyft have `request_datetime` and `driver_pay`, while traditional taxis have `RatecodeID`. Keeping them separate ensures 100% clean, native metrics without relying on `0.0` or `NULL` padding.
- **Forecasting Accuracy:** Time-series models (like Prophet) require clean, independent signals. A unified table with missing/imputed data creates noise. Independent tables provide perfect signal separation for predicting service-specific growth.
- **DuckDB Optimization:** DuckDB processes specific tables (like `v_FACT_HVFHS_TRIPS`) significantly faster than parsing complex `CASE WHEN` and `COALESCE` statements in a unified 3-billion-row view.
- **Unified Overview Option:** For general "Total Market" dashboards, the `v_MARKET_OVERVIEW` provides a minimal intersection (Trip ID, Time, Location) without any financial data, allowing rapid aggregation.

## 2. Business Forecasting: Prophet Model

**Decision:** Use **Prophet** (Meta) for time-series forecasting of market growth and trip volume.

**Rationale:**

- **Strong Seasonality:** NYC taxi demand is heavily influenced by daily (rush hour), weekly (weekends), and yearly (holidays) cycles. Prophet is specifically designed to handle these additive effects automatically.
- **Missing Data & Outliers:** Taxi data often has gaps or anomalies (e.g., lockdowns, weather events). Prophet is robust to these issues and doesn't require aggressive data interpolation.
- **Flexibility:** Allows easy integration of custom holidays or special events (e.g., New Year's Eve) as exogenous variables.

## 3. Anomaly Detection: Isolation Forest

**Decision:** Use **Isolation Forest** as the primary indicator for the Anomaly Warning System.

**Rationale:**

- **Unsupervised Learning:** Since we do not have a labeled "ground truth" for all historical anomalies, an unsupervised approach is necessary.
- **Efficiency:** Isolation Forest has a linear time complexity, making it suitable for processing the high-volume data in the `2026_Plus` test set.
- **Multidimensional:** It can detect anomalies across multiple features simultaneously (e.g., a trip with a low distance but an extremely high fare).

## 4. Agent Guidelines

- **Querying:** Always prefer `LEFT JOIN` from the Fact table to Dimension tables.
- **ML Implementation:** When implementing models in `Data.ipynb`, use the libraries specified above (`prophet`, `scikit-learn`).
- **Performance:** For heavy ML training, suggest materializing `VIEWs` into `TABLEs` in DuckDB to avoid re-calculating standardization logic multiple times.
