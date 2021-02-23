import requests
from time import time
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class MTabES(object):
    def __init__(self):
        self.URL = "http://119.172.242.147/api/v1/search"
        self.session = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=1,
                        status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def get(self, query_value, limit=20, mode="a", lang="en", expensive=0, info=0):
        query_args = {
            "q": query_value,
            "limit": limit,
            "m": mode,
            "lang": lang,
            "info": info,
            "expensive": expensive
        }
        start = time()
        responds = []
        if not query_value:
            return [], time() - start
        try:
            tmp_responds = requests.get(self.URL, params=query_args)
            # tmp_responds = self.session.get(self.URL, params=query_args)
            if tmp_responds.status_code == 200:
                tmp_responds = tmp_responds.json()
                if tmp_responds.get("hits"):
                    if info:
                        responds = [[r["id"], r["score"], r["label"], r["des"]] for r in tmp_responds["hits"]]
                    else:
                        responds = [[r["id"], r["score"]] for r in tmp_responds["hits"]]
        except Exception as message:
            print(f"\n{message}\n{str(query_args)}")
        run_time = time() - start
        return responds, run_time


if __name__ == "__main__":
    mtab_es = MTabES()
    queries = [
        "Sweden",
        "TV-Browser",
        "hideaki takeda",
        "HIdeki Tedaka",
        "2MASS J10540655-0031018",
        "Tokyo",
        "武田英明",
        "Град Скопјее",
        "Préfecture de Kanagawa",
        "Paulys Realenzyklopädie der klassischen Altertumswissenschaft",
        "La gran bretaña",
        "제주 유나이티드 FC",
        "অ্যাটলেটিকো ডি কলকাতা",
        "Nguyễn Ái Quốc",
        "ホー・チ・ミン",
    ]
    modes = ["a"]  # "a", "b", "f"
    langs = ["en"]  # "en", "all"
    expensives = [0]  # 0, 1
    info = 1
    for query in queries:
        for mode in modes:
            for lang in langs:
                for expensive in expensives:
                    responds, run_time = mtab_es.get(query, limit=20, mode=mode, lang=lang, expensive=expensive, info=info)
                    print(f"\n[{lang}|{mode}|{expensive}] About {len(responds)} results in {run_time:.4f} seconds | {query}")

                    if info:
                        for i, (r, s, l, d) in enumerate(responds[:3]):
                            print(f"{i + 1:2}. {s:.4f} - {r}[{l}] - {d}")
                    else:
                        for i, (r, s) in enumerate(responds[:3]):
                            print(f"{i+1:2}. {s:.4f} - {r}[]")

