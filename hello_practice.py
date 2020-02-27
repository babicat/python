import random

def randomNumber(size) :
    #size 갯수만큼 중복되지 않는 숫자 뽑기 (size<=10)
    randomNum = []
    while len(randomNum) < size :
        tempNum = random.randint(1, 10)

        if (tempNum in randomNum) != True :
            randomNum.append(tempNum)
    return randomNum


def splNumber(inputNum) :
    #문자열을 , 기준으로 쪼개기
    inputNum_spl = inputNum.split(",")
    return inputNum_spl


def check_decimal(inputList) :
    #list의 값들이 숫자인지 확인
    for i in range(0, len(inputList)) :
        if inputList[i].isdecimal() != True :
            print("\n!Available integer only. Retry\n")
            return False
        else :
            return True


#int형으로 변환
def convert_to_int(inputList) :
    for i in range(0, len(inputList)) :
        inputList[i] = int(inputList[i])
    

#중복되는 숫자인지 검사
def check_duplicate(inputList) :
    set1 = set(inputList)

    if (len(set1) != len(inputList)) :
        print("\n!duplicate number. Retry.\n")
        return False
    else :
        return True


#정답과 입력한 숫자 비교
def check_answer(answerList, inputList) :
    result = [0, 0, 0]

    for a in range(0,len(answerList)) :
        for b in range(0,len(inputList)) :
            if answerList[a] == inputList[b] and a == b :
                result[0] += 1
                break
            elif answerList[a] == inputList[b] and a != b :
                result[1] += 1
                break
        else :
            result[2] += 1    
    return result


#결과 판정
def resultNumber(resultNum, count, times) :
    if  resultNum[0] == count :
        print("\n★ Strike. You win. ★")
        print("\nNumber of times : ", times)
        return True

    elif resultNum[2] == count :
        print("\nOut. Retry.\n")
        times += 1
        return False

    else :
        print("\n", resultNum[0], "strike", resultNum[1], "ball.", "Retry.\n")
        times += 1
        return False