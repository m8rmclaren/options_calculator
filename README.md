# options_calculator
Find maximum covered/secured returns, relies on TD Ameritrade API

General strategy:

Find stocks with more upside potential than downside by

- Analyzing capital structure
  - low debt compared to equity/assets
  - assuming floor of stock value is implied by cash reported
  - assuming that underlying volatility decreases as share price approaches positive cash balance
- Analyzing valuation
  - Measure valuation by considering relative cash flow (value / earnings before interest (EV/EVIT))
  - Analyze PE ratio, higher = better lol
- Look into share repurchases
- Dividend ratio
- Analyze volatility
- Analyze option scene
  - Maybe average share volume - average option volume gives some clues to investor interest?
