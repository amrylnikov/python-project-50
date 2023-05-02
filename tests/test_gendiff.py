from hexlet_code.gendiff.scripts.gendiff import generate_diff
import json


def test_generate_diff():
    path1 = 'hexlet_code/gendiff/files/file1.json'
    path2 = 'hexlet_code/gendiff/files/file2.json'
    result = {'- follow': False,
              'host': 'hexlet.io',
              '- proxy': '123.234.53.22',
              '- timeout': 50, '+ timeout': 20,
              '+ verbose': True}
    assert generate_diff(json.load(open(path1)),
                         json.load(open(path2))) == result
