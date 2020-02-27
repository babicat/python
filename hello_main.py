import hello_practice

count = int(input("Input number (range: 1~10) : "))

answer = hello_practice.randomNumber(count)

print("Answer : ",answer)


#몇 번 안에 맞추었는지 카운트
times = 0

while True :
    times += 1

    # 숫자 3개 한꺼번에 받기(사이에 ,로 구분)
    temp_num = input("Enter 3 integers(range:1~10):") 
    inputNum = hello_practice.splNumber(temp_num)

    #숫자인지 확인
    if hello_practice.check_decimal(inputNum) == False :
        continue
    else :
        hello_practice.convert_to_int(inputNum)

    #중복된 숫자인지 확인
    if hello_practice.check_duplicate(inputNum) == False :
        continue
    else :
        pass

    #정답과 입력값 비교
    result = hello_practice.check_answer(answer, inputNum)

    #result를 보고 결과 판정
    if hello_practice.resultNumber(result, count, times) == True :
        break
    else :
        continue