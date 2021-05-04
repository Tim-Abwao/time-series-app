import json
import dash_html_components as html


definitions = json.loads("""
[{"title":"Trend",
  "definition":"The general upward(increase) or downward(decrease) progression\
   in the data points."},
 {"title":"Time Series",
  "definition":"A time series is a series of data points indexed in time\
   order. For example, daily sales totals over a reasonably lengthy period\
   constitute a time series."},
 {"title":"Seasonality",
  "definition":"This refers to variations that occur at specific regular\
   intervals e.g. every weekend, month-end or festive period."},
 {"title":"Cyclic patterns",
  "definition":"These are the rises and falls in the data that occur at\
   flexible periods, usually extending a year and mostly due to economic\
   factors."},
 {"title":"Stationarity",
  "definition":"A stationary time series is one which has constant mean and\
   variance; which implies that the underlying data-generating-process (e.g.\
   annual sales) creating it does not change over time."},
 {"title":"Auto-Regressive(AR) model",
  "definition":"A model which expresses the time series as a function of its\
   own past values, plus a random error term. Previous values serve as the\
   explanatory variables, and the number of these previous values used in the\
   model is the order of the model, usually denoted by p."},
 {"title":"Moving Average(MA) Model",
  "definition":"A model which specifies that a value depends on the current,\
   and various previous values, of the random error terms. The number of error\
   terms in an MA model, usually denoted by q, is its order."},
 {"title":"ARMA",
  "definition":"An Auto-Regressive Moving Average model combines the concepts\
   of the AR and MA models, to better simulate a relatively stationary time\
   series."},
 {"title":"Autocorrelation",
  "definition":"The similarity between the observations of a time series and\
   a delayed copy of itself. The magnitude of the delay is called the lag."}
]""")


components = sum([[html.Dt(item['title'], id=item['title']),
                   html.Dd(item['definition'], id=item['definition'])]
                  for item in definitions], start=[])

layout = html.Div([
  html.H2('Glossary of Time Series Terms'),
  html.Dl(components),
  html.Footer([
    html.A('Back to home', href='/', className='hvr-bob button')
  ])
])
