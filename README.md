# Food Delivery Bot

---

## Create virtual environment

```
python3 -m venv venv
```

## Activate virtual environment

``` python
source venv\bin\activate
```

## Install dependencies

``` python
pip install -r requirements.txt
```

## Create .env file and fill this file with environment variables to run a project

``` shell
touch .env
```

## Fill this file with required variables

``` text 
TOKEN=<BOT_TOKEN>
DB_NAME=<DATABASE_NAME>
DB_USER=<DATABASE_USER>
DB_PASSWORD=<DATABASE_PASSWORD>
DB_PORT=<DATABASE_PORT>
DB_HOST=<DATABASE_HOST>
```

## Run a bot

``` python
python app.py
```



