from flask import render_template, request, redirect
from ts_app.file_upload import process_upload
from ts_app.index import server
import json


server.config["MAX_CONTENT_LENGTH"] = 7 * 1024 * 1024  # 7MB limit

with open("data/glossary.json") as file:
    glossary_data = json.load(file)

glossary_data = sorted(glossary_data, key=lambda x: x['title'])


@server.route("/")
def index():
    """Home page."""
    return render_template("index.html")


@server.route("/glossary")
def glossary():
    """Glossary page."""
    return render_template("glossary.html", definitions=glossary_data)


@server.route("/upload", methods=["GET", "POST"])
def upload_file():
    """Process and analyse uploaded file."""
    if request.method == "POST":
        error, file_name, data = process_upload(request)

        if error:
            return render_template('upload.html', input_error=error)

        data.rename(file_name).to_pickle('sample.pkl')  # persist data
        return redirect('/dashboard/upload')

    return render_template("upload.html")


@server.route("/dashboard")
def sample_dashboard():
    """Create and process sample time series data."""
    return redirect("/dashboard/sample")


@server.route("/server_timeout")
def heroku_timeout():
    """
    Create the custom error page to be displayed if the app takes more
    than 30 seconds to process a request.
    See https://devcenter.heroku.com/articles/error-codes#h12-request-timeout
    """
    return render_template('heroku_custom_503.htm')
