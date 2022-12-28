## What this does

When reopening a word mailmerge file and the backing excel file is not in the
expected location, then you will lose the filters and sort that were set.

This tool shows the filter and sort information of a mailmerge docx file, it looks like this :

    SELECT * FROM /Users/wolff_n/Desktop/clients 10 ans.xlsx
    WHERE ((Carte_Club_4Vallées = 'oui')) ORDER BY Nom

## Running the online webapp

https://word-mailmerge-datasource-yjvahykdxa-oa.a.run.app/

## Running from the command-line

`./retrieve_datasource_query.py` takes the path to a docx or dotx file and displays the datasource query
