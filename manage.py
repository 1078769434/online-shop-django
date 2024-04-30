#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """
    执行管理任务。

    该函数不接受参数，也不直接返回任何内容。
    主要功能是设置Django的环境变量，并从命令行执行Django管理命令。
    """
    # 设置Django环境变量
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')
    try:
        # 尝试从Django核心管理模块导入执行命令的函数
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 如果导入失败，抛出自定义的ImportError异常
        raise ImportError(
            "无法导入Django。你确定它已安装并在你的PYTHONPATH环境变量中可用吗？"
            "你是否忘记了激活虚拟环境？"
        ) from exc
    # 从命令行执行Django管理命令
    execute_from_command_line(sys.argv)


# 如果当前脚本作为主程序运行，则调用main函数
if __name__ == '__main__':
    main()

