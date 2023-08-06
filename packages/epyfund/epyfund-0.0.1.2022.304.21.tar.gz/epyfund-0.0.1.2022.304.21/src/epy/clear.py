# -*- coding: utf-8 -*-
"""
Clear
"""


from ctypes import windll, c_int


user32 = windll.user32 

'''
def get_clipboard(): 
    user32.OpenClipboard(c_int(0)) 
    contents = c_char_p(user32.GetClipboardData(c_int(1))).value 
    user32.CloseClipboard() 
    return contents 
'''

def empty_clipboard(): 
    user32.OpenClipboard(c_int(0)) 
    user32.EmptyClipboard() 
    user32.CloseClipboard() 



if __name__ == '__main__':
    # 清空剪切板
    empty_clipboard()
    print('clear ok')