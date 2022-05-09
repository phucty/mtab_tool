import csv
import fnmatch
import json
import os
import signal
import urllib
from collections import defaultdict, Counter
from contextlib import closing
from datetime import timedelta
from math import pi
from multiprocessing import Pool
from time import time, sleep

import chardet
import matplotlib.pyplot as plt
import numpy
import pandas
import petl
import requests
from contextlib2 import contextmanager
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm

import m_config as cf

DOMAIN = "https://mtab.app"

DIR_ROOT = "/Users/phucnguyen/git/mtab"

# Dataset Directories
DIR_TABLES = DIR_ROOT + "/data/tables/{challenge}/{data_name}/tables"

# Target files
DIR_CEA_TAR = DIR_ROOT + "/data/tables/{challenge}/{data_name}/cea.csv"
DIR_CTA_TAR = DIR_ROOT + "/data/tables/{challenge}/{data_name}/cta.csv"
DIR_CPA_TAR = DIR_ROOT + "/data/tables/{challenge}/{data_name}/cpa.csv"


DIR_CEA_GT = DIR_ROOT + "/data/tables/{challenge}/{data_name}/gt/CEA_2T_WD_gt.csv"

# Result files
DIR_CEA_RES = DIR_ROOT + "/results/{challenge}/{data_name}/{source}/cea.csv"
DIR_CTA_RES = DIR_ROOT + "/results/{challenge}/{data_name}/{source}/cta.csv"
DIR_CPA_RES = DIR_ROOT + "/results/{challenge}/{data_name}/{source}/cpa.csv"


# Request config
LIMIT_TIME_OUT = 259200  # 2h: 7200 1D: 86400 3D:259200
LIMIT_RETRIES = 3


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise Exception("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def create_dir(file_dir):
    """Create a directory

    Args:
        file_dir (str): file directory
    """
    folder_dir = os.path.dirname(file_dir)
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)


def load_object_csv(file_name, encoding="utf8"):
    content = []
    if os.path.exists(file_name):
        with open(file_name, "r", encoding=encoding, errors="ignore") as f:
            reader = csv.reader(f, delimiter=",")
            for r in reader:
                row_norm = []
                for c in r:
                    row_norm.append(c)
                content.append(row_norm)
    return content


def save_object_csv(file_name, rows):
    create_dir(file_name)
    temp_file = "%s.temp" % file_name
    with open(temp_file, "w") as f:
        try:
            writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
            for r in rows:
                if (
                    isinstance(r, list)
                    or isinstance(r, tuple)
                    or isinstance(r, numpy.ndarray)
                ):
                    writer.writerow(r)
                else:
                    writer.writerow([r])
        except Exception as message:
            print(message)
    if os.path.exists(file_name):
        os.remove(file_name)
    os.rename(temp_file, file_name)


def get_files_from_dir_subdir(folder_path, extension="*"):
    all_files = []
    for root, _, file_dirs in os.walk(folder_path):
        for file_dir in fnmatch.filter(file_dirs, "*.%s" % extension):
            if ".DS_Store" not in file_dir:
                all_files.append(os.path.join(root, file_dir))
    return all_files


def get_files_from_dir(
    folder_path, extension="*", limit_reader=-1, is_sort=False, reverse=False
):
    all_file_dirs = get_files_from_dir_subdir(folder_path, extension)

    if is_sort:
        file_with_size = [(f, os.path.getsize(f)) for f in all_file_dirs]
        file_with_size.sort(key=lambda f: f[1], reverse=reverse)
        all_file_dirs = [f for f, _ in file_with_size]
    if limit_reader < 0:

        limit_reader = len(all_file_dirs)
    return all_file_dirs[:limit_reader]


def get_encoding(source, method="charamel"):
    result = "utf-8"
    if os.path.isfile(source):
        with open(source, "rb") as file_open:
            # Read all content --> make sure about the file encoding
            file_content = file_open.read()

            # predict encoding
            if method == "charamel":
                try:
                    import charamel

                    charamel.Detector()
                    encoding_detector = charamel.Detector()
                    detector = encoding_detector.detect(file_content)
                    if detector:
                        result = detector.value
                except Exception as message:
                    print(message)
                    pass
            else:
                detector = chardet.detect(file_content)
                if detector["encoding"]:
                    result = detector["encoding"]
    return result


def load_table(dir_table):
    def parse_xml_table(source):
        tables_xml = pandas.read_html(source)
        if tables_xml:
            return [tables_xml[0].columns.values.tolist()] + tables_xml[
                0
            ].values.tolist()
        else:
            return None

    table_obj = None
    encoding = get_encoding(dir_table)
    file_ext = os.path.splitext(dir_table)[1][1:]
    if file_ext == "csv":
        table_obj = load_object_csv(dir_table, encoding=encoding)
    elif file_ext == "tsv":
        table_obj = petl.fromtsv(dir_table, encoding=encoding)
    elif file_ext == "txt":
        table_obj = petl.fromtext(dir_table, encoding=encoding)
    elif file_ext == "xls":
        table_obj = petl.fromxls(dir_table, encoding=encoding)
    elif file_ext in ["xlsm", "xlsb", "xltx", "xlsx", "xlt", "xltm"]:
        table_obj = petl.fromxlsx(dir_table)
    elif file_ext == "xml":
        table_obj = parse_xml_table(dir_table)
    cells = []
    if table_obj:
        for row in table_obj:
            row_norm = []
            for col in row:
                tmp_cell = str(col)
                # tmp_cell = ul.norm_text(str(col), punctuations=True, lower=False)
                # tmp_date = ul.get_date(tmp_cell)
                # if tmp_date:
                #     tmp_cell = tmp_date
                row_norm.append(tmp_cell)
            if row_norm:
                # row = ftfy.fix_text(row)
                cells.append(row_norm)

    return cells


TABLE_CATEGORIES = {
    "ALL": ([""], []),
    "CTRL_WIKI": (["WIKI"], ["NOISE2"]),
    "CTRL_DBP": (["CTRL", "DBP"], ["NOISE2"]),
    "CTRL_NOISE2": (["CTRL", "NOISE2"], []),
    "TOUGH_T2D": (["T2D"], ["NOISE2"]),
    "TOUGH_HOMO": (["HOMO"], ["SORTED", "NOISE2"]),
    "TOUGH_MISC": (["MISC"], ["NOISE2"]),
    "TOUGH_MISSP": (["MISSP"], ["NOISE1", "NOISE2"]),
    "TOUGH_SORTED": (["SORTED"], ["NOISE2"]),
    "TOUGH_NOISE1": (["NOISE1"], []),
    "TOUGH_NOISE2": (["TOUGH", "NOISE2"], []),
}


def _is_table_in_cat(x, whitelist, blacklist):
    b = True
    for i in whitelist:
        if not (b and (i in x)):
            return False
    for e in blacklist:
        if not (b and (e not in x)):
            return False
    return True


def precision_score(correct_cells, annotated_cells):
    """
    Precision = (# correctly annotated cells) / (# annotated cells)
    :param correct_cells:
    :param annotated_cells:
    :return:
    """
    return (
        float(len(correct_cells)) / len(annotated_cells)
        if len(annotated_cells) > 0
        else 0.0
    )


def recall_score(correct_cells, gt_cell_ent):
    """
    Recall = (# correctly annotated cells) / (# target cells)
    :param correct_cells:
    :param gt_cell_ent:
    :return:
    """
    return float(len(correct_cells)) / len(gt_cell_ent.keys())


def f1_score(precision, recall):
    """
    F1 Score = (2 * Precision * Recall) / (Precision + Recall)
    :param precision:
    :param recall:
    :return:
    """
    return (
        (2 * precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )


def _get_radar_plot(scores, title):
    categories = list(scores.keys())
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    f = plt.figure()
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)
    plt.yticks([0.25, 0.5, 0.75], ["0.25", "0.50", "0.75"], color="grey", size=7)
    plt.ylim(0, 1)

    values = list(map(lambda x: x["f1"], scores.values()))
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle="solid", label="f1")
    ax.fill(angles, values, "b", alpha=0.1)
    for angle, value in zip(angles, values):
        ax.annotate(
            round(value, 2), (angle, value), size=8, weight="bold", ha="center", c="b"
        )

    values = list(map(lambda x: x["precision"], scores.values()))
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle="solid", label="precision")
    ax.fill(angles, values, "r", alpha=0.1)

    values = list(map(lambda x: x["recall"], scores.values()))
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle="solid", label="recall")
    ax.fill(angles, values, "g", alpha=0.1)

    plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
    plt.title(title, size=11, y=1.1)

    return f


def _write_df(
    df, filename, drop=True, strip=True, index=False, header=True, quoting=csv.QUOTE_ALL
):
    if drop:
        df = df.drop_duplicates()
    if strip:
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df.to_csv(filename, index=index, header=header, quoting=quoting)


def score_cea(gs_file, submission_file):
    scores = {}
    gt = pandas.read_csv(
        gs_file,
        delimiter=",",
        names=["tab_id", "col_id", "row_id", "entity"],
        dtype={"tab_id": str, "col_id": str, "row_id": str, "entity": str},
        keep_default_na=False,
    )
    sub = pandas.read_csv(
        submission_file,
        delimiter=",",
        names=["tab_id", "col_id", "row_id", "entity"],
        dtype={"tab_id": str, "col_id": str, "row_id": str, "entity": str},
        keep_default_na=False,
    )

    gt = gt.to_dict("records")
    sub = sub.to_dict("records")

    gt_cell_ent = dict()
    gt_cell_ent_orig = dict()
    for row in gt:
        cell = "%s %s %s" % (row["tab_id"], row["col_id"], row["row_id"])
        gt_cell_ent[cell] = urllib.parse.unquote(row["entity"]).lower().split(" ")
        gt_cell_ent_orig[cell] = row["entity"].split(" ")

        gt_cell_ent[cell] = [i.replace(cf.WD, "") for i in gt_cell_ent[cell]]
        gt_cell_ent_orig[cell] = [i.replace(cf.WD, "") for i in gt_cell_ent_orig[cell]]

    correct_cells, wrong_cells, annotated_cells = set(), list(), set()
    for row in sub:
        cell = "%s %s %s" % (row["tab_id"], row["col_id"], row["row_id"])
        if cell in gt_cell_ent:
            if cell in annotated_cells:
                raise Exception("Duplicate cells in the submission file")
            else:
                annotated_cells.add(cell)

            annotation = urllib.parse.unquote(row["entity"]).lower()
            if annotation in gt_cell_ent[cell]:
                correct_cells.add(cell)
            else:
                wrong_cells.append(
                    {
                        "table": row["tab_id"],
                        "col": int(row["col_id"]),
                        "row": int(row["row_id"]),
                        "actual": row["entity"],
                        "target": " ".join(gt_cell_ent_orig[cell]),
                    }
                )

    for cat in TABLE_CATEGORIES:
        include, exclude = TABLE_CATEGORIES[cat]
        c_cells = {x for x in correct_cells if _is_table_in_cat(x, include, exclude)}
        a_cells = {x for x in annotated_cells if _is_table_in_cat(x, include, exclude)}
        g_cells = dict(
            filter(
                lambda elem: _is_table_in_cat(elem[0], include, exclude),
                gt_cell_ent.items(),
            )
        )
        if len(g_cells) > 0:
            precision = precision_score(c_cells, a_cells)
            recall = recall_score(c_cells, g_cells)
            f1 = f1_score(precision, recall)
            scores[cat] = {
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "correct": len(c_cells),
                "gt": len(g_cells),
                "submit": len(a_cells),
            }

    return scores


class MTab(object):
    def __init__(self):
        self.F_MTAB = f"{DOMAIN}/api/v1.1/mtab"

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

    def get_table_annotation(self, args):
        try:
            with time_limit(LIMIT_TIME_OUT):
                responds = self._request(self.F_MTAB, args)
        except Exception as message:
            print(message)
            responds = self.get_table_annotation(args)
        return responds


def pool_table_annotation(args):
    responds = {}
    map_row_index = args.pop("map_row_index")
    try:
        mtab_api = MTab()
        responds = mtab_api.get_table_annotation(args)
    except Exception as message:
        print(message)
        responds.update({"status": "Error", "message": message})

    # overloading - try 10 times, 5s / a sleep
    if (not responds or responds["status"] == "Error") and args.get("sleep", 0) < 50:
        sleep(5)
        args.update({"sleep": args.get("sleep", 0) + 5})
        print(args.get("sleep", 0))
        return pool_table_annotation(args)

    if responds.get("semantic") and responds["semantic"].get("cea"):
        responds["semantic"]["cea"] = [
            [map_row_index[r], c, a] for r, c, a in responds["semantic"]["cea"]
        ]
    return args, responds


def load_resources(
    challenge="semtab2020",
    data_name="2T",
    search_mode="a",
    table_limit=0,
    search_limit=50,
    search_expensive=False,
    chunk_size=200,
    chunk_limit=0,
):
    dir_folder_tables = DIR_TABLES.format(challenge=challenge, data_name=data_name)

    # Load tables
    dir_tables = get_files_from_dir(dir_folder_tables, is_sort=True, reverse=False)

    if table_limit:
        dir_tables = dir_tables[:table_limit]

    # Matching targets
    tar_cea, tar_cta, tar_cpa = defaultdict(list), defaultdict(list), defaultdict(list)

    # Load targets
    dir_tar_cea = DIR_CEA_TAR.format(challenge=challenge, data_name=data_name)
    dir_tar_cta = DIR_CTA_TAR.format(challenge=challenge, data_name=data_name)
    dir_tar_cpa = DIR_CPA_TAR.format(challenge=challenge, data_name=data_name)
    # Load target cea
    for line in load_object_csv(dir_tar_cea):
        table_name, row_i, col_i = line[:3]
        tar_cea[table_name].append([row_i, col_i])

    # Load target cta
    for line in load_object_csv(dir_tar_cta):
        table_name, col_i = line[:2]
        tar_cta[table_name].append(col_i)

    # Load target cpa
    for line in load_object_csv(dir_tar_cpa):
        table_name, col_i1, col_i2 = line[:3]
        tar_cpa[table_name].append([col_i1, col_i2])

    # Create input args in chunks
    args = []
    total_cea = 0
    for dir_table in dir_tables:
        table_name = os.path.splitext(os.path.basename(dir_table))[0]
        table_content = load_object_csv(dir_table)
        chunk_tar_cea = tar_cea.get(table_name)
        lines = {row_i for row_i, col_i in chunk_tar_cea}
        lines = sorted(list(lines), key=lambda x: int(x))
        buff_table = []
        buff_line = set()
        buff_line_map = {}
        buff_line_map_inverse = {}
        count_tar = 0
        for line in lines:
            line = int(line)
            buff_line.add(line)
            buff_line_map[line] = len(buff_table)
            buff_line_map_inverse[len(buff_table)] = line
            buff_table.append(table_content[line])
            if len(buff_line) == chunk_size or line == int(lines[-1]):
                chunks_tar_cea_obj = [
                    [str(buff_line_map[int(row_i)]), col_i]
                    for row_i, col_i in chunk_tar_cea
                    if int(row_i) in buff_line
                ]
                args_obj = {
                    "table": buff_table,
                    "table_name": table_name,
                    "tar_cea": chunks_tar_cea_obj,
                    "tar_cta": tar_cta.get(table_name),
                    "tar_cpa": tar_cpa.get(table_name),
                    "search_mode": search_mode,
                    "search_limit": search_limit,
                    "search_expensive": search_expensive,
                    "map_row_index": buff_line_map_inverse,
                }
                count_tar += len(chunks_tar_cea_obj)
                args.append(args_obj)
                buff_line = set()
                buff_table = []
                buff_line_map = {}
                buff_line_map_inverse = {}
        if count_tar != len(chunk_tar_cea):
            print("Missing targets: " + table_name)
        total_cea += count_tar
    if chunk_limit:
        args = args[:chunk_limit]

    total_tables = len(dir_tables)

    return args, total_cea, total_tables


def m_call_run_semtab(
    challenge="semtab2020",
    data_name="2T",
    n_thread=1,
    search_mode="a",
    table_limit=0,
    search_limit=50,
    search_expensive=False,
    chunk_size=200,
    chunk_limit=0,
):
    start = time()
    args, total_cea, total_tables = load_resources(
        challenge,
        data_name,
        search_mode,
        table_limit,
        search_limit,
        search_expensive,
        chunk_size,
        chunk_limit,
    )
    # Call MTab
    res_cea, res_cta, res_cpa = (
        defaultdict(Counter),
        defaultdict(Counter),
        defaultdict(Counter),
    )
    # Save annotation files
    domain = "online"

    dir_cea_res = DIR_CEA_RES.format(
        challenge=challenge, data_name=data_name, source=domain
    )
    dir_cta_res = DIR_CTA_RES.format(
        challenge=challenge, data_name=data_name, source=domain
    )
    dir_cpa_res = DIR_CPA_RES.format(
        challenge=challenge, data_name=data_name, source=domain
    )

    def save_final_result(dir_res_obj, res_obj):
        res_cea_final = []
        for key, values in res_obj.items():
            res_cea_final.append(list(key) + [max(values, key=values.get)])
        res_cea_final.sort(key=lambda x: x[0])
        save_object_csv(dir_res_obj, res_cea_final)
        return res_cea_final

    p_bar = tqdm(total=total_cea)
    processed_tables = set()
    with closing(Pool(processes=n_thread)) as p:
        for input_args, output_args in p.imap_unordered(pool_table_annotation, args):
            processed_tables.add(input_args["table_name"])
            p_bar.update(len(input_args["tar_cea"]))
            p_bar.set_description(
                desc=f"{len(processed_tables)}/{total_tables}. "
                + input_args["table_name"]
            )
            if not output_args or output_args["status"] == "Error":
                if output_args.get("message"):
                    print(output_args.get("message"))
                else:
                    print(
                        "Error: Could not get POST input, please retry again. (The server is overloading now)"
                    )
                continue
            if not output_args.get("semantic"):
                continue
            if output_args["semantic"].get("cea"):
                for r, c, a in output_args["semantic"]["cea"]:
                    res_cea[(output_args["table_name"], r, c)][a] += len(
                        input_args["tar_cea"]
                    )

            if output_args["semantic"].get("cta"):
                for c, a in output_args["semantic"]["cta"]:
                    res_cta[(output_args["table_name"], c)][a[0]] += len(
                        input_args["tar_cea"]
                    )
            if output_args["semantic"].get("cpa"):
                for c1, c2, a in output_args["semantic"]["cpa"]:
                    res_cpa[(output_args["table_name"], c1, c2)][a[0]] += len(
                        input_args["tar_cea"]
                    )

            save_final_result(dir_cea_res, res_cea)
            save_final_result(dir_cta_res, res_cta)
            save_final_result(dir_cpa_res, res_cpa)
    p_bar.close()

    save_final_result(dir_cea_res, res_cea)
    save_final_result(dir_cta_res, res_cta)
    save_final_result(dir_cpa_res, res_cpa)

    print(f"Run time: {str(timedelta(seconds=round(time() - start)))}")


if __name__ == "__main__":
    challenge = "semtab2020"
    data_name = "2T"
    domain = "online"

    m_call_run_semtab(
        challenge=challenge,
        data_name=data_name,
        n_thread=4,
        table_limit=0,
        search_mode="a",
        search_limit=100,
        search_expensive=True,
        chunk_size=200,
        chunk_limit=4,
    )
    scores = score_cea(
        DIR_CEA_GT.format(challenge=challenge, data_name=data_name),
        DIR_CEA_RES.format(challenge=challenge, data_name=data_name, source=domain),
    )
    print(json.dumps(scores, indent=4))


"""
180/180. Z4M8AT89: 100%|██████████████████████████████████████| 667244/667244 [21:53:57<00:00,  8.46it/s]
{
    "ALL": {
        "precision": 0.8954061559997541,
        "recall": 0.8953726073220591,
        "f1": 0.8953893813466541,
        "correct": 597432,
        "gt": 667244,
        "submit": 667219
    }
}
"""
