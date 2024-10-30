Чтобы создать новый проект Django с папкой `core`, следуй этим шагам:

### 1. Установка виртуального окружения
1. **Создай папку для проекта**:
	Можно это сделать вручную, а можно с помощью команд:
   ```bash
   mkdir my_django_project
   cd my_django_project
   ```
   
2. **Создай виртуальное окружение** `venv`:
   ```bash
   python -m venv venv
   ```
   
3. **Активируй виртуальное окружение**:
   - На Windows:
     ```bash
     venv\Scripts\activate
     ```
   - На macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### 2. Установка Django
Установи Django в виртуальном окружении:
```bash
pip install django
```

### 3. Создание проекта
Создай проект Django, указав имя `core`:
```bash
django-admin startproject core
```
Должна добавиться общая папка проекта `core (её можно переименовать, что бы не путаться)` и в ней тоже папка `core`.

### 4. Структура проекта
Нужно закрыть терминал и удалить папку `venv`. Далее переходим в папку с проектом, которую переименовали. открываем терминал. Устанавливаем и активируем `venv`, устанавливаем `Django`.

### 5. Добавление файла с зависимостями и переменными окружения
В корне проекта, где находится файл `manage.py`, добавляем файл `requirements.txt` и прописываем установленные библиотеки и их версии через знак `==`.

Это можно сделать так же с помощью команды:
```Shell
pip freeze > requirements.txt
```

Но при этой команде пропишутся все библиотеки, которые устанавливались вместе с `Django`.
Далее, в корне проекта, где находится файл `manage.py` и `requirements.txt` создаем файл `.env`.

```makefile
SECRET_KEY=''
DEBUG=True
ALLOWED_HOSTS='127.0.0.1,localhost'

SQL_ENGINE='django.db.backends.postgresql'
SQL_DATABASE=''
SQL_USER=''
SQL_PASSWORD=''
SQL_HOST='localhost'
SQL_PORT='5432'
DATABASE='postgres'
```

Указываем свои данные в файле.

### 6. Создание приложения
Перейди в директорию проекта и создай приложение (например, `myapp`):
```bash
cd core
django-admin startapp myapp
```

### 7. Настройка проекта
1. **Устанавливаем библиотеку** `environs`. С помощью команды `pip install environs`. Добавляем библиотеку в файл с зависимостями `requirements.txt`.

2. **В файле `core/settings.py`**:
   - Импортировать библиотеки `os`, `Env`:
   ```Python
	import os
	
	from pathlib import Path
	from environs import Env
```

   - Далее подключить `env`:
```Python
	env = Env()
	env.read_env()
```

   - Перенести данные `SECRET_KEY`, `DEBUG`,  `ALLOWED_HOSTS` в `.env`.

   - Добавь `myapp` в список `INSTALLED_APPS`:
     ```python
     INSTALLED_APPS = [
         ...
         'myapp',
     ]
     ```

   - Настройка системы шаблонов в проекте Django. Определяем место для хранения HTML-шаблонов, которые будут использоваться для рендеринга страниц.:
```Python
	TEMPLATES = [
	...
	'DIRS': [os.path.join(BASE_DIR, 'templates')],
	...
	]
```

   - Настройка путей для статических файлов и медиафайлов(загружаемыми пользователями) в Django:
```Python
	STATIC_URL = 'static/'
	STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
	MEDIA_URL = 'media/'
```

2. **В файле `core/urls.py`**:
   - Настрой базовые маршруты:
     ```python
     from django.contrib import admin
     from django.urls import path, include

     urlpatterns = [
         path('admin/', admin.site.urls),
         path('', include('myapp.urls', namespace='my_app')),  # Добавь urls.py из myapp
     ]
     ```

3. **В корневую папку проекта добавляем папки** `temlates`, `static`
   - В `temlates` создаем базовый шаблон `base.html`. Так же добавляем папку `myapp`, где будут храниться шаблоны относящиеся к этому приложению :
```HTML
{% load static %}
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>{% block lists %}{% endblock %}Книги</title>
	</head>
	<body>
	</body>
</html>
```

   - В папке `static` добавляем файл с расширением `css`, который будем использовать для общих стилей проекта. 
### 8. Создание файла `urls.py` в приложении `myapp`
В папке `myapp` создай файл `urls.py` и добавь базовый маршрут:
```python
from django.urls import path
from .views import view_index

app_name = my_app

urlpatterns = [
    path('', view_index, name='index'),  # Путь к домашней странице
]
```

### 9. Создание представления
В файле `myapp/views.py` добавь простое представление:
```python
from django.shortcuts import render

def view_index(request):
    return render(request, 'myapp/index.html')
```

### 10. Добавляем шаблон для показа главной страницы
В папке `myapp` в `templates` добавляем файл `index.html`. Это наша главная страница проекта, которая унаследуется от базового шаблона:
```HTML
{% extends 'base.html' %}

{% load static %}
{% block lists %}
Главная страница
{% endblock %}
{% block content %}
<div>
</div>
{% endblock %}
```

### 11. Запуск сервера
   ```bash
   python manage.py runserver
   ```

### 11. Проверка работы
Перейди по адресу `http://127.0.0.1:8000/` в браузере, чтобы увидеть сообщение "Hello, Django!".

