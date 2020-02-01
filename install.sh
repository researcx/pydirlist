virtualenv --python=python3 venv
source venv/bin/activate
pip install -e .
mkdir keiDirList/static/files/
mkdir keiDirList/static/.thumbnails/
mkdir logs/
touch logs/access.log
touch logs/error.log