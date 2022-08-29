import subprocess

from profiler.android.utils.log import logger


class Adb(object):
    adb_path = None
    os_name = None

    def __init__(self, device_serial_num=None):
        self._adb_path = Adb.get_adb_path()
        self._device_serial_num = device_serial_num

    @staticmethod
    def get_adb_path():
        if Adb.adb_path:
            return Adb.adb_path

        logger.info("try get adb path")
        # 先探测一下当前环境变量中是否有adb可用，如果系统有配置，优先使用系统的
        proc = subprocess.Popen("adb devices", stdout=subprocess.PIPE, shell=True)
        result = proc.stdout.read()
        if not isinstance(result, str):
            result = str(result, 'utf-8')
        logger.debug(result)
        if result and len(result.strip()) > 0 and 'command not found' not in result:
            Adb.adb_path = 'adb'
            return Adb.adb_path

        logger.info("adb not found in system")

    @staticmethod
    def get_device_list():
        proc = subprocess.Popen("adb devices", stdout=subprocess.PIPE, shell=True)
        result = proc.stdout.read()
        if not isinstance(result, str):
            result = str(result, 'utf-8')

        result = result.replace('\r', '').splitlines()

        device_list = []
        if len(result) < 1:
            return device_list
        for info in result[1:]:
            if len(info.strip()) == 0 or '\t' not in info:
                continue
            if info.split('\t')[1] == 'device':
                device_list.append(info.split('\t')[0])

        return device_list

    @staticmethod
    def is_connected(serial_num):
        return serial_num in Adb.get_device_list()

    def _run_cmd_once(self, cmd, *argv):

        cmdlet = [self._adb_path, cmd]

        for i in range(len(argv)):
            arg = argv[i]
            if not isinstance(arg, str):
                arg = str(arg, 'utf-8')
            cmdlet.append(arg)

        cmdStr = " ".join(cmdlet)
        logger.info(cmdStr)

        process = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=True)

        (out, error) = process.communicate()

        if not isinstance(out, str):
            try:
                out = str(out, 'utf-8')
            except Exception as e:
                out = repr(e)
        return out.strip()

    def _run_adb_cmd(self, cmd, *argv):
        retry_cnt = 3
        while retry_cnt > 0:
            ret = self._run_cmd_once(cmd, *argv)
            if ret:
                break
            retry_cnt = retry_cnt-1

        return ret

    def run_shell_cmd(self, cmd):

        ret = self._run_adb_cmd('shell', '%s' % cmd)
        if ret:
            logger.error('adb cmd failed:%s' % cmd)
        return ret


class AndroidDevice(object):

    def __init__(self, device_serial_num=None):
        self._is_local = False
        self._serial_num = device_serial_num
        self._adb = Adb(self._serial_num)

    @staticmethod
    def is_local_device(device_id):
        if not device_id:
            return True

    def list_app_installed(self):

        result = self._adb.run_shell_cmd('pm list packages')
        if not isinstance(result, str):
            result = str(result, 'utf_8')

        result = result.replace('\r', '').splitlines()

        installed_app_list = []
        for info in result:
            if not 'package' in info:
                continue
            if info.split(':')[0] == 'package':
                installed_app_list.append(info.split(':')[1])

        return installed_app_list

    def is_app_installed(self, package_name):
        return package_name in self.list_app_installed()
