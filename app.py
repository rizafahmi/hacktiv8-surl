from flask import Flask, request, render_template, redirect, g, url_for
from urlparse import urlparse

import models
import ast
import urllib
import shortuuid
import utils

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
def index():
    sites = models.Site.select()
    return render_template("index.html", sites=sites)

@app.route("/new", methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        original_url = request.form.get('url').encode('utf-8')
        # if urlparse(original_url).schema == '':
        # original_url = 'http://' + original_url
        if "http" in original_url:
            original_url = original_url.strip("http://")
        if "https" in original_url:
            original_url = original_url.strip("https://")
        pixel_script = request.form.get('pixel_script').encode('utf-8')
        # (site, created) = models.Site.create_surl(original_url.encode('utf-8'), pixel_script.encode('utf-8'))

        # return render_template("result.html", id=site.id)
        # return redirect(url_for("result", id=site.id))

        metadata = utils.get_metadata(original_url)
        html_file = render_template("redirection.html", url=original_url, title=metadata.get("title"), type=metadata.get("type"), image=metadata.get("image"), image_type=metadata.get("image_type"), image_width=metadata.get("image_width"), image_height=metadata.get("image_height"), description=metadata.get("description"), pixel_script=pixel_script)
        filename = original_url.encode('utf-8').split("/")[0]
        file = open("static/" + filename + ".html", "w");
        file.write(html_file.encode('utf-8'))
        file.close()

        return redirect(SHORT_SITE + "/static/" + filename + ".html" )

    return render_template("new.html")

@app.route("/result/<id>")
def result(id):
    site = models.Site.get(models.Site.id == id)
    return render_template("result.html", surl=site.surl)

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
