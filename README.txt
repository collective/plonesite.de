****************
Website plone.de
****************

Webseite der `deutschen Plone Community <http://plone.de>`_,.

Lokale development Installation
-------------------------------

.. code:: bash

    $ git clone git@github.com:collective/plonesite.de.git
    $ echo -e "[buildout]\nlogin = admin\npassword = admin" > secret.cfg
    $ ln -s local_develop.cfg local.cfg
    $ python3.7 -m venv .
    $ bin/pip install -r requirements.txt
    $ bin/buildout
    $ bin/instance fg

