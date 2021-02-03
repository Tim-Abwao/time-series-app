from flask import redirect, render_template, request
from ts_app.file_upload import process_upload
from ts_app.index import server
from ts_app.glossary import definitions

server.config["MAX_CONTENT_LENGTH"] = 7 * 1024 * 1024  # 7MB limit


glossary_data = sorted(definitions, key=lambda x: x['title'])


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
        error = process_upload(request)

        if error:
            return render_template('upload.html', input_error=error)

        return redirect('/dashboard/upload')

    return render_template("upload.html")


@server.route("/dashboard")
def sample_dashboard():
    """Create and process sample time series data."""
    return redirect("/dashboard/sample")
