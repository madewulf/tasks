A very simple API for to-do lists
---

Installation: 
 
git clone https://github.com/madewulf/tasks
python3 -m venv tasks
cd tasks
source bin/activate
pip install -r requirements.txt
cp meta/dev-settings.py tasks/settings.py
./manage.py migrate
./manage.py runserver