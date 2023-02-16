from retrieve_datasource_query import retrieve_datasource_query
import cgi


def respond_html(start_response, path):
    with open(path) as f:
        data = f.read()
        data = data.encode("utf-8")
        start_response(
            "200 OK",
            [("Content-Type", "text/html"), ("Content-Length", str(len(data)))],
        )
        return iter([data])


def respond_text(start_response, text, status="200 OK"):
    text = text.encode("utf-8")
    start_response(
        status, [("Content-Type", "text/plain"), ("Content-Length", str(len(text)))]
    )
    return iter([text])


def respond_error(start_response, error_description, status="400 Bad request"):
    return respond_text(start_response, error_description, status)


def app(environ, start_response):
    """We ignore the path, and simply discriminate on the http method"""
    if environ["REQUEST_METHOD"] == "GET":
        return respond_html(start_response, "index.html")
    elif environ["REQUEST_METHOD"] == "POST":
        post = cgi.FieldStorage(
            fp=environ["wsgi.input"], environ=environ, keep_blank_values=True
        )
        file_item = post["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file_item.filename == "":
            return respond_error(start_response, "No selected file")
        try:
            ds_query = retrieve_datasource_query(file_item.file)
            return respond_text(start_response, ds_query or "No Datasource info found")
        except Exception:
            return respond_error(start_response, "Not a valid mailmerge file")
    else:
        return respond_error(start_response, "Invalid method")
