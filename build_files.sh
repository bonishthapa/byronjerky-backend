echo "Unistalling psycopg"
python3 -m pip uninstall psycopg2

echo "Install psycop binary"
python3 -m pip install psycopg2-binary

echo "setuptools"
python3 -m pip install -U setuptools

echo "Building project...."
python3 -m pip install -r requirements.txt

echo "Make Migration..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect Static..."
python3 manage.py collectstatic --noinput --clear
