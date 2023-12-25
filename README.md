# Stripe


## Требования


- docker-compose
- nginx

## Установка

1. Клонируйте репозиторий на свой локальный компьютер:

```
git clone git@github.com:Cardebul/stripe.git
```

2. Перейдите в директорию проекта:

```
cd stripe
```

3. Создайте и заполните .env по образцу:

STRIPE_SECRET_KEY=<your_stripe_secret_key>
STRIPE_PUBLISHABLE_KEY=..
...

4. Запустите compose:

```
docker compose -f docker-compose.production.yml up -d
```

5. Настройте базу данных и скопируйте статику:

```
docker compose -f docker-compose.production.yml exec -i backend bash
```

```
python manage.py migrate
```


```
python manage.py loaddata --exclude auth.permission --exclude contenttypes db.json
```


```
cd /backend_static
```


```
mkdir static
```

```
cp admin static
```


```
cp style.css static
```


