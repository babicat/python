class Knight :
    def __init__(self, health, mana, armor) :
        self.health = health
        self.mana = mana
        self.armor = armor

    def slash(self) :
        print("베기")

x= Knight(health = 500, mana = 300, armor = 100)
print(x.health, x.mana, x.armor)
x.slash()




'''
class Date :

    @classmethod
    def is_date_valid(cls, date):
    
    #    if (date.count("-") > 3) :
    #       print("Wrong")
    #      return False

        date = date.split("-")

        for d in range (len(date)) :
            date[d] = int(date[d])
        
        if (date[1] > 13 or date[1] < 1) :
            print("잘못된 날짜 형식입니다.")
        elif (date[2] > 32 or date[2] < 1) :
            print("잘못된 날짜 형식입니다.")
        else :
            print("올바른 날짜 형식입니다.")


Date.is_date_valid("20-10-10")
'''

'''
str= "Rise to vote, Sir."

str = str.lower()
str = str.replace(" ", "")
str = str.replace(".", "")
str = str.replace(",", "")
str = str.replace("^", "")
print(str[::-1])

print()


'''