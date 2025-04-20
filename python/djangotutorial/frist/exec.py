import os


if __name__ == '__main__':
    cmd = "/usr/local/bin/python3.11 /Users/edy/owner/study_notes/python/djangotutorial/frist/manage.py runserver 192.168.0.9:8000"
    # os.popen(cmd, mode='r', buffering=-1)
    os.system(cmd)
