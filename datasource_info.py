from zipfile import ZipFile
import xml.etree.ElementTree as ET

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
            root = ET.parse(settings).getroot()
            query_node = root.find("w:mailMerge/w:query", {"w": word_ns})
            if query_node is not None:
                return query_node.attrib[f"{{{word_ns}}}val"]
