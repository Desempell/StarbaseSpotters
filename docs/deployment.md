# Развёртывание

Проект по умолчанию настроен для локальной разработки. Перед публикацией в интернете
нужно поменять настройки безопасности и подключить раздачу статики.

## Чек-лист перед публикацией

| Шаг | Как |
|---|---|
| Отключить режим отладки | `DJANGO_DEBUG=0` |
| Задать секретный ключ | `DJANGO_SECRET_KEY=<длинная случайная строка>` |
| Разрешить домен | `DJANGO_ALLOWED_HOSTS=example.com,www.example.com` |
| Применить миграции | `python manage.py migrate` |
| Собрать статику | `python manage.py collectstatic` |
| Создать администратора | `python manage.py createsuperuser` |

Сгенерировать секретный ключ можно так:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

Ключ задаётся переменной окружения и никогда не коммитится в репозиторий.

## Раздача статики

При `DEBUG=0` Django перестаёт отдавать файлы из `static/` сам. Есть два варианта.

**WhiteNoise** — статику отдаёт само приложение, отдельный веб-сервер не нужен:

```bash
pip install whitenoise
```

Затем в `config/settings.py` добавьте middleware сразу после `SecurityMiddleware`:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ...
]
```

**Nginx** — статику отдаёт веб-сервер: направьте адрес `/static/` в папку `STATIC_ROOT`
(по умолчанию это `staticfiles/`).

## Вариант 1: PythonAnywhere

Бесплатного тарифа хватает для учебного проекта.

1. Загрузите код: в консоли PythonAnywhere выполните `git clone` вашего репозитория.
2. Создайте окружение и поставьте зависимости:
   `mkvirtualenv --python=python3.12 spotters && pip install -r requirements.txt`.
3. На вкладке **Web** создайте приложение с ручной настройкой (Manual configuration).
4. В WSGI-файле укажите путь к проекту и `DJANGO_SETTINGS_MODULE = config.settings`,
   а переменные окружения задайте там же через `os.environ`.
5. В разделе **Static files** пропишите адрес `/static/` и путь к папке `staticfiles`.
6. Выполните `migrate`, `collectstatic` и `createsuperuser`, затем нажмите Reload.

## Вариант 2: свой сервер с gunicorn

```bash
pip install gunicorn whitenoise
```

```bash
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
```

Gunicorn запускают под systemd, а перед ним ставят nginx, который отдаёт статику и
терминирует HTTPS. Если сайт работает по HTTPS, добавьте в настройки:

```python
CSRF_TRUSTED_ORIGINS = ["https://example.com"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## База данных

SQLite подходит для демонстрации и небольшой нагрузки. Если пользователей станет много,
переходите на PostgreSQL: поставьте `psycopg[binary]`, замените блок `DATABASES` в
настройках и выполните `migrate` на новой базе. Файл `db.sqlite3` в репозиторий не
попадает, поэтому на сервере база создаётся с нуля.

## Проверка после публикации

```bash
python manage.py check --deploy
```

Команда покажет, какие настройки безопасности стоит включить.
