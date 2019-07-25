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

**Configure**
```bash
cp instance/config.dist.py instance/config.py
```

Then set the correct values in `instance/config.py`

**Run the local server**
```bash
export FLASK_APP=pet_hotel
export FLASK_ENV=development
flask run
```






