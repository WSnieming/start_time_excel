import os


get_devices_command = os.popen('adb devices')

devices_info = get_devices_command.read().strip('').split('\n')
devices_list = list()
for device in devices_info[1:]:
    if len(device) > 2:
        device_name = device.split('\t')[0]
        devices_list.append(device_name)
print(devices_list)
