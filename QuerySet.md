Это объект в [[Django]], который представляет собой набор запросов к базе данных, возвращающий множество объектов модели. Это ленивый запрос, что означает, что запрос к базе данных выполняется только тогда, когда нужно получить данные (например, при итерации по QuerySet или его фильтрации).

**Основные операции с QuerySet**:

- **`get()`** — извлекает один объект, выбрасывает исключение, если найдено несколько объектов или если объект не найден.
- **`filter()`** — возвращает список объектов, соответствующих критериям фильтрации.
- **`all()`** — возвращает все объекты модели.
- **`get_object_or_404()`** — выполняет запрос через `get()` и вызывает ошибку 404, если объект не найден.

```Python
book = Book.objects.get(id=book_id)  # если уверен, что книга есть
books = Book.objects.filter(author='John Doe')  # когда несколько книг одного автора
books = Book.objects.all()  # получить все книги
book = get_object_or_404(Book, id=book_id)  # если книга обязательна, иначе ошибка 404
```


#### Когда использовать `get_object_or_404`, `get`, `filter`, и `all`?

1. **`get_object_or_404`**:
    
    - Используется, когда нужно получить объект по одному критерию, и если он не найден — автоматически вызывает ошибку 404.
    - **Когда использовать**: Когда необходимо быть уверенным, что объект существует. Например, при получении объекта по его `id` в представлениях.
2. **`get`**:
    
    - Получает один объект по критериям. Если нет или несколько объектов — вызовет исключение.
    - **Когда использовать**: Когда вы уверены, что объект уникален (например, по уникальному `id`).
3. **`filter`**:
    
    - Возвращает queryset (список объектов), которые соответствуют критериям. Может вернуть несколько объектов или пустой список.
    - **Когда использовать**: Когда ожидается несколько объектов или нужна фильтрация по нескольким критериям.
4. **`all`**:
    
    - Возвращает все объекты модели.
    - **Когда использовать**: Когда нужно получить все записи из таблицы.