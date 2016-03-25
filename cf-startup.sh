set -e
set -x

if [ $CF_INSTANCE_INDEX = '0' ]; then
  python manage.py migrate --fake-initial
  python manage.py rebuild_index --noinput --remove
  python manage.py setup_cors
fi

python manage.py collectstatic --noinput
waitress-serve --port=$VCAP_APP_PORT notice_and_comment.wsgi:application
