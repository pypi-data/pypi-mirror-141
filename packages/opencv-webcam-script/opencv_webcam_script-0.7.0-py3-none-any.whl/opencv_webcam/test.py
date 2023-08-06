import sys
from utils.fonts_opt import fonts_color

ROOT_PATH = sys.path[0]  # 项目根目录


# 日志管理
def log_management(logContent, logName, logSaveMode):
    logFile = open(f'{ROOT_PATH}/{logName}', logSaveMode)  # 日志文件
    logFile.write(logContent)  # 日志写入


if __name__ == '__main__':
    str01 = '\033[94m' + 'abc' + '\033[0m' + \
        'abc' + '\033[92m' + 'abc' + '\033[0m'
    a, b = fonts_color()
    for k in a.keys():
        str01 = str01.replace(a[k], '').replace(b, '')

    log_management(str01, "abc.log", "w")
