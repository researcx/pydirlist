virtualenv --python=python3 venv
source venv/bin/activate
pip install -e .
mkdir pydirlist/static/files/
mkdir pydirlist/static/.thumbnails/
mkdir logs/
touch logs/access.log
touch logs/error.log