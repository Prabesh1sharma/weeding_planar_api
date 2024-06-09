echo "BUILD START"
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
mkdir -p staticfiles_build
cp -r static/* staticfiles_build/
echo "BUILD END"
