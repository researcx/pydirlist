source venv/bin/activate
source config
echo "=== Configuration ==="
echo "HOST:" $KEIDIRLIST_HOST

echo ""

echo "=== Starting Server ==="
flask run --host=$KEIDIRLIST_HOST
