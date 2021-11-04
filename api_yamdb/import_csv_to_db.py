import os
import datetime as dt
import django
from tqdm import tqdm
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()
# Тут перед отправкой на ревью надо будет закоментить
# Но иначе не рабоатет, если эти импорты перенести выше
from reviews.models import (User, Genre, Genre_title, Title,
                            Category, Comment, Review)


DIR_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'static/data'
)

NEED_TO_PARSE = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': Genre_title,
    'review.csv': Review,
    'comments.csv': Comment,
}

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def read_and_write_to_DB(file, Model):
    file_name = str(os.path.join(DIR_CSV, file))
    with open(file_name, encoding='utf-8') as r_file:
        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter=",")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 0
        # Считывание данных из CSV файла
        index_of_date = None
        for row in file_reader:
            if count == 0:
                fields = row
                # if 'pub_date' in row:
                try:
                    index_of_date = row.index('pub_date')
                except Exception:
                    pass

            else:
                # Так не работает, приходится котстыль делать, который ниже,
                # с еще одним save
                # if index_of_date is not None:
                #     time_str = row[index_of_date]
                #     time_dt_obj = dt.datetime.strptime(time_str, TIME_FORMAT)
                #     row[index_of_date] = time_dt_obj
                data = dict(zip(fields, row))
                obj, done = Model.objects.get_or_create(**data)
                if index_of_date is not None:
                    time_str = row[index_of_date]
                    time_dt_obj = dt.datetime.strptime(time_str, TIME_FORMAT)
                    obj.pub_date = time_dt_obj
                    obj.save()
            count += 1
        print(f'    Добавлено {count} записей в {Model} из {file}')


def main():
    for file, model in tqdm(NEED_TO_PARSE.items()):
        print(file, model, sep=' - ')
        read_and_write_to_DB(file, model)


if __name__ == "__main__":
    main()
