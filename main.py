import argparse
import os
import time


from tools.Utils import *


class Main(object):
    def __init__(self, file1, file2):
        super().__init__()
        self.f1 = file1
        self.f2 = file2
        # 保存 测试机 和 对比机 的文件内容
        self.content_1 = None
        self.content_2 = None

    def load_log_file(self):
        # 读文件内容
        with open(self.f1, 'r', encoding='utf-8', errors='ignore') as f:
            self.content_1 = f.readlines()
        with open(self.f2, 'r', encoding='utf-8', errors='ignore') as f:
            self.content_2 = f.readlines()


    def get_info(self):
        info1 = get_keywords_and_timestamp(self.content_1)
        info2 = get_keywords_and_timestamp(self.content_2)
        return info1, info2

    def general_android_result(self):
        print("程序开始执行， 开始解析文件。。。")
        self.load_log_file()
        info1, info2 = self.get_info()
        print("文件解析完成， 开始生成excel。。。")
        # 文件名称
        current_directory = os.path.dirname(os.path.abspath(__file__))
        t = time.strftime("%m-%d_%H_%M", time.localtime())
        save_dir = os.path.join(current_directory, 'result')
        os.mkdir(save_dir) if not os.path.exists(save_dir) else None
        xlsx_general(info1, info2, save_dir+ '\\results_'+ t + '.xlsx')
        print('表格生成结束，文件保存路径: ' + save_dir + '\\results_' + t + '.xlsx')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'please enter two parameters a and b ...'
    parser.add_argument("-c", "--c", help="bugreport patch", type=str, default="")
    parser.add_argument("-d", "--d", help="contrast patch", type=str, default="")
    args = parser.parse_args()

    main = Main(args.c, args.d)
    try:
        main.general_android_result()
    except Exception as e:
        print(e)
    # logger.info('5s 后窗口关闭。。。')
    # time.sleep(5)
    # os.system("taskkill /f /im cmd.exe")  # 关闭cmd窗口