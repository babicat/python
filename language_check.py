import re
import operator

def percentage(max, li):
    sum = 0
    for i in li:
        sum += i
    return 100 * float(max)/float(sum)

def check(string):
    hangul = re.compile('[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]+')
    english = re.compile('[a-zA-Z]+')
    japanese = re.compile('[\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF]+')

    ko = hangul.findall(string)
    en = english.findall(string)
    ja = japanese.findall(string)

    lang = {'Korean': len(ko), 'English': len(en), 'Japanese': len(ja)}

    length = len(set(lang.values()))

    #모두 동일하지 않으면
    if length != 1:
        print("비중이 높은 언어: ", end=' ')
        #제일 큰 길이 구하기
        max_num = max(lang.values())
        for i, j in lang.items():
            #제일 큰 길이면
            if j == max_num:
                #해당 key 출력
                print(i, end=' ')
        ratio = percentage(max_num, lang.values())
        print('(', ratio, '% )')

    #모두 동일하면
    elif length == 1:
        print("모든 언어의 비중이 동일합니다")
    #판별 불가한 언어면
    else:
        print("언어 판별이 불가능 합니다.")

    return None

string = 'I am a 한국 ひと 입니다.'
result = check(string)
