# api_yamdb
api_yamdb
Потом оформим покрасивше))


1)  Для заполнения БД используем  import_csv_to_db.py

Правда теперь это целая менеджмент команда!!!!

Хочешь ее вызвать и выгрузить данные из: 
```python
NEED_TO_PARSE = {
'users.csv': User,
'category.csv': Category,
'genre.csv': Genre,
'titles.csv': Title,
'genre_title.csv': Genre_title,
'review.csv': Review,
'comments.csv': Comment,
}
```
НО, прежде выполни миграции, и проверь файл `api_yamdb/reviews/management/commands/_settings_for_import.py`, в нем находятся настройи... Можешь изменять NEED_TO_PARSE, так уж и быть... НО! csv должны храниться в `api_yamdb/static/data`

Уачи! Я верю ты справишься с этим пунктом...
    
___
10.11.2021 - Отправка на 1ое ревью