import argparse
import os
import time

from deal_with_bugreport import get_bugreport, get_devices
from tools.Utils import *


class Main(object):
    def __init__(self, file1, file2=None):
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
        if self.f2 is not None:
            with open(self.f2, 'r', encoding='utf-8', errors='ignore') as f:
                self.content_2 = f.readlines()


    def get_info(self):
        info1 = get_keywords_and_timestamp(self.content_1)
        if self.content_2 is not None:
            info2 = get_keywords_and_timestamp(self.content_2)
            return info1, info2
        return info1, None

    def general_android_result(self):
        print("程序开始执行， 开始解析文件。。。")
        self.load_log_file()
        info1, info2 = self.get_info()
        if info2 is None:
            print('文件内容缺失...')
            exit()
        print("文件解析完成， 开始生成excel。。。")
        # 文件名称
        current_directory = os.path.dirname(os.path.abspath(__file__))
        t = time.strftime("%m-%d_%H_%M", time.localtime())
        save_dir = os.path.join(current_directory, 'result')
        os.mkdir(save_dir) if not os.path.exists(save_dir) else None
        xlsx_general(info1, info2, save_dir+ '\\results_'+ t + '.xlsx')
        print('表格生成结束，文件保存路径: ' + save_dir + '\\results_' + t + '.xlsx')

    #单机生成excel
    def general_one_device(self):
        print("程序开始执行， 开始解析文件。。。")
        self.load_log_file()
        info1, info2 = self.get_info()
        print("文件解析完成， 开始生成excel。。。")
        # 文件名称
        current_directory = os.path.dirname(os.path.abspath(__file__))
        t = time.strftime("%m-%d_%H_%M", time.localtime())
        save_dir = os.path.join(current_directory, 'result')
        os.mkdir(save_dir) if not os.path.exists(save_dir) else None
        _, _, dev_info, _ = info1
        d_name, _ = dev_info
        result_file = save_dir + '\\results_' + d_name + '_' + t + '.xlsx'
        one_devices_excel(info1, result_file)
        print('表格生成结束，文件保存路径: ' + result_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'please enter two parameters a and b ...'
    parser.add_argument("-c", "--c", help="bugreport patch", type=str, default="auto")
    parser.add_argument("-d", "--d", help="contrast patch", type=str, default="auto")
    args = parser.parse_args()
    if args.c == "auto" and args.d == "auto":   #连接设备直接生成逻辑
        bugreport_txt_file_list = get_bugreport(get_devices())
        if len(bugreport_txt_file_list) == 1:
            main = Main(bugreport_txt_file_list[0])
            main.general_one_device()
        elif len(bugreport_txt_file_list) == 2:
            main = Main(bugreport_txt_file_list[0], bugreport_txt_file_list[1])
            main.general_android_result()
        else:
            print('未找到对应log文件, 请检查bugreport是否抓取成功...')
    elif args.c != "auto" and args.d != "auto":
        main = Main(args.c, args.d)
        main.general_android_result()
    else:
        print('参数错误, 请参考使用说明运行程序!')
        exit()
    # logger.info('5s 后窗口关闭。。。')
    # time.sleep(5)
    # os.system("taskkill /f /im cmd.exe")  # 关闭cmd窗口