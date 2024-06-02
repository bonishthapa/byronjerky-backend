# Build the project
echo "Installing pip...."
python3.9 -m get-pip

echo "Installing Django"
python3.9 -m pip install Django

echo "Building project...."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear