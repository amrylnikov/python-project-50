import argparse
import json
import yaml


# def generate_diff(file1, file2):
#     myKeys = list(file1.keys())
#     myKeys.sort()
#     sorted_dict1 = {i: file1[i] for i in myKeys}
#     myKeys = list(file2.keys())
#     myKeys.sort()
#     sorted_dict2 = {i: file2[i] for i in myKeys}
#     print("Sortet 1:", sorted_dict1)
#     print("Sortet 2:", sorted_dict2)
#     output = {}
#     index_list1 = list(sorted_dict1.keys())
#     for index1, value1 in sorted_dict1.items():
#         flag = False
#         for index2, value2 in sorted_dict2.items():
#             if index1 == index2:
#                 flag = True
#                 if value1 == value2:
#                     output[str(index1)] = value1
#                 else:
#                     output['- ' + str(index1)] = value1
#                     output['+ ' + str(index1)] = value2
#             if index2 not in index_list1 and index2 < index1:
#                 output['+ ' + str(index2)] = value2
#         if flag is False:
#             output['- ' + str(index1)] = value1
#     # add all from dict 2 that is not in dict 1 aka "+"
#     for index2, value2 in sorted_dict2.items():
#         flag = True
#         for index1, value1 in sorted_dict1.items():
#             if index2 == index1:
#                 flag = False
#         if flag:
#             output['+ ' + str(index2)] = value2
#     return output


def diff(unsorted_dict1, unsorted_dict2):
    myKeys = list(unsorted_dict1.keys())
    myKeys.sort()
    dict1 = {i: unsorted_dict1[i] for i in myKeys}
    myKeys = list(unsorted_dict2.keys())
    myKeys.sort()
    dict2 = {i: unsorted_dict2[i] for i in myKeys}
    output = {}
    for index1, value1 in dict1.items():
        flag = True
        for index2, value2 in dict2.items():
            # Если ключи равны и оба значения -- словари, то рекурсируем в них
            if index1 == index2 and type(value1) is dict and type(value2) is dict:
                flag = False
                output[index1] = diff(value1, value2)
            else:
                if index1 == index2:
                    flag = False
                    if value1 == value2:
                        output[str(index1)] = value1
                    elif value1 != value2:
                        output["- " + str(index1)] = value1
                        output["+ " + str(index1)] = value2
                if index2 not in list(dict1.keys()) and index2 < index1:
                    output['+ ' + str(index2)] = value2
        if flag:
            output["- " + str(index1)] = value1
    # add all from dict 2 that is not in dict 1 aka "+"
    for index2, value2 in dict2.items():
        flag = True
        for index1, value1 in dict1.items():
            if index2 == index1:
                flag = False
        if flag:
            output['+ ' + str(index2)] = value2
    return output


def generate_diff(unsorted_dict1, unsorted_dict2, path=''):
    myKeys = list(unsorted_dict1.keys())
    myKeys.sort()
    dict1 = {i: unsorted_dict1[i] for i in myKeys}
    myKeys = list(unsorted_dict2.keys())
    myKeys.sort()
    dict2 = {i: unsorted_dict2[i] for i in myKeys}
    default_path = path
    path_keys = []
    output_plain = ''
    for index1, value1 in dict1.items():
        if path != '':
            path += '.' + str(index1)
        else:
            path = str(index1)
        flag = True
        for index2, value2 in dict2.items():
            # Если ключи равны и оба значения -- словари, то рекурсируем в них
            if index1 == index2 and type(value1) is dict and type(value2) is dict:
                flag = False
                output_plain += generate_diff(value1, value2, path)
            else:
                path_before = path
                if index2 not in list(dict1.keys()) and index2 < index1:
                    path = default_path + '.' + str(index2)
                    if path not in path_keys:
                        if type(value2) is dict:
                            output_plain += "Property \'" + path + '\' was added with value: ' + '[complex value]' + "\n"
                        else:
                            output_plain += "Property \'" + path + '\' was added with value: \'' + str(value2) + '\'' + "\n"
                    path_keys.append(path)
                path = path_before
                if index1 == index2:
                    flag = False
                    # Всё сложно. Тут надо проверить, переменную на словарь и стринговость
                    if value1 != value2 and type(value1) is not str:
                        if type(value2) is dict:
                            output_plain += "Property \'" + path + '\' was updated. From ' + str(value1) + ' to ' + '[complex value]' + "\n"
                        elif type(value1) is dict:
                            output_plain += "Property \'" + path + '\' was updated. From ' + '[complex value]' + ' to ' + str(value2) + "\n"
                        elif type(value1) is dict and type(value2) is dict:
                            output_plain += "Property \'" + path + '\' was updated. From ' + '[complex value]' + ' to ' + '[complex value]' + "\n"
                        else:
                            output_plain += "Property \'" + path + '\' was updated. From ' + str(value1) + ' to ' + str(value2) + "\n"
                    if value1 != value2 and type(value1) is str:
                        if type(value2) is dict:
                            output_plain += "Property \'" + path + '\' was updated. From \'' + str(value1) + '\' to ' + '[complex value]' + "\n"
                        elif type(value1) is dict:
                            output_plain += "Property \'" + path + '\' was updated. From ' + '[complex value]' + ' to \'' + str(value2) + '\'' + "\n"
                        elif type(value1) is dict and type(value2) is dict:
                            output_plain += "Property \'" + path + '\' was updated. From ' + '[complex value]' + ' to ' + '[complex value]' + "\n"
                        else:
                            output_plain += "Property \'" + path + '\' was updated. From \'' + str(value1) + '\' to \'' + str(value2) + '\'' + "\n"
        path = default_path
        if flag:
            if default_path != '':
                path += '.' + str(index1)
            else:
                path = str(index1)
            output_plain += "Property \'" + path + '\' was removed: ' + "\n"
        path = default_path
    # add all from dict 2 that is not in dict 1 aka "+"
    for index2, value2 in dict2.items():
        flag = True
        if path != '':
            path += '.' + str(index2)
        else:
            path = str(index2)
        for index1, value1 in dict1.items():
            if index2 == index1:
                flag = False
        if flag and path not in path_keys:
            if type(value2) is dict:
                output_plain += "Property \'" + path + '\' was added with value: ' + '[complex value]' + "\n"
            else:
                output_plain += "Property \'" + path + '\' was added with value: \'' + str(value2) + '\'' + "\n"
        path = default_path
    return output_plain


def stylish(dict1):
    str_dict = json.dumps(dict1, indent=4)
    trans1 = str_dict.replace('\"', '')
    trans2 = trans1.replace('  + ', '+ ')
    trans3 = trans2.replace('  - ', '- ')
    trans4 = trans3.replace(',', '')
    return trans4


def main():
    parser = argparse.ArgumentParser(description='giving info')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    if args.first_file[-4:] == 'json':
        data1 = json.load(open(args.first_file))
    elif (args.first_file[-4:] == '.yml'
            or args.first_file[-4:] == 'yaml'):
        with open(args.first_file) as f:
            data1 = yaml.load(f, Loader=yaml.FullLoader)
    if args.second_file[-4:] == 'json':
        data2 = json.load(open(args.second_file))
    elif ((args.second_file[-4:] == '.yml'
            or args.second_file[-4:] == 'yaml')):
        with open(args.second_file) as f:
            data2 = yaml.load(f, Loader=yaml.FullLoader)
    if args.format == 'plain':
        result = generate_diff(data1, data2)
    elif args.format == 'json':
        result = json.dumps(diff(data1, data2))
    else:
        result = stylish(diff(data1, data2))
    print(result)

    # file1 = r"C:\Users\Алексей\PycharmProjects\diff-calc\hexlet_code\gendiff\files\file1.json"
    # file2 = r"C:\Users\Алексей\PycharmProjects\diff-calc\hexlet_code\gendiff\files\file2.json"
    # file1_new = r"C:\Users\Алексей\PycharmProjects\diff-calc\tests\fixtures\file1.json"
    # file2_new = r"C:\Users\Алексей\PycharmProjects\diff-calc\tests\fixtures\file2.json"
    # a_old = json.load(open(file1))
    # b_old = json.load(open(file2))
    # print(generate_diff(a_old, b_old))
    # q = {
    #     "host": "hexlet.io",
    #     "timeout": 50,
    #     "proxy": "123.234.53.22",
    #     "follow": False
    # }
    # w = {
    #     "timeout": 20,
    #     "verbose": True,
    #     "host": "hexlet.io"
    # }
    # a = {
    #         "common": {
    #             "setting1": "Value 2"
    #         },
    #         "group1": {
    #             "a": "s",
    #             "c": 5
    #         }
    # }
    # b = {
    #         "common": {
    #             "setting1": "Value 1",
    #             "setting2": 200
    #         },
    #         "group1": {
    #             "a": "s"
    #         },
    #         "zzz": {
    #             "m": 23
    #         }
    # }
    # z = {
    #     "common": {
    #         "setting1": "Value 1",
    #         "setting2": 200,
    #         "setting3": True,
    #         "setting6": {
    #             "key": "value",
    #             "doge": {
    #                 "wow": ""
    #             }
    #         }
    #     },
    #     "group1": {
    #         "baz": "bas",
    #         "foo": "bar",
    #         "nest": {
    #             "key": "value"
    #         }
    #     },
    #     "group2": {
    #         "abc": 12345,
    #         "deep": {
    #             "id": 45
    #         }
    #     }
    # }
    # x = {
    #     "common": {
    #         "follow": False,
    #         "setting1": "Value 1",
    #         "setting3": None,
    #         "setting4": "blah blah",
    #         "setting5": {
    #             "key5": "value5"
    #         },
    #         "setting6": {
    #             "key": "value",
    #             "ops": "vops",
    #             "doge": {
    #                 "wow": "so much"
    #             }
    #         }
    #     },
    #     "group1": {
    #         "foo": "bar",
    #         "baz": "bars",
    #         "nest": "str"
    #     },
    #     "group3": {
    #         "deep": {
    #             "id": {
    #                 "number": 45
    #             }
    #         },
    #         "fee": 100500
    #     }
    # }
    # deep_json1 = r'C:\Users\Алексей\PycharmProjects\diff-calc\tests\fixtures\file1.json'
    # deep_json2 = r'C:\Users\Алексей\PycharmProjects\diff-calc\tests\fixtures\file2.json'
    # t = json.load(open(deep_json1))
    # h = json.load(open(deep_json2))
    # print(t)
    # print(h)
    # m = diff_plain(z, x)
    # d = stylish(m)
    # f = None
    # l = json.dumps(f)
    # print(l)


if __name__ == '__main__':
    main()
