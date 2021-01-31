Graphs help **visualise the trend** in the data. They clearly reveal whether
there's been an increase, decrease or no change in the data values over time.

Graphs also help **discover seasonal** and **cyclic patterns** present in the
data. These usually manifest as occasional peaks or troughs.

Testing for [stationarity][1], and filtering out seasonal & trend effects is an
essential first step. Model fitting usually requires that the time series data
be stationary, and may even contain transformations to make the data
stationary.

Graphs are also useful in **assessing the goodness of fit**. In general, a good
model should reasonably replicate the behaviour of the data used.

[Autocorrelation][2] and [Partial-Autocorrelation][3] plots can provide hints
on a potentially suitable model to start with. [This article][4] describes how.

[1]: https://cran.r-project.org/web/packages/TSTutorial/vignettes/Stationary.pdf
[2]: https://en.wikipedia.org/wiki/Autocorrelation
[3]: https://en.wikipedia.org/wiki/Partial_autocorrelation_function
[4]: https://en.wikipedia.org/wiki/Box%E2%80%93Jenkins_method#Autocorrelation_and_partial_autocorrelation_plots
