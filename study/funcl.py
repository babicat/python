'''
#1. Filter, Map, Reduce

원래 위의 함수들만 찾아보려 했는데, 이 글을 이해하기 위해서는 lambda 함수에 대한 이해가 바탕이 되어야 함.

Filer(f, l) 
리스트 값을 순차적으로 함수에 대입하여 결과가 True인 값만 남겨준다. 리턴값을 출력하려면 list형으로 변환해야 함

Map(f, l)
리스트 값을 순차적으로 함수에 대입하여 연산된 값(?)을 새로운 리스트로 리턴해 준다. 이것도 출력하려면 list형으로 변환해야 함

Reduce(f, l)  << 요기는 리스트 값 자체를 변경하는게 아니므로, 튜플도 사용 가능할 듯?
리스트의 1번째 값과 2번째 값을 함수에 대입하여 연산. 다음으로 그 결과물과 3번째 리스트 값을 함수에 대입하여 연산. 이런식으로 리스트 마지막 값 까지 연산을 진행한다.
이 함수를 사용하기 위해서는 import 해야 함. (from functools import reduce)


http://seorenn.blogspot.com/2018/08/python3-filter-map-reduce.html




#2. 초보를 위한 lambda 함수 설명

익명의 함수. 잠깐 쓰고 버리는 용도? 메모리 관리에 좋다고 한다. 함수를 한줄로 간결하게 표현해서 사용 할 수 있음.
처음코딩에서 연산속도 관련해서 설명했던게 기억이 나는데, lambda 함수의 연산속도가 가장 느려서 인상 깊었다.(?)

https://wikidocs.net/64


#3. Iterator 설명(1번 글을 이해하기 위해 필요)
반복 가능한 객체. list, tuple, range 등. 배열 형태들을 말하는건가?
일단 iter() 함수 사용법은 패스했음.

https://niceman.tistory.com/136



#4. strip()
주어진 문자열에서 양쪽 끝에 있는 공백과 \n 기호를 삭제시켜 주는 함수 (문자열 중간은 X)
ex)  '\nabcde '.strip()

#5. replace()
첫 번째 인자를 두 번째 인자로 대체하는 함수
ex) 'a,b,c,d'.replace(',','/')
연달아서 사용도 가능하다. 다만 앞의 함수를 적용한 결과에 다음 함수를 적용한다.
ex) 'a,b,c,d'.replace(',','/').replace('/','-')

#6. readlines()
각 라인이 하나의 원소로 있는 리스트를 생성해준다.
read()
라인을 구분하지 않고 파일에 있는 내용을 한꺼번에 연결해서 표현해준다.


#7. f.read().splitlines()
문자열을 배열로 저장



#8. 각종 내장함수들
https://dojang.io/mod/page/view.php?id=2464


#9. list
append: 요소 하나를 추가
extend: 리스트를 연결하여 확장
insert: 특정 인덱스에 요소 추가


#10. dict
https://wikidocs.net/16043



#11. str 메소드
s = "my name is seo"
len(s)    // 문자열 길이
s.split() // 공백 문자를 기준으로 문자열을 분리하여 list로 저장
s.startswith('all') // 문자열의 all로 시작하는가? True : False
s.endswith('all')   // 문자열의 all로 끝나는가? True : False
s.find('seo')       // 첫 번째로 seo가 나오는 인덱스
s.rfind('seo')      // 마지막으로 seo가 나오는 인덱스
s.count('seo')      // 문자열 seo가 몇 번 나오는가?
s.isalnum()         // 문자열이 글자와 숫자로만 이뤄져있는가? True : False
s.strip('.')        // 문자열 양끝의 .를 삭제한다.
s.capitalize()      // 첫 단어를 대문자로 만든다.
s.title()           // 모든 단어의 첫 글자를 대문자로 만든다.
s.upper()           // 문자열을 모두 대문자로 만든다.
s.lower()           // 문자열을 모두 소문자로 만든다.
s.swapcase()        // 문자열의 대문자는 소문자로, 소문자는 대문자로
s.center(30)        // 문자열을 30칸중 중앙에 배치한다.
s.ljust(30)         // 문자열을 30칸중 왼쪽에 배치한다.
s.rjust(30)         // 문자열을 30칸중 오른쪽에 배치한다.
s.replace('seo', 'kuk') // 문자열의 seo를 kuk로 변경한다.



#12. list 메소드
l = []
l.append(1)       // list에 값 1을 요소로 추가한다.
l.insert(2, 'data') // list의 두 번째 요소에 'data'를 삽입한다.
del l[index]      // index 기반 삭제
l.remove(삭제할값) // value 기반 삭제
l.pop()           // list의 tail 삭제 및 반환
l.pop(0)          // list의 head 삭제 및 반환
l.extend(new_list)// list l과 new_list를 병합한다.
l+= new_list      // list l과 new_list를 병합한다.
b = l.copy()      // list l의 복사값을 b에 대입
b = list(l)       // list l의 복사값을 b에 대입
b = l[:]          // list l의 복사값을 b에 대입
l.index('data')   // list 요소 중 'data'의 인덱스 반환
'data' in l       // list에 'data' 요소가 있는지 True, False 반환
l.count('data')   // 'data' 개수 확인
", ".join(l)      // ,를 기준으로 list를 문자열로 만든다.
sorted(l)         // 정렬된 복사본을 반환
l.sort()          // list 자체를 정렬한다.
len(l)            // list 개수



#13. dict 메소드
d = dict()
d.update(new_dict) // new_dict 딕셔너리를 d에 붙여준다.
d.clear()          // 딕셔너리 초기화
d.keys()           // 딕셔너리의 key 조회
d.values()         // 딕너리의 value 조회
d.items()          // 딕셔너리의 key-value를 리스트로 조회
new_dict = d.copy()// 딕셔너리 copy







'''
