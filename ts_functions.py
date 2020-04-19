from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import os


def clear_old_files(extension):
    old_files = glob.glob('static/files/*.' + extension, recursive=True)
    for file in old_files:
        os.remove(file)


def get_graphs(data):
    t = str(datetime.now())
    graphs = ['static/files/' + t+i for i in ['_acf_pacf_plots.png',
                                              '_plot.png']]
    plt.figure(figsize=(10, 6))
    plt.plot(data, color='seagreen')
    plt.xticks(rotation=90)
    plt.title('A line-plot of the data', size=20, pad=10)
    plt.savefig(graphs[0], transparent=True)

    fig1 = plt.figure(figsize=(10, 8))
    ax1 = fig1.add_subplot(211)
    plot_acf(data.values, ax=ax1, color='coral')
    ax2 = fig1.add_subplot(212)
    plot_pacf(data.values, ax=ax2, color='coral')
    plt.savefig(graphs[1], transparent=True)

    return graphs

def fit_tsmodels(data):
    t = str(datetime.now())
    start = data.index[int(len(data)*0.3)]
    end = data.index[-1]
    pred1 = sm.tsa.AutoReg(data, lags=10).fit().predict(start, end)
    pred2 = sm.tsa.SARIMAX(data).fit().predict(start, end)
    pred3 = sm.tsa.ExponentialSmoothing(data).fit().predict(start, end)
    
    models_dict={'AR':pred1, 'SARIMAX':pred2, 'Exponential Smoothing':pred3}
    df=pd.DataFrame({**models_dict})
    results = pd.concat([data, df], axis=1).tail(14).round(2)
    graphs_names=[]
    for model, values in models_dict.items():   
        plt.figure(figsize=(10,6))
        plt.plot(data, label='Original', color='seagreen')
        plt.plot(values, label='Modelled', color='orangered')
        plt.legend()
        plt.title(model+' Model Fit', size=20, pad=10)
        plt.xticks(rotation=90)
        name='static/files/' + '_'.join([t, model])+'.png'
        graphs_names.append(name)
        plt.savefig(name, transparent=True)
        
        
    return results, graphs_names 
