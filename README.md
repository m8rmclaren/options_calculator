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

# config.json - Layout

{
  "options_endpoint": <TD API endpoint for options chain data>,
  "auth_endpoint": <TD API endpoint for oAuth token generation>,
  "watchlist_id": <TD brokerage watchlist ID to pull ticker symbol data>,
  "account_num": <TD brokerage account ID>,
  "client_id": <Dev API app key + @AMER.OAUTHAP>,
  "apikey": <Dev API app key>,
  "refresh_token": <Refresh token generated by TD auth API endpoint>
}

- Note that refresh token must be created manually using https://api.tdameritrade.com/v1/oauth2/token endpoint by creating bearer token.
  - Auth code generated by authenticating TD brokerage with Dev API application. Read documentation lol

# Configuration method

1. Configuration class reads and serializes JSON content to dict
2. get-token member function uses refresh token to generate 30 minute bearer token
3. Returned refresh token replaces old refresh token, dict is deserialized, and JSON file is updated
