def fwrite(path: str, text, encoding=None):
    """
    Args:
        path (str): file path
        text (str | Any): any textable object.
        encoding (str, optional): encoding type. Defaults to None.
    """
    text = str(text)
    if not text:
        text += '\n'
    elif text[-1] != '\n':
        text += '\n'
    with open(path, 'a', encoding=encoding) as f:
        f.write(text)


def distinct(myList: list):
    '''리스트 중복 제거'''
    return list(dict.fromkeys(myList))


def ip_change2():
    """Change IP.
    USB Tethering is Needed.

    Returns:
        bool: True if success, False otherwise.
    """
    import requests
    import subprocess
    try:
        old_ip = requests.get('http://wkwk.kr/ip', timeout = 1).text
    except:
        while True:
            old_ip = requests.get('http://wkwk.kr/ip', timeout = 1).text
            break
    subprocess.call(['c:\\adb\\adb', 'shell', 'am', 'start', '-a', 'android.intent.action.MAIN', '-n', 'com.mmaster.mmaster/com.mmaster.mmaster.MainActivity'])
    result_flag = False
    for cnt in range(90):
        print('인터넷 접속대기중 - {}초'.format(cnt+1))
        try:
            cur_ip = requests.get('http://wkwk.kr/ip', timeout = 1).text
            if old_ip == cur_ip:
                print('아이피가 변경되지 않았습니다.')
                return result_flag
            else:
                print(f'{old_ip} -> {cur_ip} 변경 완료.')
                result_flag = True
                return result_flag
        except:
            pass
    print('아이피가 변경되지 않았습니다.')
    return result_flag


def run_everyday_between(start_time: str, end_time: str, job, *args, **kwargs):
    """run given job between given time.

    Args
    ----
        start_time (str): The time to be start
        end_time (str): The time to be end
        job (function): The function to be execute
    
    Optional
    --------
        args : if a function has a args
        kwargs : if a function has a kwargs
    """
    import datetime
    start_hour, start_minute = [int(x.strip()) for x in start_time.split(':')]
    end_hour, end_minute = [int(x.strip()) for x in end_time.split(':')]
    
    while True:
        now = datetime.datetime.now()
        if datetime.timedelta(hours=start_hour, minutes=start_minute) <= datetime.timedelta(hours=now.hour, minutes=now.minute) <= datetime.timedelta(hours=end_hour, minutes=end_minute):
            if args:
                if kwargs:
                    job(*args, **kwargs)
                else:
                    job(*args)
            else:
                if kwargs:
                    job(**kwargs)
                else:
                    job()