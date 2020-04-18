from flask import Flask, flash, render_template, url_for, request, redirect
from ts_functions import get_graphs, clear_old_files
import os
from werkzeug.utils import secure_filename
from datetime import date
import pandas as pd
import numpy as np


UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'csv'}
frequencies={'H':'Hours', 'D':'Days', 'B':'Business days', 'w':'Weeks',
             'M':'Months', 'Q':'Quarters', 'Y':'Years'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html', start=True)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            clear_old_files('csv')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('process_file',
                                    filename=filename))
    return render_template('upload.html')


@app.route('/processing_<filename>')
def process_file(filename):
    ts = pd.read_csv('static/files/' + filename, index_col=0)
    ts.index = pd.to_datetime(ts.index)
    graphs = get_graphs(ts)

    return render_template('processing_file.html', graphs=graphs,
                           filename=filename)


@app.route('/sample', methods=['GET', 'POST'])
def create_sample():
    if request.method == 'GET':
        today=date.today().isoformat()
        return render_template('processing_sample.html', sample=True,
                               frequencies=frequencies, today=today)
    if request.method == 'POST':
        start = request.form['start']
        stop = request.form['stop']
        frequency = request.form['frequency']
        index=pd.date_range(start, stop, freq=frequency)
        size=len(index)
        ts = pd.Series(np.random.rand(size), index=index)
        graphs = get_graphs(ts)
        return render_template('processing_sample.html', graphs=graphs)


if __name__ == '__main__':
    app.run(debug=True)
