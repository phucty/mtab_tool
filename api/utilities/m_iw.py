import csv
import fnmatch
import os
import pandas
import numpy as np
import petl as petl


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
                    or isinstance(r, np.ndarray)
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
