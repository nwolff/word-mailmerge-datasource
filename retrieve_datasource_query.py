#!/usr/bin/env python

import argparse
import xml.etree.ElementTree as ElementTree
from zipfile import ZipFile

word_ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def retrieve_datasource_query(file):
    """
    A docx file is just a zip file.
    The info we are looking for is stored in the word/settings.xml file
    in the val attribute of node "settings/mailMerge/query"

    Raises Exceptions if file is not a docx document.

    Returns None if there is no query
    """
    with ZipFile(file) as docx_as_zip:
        with docx_as_zip.open("word/settings.xml") as settings:
            root = ElementTree.parse(settings).getroot()
            query_node = root.find("w:mailMerge/w:query", {"w": word_ns})
            if query_node is not None:
                return query_node.attrib[f"{{{word_ns}}}val"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Retrieves a mail merge datasource information (including filters and sorts)"
    )
    parser.add_argument(
        "file",
        metavar="FILE",
        help="The path to a .docx mail merge file",
    )
    args = parser.parse_args()
    ds_query = retrieve_datasource_query(args.file)
    print(ds_query or "No Datasource info found")
