## What this does 

When reopening a word mailmerge file and the backing excel file is not in the
expected location, then you will lose the filters and sort that were set.

This tool shows the filter and sort information of a mailmerge docx file, it looks like this :

    SELECT * FROM /Users/wolff_n/Desktop/clients 10 ans.xlsx
    WHERE ((Carte_Club_4Vallées = 'oui')) ORDER BY Nom

`./retrieve_datasource_query.py` takes the path to a docx or dotx file and displays the datasource query

## Running in a browser 

There are 2 different implementations of web apps that let you upload docx files and displays their datasource info (they all share the same html frontend):

*bottle_server* requires the bottle python package and is run with:

    ./bottle_server.py

bottle_server is deployed to: https://word-mailmerge-datasource.nwolff.repl.co/


*wsgi_app* was developed to experiment with the wsgi api, it requires the gunicorn python package and is run with:

    gunicorn wsgi_app:app --reload
    
