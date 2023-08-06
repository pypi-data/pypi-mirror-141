def fwrite(path: str, text, encoding=None):
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