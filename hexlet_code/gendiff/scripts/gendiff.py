import argparse
import json


def generate_diff(file1, file2):
    myKeys = list(file1.keys())
    myKeys.sort()
    sorted_dict1 = {i: file1[i] for i in myKeys}
    myKeys = list(file2.keys())
    myKeys.sort()
    sorted_dict2 = {i: file2[i] for i in myKeys}
    output = {}
    for i, j in sorted_dict1.items():
        flag = False
        for a, b in sorted_dict2.items():
            if i == a and j == b:
                flag = True
        if flag:
            output[str(i)] = j
            # output += '  ' + str(i) + ': ' + str(j) + '\n'
        else:
            output['- ' + str(i)] = j
            # output += '- ' + str(i) + ': ' + str(j) + '\n'
    for i, j in sorted_dict2.items():
        flag = True
        for a, b in sorted_dict1.items():
            if i == a and j == b:
                flag = False
        if flag:
            output['+ ' + str(i)] = j
            # output += '+ ' + str(i) + ': ' + str(j) + '\n'
    return output


def main():
    parser = argparse.ArgumentParser(description='giving info')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    result = (generate_diff(json.load(open(args.first_file)),
                            json.load(open(args.second_file))))
    for i, j in result.items():
        print(i, j)
    # generate_diff(json.load(open('hexlet_code/gendiff/files/file1.json')),
    # json.load(open('hexlet_code/gendiff/files/file2.json')))


if __name__ == '__main__':
    main()
