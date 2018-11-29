**Notes**

Tests are run with pytest

drugdev> pytest

Celery task are run with the app in drugdev.tasks

drugdev> celery beat -A drugdev.tasks.celery
drugdev> celery worker -A drugdev.tasks.celery --loglevel=info

Endpoits for the app are

/api/contacts [GET] (List of contacts)
/api/contact/<username|email> [GET, POST, PUT, DELETE] (get, post, put, delete a contact)

data format for post/put is 

{'email': 'jim@jim.com', 'surname': 'greeve', 'first_name': 'jim'}

To add a second email, issue a put

{'email': 'jim-2@jim.com'}

**Extra Notes**

I initially ued Python 3.7, but Celery has issues with this due to using async as a module name.  I also ran into issues 
with using the latest redis library (3.0.1), and have to revert back to 2.10.6.  This is reflected in the requirements 
file