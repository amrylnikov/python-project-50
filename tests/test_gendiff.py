# from hexlet_code.gendiff.scripts.gendiff import diff, stylish
from gendiff import diff, stylish
import json
import yaml


def test_generate_diff():
    json1 = 'tests/fixtures/old_file1.json'
    json2 = 'tests/fixtures/old_file2.json'
    yml1 = 'tests/fixtures/file1.yml'
    yml2 = 'tests/fixtures/file2.yml'
    # deep_json1 = 'tests/fixtures/file1.json'
    # deep_json2 = 'tests/fixtures/file2.json'
    with open(yml1) as f:
        data1 = yaml.load(f, Loader=yaml.FullLoader)
    with open(yml2) as f:
        data2 = yaml.load(f, Loader=yaml.FullLoader)
    result = '''{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}'''
#     result_line = '{\n    common: {\n      + follow: false\n        setting1: Value 1\n      - setting2: 200\n      - setting3: true\n      + setting3: null\n      + setting4: blah blah\n      + setting5: {\n            key5: value5\n        }\n        setting6: {\n            doge: {\n              - wow: \n              + wow: so much\n            }\n            key: value\n          + ops: vops\n        }\n    }\n    group1: {\n      - baz: bas\n      + baz: bars\n        foo: bar\n      - nest: {\n            key: value\n        }\n      + nest: str\n    }\n  - group2: {\n        abc: 12345\n        deep: {\n            id: 45\n        }\n    }\n  + group3: {\n        deep: {\n            id: {\n                number: 45\n            }\n        }\n        fee: 100500\n    }\n}' == '{\n    common: {\n      + follow: false\n        setting1: Value 1\n      - setting2: 200\n      - setting3: true\n      + setting3: null\n      + setting4: blah blah\n      + setting5: {\n            key5: value5\n        }\n        setting6: {\n            doge: {\n              - wow:\n              + wow: so much\n            }\n            key: value\n          + ops: vops\n        }\n    }\n    group1: {\n      - baz: bas\n      + baz: bars\n        foo: bar\n      - nest: {\n            key: value\n        }\n      + nest: str\n    }\n  - group2: {\n        abc: 12345\n        deep: {\n            id: 45\n        }\n    }\n  + group3: {\n        deep: {\n            id: {\n                number: 45\n            }\n        }\n        fee: 100500\n    }\n}'
#     result_large = '''{
#     common: {
#       + follow: false
#         setting1: Value 1
#       - setting2: 200
#       - setting3: true
#       + setting3: null
#       + setting4: blah blah
#       + setting5: {
#             key5: value5
#         }
#         setting6: {
#             doge: {
#               - wow:
#               + wow: so much
#             }
#             key: value
#           + ops: vops
#         }
#     }
#     group1: {
#       - baz: bas
#       + baz: bars
#         foo: bar
#       - nest: {
#             key: value
#         }
#       + nest: str
#     }
#   - group2: {
#         abc: 12345
#         deep: {
#             id: 45
#         }
#     }
#   + group3: {
#         deep: {
#             id: {
#                 number: 45
#             }
#         }
#         fee: 100500
#     }
# }'''
    assert stylish(diff(json.load(open(json1)),
                        json.load(open(json2)))) == result
    assert stylish(diff(data1, data2)) == result
    # print(stylish(diff(json.load(open(deep_json1)),
    #                     json.load(open(deep_json2)))))
