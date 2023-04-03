#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json
import datetime
import os.path

@click.group()
def main():
    pass


@main.command('add')
@click.argument('filename')
@click.option('--name',  help="The human's name")
@click.option('--phone',  type=int, help="The human's phone")
@click.option('--bday', help="Birthday of a person")
def add_human(filename, name, phone, bday):
    """
    Запросить данные о человеке.
    """
    if os.path.exists(filename):
        people = load_humans(filename)
    else:
        people = []

    list_bday = list(map(int, bday.split(".")))
    date_bday = datetime.date(list_bday[2], list_bday[1], list_bday[0])
    people.append(
        {
            "name": name,
            "phone": phone,
            "birthday": date_bday
        }
    )
    save_humans(filename, people)
    click.secho("Данные добавлены")


@main.command("display")
@click.argument('filename')
def display_CLI(filename):
    if os.path.exists(filename):
        people = load_humans(filename)
    else:
        people = []
    display_human(people)


@main.command("find")
@click.argument('filename')
@click.option('--surname', help="The human's name")
def find_human(filename, surname):
    """
    Выбрать работников с заданным стажем.
    """
    people = load_humans(filename)
    # Сформировать список людей.
    result = []
    for h in people:
        if surname in str(h.values()):
            result.append(h)

    # Проверка на наличие записей
    if len(result) == 0:
        return print("Запись не найдена")

    # Возвратить список выбранных работников.
    display_human(result)


def display_human(staff):
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if staff:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4,
            "-" * 30,
            "-" * 15,
            "-" * 15
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^15} | {:^15} |".format(
                "№",
                "Фамилия и имя",
                "Телефон",
                "День рождения"
            )
        )
        print(line)

        # Вывести данные о всех сотрудниках.
        for idx, human in enumerate(staff, 1):
            print(
                f"| {idx:>4} |"
                f' {human.get("name", ""):<30} |'
                f' {human.get("phone", 0):<15} |'
                f' {human.get("birthday")}      |'
            )
            print(line)

    else:
        print("Список пуст.")


def json_deserial(obj):
    """
    Деериализация объектов datetime
    """
    for h in obj:
        if isinstance(h["birthday"], str):
            # print(datetime.strptime(h['birthday'], '%Y-%m-%d'))
            bday = list(map(int, h["birthday"].split("-")))
            h["birthday"] = datetime.date(bday[0], bday[1], bday[2])


def load_humans(file_name):
    """
    Загрузить всех работников из файла JSON.
    """

    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def json_serial(obj):
    """Сериализация объектов datetime"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()


def save_humans(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4, default=json_serial)


if __name__ == "__main__":
    main()
