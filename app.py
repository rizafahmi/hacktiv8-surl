from flask import Flask, request, render_template, redirect, g, url_for
from urlparse import urlparse

import models
import ast
import urllib

DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
SHORT_SITE = 'http://localhost:5000'

app = Flask(__name__)

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the connection to the database after each request."""
    g.db.close()
    return response

@app.route("/")
def hello():
    return "Hello, nurse!"

@app.route("/new", methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        original_url = request.form.get('url')
        # if urlparse(original_url).schema == '':
        # original_url = 'http://' + original_url
        if "http" in original_url:
            original_url = original_url.strip("http://")
        if "https" in original_url:
            original_url = original_url.strip("https://")
        pixel_script = request.form.get('pixel_script')
        (site, created) = models.Site.create_surl(original_url.encode('utf-8'), pixel_script.encode('utf-8'))

        # return render_template("result.html", id=site.id)
        return redirect(url_for("result", id=site.id))

    return render_template("new.html")

@app.route("/r/<surl>")
def redirect_surl(surl):
    site = models.Site.get(models.Site.surl == SHORT_SITE + "/r/" + surl)

    metadata = ast.literal_eval(site.metadata)

    return render_template("redirection.html", url=site.url, title=metadata.get("title"), type=metadata.get("type"), image=metadata.get("image"), image_type=metadata.get("image_type"), image_width=metadata.get("image_width"), image_height=metadata.get("image_height"), description=metadata.get("description"), pixel_script=site.pixel_script)

@app.route("/result/<id>")
def result(id):
    site = models.Site.get(models.Site.id == id)
    return render_template("result.html", surl=site.surl)

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
