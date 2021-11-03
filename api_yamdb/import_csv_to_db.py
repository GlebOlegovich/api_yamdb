import os
import django
from tqdm import tqdm
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()
# Тут перед отправкой на ревью надо будет закоментить
# Но иначе не рабоатет, если эти импорты перенести выше
from yamdb.models import User, Genre, Genre_title, Titles, Category


DIR_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'static/data'
)

NEED_TO_PARSE = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Titles,
    'genre_title.csv': Genre_title,
    # 'comments.csv': Comments,
    # 'review.csv': Review,
}


def read_and_write_to_DB(file, Model):
    file_name = str(os.path.join(DIR_CSV, file))
    print(file_name)
    with open(file_name, encoding='utf-8') as r_file:
        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter=",")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 0
        # Считывание данных из CSV файла
        for row in file_reader:
            if count == 0:
                fields = row[1:]
            else:
                # Вывод строк
                data = dict(zip(fields, row[1:]))
                Model.objects.get_or_create(**data)
            count += 1
        print(f'    Добавлено {count} записей в {Model} из {file}')


def main():
    for file, model in tqdm(NEED_TO_PARSE.items()):
        print(file, model, sep=' - ')
        read_and_write_to_DB(file, model)


if __name__ == "__main__":
    main()
