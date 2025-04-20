#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frist.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    # cmd = "/usr/local/bin/python3.11 /Users/edy/owner/study_notes/python/djangotutorial/frist/manage.py runserver 192.168.110.14:8000"
    # # os.popen(cmd, mode='r', buffering=-1)
    # os.system(cmd)
# python manage.py runserver

#  /usr/local/bin/python3.11 /Users/edy/owner/study_notes/python/djangotutorial/frist/manage.py runserver
#  /usr/local/bin/python3.11 /Users/edy/owner/study_notes/python/djangotutorial/frist/manage.py runserver 192.168.110.14:8000
#  /usr/local/bin/python3.11 /Users/edy/owner/study_notes/python/djangotutorial/frist/manage.py migrate
#  /usr/local/bin/python3.11 /Users/edy/owner/study_notes/python/djangotutorial/frist/manage.py startapp service 
# python manage.py  startapp api 
# {"S":1,"M":"“计算结果”错误。（010）","D":null} 

# pip install pytesseract -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# pip install ultralytics -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
