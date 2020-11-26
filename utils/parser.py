import os
import re
import csv
from typing import List
from locale import atof, setlocale, LC_NUMERIC

import requests
from bs4 import BeautifulSoup


class Parser:
    GOOGLE_BASE_URL = 'https://www.google.com/search?q='
    DEFAULT_HEADER = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    BEHIND_THE_NAME_REQ_URL = 'https://www.behindthename.com/api/lookup.json?name='
    BEHIND_API_KEY = 'on615856678'

    @classmethod
    def run(cls, opt, args):
        if opt == '-f':
            input_names = cls.__read_file(args)
        else:
            input_names = args

        names = [name.strip() for name in input_names.split(',')]
        results = []

        print('-----------------------------------------------')
        session = requests.Session()

        for name in names:
            if not name:
                continue
            print(f"Name: {name}")
            count = cls.__get_google_search_count_by_name(name.lower(), session)
            name_origin = cls.__get_origin_by_name(name.lower(), session)
            result = {
                "name": name,
                "count": count,
                "origin": 'None' if name_origin is None else ','.join(name_origin)
            }
            results.append(result)
            print('-----------------------------------------------')

        sort_result = sorted(results, key = lambda i: i['count'], reverse=True)
        print(f"Exporting as the CSV file....")
        cls.__to_csv(sort_result)
        print("Ended!")

    @staticmethod
    def __to_csv(data):
        if len(data) == 0:
            print("No data.")
            return;

        keys = data[0].keys()
        with open('result.csv', 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    @staticmethod
    def __read_file(path: str) -> str:
        if not os.path.isfile(path):
            raise FileNotFoundError()

        file = open(path, "r")
        return file.read()

    @staticmethod
    def __to_number(num: str) -> int:
        setlocale(LC_NUMERIC, '')
        return int(atof(num))

    @classmethod
    def __get_origin_by_name(cls, name, session, raise_exception: bool = True):
        url = cls.BEHIND_THE_NAME_REQ_URL + name + '&key=' + cls.BEHIND_API_KEY + ''
        usage = []
        try:
            response = session.get(url)
            response.raise_for_status()
            json_response = response.json()

            if "error_code" in json_response:
                usage.append('Name could not be found.')
                return

            usages = json_response[0].get('usages')
            for u in usages:
                if 'usage_full' in u:
                    usage.append(u.get('usage_full'))
        except Exception as err:
            if raise_exception:
                raise err
            else:
                usage.append(str(err))

        print(f"Origins: {usage}")
        return usage

    @classmethod
    def __get_google_search_count_by_name(cls, name, session, raise_exception: bool = True):
        url = cls.GOOGLE_BASE_URL + name

        try:
            response = session.get(url, headers=cls.DEFAULT_HEADER)
            search_result = BeautifulSoup(response.content, features="lxml")

            if len(search_result.select("#result-stats")) == 0:
                return 0

            result_stats = search_result.select("#result-stats")[0].get_text()
            match = re.search("(\d{1,3}(,\d{3})+)", result_stats)
            if not match:
                return 0

            count = cls.__to_number(match.group())
        except Exception as e:
            if raise_exception:
                raise e
            else:
                count = 0
                print(e)

        print(f"Google Search Result Count: about {count}")
        return count
