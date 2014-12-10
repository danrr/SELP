Software Engineering Large Practical
====
Dan Ristea <br />
s1244166

###Setup###
Prerequisites:

* virtualenv
* git

To install run *source setup.sh*. It will install a virtualenv with dependencies and a node.js instance with nvm, compile coffee-script and scss, and initialize the databases. (Windows environments are not supported by the setup but a manual installation based on the steps in it is possible)

###Run###
To run the app run *source setup.sh*. This will initialize the app on port 5000.

To run the python tests run *source run_tests.sh*.

To recompile the static assets, run *source compile_js.sh* for the coffeescript and *compile_css.sh* for the SCSS

###Structure###
* app - module containing all the app specific files
  * db_repository - folder containing the generated migrations for the app database
  * search.db - database used by whoosh, the search library
  * static - folder containing the static resources of the app
    * app.coffee - coffeescript file containing all the client-side scripts
      * app.js - javascript file generated from the coffeescript
    * app.scss - SCSS file containing all the custom styling for the app, builds on Bootstrap styles
      * app.css - CSS file generated from the SCSS file
  * templates - folder containing all the templates used by the app
    * partials - folder containing partials and macros used in multiple templates
  * app.db - SQLite database for the app
  * config.py - configuration file for the app
  * forms.py - file containing all the WTforms objects
  * helpers.py - file containing helper functions for use in views
  * models.py - file containing all the models used by SQLalchemy to interact with the db
  * views.py
* scripts - module containing scripts used to manage the database
  * db_create - creates app and test databases
  * db_migrate - creates a migration based on models.py
  * db_upgrade - upgrades the db to the latest migration
  * db_reset - purges all entries from the database and populates it with canned data
* tests - module containing unit and integration tests
  * db_repository - folder containing the generated migrations for the test database
  * search.db - database used by whoosh, the search library, exists only to prevent the actual search database from being polluted by tests
  * base_test.py - contains base test class which deals with setting up and tearing down the database for tests, all tests inherit from it
  * test.db - SQLite database for tests
  * test_config.py - configuration file used by test app
  * test_models.py - unit tests around SQLalchemy models
  * test_views.py - integration tests around view functions
  * test_helpers.py - unit tests around helper functions
* uploads - temp storage for image uploads

###Proposal###

Please find the proposal in the PROPOSAL.md file at the root of this repo.

###Report###
For evaluation purposes the databases in prepopulated, as the application is time dependant. The state of a post being derived from the time at which it was published, and as I'm sure you wouldn't want to wait 7 days (or bother hacking about with the time in any way) to fully evaluate my submission, the following users are provided:



<pre>Username | Password
--------------------
Erik     | 12345
Jane     | qwert
Mike     | asdfg
John     | zxcvb</pre>

Of course, I encourage you to test out creating a brand new user, new posts, and new submissions.

Please find the report in the REPORT.md file at the root of this repo.


