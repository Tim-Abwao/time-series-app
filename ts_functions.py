from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import os


def clear_old_files(extension):
    old_files = glob.glob('static/files/*.' + extension, recursive=True)
    for file in old_files:
        os.remove(file)


def get_graphs(data):
    clear_old_files('png')
    t = str(datetime.now())
    graphs = ['static/files/' + t+i for i in ['_acf_pacf_plots.png',
                                              '_plot.png']]
    plt.figure(figsize=(10, 6))
    plt.plot(data)
    plt.savefig(graphs[0], transparent=True)

    fig1 = plt.figure(figsize=(10, 8))
    ax1 = fig1.add_subplot(211)
    plot_acf(data.values, ax=ax1, color='coral')
    ax2 = fig1.add_subplot(212)
    plot_pacf(data.values, ax=ax2, color='coral')
    plt.savefig(graphs[1], transparent=True)

    return graphs
