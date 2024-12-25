import os
import shutil
import tempfile
import time
import zipfile

current_directory = os.path.dirname(os.path.abspath(__file__))

def get_devices():
    get_devices_command = os.popen('adb devices')
    devices_info = get_devices_command.read().strip('').split('\n')
    devices_list = list()
    for device in devices_info[1:]:
        if len(device) > 2:
            device_name = device.split('\t')[0]
            devices_list.append(device_name)
    if len(devices_list) == 0:
        print('未找到设备, 请检查设备是否链接正常!')
        exit()
    elif len(devices_list) > 2:
        print('设备数量过多, 最多支持两台设备同时连接.')
        exit()
    return devices_list

'''
获取 bugreport, 解压缩, 对 bugreport_xxxxx.txt 重命名
'''
def get_bugreport(devices_list):
    bugreport_txt_file_list = list()
    t = time.strftime("%H_%M", time.localtime())
    save_dir = current_directory+ '\\bugreport'
    os.mkdir(save_dir) if not os.path.exists(save_dir) else None
    for devices_name in devices_list:
        zip_file_path = save_dir + '\\bug_' + devices_name +'_'+t +'.zip'
        command = ('adb -s ' + devices_name + ' bugreport ' +zip_file_path)
        print(devices_name + "设备 bugreport 抓取......")
        command_result = os.popen(command).read()
        print(command_result)
        print(devices_name+'设备 bugreport获取成功!')

        print('解压缩 bugreport...')
        extraction_directory = zip_file_path.replace('.zip', '')
        unzip_file(zip_file_path, extraction_directory)
        print('解压缩完成...')

        # 获取最终的 bugreport.txt 的路径
        file_list = os.listdir(extraction_directory)
        for f in file_list:
            if f.startswith('bugreport') and f.endswith('.txt'):
                new_file_name = 'bugreport_'+devices_name+'.txt'
                new_file_name = os.path.join(extraction_directory, new_file_name)
                old_file_name = os.path.join(extraction_directory, f)
                os.rename(old_file_name, new_file_name)
                bugreport_txt_file_list.append(new_file_name)
    return bugreport_txt_file_list

def unzip_file(zip_path, extract_dir):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, temp_dir)
                dst_path = os.path.join(extract_dir, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.move(src_path, dst_path)


if __name__ == '__main__':
    file_name = 'D:\Documents\Desktop\start_tools\start_time_excel\\.zip'
    result = file_name.replace('.zip', '')
    unzip_file(file_name, result)
    file_list = os.listdir(result)
    for file_name in file_list:
        print(file_name)
    # unzip_file(file_name, file_name.replace('.zip', ''))
