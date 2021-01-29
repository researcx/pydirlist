source venv/bin/activate
source config
echo "=== Configuration ==="
echo "HOST:" $PYDIRLIST_HOST

echo ""

echo "=== Starting Server ==="
flask run --host=$PYDIRLIST_HOST
