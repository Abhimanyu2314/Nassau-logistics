# Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

## Abstract
This project analyzes factory-to-customer shipment efficiency for Nassau Candy Distributor using order, shipment, geographic, product, cost, and profit data. The dashboard converts raw shipment records into route-level operational intelligence by calculating lead time, delay frequency, route efficiency score, geographic bottlenecks, and ship mode performance.

## Problem Statement
Nassau Candy Distributor needs better visibility into which factory-to-customer routes are efficient, which routes suffer delays, how performance varies by region/state/ship mode, and where operational bottlenecks exist. Without route-level intelligence, logistics decisions remain reactive rather than data-driven.

## Dataset Fields Used
The dashboard supports the submitted dataset fields: Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Country/Region, City, State/Province, Postal Code, Division, Region, Product ID, Product Name, Sales, Units, Gross Profit, and Cost.

## Methodology

### 1. Data Cleaning and Validation
- Date fields are converted into datetime format.
- Invalid rows with missing order/ship dates are removed.
- Negative lead times are removed.
- Geographic fields are standardized.
- Missing optional columns are handled through safe fallbacks for uploaded datasets.

### 2. Feature Engineering
- Shipping Lead Time = Ship Date − Order Date.
- Expected Lead Time is assigned based on Ship Mode.
- Delay flag is calculated when actual lead time exceeds expected lead time.
- Delay Days are calculated as actual lead time minus expected lead time.
- Product-to-factory mapping assigns each product to its source factory.
- Route is defined as Factory → Customer State/Province.

### 3. Route Aggregation
For each route, the dashboard calculates:
- Total shipments
- Average lead time
- Lead-time variability
- Delay frequency
- Sales
- Gross profit
- Cost
- Units
- Route efficiency score

### 4. Efficiency Benchmarking
Routes are ranked by a normalized efficiency score using lead time, delay rate, variability, and shipment volume. The dashboard identifies top 10 efficient routes and bottom 10 least efficient routes.

### 5. Geographic Bottleneck Analysis
State-level metrics are calculated to identify regions with high lead time, high delay rate, and high shipment volume. The Geographic Analysis page includes a US heatmap and factory-to-state route map.

### 6. Ship Mode Performance Analysis
The dashboard compares shipping methods by average lead time, delay rate, shipment volume, sales, and profit to support cost-time tradeoff analysis.

## Key Performance Indicators
- Shipping Lead Time
- Average Lead Time
- Route Volume
- Delay Frequency
- Route Efficiency Score
- Gross Profit
- Cost
- Threshold Breach Rate

## Dashboard Modules
- Route Efficiency Overview
- Geographic Shipping Map
- Ship Mode Comparison
- Route Drill-Down
- Data Quality Validation
- AI Prediction
- Executive Summary

## User Capabilities
- Date range filter
- Region selector
- State selector
- Ship mode selector
- Factory selector
- Lead-time threshold slider
- Dataset upload for CSV/XLSX
- Downloadable CSV outputs

## Recommendations
1. Prioritize operational review for bottom-ranked routes with high delay frequency and high shipment volume.
2. Use the geographic bottleneck map to identify states requiring carrier or route policy changes.
3. Compare Standard Class and expedited modes on high-risk lanes before changing service-level strategy.
4. Track the route efficiency score monthly to monitor improvement.
5. Use AI Prediction for scenario testing before dispatch planning.

## Conclusion
The project establishes a data-driven logistics intelligence platform for Nassau Candy Distributor. It transforms shipment data into actionable route-level insights that can help reduce delays, improve service reliability, identify geographic bottlenecks, and support executive decision-making.
