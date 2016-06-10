set -e

cd $TRAVIS_BUILD_DIR
# Fetch this binary within travis rather than within cloud.gov
python manage.py fetch_wkhtmltox
./deploy.sh dev
