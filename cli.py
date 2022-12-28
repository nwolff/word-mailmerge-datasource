#!/usr/bin/env python
from datasource_info import retrieve_datasource_query
import argparse

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
    print(retrieve_datasource_query(args.file))
