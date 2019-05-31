import datetime
import itertools
import re

BASE_URL = "http://www.feriadoschilenos.cl/{from_year}-{to_year}.html"


def list_contains_element_with_class(class_name, elements_list):
    return len(list(filter(lambda x: class_name in x.classes, elements_list))) > 0


def parse_holidays(info_node):
    rows = [list(x[1]) for x in itertools.groupby(info_node, lambda x: x.tag == "br") if not x[0]]
    holidays = []
    for row in rows:
        complex_date_str = row[0].text_content()
        m_date_str = re.search(r"[^\s]+\s+([^\s]+)", complex_date_str)
        if not m_date_str:
            print("Could not parse date from", complex_date_str)
            continue
        date_str = datetime.datetime.strptime(m_date_str.group(1), "%d/%m/%Y").strftime("%Y-%m-%d")

        isIrrenunciable = list_contains_element_with_class("esIrrenunciable", row)
        isRecurrente = list_contains_element_with_class("esRecurrente", row)
        isReligioso = list_contains_element_with_class("esReligioso", row)
        isSingular = list_contains_element_with_class("esSingular", row)
        isEscolar = list_contains_element_with_class("esEscolar", row)
        isLocal = list_contains_element_with_class("esLocal", row)
        locality = None
        if isLocal:
            locality_node = list(filter(lambda x: "esLocal" in x.classes, row))
            m_locality = re.search(r"\(válido solamente en (.+)\)", locality_node[0].text)
            if m_locality:
                locality = m_locality.group(1)
            else:
                print("Could not parse locality for date", date_str)

        name = None

        name_node_candidates = list(filter(lambda x: x.tag == "a", row))
        if name_node_candidates:
            name = name_node_candidates[0].text

        holidays.append({
            "date": date_str,
            "name": name,
            "irrenunciable": isIrrenunciable,
            "recurrente": isRecurrente,
            "religioso": isReligioso,
            "singular": isSingular,
            "escolar": isEscolar,
            "local": isLocal,
            "locality": locality,
        })
    return holidays


def year_ranges_between(from_year, to_year):

    floor_year = int((from_year-1)/10)*10+1
    ceil_year = int((to_year-1)/10)*10+10

    starting_years_per_range = list(range(floor_year, ceil_year + 1, 10))

    return [[x, x + 9] for x in starting_years_per_range]


if __name__ == "__main__":
    import argparse
    import json

    import urllib.request
    import lxml.html

    parser = argparse.ArgumentParser("Chilean holidays scrapper for the site www.feriadoschilenos.cl")
    parser.add_argument("from_year", type=int, help="starting year for the list of holidays (included)")
    parser.add_argument("to_year", type=int, help="ending year for the list of holidays (included)")
    #parser.add_argument("urls", nargs="+", help="a list of urls like the following http://www.feriadoschilenos.cl/2011-2020.html")

    args = parser.parse_args()
    from_year = args.from_year
    to_year = args.to_year
    if to_year < from_year:
        print("Invalid year range")
        exit(-1)

    if from_year < 1981 or to_year > 2100:
        print("Year range must be in the range [1981,2100]")
        exit(-1)

    url_year_ranges = year_ranges_between(from_year, to_year)

    urls = [
        BASE_URL.format(from_year=x[0], to_year=x[1])
        for x in url_year_ranges
    ]

    holidays_by_year = {}

    for url in urls:
        http_response = urllib.request.urlopen(url)
        root = lxml.html.fromstring(http_response.read())

        current_year_node = root.xpath("/html/body/h2[1]")[0]

        while current_year_node.tag == "h2":
            current_year_info_node = current_year_node.getnext()
            year = current_year_node.text

            if int(year) in range(from_year, to_year + 1):
                holidays = parse_holidays(current_year_info_node)
                holidays_by_year[year] = holidays

            current_year_node = current_year_info_node.getnext()

    print(json.dumps(holidays_by_year, indent=4, separators=(',', ': ')))
