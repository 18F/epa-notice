set -e

API="https://api.cloud.gov"
ORG="eregs-nc"
APP_NAME="eregs-web"
WORKER_NAME="eregs-worker"
SPACE=$1

if [ $# -ne 1 ]; then
  echo "Usage: deploy <space>"
  exit
fi

if [ $SPACE = 'prod' ]; then
  MANIFEST="manifest_prod.yml"
elif [ $SPACE = 'dev' ]; then
  MANIFEST="manifest_dev.yml"
else
  echo "Unknown space: $SPACE"
  exit
fi

cf login --a $API --u $CF_USERNAME --p $CF_PASSWORD --o $ORG -s $SPACE
cf zero-downtime-push $APP_NAME -f $MANIFEST
cf zero-downtime-push $WORKER_NAME -f $MANIFEST
