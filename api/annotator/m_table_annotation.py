import json
import os
from collections import defaultdict
from contextlib import closing
from datetime import timedelta
from time import time, sleep
from multiprocessing import Pool

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from tqdm import tqdm

from api.utilities import m_iw

# Request config
LIMIT_TIME_OUT = 7200  # 2h: 7200 - 24h: 86400 -3days:259200
LIMIT_RETRIES = 3


class MTab(object):
    def __init__(self):
        self.F_MTAB = "https://mtab.app/api/v1.1/mtab"
        # self.F_MTAB = "http://localhost:5000/api/v1.1/mtab"

        self.session = requests.Session()
        retries = Retry(
            total=LIMIT_RETRIES,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def _request(self, func_name, query_args, retries=3, message=""):
        responds = defaultdict()
        if retries == 0:
            print(message)
            return responds
        try:
            # _responds = requests.post(func_name, json=query_args, timeout=self.TIME_OUT)
            _responds = self.session.post(
                func_name, json=query_args, timeout=LIMIT_TIME_OUT
            )
            if _responds.status_code == 200:
                responds = _responds.json()
                if not responds or (
                    responds.get("status") == "Error" and not responds.get("message")
                ):
                    sleep(300)
                    return self._request(
                        func_name,
                        query_args,
                        retries - 1,
                        message=f"Error: Retry {retries-1}",
                    )
        except Exception as message:
            if func_name == self.F_MTAB and query_args.get("table_name"):
                args_info = func_name + ": " + query_args.get("table_name")
            else:
                args_info = func_name
            sleep(300)
            return self._request(
                func_name, query_args, retries - 1, message=f"\n{message} - {args_info}"
            )
        return responds

    def get_table_annotation(
        self,
        table_content,
        table_name="",
        predict_target=False,
        tar_cea=None,
        tar_cta=None,
        tar_cpa=None,
        search_mode="a",
        search_limit=50,
        debug=False,
    ):
        query_args = {
            "table_name": table_name,
            "table": table_content,
            "predict_target": predict_target,
            "tar_cea": tar_cea,
            "tar_cta": tar_cta,
            "tar_cpa": tar_cpa,
            "search_mode": search_mode,
            "search_limit": search_limit,
            "debug": debug,
        }
        responds = self._request(self.F_MTAB, query_args)
        return responds


def example_table_annotation():
    mtab_api = MTab()

    # Table file
    dir_table = "/Users/phucnguyen/Downloads/0AJSJYAL.xltx"
    # dir_table = f"/Users/phucnguyen/git/dprofile/data/tables/wikitable_1.xlsx"
    table_name = os.path.splitext(os.path.basename(dir_table))[0]
    table_content = m_iw.load_table(dir_table)

    # Run 1: Let MTab predict annotation targets
    responds_auto = mtab_api.get_table_annotation(
        table_content,
        table_name=table_name,
        predict_target=True,  # Set this is True
        search_mode="a",  # Using aggregation search
        search_limit=100,  # candidate entity generation limit
        debug=True,  # return all candidates, and their confidence scores in CEA tasks
    )

    print(json.dumps(responds_auto, indent=2))

    # Run 2: provide annotation targets

    # Annotation targets
    # tar_cea = [
    #     [1, 0],
    #     [2, 0],
    #     [3, 0],
    #     [4, 0],
    #     [5, 0],
    #     [6, 0],
    #     [7, 0],
    #     [8, 0],
    #     [9, 0],
    #     [10, 0],
    # ]
    # tar_cta = [0]
    # tar_cpa = [[0, 1], [0, 2]]
    #
    # responds = mtab_api.get_table_annotation(
    #     table_content,
    #     table_name=table_name,
    #     tar_cea=tar_cea,
    #     tar_cta=tar_cta,
    #     tar_cpa=tar_cpa,
    #     search_mode="a",
    # )
    # print(responds)


if __name__ == "__main__":
    example_table_annotation()
