import random

#중첩되지 않는 숫자 3개 뽑기
answer1 = random.randint(1, 10) #1~10 포함됨

while True :
    answer2 = random.randint(1, 10)
    answer3 = random.randint(1, 10)
    if answer1 == answer2 or answer2 == answer3 or answer1 == answer3 :
        continue
    else :
        break

ans_array = [] #연산자 사이는 띄어쓰기. 숫자를 저장할 공간

#배열에 숫자 3개 넣기
ans_array.append(answer1) # 배열에 데이터가 없을때는 이렇게 값을 넣는다
ans_array.append(answer2)
ans_array.append(answer3)

print("Answer : ",ans_array)

#몇 번 안에 맞추었는지 카운트
count = 0

while True :
    temp_num = input("Enter 3 integers(range:1~10):") # 숫자 3개 한꺼번에 받기(사이에 ,로 구분)
    input_num = temp_num.split(",")     #잘라서 저장

    #숫자인지 확인
    if input_num[0].isdecimal() == False or input_num[1].isdecimal() == False or input_num[2].isdecimal() == False :
        print("\n!Available integer only. Retry\n")
        continue
    else :
        for i in range(0,3) :
            input_num[i] = int(input_num[i])            
    
    if input_num[0] == input_num[1] or input_num[1] == input_num[2] or input_num[0] == input_num[2] :
        print("\n!duplicate number. Retry.\n")
        continue

    #스코어
    strike = 0
    ball = 0
    out = 0

    for a in range(0,3) :
        for b in range(0,3) :
            if ans_array[a] == input_num[b] and a == b :
                strike+=1
                break
            elif ans_array[a] == input_num[b] and a != b :
                ball+=1
                break
        else :
            out+=1    
    count += 1

    if strike == 3 :
        print("\n★", strike, "strike. You win.★")
        print("\n > Number of times : ", count, "<")
        break
    elif out == 3 :
        print("\nOut. Retry.\n")
        continue
    else :
        print("\n", strike, "strike", ball, "ball.", "Retry.\n")
        continue





#n = len(num_array) #배열의 길이 알아보는 함수
#5,8,9,10 다시봐라
