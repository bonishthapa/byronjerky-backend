echo "Unistalling psycopg"
python3 -m pip uninstall psycopg2

echo "setuptools"
python3 -m pip install -U setuptools

echo "ruamel"
python3 -m pip install --no-deps ruamel.yaml

echo "Building project...."
python3 -m pip install -r requirements.txt

echo "Make Migration..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect Static..."