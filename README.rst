.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org//ckanext-panama.svg?branch=master
    :target: https://travis-ci.org//ckanext-panama

.. image:: https://coveralls.io/repos//ckanext-panama/badge.png?branch=master
  :target: https://coveralls.io/r//ckanext-panama?branch=master


==============
ckanext-panama
==============

An Open Data portal for Panama


------------
Requirements
------------

* ckanext-scheming: https://github.com/open-data/ckanext-scheming
* ckanext-fluent: https://github.com/open-data/ckanext-fluent
* ckanext-disqus: https://github.com/ckan/ckanext-disqus
* ckanext-widgets: https://github.com/ckan/ckanext-widgets
* ckanext-pages: https://github.com/ckan/ckanext-pages

Add these to the `ckan.plugins` setting in order::

  ckan.plugins = ... panama panama_groups fluent scheming_datasets panama_scheming_groups disqus pages widgets

Configuration settings for these extensions are detailed below.

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-panama:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-panama Python package into your virtual environment::

     pip install ckanext-panama

3. Add ``panama`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Several of the CKAN extension require configuration settings.

ckanext-pages should use the ckeditor::

  ckanext.pages.editor = ckeditor

ckanext-disqus needs the account name::

  disqus.name = <disqus account name>

ckanext-scheming and ckanext-fluent need schema and presets specified::

  scheming.dataset_schemas = ckanext.panama:fluent_panama.json

  scheming.presets = ckanext.scheming:presets.json
                     ckanext.fluent:presets.json


------------------------
Development Installation
------------------------

To install ckanext-panama for development, activate your CKAN virtualenv and
do::

    git clone https://github.com//ckanext-panama.git
    cd ckanext-panama
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.panama --cover-inclusive --cover-erase --cover-tests


----------------------------------
Registering ckanext-panama on PyPI
----------------------------------

ckanext-panama should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-panama. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


-----------------------------------------
Releasing a New Version of ckanext-panama
-----------------------------------------

ckanext-panama is availabe on PyPI as https://pypi.python.org/pypi/ckanext-panama.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
