import sys
import os.path
from tbl import Tbl

first_row = []
all_rows = []
result = {}

def tokenize_first_row(list = []):
    for item in list:
        item = item.strip()
        if not item[0] == '?':
            first_row.append(item)
            result[item] = []
        else:
            first_row.append(False)


def tokenize_row(list = []):
    skips = 0
    for i, item in enumerate(list):
        item = item.strip()
        if item == '':
            skips = skips + 1
            continue
        try:
            val = float(item)
        except ValueError:
            if item == 'True' or item == 'true' or item == 'TRUE' or item == 't' or item == 'T':
                val = True
            elif item == 'False' or item == 'false' or item == 'FALSE' or item == 'f' or item == 'F':
                val = False
            else:
                val = item
        index = i - skips
        if first_row[index] and index < len(first_row):
            result[first_row[index]].append(val)


def main(file_name):
    if not os.path.exists(file_name):
        print("File {} does not exist in current path\n".format(file_name))
        return
    print("File {} exist in current path\n".format(file_name))
    first = True
    for line in open(file_name):  # POM3A.csv file.csv
        if first:
            first = False
            first_row_list = line.split(',')
            tokenize_first_row(first_row_list)
            print("{}\n".format(first_row))
        else:
            # all_rows.append(line.split('#')[0].split(','))
            all_rows.append(line.split('#')[0])

    weird_rows = {}
    skip_next = False
    l = len(all_rows)

    for index, row in enumerate(all_rows):
        row = row.strip()
        if skip_next:
            skip_next = False
            continue
        if row == '' or len(row) == 0 :
            continue
        if row[-1] == ',':
            skip_next = True
            if index < (l - 1):
                weird_rows[index] = {"current": row, "next": all_rows[index + 1]}
        else:
            tokenize_row(row.split(','))

    prev_key = -2
    for key in weird_rows.keys():
        if key - prev_key > 1:
            item = weird_rows[key]
            tokenize_row(item.get("current").split(',') + item.get("next").split(','))
        prev_key = key

    # print(result)
    #for key in result.keys():
    #    print("{}:\t{}\n".format(key, result.get(key)))
    tbl = Tbl()
    tbl.consume(result)
    tbl.calculate_dom()
    my_list = tbl.get_ret()
    sorted_my_list = sorted(my_list, key=lambda k: k['dom_val'], reverse=True)


    if len(sorted_my_list) > 10:
        print("Top 5 dominating items\n")
        for item in sorted_my_list[:5]:
            print(item.get('val').cells)

        print("\n\nLast 5 dominating items\n")
        for item in sorted_my_list[-5:]:
            print(item.get('val').cells)
    else:
        print("\n\nItems in sorted list\n")
        for item in sorted_my_list:
            print(item.get('val').cells)
        


if __name__ == "__main__":
    #main("test.csv")
    if len(sys.argv) > 1:
         main(sys.argv[1])
    else:
         print("Please enter the .csv file name")



