set -e

API="https://api.cloud.gov"
ORG="eregs-nc"
APP_NAME="eregs-web"
WORKER_NAME="eregs-worker"
DEV_INSTANCES=2
PROD_INSTANCES=3
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
# TODO: Restore zero-downtime push after https://github.com/concourse/autopilot/issues/23 is resolved
# cf zero-downtime-push $WORKER_NAME -f $MANIFEST
cf push $WORKER_NAME -f $MANIFEST

if [ $SPACE = 'prod' ]; then
  # Scale outside of the application manifest so that we avoid hitting a
  # memory ceiling. Note that this workaround won't be needed when the memory
  # quota goes away
  cf scale $APP_NAME -i $PROD_INSTANCES
elif [ $SPACE = 'dev' ]; then
  # See above
  cf scale $APP_NAME -i $DEV_INSTANCES
fi
