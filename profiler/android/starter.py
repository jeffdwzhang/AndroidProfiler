import time

from profiler.android.utils.log import logger
from profiler.android.device.androiddevice import Adb
from profiler.android.device.androiddevice import AndroidDevice


class Profiler:

    def __init__(self):
        self.adb = Adb()
        self.device = None
        self.monitors = {}
        self.serial_num = None
        self.package_name = None

    def run(self):

        # 检查系统是否支持adb
        if not self.adb.adb_path:
            logger.info("please config adb")
            return

        # 加载配置


        # 检查设备是否已链接
        device_serial_num = self.serial_num
        if not device_serial_num:
            # 若未指定设备，则默认选择第一个已链接的设备
            for i in range(0, 10):
                device_list = self.adb.get_device_list()
                if len(device_list) > 0:
                    device_serial_num = device_list[0]

            if not device_serial_num:
                logger.info("no device")
                return
            logger.info('device serial num : %s' % device_serial_num)
        else:
            is_device_connected = False
            for i in range(0, 10):
                if self.adb.is_connected(device_serial_num):
                    is_device_connected = True
                    break
                else:
                    time.sleep(2)

            if not is_device_connected:
                logger.error("device not found")
                return

        self.device = AndroidDevice()
        if not self.device.is_app_installed(self.package_name):
            logger.error("app not installed")
            return

        # 启动监控



if __name__ == '__main__':
    # 启动性能探测
    logger.info('start profiler')

    profiler = Profiler()

    profiler.run()

    logger.info("profiler end")
