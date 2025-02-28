import requests
from bs4 import BeautifulSoup

from telegram_assistant.parser.parser import Parser


class TableParser(Parser):
    def lite_parse_table(
        self,
        url: str,
        table_class: str,
        row_class_name: str,
        data_row_offset: int,
        table_number: int | None = None,
    ) -> dict[str, str]:
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

        return rows_dict

    def parse_specific_row(
        self,
        url: str,
        table_class: str,
        row_class_name: str,
        row_number: int,
        table_number: int | None = None,
    ) -> dict[str, str]:
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
