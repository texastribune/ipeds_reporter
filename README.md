IPEDS Importer
==============

The purpose of this is to make it easier to interact with the [IPEDS Data
Center](nces.ed.gov/ipeds/datacenter/Default.aspx)

If you've built your variables in the report builder, you'll find that your
reports are limited to 250 variables. This can be a problem because just
getting a report with test scores will take up 207 variables. Juggling the MVL
files to upload reports can be a pain, but that's still easier than dealing
with creating a new set of variables.



Usage
-----

Running this project assumes you're familiar with running Python projects.
Beyond that, it's not too bad.


In your virtualenv:

    pip install -r requirements.txt
    make resetdb
    python manage.py createsuperuser
    make start
