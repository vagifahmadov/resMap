from setting.config import *
# from setting.db import mongo, mssql, con_mssql, mysql, con_mysql
import random


def return_output(data, message, status):
    return {"message": message, "data": data, "status": status}


def validate(request_data, validate_list):
    validation_list = []
    request_keys = []
    result = []
    valid_sub_key = []
    main_keys_only = []
    status_code = 200
    for key, value in validate_list.items():
        validation_list.append(key)  # to load given validation key

    for key, value in request_data.items():
        if key not in validation_list:
            main_keys_only.append(key)
        request_keys.append(key)  # to load request keys
        if type(value) is dict:
            for k, v in value.items():
                if k not in validation_list:
                    valid_sub_key.append(key + "." + k)
                request_keys.append(k)  # to load request sub keys
        else:
            if value is None or not value or value == " ":
                status_code = validate_list[key]

    keys_difference = list(set(validation_list) - set(request_keys))  # find difference

    if keys_difference:
        # if keys is invalid
        status_code = 1005
        if valid_sub_key:
            if len(valid_sub_key) == len(keys_difference) and len(valid_sub_key) == 1:
                output = {"request": valid_sub_key[0],
                          'actually': str(valid_sub_key[0]).split(".")[0] + "." + keys_difference[0]}
            elif len(valid_sub_key) == len(keys_difference):
                output = {"request": valid_sub_key, 'actuallySubKeys': keys_difference}
            else:
                output = {"request": {"mainKeys": main_keys_only, "subKeys": valid_sub_key},
                          "actually": keys_difference}
                # output=keys_difference+valid_sub_key
        else:
            if len(main_keys_only) > 0:
                if len(keys_difference) == 1:
                    print(main_keys_only)
                    output = {"request": main_keys_only[0], "actually": keys_difference[0]}
                else:
                    output = {"request": {"mainKeys": main_keys_only}, "actually": keys_difference}
            else:
                if len(keys_difference) == 1:
                    actually = keys_difference[0]
                else:
                    actually = keys_difference
                output = {"Request": "No such key", "actually": actually}
    else:
        # if key valid and no values
        for k_v, v_v in request_data.items():
            if type(v_v) is dict:
                for k, v in v_v.items():
                    if type(v_v[k]) is not bool and not v_v[k]:  # if value is not empty or not bool
                        result.append(k_v + "." + k)
                        status_code = validate_list[k]
                        break
            if not request_data[k_v]:
                result.append(k_v)
                status_code = validate_list[k_v]
        output = result

    return {"code": status_code, 'data': output}


def current_full_str_date():
    return strftime("%d.%m.%Y %H:%M:%S", localtime())


def current_str_date():
    today = date.today()
    return today.strftime("%d.%m.%Y")


def current_str_time():
    format_time = "%H:%M"
    return datetime.now().time().strftime(format_time)


def current_full_obj_date():
    full_format_date = "%d.%m.%Y %H:%M:%S"
    return datetime.today().strptime(current_full_str_date(), full_format_date)


def insert_query_helper(values_and_rows: list, type_element: str):
    """
    This function is helps to make insert query
    :param values_and_rows:
    :param type_element:
    :return:
    """
    query_elements = []
    list(map(lambda u: u.update({str(next(iter(u.keys()))): '\'' + str(next(iter(u.values()))) + '\''}) if type(
        u[str(next(iter(u.keys())))]) is str else None, values_and_rows))
    if type_element == "keys":
        list(map(lambda ql: query_elements.append(str(next(iter(ql.keys()))) + ", "), values_and_rows))
    elif type_element == "values":
        list(map(lambda ql: query_elements.append(str(next(iter(ql.values()))) + ", "), values_and_rows))
        query_elements = list(map(lambda q: q.replace("''", "'"), query_elements))
    else:
        return None
    query_elements[-1] = query_elements[-1][:-2]
    result = "".join(query_elements)
    return result


def update_query_helper(query: str, values_and_rows: list, statement: str):
    """
    This function is helps to make insert query
    :param statement:
    :param values_and_rows:
    :param query:
    :return:
    """
    query_elements = []
    helper_str_add = ""
    values_and_rows = list(filter(lambda f: str(next(iter(f.keys()))) != statement, values_and_rows))
    list(map(lambda u: u.update({str(next(iter(u.keys()))): "'" + str(next(iter(u.values()))) + "'"}) if type(
        u[str(next(iter(u.keys())))]) is str else None, values_and_rows))
    list(map(lambda q: query_elements.append(str(next(iter(q.keys()))) + "=" + str(next(iter(q.values()))) + ", "),
             values_and_rows))
    helper_str_add = helper_str_add.join(query_elements)
    query += helper_str_add
    result = query[:-2]
    return result


def query_maker(table: str, values_and_rows: list, type_query: str, statement: str = '', statement_type: str = '',
                compare_value=None):
    """
    This method modeling the query
    :param compare_value:
    :param statement_type:
    :param statement: <condition> (it works if type_query is update)
    :param type_query: <update> / <insert>
    :param table: <table name>
    :param values_and_rows: {<row>: <value>}
    :return: full sql query
    """
    result = None
    query = ""
    type_query = type_query.lower()
    if type_query in ["update", "insert"]:
        if type_query == "update" and len(statement) > 0 and len(statement_type) > 0 and compare_value is not None:
            query = query + "UPDATE " + str(table) + " SET "
            query = update_query_helper(query=query, values_and_rows=values_and_rows, statement=statement)
            result = query + " WHERE " + str(statement) + statement_type + str(compare_value) + ";"
        elif type_query == "insert":
            query = query + "INSERT INTO " + str(table) + " ("
            helper = insert_query_helper(values_and_rows=values_and_rows, type_element="keys")
            query = None if helper is None else query + helper + ") VALUES ("
            if query is not None:
                helper = insert_query_helper(values_and_rows=values_and_rows, type_element="values")
                query = None if helper is None else query + helper + ");"
            result = query
    return result


def big_datas():
    """
    It gets all datas from file and returns as JSON data via pandas.
    :return: JSON data
    """
    # get all datas from xls file using pandas
    excel_data_df = pandas.read_excel('./db.xlsx', sheet_name='Sayfa1')
    json_str = excel_data_df.to_json()
    json_json = json.loads(json_str)
    # print(json_json)
    return json_json


def jinja_data_maker(titles: list, datas: dict, col: str = None, parameter_value=None):
    """
    It wants titles for get row data as json object. All rows (json datas) are merged in list.
    :param col:
    :param parameter_value:
    :param titles:
    :param datas:
    :return:
    """
    # make data structure for jinja2
    try:
        titles = list(filter(lambda t: type(t) == str and t != '', titles))
        len_rows = len(datas[titles[0]])
        jinja2_datas = list(map(lambda d: reduce(lambda k, v: {**k, **v},
                                                 list(map(lambda tl: {tl: datas[tl][str(d)], 'id': str(d)}, titles))),
                                range(len_rows)))
        if 'Rate' in titles:
            list(map(lambda d: d.update({'noneStared': 5 - round(d['Rate']), 'stared': round(d['Rate'])}), jinja2_datas))
        if 'Review_Rate_1' in titles and 'Review_Rate_2' in titles and 'Review_Rate_3' in titles:
            list(map(lambda n: list(map(lambda d: d.update({'noneStaredRReview_{n}'.format(n=n): 5 - round(int(str(d['Review_Rate_{n}'.format(n=n)]).split(" ")[0])), 'staredRReview_{n}'.format(n=n): round(int(str(d['Review_Rate_{n}'.format(n=n)]).split(" ")[0]))}), jinja2_datas)), range(1, 4)))
        if parameter_value is not None and col is not None:
            jinja2_datas = list(filter(lambda d: d[col] == parameter_value, jinja2_datas))
            jinja2_datas = None if len(jinja2_datas) == 0 else jinja2_datas[0]
    except KeyError as er:
        print(er)
        jinja2_datas = None
    return jinja2_datas
