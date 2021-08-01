# -*- coding: utf-8 -*-
import re
import operator
import logging

LOGGER = logging.getLogger()
#LOGGER.setLevel(logging.INFO)

def percentage(max, li):
    sum = 0
    for i in li:
        sum += i
    return round(100 * float(max)/float(sum), 2)

def check(string):
    hangul = re.compile('[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]+')
    english = re.compile('[a-zA-Z]+')
    japanese = re.compile('[\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF]+')

    ko = hangul.findall(string)
    en = english.findall(string)
    ja = japanese.findall(string)

    lang = {'ko': len(ko), 'en': len(en), 'ja': len(ja)}
    length = len(set(lang.values()))
    max_lang = []

    #모두 동일하지 않으면
    if length != 1:
        #제일 큰 길이 구하기
        max_num = max(lang.values())
        for i, j in lang.items():
            #제일 큰 길이면
            if j == max_num:
                #해당 key 출력
                max_lang.append(i)
        ratio = percentage(max_num, lang.values())
        LOGGER.info('비중이 높은 언어: {} ({}%)'.format(max_lang, ratio))
        #호출한 함수 내에서 max_lang에 기준 언어가 포함되어 있는지 확인
        return max_lang if max_lang else []

    #모두 동일하면
    elif (length == 1) & (sum(lang.values()) != 0):
        LOGGER.warning("모든 언어의 비중이 동일합니다.")
        return list(lang.keys())

    else:
        LOGGER.warning("언어를 인식 할 수 없습니다.")

    return []