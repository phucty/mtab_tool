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


# Responds
# [en|a|0] About 20 results in 0.0621 seconds | hideaki takeda
#  1. 0.4854 - Q2330082[Hideaki Takeda] - Japanese association football player
#  2. 0.4854 - Q57886243[Hideaki Takeda] - informatics researcher, National Institute of Informatics, Japan
#  3. 0.1214 - Q51530155[Hiroaki Takeda] - researcher
#
# [en|a|0] About 20 results in 0.1739 seconds | Sweden
#  1. 0.2856 - Q34[Sweden] - sovereign state in northern Europe
#  2. 0.2831 - Q424644[Sweden] - Wikimedia disambiguation page
#  3. 0.2830 - Q37437749[Sweden] - family name
#
# [en|a|0] About 20 results in 0.1027 seconds | TV-Browser
#  1. 0.4968 - Q1715028[TV-Browser] - electronic program guide (tv, radio)
#  2. 0.1183 - Q399128[Browser] - Wikimedia disambiguation page
#  3. 0.1183 - Q11334456[Browser] - None
#
# [en|a|0] About 20 results in 0.0546 seconds | HIdeki Tedaka
#  1. 0.2796 - Q4924099[Hideki Todaka] - Japanese boxer
#  2. 0.2360 - Q5752358[Hideki] - male given name
#  3. 0.2359 - Q52319792[Hideki] - Japanese mangaka
#
# [en|a|0] About 20 results in 0.6296 seconds | 2MASS J10540655-0031018
#  1. 0.3943 - Q222120[2MASS J00540655-0031018] - brown dwarf
#  2. 0.2285 - Q87130330[TYC 4151-458-1] - None
#  3. 0.0419 - Q89756929[TYC 5033-427-1] - None
#
# [en|a|0] About 20 results in 0.1050 seconds | Tokyo
#  1. 0.2843 - Q1490[Tokyo] - capital and most populous prefecture of Japan
#  2. 0.2833 - Q396867[Tokyo] - Wikimedia disambiguation page
#  3. 0.2833 - Q65120889[Tokyo] - None
#
# [en|a|0] About 20 results in 0.0433 seconds | 武田英明
#  1. 0.4456 - Q2330082[Hideaki Takeda] - Japanese association football player
#  2. 0.4455 - Q57886243[Hideaki Takeda] - informatics researcher, National Institute of Informatics, Japan
#  3. 0.0284 - Q27920828[Q27920828] - None
#
# [en|a|0] About 20 results in 0.0567 seconds | Град Скопјее
#  1. 0.5780 - Q2575820[Greater Skopje] - administrative division within the Republic of Macedonia constituted of 10 municipalities
#  2. 0.0783 - Q515[city] - large permanent human settlement
#  3. 0.0775 - Q1500094[grad] - place name element meaning 'town'
#
# [en|a|0] About 13 results in 0.1200 seconds | Préfecture de Kanagawa
#  1. 0.5809 - Q127513[Kanagawa Prefecture] - prefecture of Japan
#  2. 0.0771 - Q22800853[Q22800853] - Wikimedia template
#  3. 0.0284 - Q22800872[Q22800872] - Wikimedia template
#
# [en|a|0] About 20 results in 0.0815 seconds | Paulys Realenzyklopädie der klassischen Altertumswissenschaft
#  1. 0.5782 - Q1138524[Paulys Realenzyklopädie der klassischen Altertumswissenschaft] - extensive and comprehensive German encyclopedia of classical scholarship
#  2. 0.0009 - Q19250471[Mesembria (Pauly-Wissowa)] - cross-reference in Paulys Realencyclopädie der classischen Altertumswissenschaft (RE)
#  3. 0.0005 - Q47459707[Paulys Realencyclopädie der classischen Altertumswissenschaft] - document published in 1997
#
# [en|a|0] About 19 results in 0.0856 seconds | La gran bretaña
#  1. 0.5792 - Q2841[Bogota] - capital city of Colombia
#  2. 0.0804 - Q145[United Kingdom] - country in Western Europe
#  3. 0.0776 - Q23666[Great Britain] - island in the North Atlantic off the north-west coast of continental Europe
#
# [en|a|0] About 13 results in 0.0598 seconds | 제주 유나이티드 FC
#  1. 0.5784 - Q482617[Jeju United FC] - football club in South Korea
#  2. 0.0284 - Q4591117[1996-2005 Jeju United FC (Bucheon Yukong / Bucheon SK) seasons] - South Korean football seasons
#  3. 0.0116 - Q14592084[2012 Jeju United FC season] - season of football team
#
# [en|a|0] About 20 results in 0.0345 seconds | অ্যাটলেটিকো ডি কলকাতা
#  1. 0.5787 - Q16836329[ATK] - association football club
#  2. 0.0771 - Q22003383[D.D Bhawalkar] - Indian Optical Physicist
#  3. 0.0105 - Q14221200[North Kolkata] - Northern parts and some suburbs of the city of joy kolkata
#
# [en|a|0] About 20 results in 0.0695 seconds | Nguyễn Ái Quốc
#  1. 0.4461 - Q36014[Ho Chi Minh] - Vietnamese communist leader and Chairman of the Workers' Party of Vietnam (1890-1969)
#  2. 0.4455 - Q12901199[Q12901199] - None
#  3. 0.4455 - Q10742909[Q10742909] - None
#
# [en|a|0] About 20 results in 0.0946 seconds | ホー・チ・ミン
#  1. 0.5786 - Q36014[Ho Chi Minh] - Vietnamese communist leader and Chairman of the Workers' Party of Vietnam (1890-1969)
#  2. 0.0771 - Q7410171[Category:Ho Chi Minh] - Wikimedia category
#  3. 0.0105 - Q874234[Ho Chi Minh Mausoleum] - None
