# 字体管理
# 创建人：曾逸夫
# 创建时间：2022-01-27


import os
import sys

ROOT_PATH = sys.path[0]  # 项目根目录

fonts_list = ['SimSun.ttc', 'TimesNewRoman.ttf']  # 字体列表
fonts_suffix = ['ttc', 'ttf', 'otf']  # 字体后缀


# 创建字体库
def add_fronts():
    os.system(f'if [ ! -d "./fonts" ]; then mkdir ./fonts; fi; cd ./fonts; wget -c -t 0 https://gitee.com/CV_Lab/opencv_webcam/attach_files/959173/download/SimSun.ttc; wget -c -t 0 https://gitee.com/CV_Lab/opencv_webcam/attach_files/959172/download/TimesNewRoman.ttf')
    print(f'{info_warning("字体文件加载完成！")[1]}')


# 判断字体文件
def is_fonts(fonts_dir):
    if (os.path.isdir(fonts_dir)):
        # 如果字体库存在
        fonts_flag = 0  # 判别标志
        f_list = os.listdir(fonts_dir)  # 本地字体库

        for i in fonts_list:
            if (i not in f_list):
                fonts_flag = 1  # 字体不存在

        if (fonts_flag == 1):
            # 字体不存在
            print(f'{info_warning("字体不存在，正在加载。。。")[2]}')
            add_fronts()  # 创建字体库
        else:
            print(f'{fonts_list}{info_warning("字体已存在！")[1]}')
    else:
        # 字体库不存在，创建字体库
        print(f'{info_warning("字体库不存在，正在创建。。。")[2]}')
        add_fronts()  # 创建字体库


# 字体颜色（Bash Shell版）
def fonts_color():
    # 字体颜色
    pre_colorFlag = {
        'BLUE': '\033[94m',
        'GREEN': '\033[92m',
        'RED': '\033[91m',
        'YELLOW': '\033[93m',
        'BOLD': '\033[1m',
        'PURPLE': '\033[95m',
        'CYAN': '\033[96m',
        'DARKCYAN': '\033[36m',
        'UNDERLINE': '\033[4m',
    }

    end_colorFlag = '\033[0m'  # 结尾标志符

    return pre_colorFlag, end_colorFlag


# info warning字体颜色设置
def info_warning(msg):
    pre_colorFlag, end_colorFlag = fonts_color()
    info, success, warning = pre_colorFlag['BLUE'] + pre_colorFlag['BOLD'], pre_colorFlag['GREEN'] + \
        pre_colorFlag['BOLD'], pre_colorFlag['RED'] + pre_colorFlag['BOLD']

    info_msg = f'{info}{msg}{end_colorFlag}'
    success_msg = f'{success}{msg}{end_colorFlag}'
    warning_msg = f'{warning}{msg}{end_colorFlag}'

    return [info_msg, success_msg, warning_msg]
