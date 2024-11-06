Формы в [[Programming/Django/Django]] — это мощный инструмент для обработки пользовательского ввода. Они используются для сбора, валидации и обработки данных от пользователя в веб-приложениях. Django предоставляет класс `forms.Form`, который облегчает работу с формами, и предоставляет различные методы для проверки, отображения и работы с данными.

### Основные цели использования форм в Django:

1. **Сбор данных**: Формы позволяют собирать данные от пользователя через HTML-формы.
2. **Валидация данных**: Django автоматически проверяет введенные данные на соответствие заданным условиям (например, тип данных, максимальная длина, обязательные поля).
3. **Обработка данных**: После успешной валидации формы данные можно использовать для сохранения в базе данных, отправки по электронной почте и других задач.

### Создание форм в Django

В Django формы создаются путем создания класса, наследующего от `forms.Form`. Вот базовый пример формы:

```Python
# forms.py
from django import forms

class ExampleForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)
    email = forms.EmailField(label='E-mail')
```

#### Элементы формы:

- **Поле формы (Field)** — определяет тип данных, которые форма ожидает получить от пользователя. Например, `CharField`, `EmailField`, `IntegerField` и т.д.
- **label** — это заголовок поля, который будет отображен на форме рядом с полем ввода.
- **max_length** — ограничение на максимальную длину вводимого текста.

### Использование формы в представлении (view)

Формы создаются и обрабатываются в представлениях Django. Пример базового представления для отображения формы и обработки данных:

```Python
# views.py
from django.shortcuts import render
from .forms import ExampleForm

def example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            return render(request, 'success.html', {'first_name': first_name, 'last_name': last_name})
    else:
        form = ExampleForm()

    return render(request, 'form_template.html', {'form': form})
```

- **`request.method == 'POST'`** — проверка того, отправлена ли форма (POST-запрос).
- **`form.is_valid()`** — метод проверяет, прошли ли все поля валидацию.
- **`form.cleaned_data`** — это словарь, содержащий данные формы, которые были очищены и проверены.

### Валидация данных формы

Django автоматически валидирует введенные данные в зависимости от типа поля. Например, для поля `EmailField` проверка выполняется на наличие корректного формата email. Однако можно настроить и собственные проверки.

#### Проверка через встроенные валидаторы

Каждое поле формы поддерживает добавление валидаторов. Валидаторы — это функции или методы, которые проверяют значение на определенные условия.

```Python
from django import forms
from django.core.validators import MinLengthValidator

class ExampleForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=100, validators=[MinLengthValidator(5)])
```

- **`MinLengthValidator(5)`** — проверяет, чтобы имя пользователя было не менее 5 символов.

#### Создание собственной валидации

Если вам нужно создать более сложную валидацию, можно использовать метод `clean_<fieldname>` для индивидуальных полей, либо метод `clean` для всей формы.

**Пример метода `clean_<fieldname>`:**

```Python
class ExampleForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise forms.ValidationError('Допустим только e-mail с доменом @example.com')
        return email
```

- **`clean_email`** — метод валидации для поля `email`. Если email не заканчивается на `@example.com`, будет вызвана ошибка.

**Пример метода `clean`:**

```Python
class ExampleForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
```

- **`clean`** — общий метод для проверки данных формы целиком. Здесь он проверяет совпадение паролей.

### Отображение формы в шаблоне

Django позволяет легко рендерить форму в шаблоне HTML с помощью встроенных шаблонных тегов. Пример базового шаблона:

```HTML
<!DOCTYPE html>
<html>
<head>
    <title>Пример формы</title>
</head>
<body>
    <h1>Заполните форму</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Отправить</button>
    </form>
</body>
</html>
```

- **`{{ form.as_p }}`** — вывод формы с оборачиванием полей в параграфы (`<p>`).
- **`{% csrf_token %}`** — токен защиты от CSRF-атак (обязателен для POST-запросов).

### Добавление классов к полям формы

Чтобы добавить HTML-классы к полям формы (например, для стилизации), можно использовать атрибуты виджетов (`widgets`).

```Python
class ExampleForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
```

- **`widget=forms.TextInput(attrs={'class': 'form-control'})`** — это способ добавить HTML-класс к полю ввода (например, для Bootstrap).

### Работа с полями и типами данных

Django предоставляет большое количество типов полей для различных данных:

1. **CharField**: Текстовое поле.
2. **EmailField**: Поле для email-адресов.
3. **IntegerField**: Целочисленное поле.
4. **ChoiceField**: Поле для выбора из предопределенных значений (например, выпадающий список).
5. **BooleanField**: Поле для выбора "Да" или "Нет" (галочка).
6. **DateField**: Поле для ввода даты.

**Пример работы с `ChoiceField`:**

```Python
class ExampleForm(forms.Form):
    OPTIONS = [
        ('1', 'Один месяц'),
        ('3', 'Три месяца'),
        ('6', 'Шесть месяцев'),
        ('12', 'Двенадцать месяцев'),
    ]
    delivery_duration = forms.ChoiceField(label='Длительность доставки', choices=OPTIONS)
```

### Обработка файлов (например, загрузка изображений)

Если форма предполагает загрузку файлов, необходимо добавить специальный виджет `FileField` или `ImageField` для обработки файлов.

```Python
class FileUploadForm(forms.Form):
    file = forms.FileField(label='Загрузите файл')
```

При создании формы с файлами в шаблоне нужно добавить атрибут `enctype="multipart/form-data"` в тег `<form>`:

```HTML
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Отправить</button>
</form>
```

### Форма в модели (ModelForm)

Когда данные формы напрямую связаны с моделью (например, для создания или редактирования объектов), можно использовать класс `ModelForm`, который автоматически связывает поля с моделью.

Пример `ModelForm`:

```Python
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']
```

