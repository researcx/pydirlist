source venv/bin/activate
source config

echo "=== Starting Server ==="
uwsgi --socket $KEIDIRLIST_HOST:6000 --module keiDirList --master --enable-threads --workers 8 --processes 8 --threads 4 --callab app
