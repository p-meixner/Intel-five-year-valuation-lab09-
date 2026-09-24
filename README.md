# Intel five-year statement and valuation lab

Company: Intel Corporation (NASDAQ: INTC). Units: USD millions, except per-share values.

Run `python proforma.py` from this folder. The file uses only Python's standard library.

## Question and scope

What are five years of Intel's statements worth, built from assumptions I can defend, and how do I know the statements are right?

This is an illustrative FY2025-baseline forecast for 2026–2030, discounted to the end of FY2025. It is not a September 2026 valuation or Intel guidance. It uses the same linked-statement and cash-last approach as the ABG demonstration, with Intel-specific accounting. It supersedes neither the earlier research nor its watch-defer conclusion. The earlier explicit FCFF placeholders are replaced here by statement-derived FCFE.

## Historical source

[Intel FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm), statements pp. 60–63 and Note 6, was checked for this model. Revenue was 52,853; gross profit 18,375; R&D 13,774; MG&A 4,624. Opening cash is 14,265; investments 23,151; inventory 11,618; PP&E 105,414; total assets 211,429. Debt is 46,585; Intel equity 114,281; noncontrolling interests 12,079. Other assets and other liabilities are residual aggregates, 80,132 and 38,484. Depreciation was 10,757; receivables 3,839; cost of sales 34,478. Cash capex includes 14,646 investing and 3,026 financing-classified vendor payments. Year-end shares outstanding were 4,994 million, distinct from the annual weighted-average EPS denominator.

## Assumption set

These are explicit analyst judgments for this exercise, not verified management forecasts. Their numerical levels were selected by AI and require student review.

| Driver | Assumption | Status and reasoning |
|---|---|---|
| Revenue growth | 5% annually | Judgment: gradual recovery; no assumed acquisition growth |
| Gross margin | 36%, 38%, 40%, 42%, 44% | Judgment: manufacturing recovery; a major source of uncertainty |
| R&D / revenue | 25%, 24%, 23%, 22%, 21% | Judgment: operating leverage; absolute R&D still increases |
| MG&A / revenue | 4,624 / 52,853 each year | Historical ratio held flat by judgment |
| Depreciation / opening PP&E | 10,757 / 105,414 | Historical ratio held flat; depreciation is embedded in projected operating costs, not deducted again |
| Inventory days | 11,618 / 34,478 × 365 | Historical ratio held flat |
| Change in other working capital | Change in revenue × 3,839 / 52,853 | Receivables proxy; other operating balances held flat |
| Annual capex | 17,672 | Historical cash-spending baseline held flat; assume forecast payments equal additions, with no new vendor-financing timing differences |
| Separate impairment/restructuring | Zero | Normalization judgment; costs could recur |
| Tax | 21% of positive pretax income; zero on losses | Simplified proxy, without tax-loss carryforwards |
| Debt interest | 4% of opening debt | Analyst assumption, not a verified contractual weighted rate |
| Debt repayment | 2,499 annually | Scenario based on opening short-term debt; not Intel's maturity schedule |
| Buybacks / dividends | Zero | Preserve liquidity |
| Minimum cash | 5,000 | Judgment |
| Floor-plan debt | Zero | Dealer inventory lending is not carried over from ABG |
| New revolver capacity | Zero | No unverified capacity assumed |
| Liquidity funding | Sell existing short-term investments at carrying value as needed | Judgment; capped at available investments; refuse if minimum cash cannot be maintained |
| Cost of equity / terminal growth | 12% / 2.5% | Scenario assumptions, not an estimated CAPM return |
| Shares | 4,994 million, fixed | FY2025 endpoint; no subsequent issuance or future dilution modeled |
| NCI | Hold book balance flat; subtract 12,079 as valuation proxy | Material simplification; book value need not equal market value |

The three central operating judgments are growth, gross-margin recovery, and operating-cost efficiency. Capital spending and the discount rate also materially affect value. Fixed capex with rising depreciation implies declining net reinvestment; that assumption needs scrutiny for a manufacturer.

## Results

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 55,495.7 | 67,455.3 |
| Operating income | 1,249.3 | 9,613.2 |
| Net income, consolidated | -614.1 | 6,438.2 |
| FCFE before investment sales | -10,570.2 | -963.1 |
| Cash, year end | 5,000.0 | 5,000.0 |
| Assets minus liabilities minus total equity | 0.0 | 0.0 |

The five FCFE and normalized terminal value have a combined present value of **-13,351.23**. The terminal formula adds back the 2030 debt repayment, as in the lab, before applying 2.5% perpetual growth and discounting at 12%.

Add opening cash above the minimum plus short-term investments, **32,416.00**, and subtract the book-NCI proxy, **12,079.00**. This produces an illustrative Intel common-equity scenario value of **6,985.77**, or **$1.40 per share**. Liquidation proceeds are excluded from FCFE, so the liquid assets are counted once in this bridge. Debt is already reflected through interest and repayments; it is not subtracted again.

PV of terminal value divided by the final equity scenario value is **134.60%**. This is not a conventional positive component split: negative explicit cash flows and the asset/NCI bridge affect the denominator. Intel is not expected to reproduce ABG's $291.75 or approximately 80% terminal share.

## Verification and reflection

All five years pass balance-sheet, minimum-cash and revolver-limit checks. The engine caps investment sales at available holdings. Cash follows earnings, noncash adjustments, reinvestment, debt repayment and investment sales; it is never solved from the balance-sheet gap.

The break test replaced FY2026E closing cash with opening cash of 14,265 in memory. It correctly raised:

```text
ValueError: FY2026E: balance-sheet gap 9265.0
```

Actual cash fell by 9,265. Restoring opening cash overstates assets by that amount, so the gap is positive. ABG's -61.4 applies only to ABG. The saved Intel file retains the correct cash calculation. This was an AI-run break test, not a claimed partner exchange.

Balance checks prove internal accounting consistency, not economic accuracy. This simplified model omits separate stock-compensation/dilution, intangible amortization, investment returns, government incentives, partner distributions, OCI and changes in noncontrolling interests. It assigns forecast consolidated net income to Intel equity while holding NCI flat. Its book-NCI bridge is provisional. A decision-grade valuation needs those items reconciled and the forecasting assumptions supported. Subsequent 2026 developments from the saved research are outside this annual-baseline scenario.

My conclusion remains **watch-defer**: this exercise demonstrates a functioning statement engine, not a supported investment price target.

## Checkout

Upload this README and this folder's `proforma.py` to the Intel lab repository. Suggested name: `intel-five-year-valuation`. Submit the resulting GitHub file links; no repository has been created or uploaded by this local work.

AI use: AI retrieved prior research, verified annual filing inputs, selected labeled scenario assumptions, adapted the engine, ran it, performed the cash break test, and drafted this report. Student review and any actual partner discussion should be recorded separately.
