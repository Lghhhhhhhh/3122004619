import re
import jieba
import jieba.analyse
import numpy
from scipy import spatial

numpy.seterr(divide='ignore', invalid='ignore')

"""" 
查阅信息，发现有两种实现方法，一种是利用jieba库分词，一种是利用simhash计算文本相似度，由于老师给的文本长度足够，故舍弃simhash方法
当然分词处理也有长文本与短文本的处理，长文本需要提取高频词，而短文本可以扫描全文提取全部词
"""


class DuplicateChecking:
    def __init__(self):
        self.original_text = ""
        self.compare_text = ""
        self.original_list = []
        self.compare_list = []
        self.word_store = []

    # 读取原始文件与需要查重的文件
    def read_file(self):
        """
        提示读取地址，并通过地址打开文本写入类成员中
        若使用read()方法，在大文件操作下会有卡死的风险
        所以使用readlines方法读取，将文件每一行都变成列表的一个元素
        """

        print("请输入原始论文的地址（绝对路径）：")
        original_text_address = input()
        print("请输入查重论文的地址（绝对路径）：")
        compare_text_address = input()
        try:
            with open(original_text_address, "r", encoding="utf-8") as file1:

                # self.original_text = file1.read()
                self.original_list = file1.readlines()
                self.original_text = self.original_text.join(self.original_list)
        except FileNotFoundError:
            # 提示该文件不存在
            print("原文件 " + original_text_address + " 文件不存在")
            original_text_address = ""

        try:
            with open(compare_text_address, "r", encoding="utf-8") as file2:
                self.compare_list = file2.readlines()
                self.compare_text = self.compare_text.join(self.compare_list)
        except FileNotFoundError:
            print("查重文件 " + compare_text_address + " 文件不存在")
            compare_text_address = ""

        if original_text_address == "" or compare_text_address == "":
            self.original_text = ""
            self.compare_text = ""
            self.compare_list = []
            self.original_list = []
            return False
        return True

    def short_text_preprocess(self):
        # 预处理，去除所有标点符号,分词，合并
        remove_chars = '[\x20\\t\\n。·’!"\\\\#$%&\'()＃！（）*+,-./:;<=>?\\@，：?￥★、…．＞【】［］《》？“”‘’\\[\\]^_`{|}~]+'
        # remove_chars=u"[^a-zA-Z0-9\u4e00-\u9fa5]"

        self.original_text = re.sub(remove_chars, "", self.original_text)
        self.compare_text = re.sub(remove_chars, "", self.compare_text)
        self.original_list = list(jieba.lcut(self.original_text))
        self.compare_list = list(jieba.lcut(self.compare_text))
        self.word_store = list(set(self.original_list + self.compare_list))
        return True

    def long_text_preprocess(self):
        remove_chars = '[\x20\\t\\n。·’!"\\\\#$%&\'()＃！（）*+,-./:;<=>?\\@，：?￥★、…．＞【】［］《》？“”‘’\\[\\]^_`{|}~]+'
        # remove_chars=u"[^a-zA-Z0-9\u4e00-\u9fa5]"

        self.original_text = re.sub(remove_chars, "", self.original_text)
        self.compare_text = re.sub(remove_chars, "", self.compare_text)

        # 默认20个关键字
        self.original_list = list(set(jieba.analyse.extract_tags(self.original_text, 20)))
        self.compare_list = list(set(jieba.analyse.extract_tags(self.compare_text, 20)))
        return True

    def text_checking(self):
        """
        判断采用短文本方法还是长文本方法，一般字数超过500则要选用长文本
        """

        original_vector = []
        compare_vector = []
        if not self.read_file():
            return False
        if len(self.original_text) > 1000 or len(self.compare_text) > 1000:
            self.long_text_preprocess()
        else:
            self.short_text_preprocess()
        # 合并分词列表
        self.word_store = list(set((self.original_list + self.compare_list)))
        for word in self.word_store:
            original_vector.append(self.original_list.count(word))
            compare_vector.append(self.compare_list.count(word))

        original_vector = numpy.array(original_vector)
        compare_vector = numpy.array(compare_vector)

        # 三种计算方法，结果是一样的
        cos_sim = 1 - spatial.distance.cosine(original_vector, compare_vector)

        # 写入文件中

        print("请输入查重数据文件输出的地址：")
        duplicate_data_address = input()
        try:
            with open(duplicate_data_address, "w", encoding="utf-8") as file:
                file.write("查重文本与原文本相似度为：" + str(round(cos_sim, 2)))
                print("查重数据已经输入到文件中！！！")
        except IOError:
            print("查重数据文件创建失败，请重启程序！！！")
        return True


if __name__ == '__main__':
    a = DuplicateChecking()
    a.text_checking()
