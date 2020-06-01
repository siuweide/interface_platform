from ddt import ddt, file_data
import unittest
import requests

@ddt
class RunCase(unittest.TestCase):

    @file_data('./test_data.json')
    def test_file_data_json(self, method, url, data):
        if method == "post":
            res = requests.post(url, data)
            print(res.text)

if __name__ == '__main__':
    unittest.main()