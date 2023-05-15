from gendiff import generate_diff
import json

deep_json1 = r'C:\Users\Алексей\PycharmProjects\diff-calc\tests\fixtures\file1.json'
deep_json2 = r'C:\Users\Алексей\PycharmProjects\diff-calc\tests\fixtures\file2.json'
t = json.load(open(deep_json1))
h = json.load(open(deep_json2))
diff = generate_diff(t, h)
print(diff)
