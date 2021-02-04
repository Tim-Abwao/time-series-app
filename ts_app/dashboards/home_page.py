import dash_core_components as dcc
import dash_html_components as html

layout = html.Div([
    dcc.Markdown("""
# Time Series App

---

A simple app to learn about, and apply [time series analysis][1] techniques. A
[glossary](/glossary) of terms is available to help get familiar with the main
concepts.

In a nutshell, Time Series Analysis purposes to learn and emulate the behaviour
of data over time. Time Series Forecasting then leverages this knowledge to
estimate future values.

![An example of time series analysis results, plotted](/assets/ts.svg)

To give it a try, you can upload a file or create a sample to analyse:

[1]: https://en.wikipedia.org/wiki/Time_series
"""),
    html.A('Upload a file', href='/upload', className='hvr-bob button'),
    html.A('Process a sample', href='/sample', className='hvr-bob button')
])
