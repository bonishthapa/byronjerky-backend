# Build the project
echo "Building the project..."
python3.9.19 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9.19 manage.py makemigrations --noinput
python3.9.19 manage.py migrate --noinput

echo "Collect Static..."
python3.9.19 manage.py collectstatic --noinput --clear