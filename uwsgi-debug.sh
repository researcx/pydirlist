source venv/bin/activate
source config

echo "=== Starting Server ==="
uwsgi --http $PYDIRLIST_HOST:6000 --module pydirlist --master --enable-threads --workers 8 --processes 8 --threads 4 --callab app
