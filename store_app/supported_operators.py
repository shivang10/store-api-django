def supported_operators(key):
    supported_operators_val = {
        "gt": "$gt",
        "gte": "$gte",
        "eq": "$eq",
        "lt": "$lt",
        "lte": "$lte",
    }

    if key in supported_operators_val:
        return True, supported_operators_val[key]
    else:
        return False, None
