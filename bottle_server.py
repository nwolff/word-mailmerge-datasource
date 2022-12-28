#!/usr/bin/env python
from datasource_info import retrieve_datasource_query
from bottle import route, run, static_file, request


@route("/")
def index():
    return static_file("index.html", root="")


@route("/upload", method="POST")
def upload():
    file = request.files.get("file")
    if not file:
        return "No file part", 400
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        return "No selected file", 400
    try:
        ds_query = retrieve_datasource_query(file.file)
        return ds_query or "No Datasource info found"
    except Exception:
        return "Not a valid mailmerge file", 400


if __name__ == "__main__":
    run(host="0.0.0.0", port=8000)
