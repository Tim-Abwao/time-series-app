### Guide

Graphs reveal the [trend](/glossary#Trend) in the data, and help assess the **goodness of fit**. In general, a good model should reasonably replicate the behaviour of the historical data.

Graphs also help discover [seasonal](/glossary#Seasonality) and [cyclic patterns](/glossary#Cyclic%20patterns). These usually manifest as occasional peaks or troughs.

[Autocorrelation][1] and [Partial-Autocorrelation][2] plots can provide hints on a potentially suitable model to start with. [This article][3] describes how. Testing for [stationarity][4], and filtering out seasonal & trend effects is an essential first step.

[1]: https://en.wikipedia.org/wiki/Autocorrelation
[2]: https://en.wikipedia.org/wiki/Partial_autocorrelation_function
[3]: https://en.wikipedia.org/wiki/Box%E2%80%93Jenkins_method#Autocorrelation_and_partial_autocorrelation_plots
[4]: https://cran.r-project.org/web/packages/TSTutorial/vignettes/Stationary.pdf
