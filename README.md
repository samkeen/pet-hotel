# pet-hotel

## Initialize App

**Create your virtual env then install pip packages**
```bash
python -m venv venv
./venv/bin/activate
pip install -r requirements.txt 
```

**Create Db**
```bash
mysql -u root < init-schema.sql
```
Set your db config in `demo/db.py`

**Run the local server**
```bash
export FLASK_APP=demo
export FLASK_ENV=development
flask run
```






