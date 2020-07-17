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

    #lang_len = {'k': len(ko), 'e': len(en), 'j': len(ja)}
    lang_len = [len(ko), len(en), len(ja)]
    lang_dict = {'Korean': len(ko), 'English': len(en), 'Japanese': len(ja)}

    length = len(set(lang_len))

    if length != 1:

        max_num = max(lang_len)
        for i, j in lang_dict.items():
            if j == max_num:
                print(i, end=' ')
        a = percentage(max_num, lang_len)

    return None


string = 'I am a 한국 ひと 입니다.'

result = check(string)
#a = percentage(result)
#print(a)
#print(result)
#print(result[0][0])

'''
if len(set(result)) == 3:
    p = percentage(result)

    print("대상 문자열: ", string)

    if result[0] == k_len:
        print("한국어 비중이", result, "%로 가장 높습니다.")
    elif max == e_len:
        print("영어 비중이", result, "%로 가장 높습니다.")
    elif max == j_len:
        print("일본어 비중이", result, "%로 가장 높습니다.")

elif len(set(lang_len)) == 2:
    max = max(lang_len)
    sum = len(k) + len(e) + len(j)
    result = percentage(max, sum)

    print("대상 문자열: ", string)

    if (max == len(k)) & (max == len(e)):
        print("한국어, 영어 비중이 각", result, "%로 가장 높습니다.")
    elif (max == len(k)) & (max == len(j)):
        print("한국어, 일본어 비중이 각", result, "%로 가장 높습니다.")
    elif (max == len(e)) & (max == len(j)):
        print("영어, 일본어 비중이 각", result, "%로 가장 높습니다.")

elif len(set(lang_len)) == 1:
    print("대상 문자열: ", string)
    print("모든 언어의 비중이 동일합니다.")

else:
    print("언어 판별이 불가능 합니다.")
'''