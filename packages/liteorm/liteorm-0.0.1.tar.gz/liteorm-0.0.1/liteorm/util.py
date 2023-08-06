def cov_table2dict(key_list: list or tuple, value_list: list) -> list:
    result = []
    for record in value_list:
        record_dict = {}
        index = 0
        for col in record:
            record_dict[key_list[index]] = col
            index += 1
        result.append(record_dict)
    return result
