#!/usr/bin/env python

import io

from flask import Flask, render_template, request

from retrieve_datasource_query import retrieve_datasource_query

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 600


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/upload")
def upload():
    file = request.files["file"]
    if not file:
        return "No file part", 400
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        return "No selected file", 400
    file_content = file.read()
    try:
        ds_query = retrieve_datasource_query(io.BytesIO(file_content))
        return ds_query or "No Datasource info found"
    except Exception as ex:
        print(ex)
        return "Not a valid mailmerge file", 400


if __name__ == "__main__":
    # Only when developing
    app.run(host="0.0.0.0", port=8080, debug=True)
