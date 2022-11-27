import re


def get_values(val, field):
    data = val[field]
    operator_type = "".join(re.split("[^a-zA-Z]*", data))
    value = re.findall(r'\d+', data)
    return int(value[0]), operator_type
