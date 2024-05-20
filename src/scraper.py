import os
import re
import requests
import time
import pandas as pd
from unidecode import unidecode
from bs4 import BeautifulSoup
from bs4 import ResultSet, Tag

DATA_DIRECTORY = "./data"
WAIT_TIME = 1.5
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?"
TABS = {
    "producao": 2,
    "processamento": 3,
    "comercializacao": 4,
    "importacao": 5,
    "exportacao": 6,
}


def format_text(text: str) -> str:
    """Formata o texto removendo acentos, convertendo para minúsculas e substituindo caracteres especiais."""
    formatted_text = unidecode(text).lower()
    formatted_text = formatted_text.replace("us$", "usd").replace("r$", "brl")
    formatted_text = re.sub(r"[^\w\s]", "", formatted_text).replace(" ", "_")
    return formatted_text


def format_tag_list(tag_list: ResultSet[Tag]) -> list[str]:
    return [format_text(tag.get_text(strip=True)) for tag in tag_list]


def fetch_url(url: str) -> bytes:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.HTTPError as e:
        print(f"Erro ao fazer a requisição para a url: {url}: {e}")
        raise


def generate_url(opt_id: int, sub_opt_id: int = 1, year: int | None = None) -> str:
    params = f"ano={year}&opcao=opt_0{opt_id}&subopcao=subopt_0{sub_opt_id}"
    return BASE_URL + params


def get_year_interval(soup: BeautifulSoup):
    """Obtém o ano de ínicio e de fim que o scraping deve ocorrer."""
    year_label = soup.select_one(".lbl_pesq").get_text()
    match = re.search(r"Ano: \[(\d+)-(\d+)\]", year_label)
    if match:
        start_year, end_year = map(int, match.groups())
        return start_year, end_year
    return 0, 0


def get_sub_options(soup: BeautifulSoup):
    """Obtém as sub opções disponíveis na página."""
    sub_option_buttons = soup.find_all("button", {"class": "btn_sopt"})
    if not sub_option_buttons:
        return ["dados"]

    return format_tag_list(sub_option_buttons)


def scrape_page(
    soup: BeautifulSoup, tab_name: str, tab_id: int, start_year: int, end_year: int
):
    for opt_id, sub_option in enumerate(get_sub_options(soup)):
        file_path = f"{DATA_DIRECTORY}/{tab_name}_{sub_option}.csv"
        if os.path.exists(file_path):
            continue

        rows = []

        table_headers = soup.select_one(".tb_dados > thead > tr").find_all("th")
        col_name, col_quantity, *col_value = format_tag_list(table_headers)

        for year in range(start_year, end_year + 1):
            url = generate_url(tab_id, opt_id + 1, year)
            content = fetch_url(url)
            soup = BeautifulSoup(content, "html.parser")
            table_body = soup.select_one(".tb_dados > tbody")

            parent_id = ""
            for id, row in enumerate(table_body.find_all("tr")):
                columns = row.find_all("td")
                is_parent = (
                    columns[0].has_attr("class") and columns[0]["class"][0] == "tb_item"
                )

                if is_parent:
                    parent_id = id

                product, quantity, *value = [
                    column.get_text(strip=True) for column in columns
                ]

                row_data = {
                    "id": id,
                    "id_pai": "" if is_parent else parent_id,
                    col_name: product,
                    f"{str(year)}_{col_quantity}": quantity,
                }

                # some pages have two year columns: one for quantity other for value
                if value:
                    row_data[f"{str(year)}_{col_value[0]}"] = value[0]

                rows.append(row_data)

            totals = soup.select_one(".tb_dados > .tb_total > tr").find_all("td")
            _, total_quantity, *total_value = [
                total.get_text(strip=True) for total in totals
            ]
            row_data = {
                "id": id + 1,
                "id_pai": "",
                col_name: "TOTAL",
                f"{str(year)}_{col_quantity}": total_quantity,
            }

            if total_value:
                row_data[f"{str(year)}_{col_value[0]}"] = total_value[0]

            rows.append(row_data)

            time.sleep(WAIT_TIME)

        df = pd.DataFrame(rows)
        grouped_df = df.groupby("id").first().sort_values(by="id")
        grouped_df.reset_index(inplace=True)
        os.makedirs(DATA_DIRECTORY, exist_ok=True)
        grouped_df.to_csv(file_path, index=False)
        print(f"Arquivo {file_path} criado com sucesso.")


def scrape_all_pages():
    for tab_name, tab_id in TABS.items():
        url = generate_url(tab_id)
        content = fetch_url(url)
        soup = BeautifulSoup(content, "html.parser")
        start_year, end_year = get_year_interval(soup)
        scrape_page(soup, tab_name, tab_id, start_year, end_year)


if __name__ == "__main__":
    scrape_all_pages()
