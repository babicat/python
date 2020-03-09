'''
#1. UnicodeDecodeError

UnicodeDecodeError: 'cp949' codec can't decode byte 0xe2 in position 6987: illegal multibyte sequence

아래와 같이 파일을 여세요.

open('파일경로.txt', 'rt', encoding='UTF8')




#2. unicode error

SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 30-31: truncated \uXXXX escape

1. \를 두번 써준다.
open("C:\\workspace\\sona_python\\files\\userlogs.sql", "r")

2. 따옴표 앞에 r을 붙여 준다.
open(r"C:\workspace\sona_python\files\userlogs.sql", "r")






'''