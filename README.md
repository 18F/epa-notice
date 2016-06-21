# EPA eManifest/eRegs Notice and Comment Pilot
[![Build Status](https://travis-ci.org/eregs/notice-and-comment.svg?branch=master)](https://travis-ci.org/eregs/notice-and-comment)
[![Dependency Status](https://gemnasium.com/badges/github.com/eregs/notice-and-comment.svg)](https://gemnasium.com/github.com/eregs/notice-and-comment)
[![Code Climate](https://codeclimate.com/github/eregs/notice-and-comment/badges/gpa.svg)](https://codeclimate.com/github/eregs/notice-and-comment)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/6115cfa655a041c09bff33c8a6a0bca5/badge.svg)](https://www.quantifiedcode.com/app/project/6115cfa655a041c09bff33c8a6a0bca5)

Glue project which combines regulations-site, regulations-core and
styles/templates for EPA's eManifest proposal, packaged as a cloud.gov app.

## Local Setup
This application requires Python 2.7, 3.3, 3.4, or 3.5 (we test against 3.4).
Install a version (if you haven’t already), set up a virtualenv for this
project and activate it, and then clone this repository. Throughout these
docs, we’ll assume you are running in a *nix environment (Linux, BSD, OS X,
etc.); Windows instructions would be similar.

Next, we need to install all of the appropriate requirements (including the
other components of eRegs). We’ll assume you have pip, Node.JS, and npm
installed.

```
npm install -g grunt-cli bower
pip install -r requirements.txt
```

Then initialize the database (SQLite by default; see Production) and build the
frontend:

```
python manage.py migrate --fake-initial
python manage.py compile_frontend
```

If you know that the required npm libraries are installed and up to date, you
can pass the --no-install flag to reduce front-end compilation time:

```
python manage.py compile_frontend --no-install
```

Then select one of the two setup options in the _Data_ section. Both options
will give you **read** access to the tool. See the _Write Access_ section for
more. After that, you can run a development server locally via

```
python manage.py runserver
```

### Data

For an instance of this pilot to display notice data, it needs to have access
to said data. There are two basic schemes to set this up – you can either
point your checkout to existing parsed data (ideal for folks only working on
the front-end or who want to see a UI quickly), or you can populate your
database by parsing them yourself.

#### Point to Existing Data
In this scenario, we just need to configure the UI to point to the live API:

```
echo "API_BASE = 'https://epa-notice.usa.gov/api/'" >> local_settings.py
```

As present, all of the data is behind a Basic Auth wall. You can find the
relevant username and password from cloud.gov:

```
cf target -o eregsnc -s prod
cf env eregs-web | grep HTTP_AUTH_USER
cf env eregs-web | grep HTTP_AUTH_PASSWORD
```

Then add that info to your `local_settings.py`:

```
echo "API_BASE = 'https://[AUTH_USER]:[AUTH_PASS]@epa-notice.usa.gov/api/'" >> local_settings.py
```

#### Parsing
To parse the relevant data, you will need to also install the parsing library.

```
pip install git+https://github.com/eregs/regulations-parser.git
```

Then, you will want to start your local server and send it the parsed data.
These steps will take several minutes. You can find the contents of
"epa-rule.xml" in the shared Google Drive (it is sensitive).

```
python manage.py runserver &    # start the server as a background process
eregs proposal_pipeline /path/to/epa-rule.xml http://localhost:8000/api --only-latest
```
Then navigate to http://localhost:8000

### Editable Libraries
Though this repository contains all of the pilot-specific code, you will most
likely want to extend functionality in the base libraries as well.  To do
this, fork and check out the appropriate library (regulations-site,
regulations-core, regulations-parser) into a separate directory, then install
it via

```
pip install -e /path/to/that/checkout
```

This will tell Python to use your local version of that library rather than
the upstream version. Although modifying Python will trigger the `manage.py`
command to restart, template changes will not. Modifying LESS or JS will also
require re-running `compile_frontend`.

### Fixing Errors
If you pulled down the latest code changes, ran the server locally, and
something didn’t build correctly (you got an error message instead of seeing
eRegs), try running standard updates:

Run `pip install -r requirements.txt` to pull in the latest dependencies. Note
that this resets state from the _Editable Libraries_ technique above.

If working with the parser, do `eregs clear`.

Or if working with notice-and-comment, do `python manage.py compile_frontend`.

And then try running the server again.

### Write Access

To test attachment uploads and comment previews locally, set the
`ATTACHMENT_BUCKET`, `ATTACHMENT_ACCESS_KEY_ID`, and `ATTACHMENT_SECRET_ACCESS_KEY`
variables in `local_settings.py`, or the corresponding environment variables.
To permit cross-origin requests, run `python manage.py setup_cors`.

To test PDF exports locally, install `wkhtmltox`. On Linux, install using
`python manage.py fetch_wkhtmltox`. Otherwise, follow the
[install instructions](http://wkhtmltopdf.org/downloads.html), and set
`WKHTMLTOPDF_PATH` to the path to the `wkhtmltopdf` binary.

If you need to submit a comment, you will need to have a separate worker
process, Redis, (see architecture descriptions below) and regulations.gov
credentials. Notably, the relevant settings are `REGS_GOV_API_URL`,
`REGS_GOV_API_KEY`, `REGS_GOV_API_LOOKUP_URL`, and `COMMENT_DOCUMENT_ID`.
You can start the worker process by running:

```
celery worker --app=notice_and_comment --loglevel=DEBUG
```

### Ports
For the time being, this application, which cobbles together regulations-core
and regulations-site, makes HTTP calls to itself. The server therefore needs
to know which port it is set up to listen on.

We default to 8000, as that’s the standard for django’s runserver, but if you
need to run on a different port, use:

```
python manage.py runserver 1234
```
You will also have to either export an environmental variable or create a
local_settings.py file as follows:

```
export VCAP_APP_PORT=1234
```

OR

```
echo "API_BASE = 'http://localhost:1234/api/'" >> local_settings.py
```

## Production Setup
The pilot is currently deployed on cloud.gov, a PaaS which abstracts away many
of the annoying components of maintenance. As a result, this documentation
(and the production configuration files) are largely geared towards hosting in
this environment. See Non-Cloud.gov for other environments.

### Library Architecture

![Diagram, described below](docs/library-architecture.png)

This repository is a cloud.gov app which stitches together two large Django
libraries with cloud.gov datastores and some pilot-specific styles and
templates. The first library, regulations-core, defines an API for reading and
writing regulation and associated data. This pilot mounts this application at
the /api endpoint (details about the “write” API will be discussed later). The
second library, regulations-site, defines the UI. When rendering templates,
regulations-site will first look in notice-and-comment to see if the templates
have been overridden. These views pull their data from the API; this means
that this application makes HTTP calls to itself to retrieve data (when it’s
not already cached).

### Network Architecture

![Diagram, described below](docs/network-architecture.svg)

There are two running applications, `eregs-web`, which handles web requests,
querying the appropriate data store, and `eregs-worker`, which generates PDFs
and submits data to regulations.gov asynchronously. They share access to a
Postgres database (`eregsnc-psql`) for most data, an ElasticSearch index
(`eregsnc-search`) for searching the preamble, a Redis queue (`eregsnc-redis`)
for sourcing asynchronous data, and S3 (`eregsnc-s3`) for storing attachments
and processed files. We also use a "user-provided" cloud.gov service for
storing credential information (`eregsnc-creds`).

![Diagram, described below](docs/activity-diagram.svg)

The user's browser communicates with `eregs-web` and `s3` (the latter via
pre-generated urls which allow limited upload and read capabilities).
`eregs-web` communicates indirectly with `eregs-worker` via their shared Redis
queue. `eregs-worker` indirectly sends data to the user's browser by
publishing it via `s3`.


#### Service Construction

Services are bound to applications in the manifest files. To create the
necessary services:

```
cf create-service elasticsearch-swarm-1.7.1 1x eregsnc-search
cf create-service rds shared-psql eregsnc-psql
cf create-service redis28-swarm standard eregsnc-redis
cf create-service s3 basic eregsnc-s3
```

Our cloud.gov stack should have a user-provided service named eregsnc-creds
including the following credentials:

* `HTTP_AUTH_USER` - at least 32 characters long
* `HTTP_AUTH_PASSWORD` - at least 32 characters long
* `NEW_RELIC_LICENSE_KEY`
* `REGS_GOV_API_KEY` - for communicating with api.data.gov
* `REGS_GOV_API_LOOKUP_URL` - should end with `/v3/lookup`
* `REGS_GOV_API_URL` - should end with `/v3/comment.json`


To create this service:

```
cf cups eregsnc-creds -p '{"HTTP_AUTH_USER": "...", "HTTP_AUTH_PASSWORD": ...}'
```

To update, substitute cf uups for cf cups.


### Updating Data

![Diagram, described below](docs/updating-data.png)

When there is new data available (e.g. due to modifications in the parser, new
Federal Register notices, etc.), that data must be sent to the /api endpoint
before it will be visible to users. However, we don’t want to allow the
general public to modify the regulatory data, so we need to authenticate.
Currently, this is implemented via HTTP Basic Auth and a very long user name
and password (effectively creating an API key). See the HTTP_AUTH_USER and
HTTP_AUTH_PASSWORD credentials in cloud.gov for more.

Currently, sending data looks something like this (from regulations-parser)

```
eregs proposal_pipeline /path/to/epa-rule.xml https://{HTTP_AUTH_USER}:{HTTP_AUTH_PASSWORD}@{LIVE_OR_DEMO_HOSTNAME}/api --only-latest
# To break the above up into multiple steps (can be useful for saving time:)
# eregs clear   # removes all local data
# eregs proposal_pipeline /path/to/epa-rule.xml output-dir --only-latest  # write to disk
# eregs write_to https://{HTTP_AUTH_USER}:{HTTP_AUTH_PASSWORD}@{LIVE_OR_DEMO_HOSTNAME}/api
```

This updates the data, but does not update the search index and will not clear
various caches. It’s generally best to cf restage the application at this
point, which clears the caches and rebuilds the search index. Note that this
will also pull down the latest versions of the libraries (see the next
section); as a result it’s generally best to do a full deploy after updating
data.

### Deploying Code
If the code within notice-and-comment, regulations-core, or regulations-site
has been updated, you will want to deploy the updated code to cloud.gov. At
the moment, we build all of the front-end code locally, shipping the compiled
CSS/JS when deploying. This means we’ll need to update our libraries, build
the new front end, and push the result.

To run this all (including a zero-downtime push):

```
pip install -r requirements.txt   # updates the -core/-site repositories
python manage.py compile_frontend   # builds the frontend

go get github.com/concourse/autopilot   # zero-downtime plugin
cf install-plugin $GOPATH/bin/autopilot

export CF_USERNAME="My Username"
export CF_PASSWORD="My cloud.gov password"

./deploy.sh [prod|dev]  # select space
```

Confusingly, although the front-end compilation step occurs locally, all other
library linking (in particular to regulations-site and regulations-core) takes
place within cloud.gov. In other words, the setup process for cloud.gov will
pull in the latest from regulations-site and regulations-core, regardless of
what you have locally and regardless of what you’ve built the front-end
against. Be sure to always update your local libraries (via pip) before
building and pushing.

### Non-Cloud.gov
TODO; see `manifest` files, the cloud.gov documentation and
https://atf-eregs.readthedocs.io/en/latest/production_setup.html#non-cloud-gov

### Visual regression tests
Visual regression tests can be run via BackstopJS.
If not already installed, install BackstopJS via npm:
```
npm install backstopjs
```
There is already a `backstop.json` configuration file in the root of this repo that
defines various scenarios for screenshots reference and testing. There is
also a `backstop_scripts` directory that holds CasperJS scripts to define
dynamic action states like writing and review comments that can't be directly accessed
via a unique URL.

#### Reference set capture
Before visual regression testing can begin, reference screenshots need to be captured.
A reference set can be captured by this command:
```
npm run reference
```
After the reference set capture is finished, then tests can be run against the reference set.

#### Running tests
Tests must be run in the `node_modules/backstop_data/` directory with this command:
```
npm run test
```

#### Viewing the report
Timestamped directories of tests will be created in `node_modules/backstop_data/bitmaps_test/`
folder. After the tests run, the browser will open a BackstopJS report but may not show
any passing or failing tests. Upon command line prompt you might have to additionally run:
```
npm run openReport
```
for the visual diffs to show up in the BackstopJS browser report.

#### More documentation
More detailed documentation about BackstopJS can be found on the [github repo](https://github.com/garris/BackstopJS) or the [css-tricks tutorial](https://css-tricks.com/automating-css-regression-testing/).
