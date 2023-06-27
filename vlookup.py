import csv

# - input file
# - source of vlookup
# - list of items you want to vlookup
# output file
# -list of items you want to vlookup: the value

# vlookup(input_column,source_range,column,is_sorted=T/F)


# hash = {
#     A1: ("a", 0)
#     c26: ("z", 25)
# }

# arr = [("a", 0).......("z", 25)]

library = {}
requirement = []

def getSheetInfo(source_file):
    source = None
    with open('input/{}.csv'.format(source_file), newline='') as csvfile:
        if source_file not in library:
            library[source_file] = {
                "sheet_hash_map": dict(),
                "sheet_value_list": list(),
                "sheet_processing": False
            }
        
        source = library[source_file]
        reader = csv.DictReader(csvfile)
        idx = 0
        if source["sheet_processing"]:
            return source
        for row in reader:
            source["sheet_value_list"].append([])

            for key, val in row.items():
                new_key = "{}{}".format(key, idx+1)
                source["sheet_hash_map"][new_key] = (val, idx)
                source["sheet_value_list"][idx].append(val)
            idx+=1
        source["sheet_processing"] = True
        # print("sheet_hash_map: ",source["sheet_hash_map"])
        # print("-"*20)
        # print("sheet_value_list: ", source["sheet_value_list"])
    return source



def linearSearch(source, input_column, source_range, column, col_range):
    print("input_column, source_range, column, is_sorted: ",input_column, source_range, column)
    col_range = col_range.split(":")
    start = source["sheet_hash_map"][col_range[0]]
    end = source["sheet_hash_map"][col_range[1]]
    idx = start[1]
    while idx<=end[1]:
        row = source["sheet_value_list"][idx]
        # print("input_column: ", input_column, input_column in row)
        if input_column in row:
            # print("found")
            return row[int(column)-1]
        idx+=1
    return None

def binarySearch(source, input_column, source_range, column, col_range):
    col_range = col_range.split(":")
    start = source["sheet_hash_map"][col_range[0]]
    end = source["sheet_hash_map"][col_range[1]]
    start, end = start[1], end[1]

    while start<=end:
        mid = (start+end)//2
        row = source["sheet_value_list"][mid]
        search_idx = 0
        if input_column == row[search_idx]:
            return row[int(column)-1]
        if int(input_column) < int(row[search_idx]):
            end = mid
        else:
            start = mid+1
        print(start, end, row[search_idx], input_column, (row[search_idx]> input_column), (row[search_idx] < input_column))
    return None

def vlookup(input_column, source_range, column, is_sorted=True):

    source_file, col_range = source_range.split("!")
    source = getSheetInfo(source_file)
    
    if not is_sorted: 
        return linearSearch(source, input_column, source_range, column, col_range)
    else:
        return binarySearch(source, input_column, source_range, column, col_range)
    # print(source["sheet_value_list"][start[1]:end[1]])
    




def main():
    with open('input/sheet2.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        sheet2_hash_map = dict()
        idx=0
        for row in reader:
            requirement.append(dict())
            current_obj = requirement[idx]
            for key, val in row.items():
                new_key = "{}{}".format(key, idx+1)
                current_obj[new_key] = val

                if val.startswith("=VLOOKUP"):
                    command = val[len("=VLOOKUP("):-1].split(",")
                    if command[0] not in current_obj:
                        raise Exception("column := {} not found".format(command[0]))
                    current_obj[new_key] = vlookup(current_obj[command[0]], *command[1:])
                    print("current_obj[new_key]: ", current_obj[new_key])
            idx+=1
        for obj in requirement:
            print(obj)


main()