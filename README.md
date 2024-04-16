# icecharts

## setup virtual environment

```
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt 
deactivate
```

## run

```
. .venv/bin/activate
python3 getchart.py
deactivate
```

## schedule cron job

Add the following to the file .github/workflows/run_action.yaml:

```
on:
  schedule:
    - cron: '10 */3 * * *'
```
