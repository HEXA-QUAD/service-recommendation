

Migrate DB
```
python3 -m flask db migrate -m "Initial migration."
python3 -m flask db migrate -m "commit"
```


Upgrade DB
```
python3 -m flask db upgrade

# downgrade
python3 -mflask db downgrade
```
