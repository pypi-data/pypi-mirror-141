import os

import openpyxl

from .globals import SHEET, VCARD


def read_file_xlsx_data(fn):
    global SHEET
    assert os.path.isfile(fn), "文件不存在"

    execl = openpyxl.load_workbook(fn)
    sheet = execl.active
    if SHEET is not None:
        sheet = execl[SHEET]

    i = 1
    ds = {}
    while True:
        k = chr(64+i)
        value = sheet[k + "1"].value
        if not value:
            break
        ds[value] = i-1
        i += 1

    okds = {}
    for k in VCARD:
        if VCARD[k] in ds:
            okds[VCARD[k]] = ds[VCARD[k]]

    if (VCARD["N"] not in okds) or (VCARD["TEL"] not in okds):
        print("缺少必要数据\n--help 显示帮助信息")
        return 1
    
    f = 0
    # data = []
    for r in sheet.rows:
        f+=1
        if f<=1:
            continue
        
        data_one = {}
        for k in VCARD:
            n = okds.get(VCARD[k])
            if n is None:
                continue

            data_one[k] = r[n].value
        yield data_one


def read_file_csv_data(fn):
    return