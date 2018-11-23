

import random


def CodeStr(requsest):
    '''
    生成一个包含大小写的4位随机验证码
    :return:
    '''

    code_str = ''

    for i in range(4):
        num = random.randint(0,9)
        low_al = chr(random.randint(97, 122)) # a-z
        upper_al = chr(random.randint(65, 90)) # 65-91对应字符A-Z
        random_one = random.choice([num,low_al,upper_al])
        code_str += str(random_one)


    requsest.session["code_str"] = code_str


    return code_str
