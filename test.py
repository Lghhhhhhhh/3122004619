import unittest
import random
from main import DuplicateChecking
from unittest.mock import patch  # 用于模拟输入

original_text = [r'C:\Users\Lenovo\Desktop\测试集\orig.txt', r'C:\Users\Lenovo\Desktop\测试集\短orig.txt', '666', '777',
                 '888', '999']
test_text = [r'C:\Users\Lenovo\Desktop\测试集\orig_0.8_add.txt',
             r'C:\Users\Lenovo\Desktop\测试集\orig_0.8_del.txt',
             r'C:\Users\Lenovo\Desktop\测试集\orig_0.8_dis_1.txt',
             r'C:\Users\Lenovo\Desktop\测试集\orig_0.8_dis_10.txt',
             r'C:\Users\Lenovo\Desktop\测试集\orig_0.8_dis_15.txt',
             r'C:\Users\Lenovo\Desktop\测试集\短compare.txt',
             '666', '777', '888', '999']


class MyTestCase(unittest.TestCase):
    @patch('builtins.input')
    def test_IO(self, mock_input):
        result = DuplicateChecking()
        mock_input.side_effect = [original_text[0], test_text[random.randint(0, 4)]]  # 正确的输入
        self.assertEqual(result.read_file(), True)
        mock_input.side_effect = [original_text[1], test_text[5]]  # 正确的输入
        self.assertEqual(result.read_file(), True)
        mock_input.side_effect = [original_text[random.randint(2, 5)], test_text[random.randint(6, 9)]]  # 错误的输入
        self.assertEqual(result.read_file(), False)

    @patch('builtins.input')
    def test_long_text_preprocess(self, mock_input):
        result = DuplicateChecking()
        mock_input.side_effect = [original_text[0], test_text[random.randint(0, 4)]]  # 正确的输入
        result.read_file()
        self.assertEqual(result.long_text_preprocess(), True)

    def test_short_text_preprocess(self):
        result = DuplicateChecking()
        result.original_text = "废话覅哦说不定v哦i被释冯绍峰放北京库房不玩"
        result.compare_text = "我IC呢嫩IC那我可浪放放瑟夫费钱农村"
        self.assertEqual(result.short_text_preprocess(), True)

    @patch('builtins.input')
    def test_text_checking(self, mock_input):
        result = DuplicateChecking()
        mock_input.side_effect = [original_text[0], test_text[random.randint(0, 4)],
                                  r'C:\Users\Lenovo\Desktop\测试集\查重数据.txt']  # 正确的输入
        self.assertEqual(result.text_checking(), True)

        mock_input.side_effect = [original_text[1], test_text[5],
                                  r'C:\Users\Lenovo\Desktop\测试集\查重数据.txt']  # 正确的输入
        self.assertEqual(result.text_checking(), True)

        mock_input.side_effect = [original_text[random.randint(2, 5)], test_text[random.randint(6, 9)],
                                  r'C:\Users\Lenovo\Desktop\测试集\查重数据.txt']  # 正确的输入
        self.assertEqual(result.text_checking(), False)


if __name__ == '__main__':
    unittest.main()
