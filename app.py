from flask import Flask, request, render_template, redirect, g, url_for

import ast
import urllib
import utils
import csv

DEBUG = False
HOST = '0.0.0.0'
PORT = 5000
SHORT_SITE = 'http://localhost:5000'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new", methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        original_url = str(request.form.get('url'))
        pixel_script = str(request.form.get('pixel_script'))

        try:
            metadata = utils.get_metadata(original_url)

            template_name = "redirection_debug.html"
            if DEBUG == True:
                template_name = "redirection_debug.html"
            else:
                template_name = "redirection.html"

            if "title" in metadata:
                metadata_title = metadata.title
            else:
                metadata_title = ""

            if "type" in metadata:
                metadata_type = metadata.type
            else:
                metadata_type = ""

            if "image" in metadata:
                metadata_image = metadata.image
            else:
                metadata_image = ""

            if "description" in metadata:
                metadata_description = metadata.description
            else:
                metadata_description = ""
        finally:
            metadata_title = ""
            metadata_type = ""
            metadata_image = ""
            metadata_description = ""

        html_file = render_template(template_name, url=original_url, title=metadata_title, type=metadata_type, image=metadata_image, description=metadata_description, pixel_script=pixel_script)

        filename = str(original_url).split("/")[2]
        if "." in filename:
            filename = filename.split(".")[0]
        filename = filename + ".html"
        with open("static/" + filename, mode="w", encoding="utf-8") as file:
            file.write(str(html_file))
            file.close()

        # write to csv
        fp = open("static/" + "data.csv", "a")
        try:
            writer = csv.writer(fp)
            writer.writerow((str(original_url), str(filename)))
        finally:
            fp.close()


        # return redirect(SHORT_SITE + "/static/" + filename )
        return render_template("new.html", redirect_url=SHORT_SITE + "/static/" + filename)

    return render_template("new.html")

# @app.route("/result/<id>")
# def result(id):
#     site = models.Site.get(models.Site.id == id)
#     return render_template("result.html", surl=site.surl)

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
