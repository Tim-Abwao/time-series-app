from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import os


def fit_tsmodels(data):
    """
    This function fits AR, SARIMAX and Holt-Winters Exponential Smoothing
    models on the {data}. It then makes predictions over 60% of the data,
    plots graphs to show model-fit, and saves them as png files. FInally, a
    dataframe of sample results, and list of graph locations are returned.
    """
    # to predict over 60% of the data
    start = data.index[int(len(data) * 0.4)]
    end = data.index[-1]
    pred1 = sm.tsa.AutoReg(data, lags=10).fit().predict(start, end)
    pred2 = sm.tsa.SARIMAX(data).fit().predict(start, end)
    pred3 = sm.tsa.ExponentialSmoothing(data).fit().predict(start, end)
    # getting sample results as a dataframe
    models_dict = {"AR": pred1, "SARIMAX": pred2,
                   "Exponential Smoothing": pred3}
    df = pd.DataFrame({**models_dict})
    results = pd.concat([data, df], axis=1).tail(14).round(2)
    # plotting results
    graphs_names = []
    t = str(datetime.now())
    for model, values in models_dict.items():
        plt.figure(figsize=(8, 4.5))
        plt.plot(data, label="Original", color="navy")
        plt.plot(values, label="Modelled", color="aqua")
        plt.legend()
        plt.title(model + " Model Fit", size=15, pad=10)
        plt.xticks(rotation=90)
        name = "static/files/" + "_".join([t, model]) + ".png"
        graphs_names.append(name)
        plt.savefig(name, transparent=True)
    return results, graphs_names


def clear_old_files(extension, filepath="static/files/*."):
    """
    A utility function to remove old files of {extension} format, from the
    {filepath} folder.
    """
    old_files = glob.glob(filepath + extension, recursive=True)
    for file in old_files:
        os.remove(file)


def get_graphs(data):
    """
    A function that produces a lineplot of the data, and ACF & PACF plots.
    It then saves the graphs as png files, and returns their location.
    """
    # time-stamping graph names
    t = str(datetime.now())
    graphs_names = [
        "static/files/" + t + i for i in ["_acf_pacf_plots.png", "_plot.png"]
    ]
    # line plot
    plt.figure(figsize=(8, 4.5))
    plt.plot(data, color="navy")
    plt.xticks(rotation=90)
    plt.title("A line-plot of the data", size=15, pad=10)
    plt.savefig(graphs_names[0], transparent=True)
    # acf & pacf plots
    fig1 = plt.figure(figsize=(8, 6))
    ax1 = fig1.add_subplot(211)
    plot_acf(data.values, ax=ax1, color="navy")
    ax2 = fig1.add_subplot(212)
    plot_pacf(data.values, ax=ax2, color="navy")
    plt.savefig(graphs_names[1], transparent=True)
    return graphs_names
