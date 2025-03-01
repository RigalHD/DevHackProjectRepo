import requests
from bs4 import BeautifulSoup


class TableParser:
    def lite_parse_table(
        self,
        url: str,
        table_class: str,
        row_class_name: str,
        data_row_offset: int,
        table_number: int | None = None,
        reversed_result: bool = False,
    ) -> dict[str, str]:
        """
        Парсит HTML-таблицы.

        :param url: URL-адрес страницы для парсинга;
        :param table_class: HTML-класс таблицы для парсинга;
        :param row_class_name: HTML-класс ряда таблицы без номера
                               (Пример: было - row11, стало - row);
        :param data_row_offset: количество рядов, парсинг которых не должен проводиться
                                (Пример: первые 2 ряда таблицы - названия колонок. Значением будет 2);
        :param table_number: Применяется только в случае, если на сайте присутствует
                             две или более таблицы с одинаковым названием класса;
        :param reversed_result: False - обычный результат работы метода,
                                True - ключ и значение в словаре поменяются местами;

        Возвращает результат в формате словаря:
            ключ - ряд в таблице (Пример: row1, row15 и т.п.),
            значение - первая ячейка ряда.
        """
        response = requests.get(url=url)
        
        bs = BeautifulSoup(response.text, "html.parser")

        if table_number is None:
            table = bs.find(class_=table_class)
        else:
            table = bs.find_all(class_=table_class)[table_number]
        rows_dict: dict[str, str] = {}

        for row in table.find_all("tr"):
            cells = row.find_all("td")
            rows_dict[row.get("class")[0]] = cells[0].text

        rows_dict_keys = tuple(rows_dict.keys())

        for row_name in rows_dict_keys:
            if int(row_name.lstrip(row_class_name)) < data_row_offset:
                del rows_dict[row_name]

        if reversed_result is True:
            reversed_rows_dict: dict[str, str] = {}
            for key, value in rows_dict.items():
                reversed_rows_dict[value] = key
            return reversed_rows_dict

        return rows_dict

    def parse_specific_row(
        self,
        url: str,
        table_class: str,
        row_class_name: str,
        row_number: int,
        table_number: int | None = None,
    ) -> dict[str, str | dict[str, str]]:
        """
        Подробно парсит ряд HTML-таблицы.

        :param url: URL-адрес страницы для парсинга;
        :param table_class: HTML-класс таблицы для парсинга;
        :param row_class_name: HTML-класс ряда таблицы без номера
                               (Пример: было - row11, стало - row);
        :param row_number: номер ряда таблицы, парсинг которого будет произведен;
        :param table_number: Применяется только в случае, если на сайте присутствует
                             две или более таблицы c одинаковым названием класса;

        Возвращает результат в формате словаря:
            ключ - имя колонки в таблице,
            значение - значение ячейки ряда c этим именем
                       ИЛИ словарь c "подколонками" в качестве ключа
                             и значение ячейки ряда c именем колонки.

        """
        response = requests.get(url=url)

        name_rows_count = 2

        bs = BeautifulSoup(response.text, "html.parser")

        if table_number is None:
            table = bs.find(class_=table_class)
        else:
            table = bs.find_all(class_=table_class)[table_number]

        cells_dict: dict[str, str] = {}
        row = table.find("tr", {"class": row_class_name + str(row_number)})
        for cell in row.find_all("td"):
            cells_dict[str(cell.get("class")[0])] = cell.text

        cells_list = []
        for number in range(name_rows_count):
            cells_list.append({})
            row = table.find("tr", {"class": row_class_name + str(number)})
            for cell in row.find_all("td"):
                cells_list[number][str(cell.get("class")[0])] = cell.text

        sectors = cells_list[0]
        columns = cells_list[1]

        sorted_column_names = {}
        sector_keys = list(sectors.keys())

        for i in range(len(sector_keys) - 1):
            sector_key = sector_keys[i]
            next_sector_key = sector_keys[i + 1]

            sorted_column_names[sector_key] = {}

            for column_key in columns.keys():
                if column_key == sector_key or (
                    int(sector_key.lstrip("column"))
                    < int(column_key.lstrip("column"))
                    < int(next_sector_key.lstrip("column"))
                ):
                    sorted_column_names[sector_key][column_key] = columns[column_key]

            if sorted_column_names[sector_key] == {}:
                sorted_column_names[sector_key] = sectors[sector_key]

        full_row_info: dict[str, str | dict[str, str]] = {}

        for column_key, column_value in sorted_column_names.items():
            if isinstance(column_value, dict):
                full_row_info[sectors[column_key]] = {}
                for key, value in column_value.items():
                    full_row_info[sectors[column_key]][value] = cells_dict[key]
            else:
                full_row_info[column_value] = cells_dict[column_key]

        return full_row_info
