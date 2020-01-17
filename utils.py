def str_to_list(string):
    return [int(s) for s in string.split(' ')]

def list_to_str(lst):
    return " ".join([str(elem) for elem in lst])
