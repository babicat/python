import userlogs_func_m as f

# 데이터 읽어오기
read_data = f.read_file("C:\\workspace\\sona_python\\files\\userlogs.sql")

# 읽어온 데이터를 list에 넣는다.
create_list = f.create_list(read_data)

# sno, typelog 를 dict형으로 묶어서 새로운 list에 넣는다.
userlogs_dict = f.create_dict(create_list)

while True :

    input_num = input("[Select Menu]\n1. Total log count\n2. Top typelog\n3. Searching by typelog\n4. Searching by SNO\n>> ")

    if input_num == '1' :
        f.total_log(userlogs_dict)
        break

    elif input_num == '2' :
        rank = input("Input rank (range: 1 ~ 10): ")
        if rank.isdecimal() == False :
            print("\n※ Invalid number. Retry ※\n")
            continue
        else :
            rank = int(rank)

        if rank not in range(1, 11) :
            print("\n※ Invalid number. Retry ※\n")
            continue

        f.top_typelog(userlogs_dict, rank)
        break

    elif input_num == '3' :
        f_typelog = input("Input typelog : ")
        f.sno_count(userlogs_dict, f_typelog)
        break

    elif input_num == '4' :
        sno = input("Input SNO : ")
        f.typelog_count(userlogs_dict, sno)
        break

    else : 
        print("\n※ Invalid number. Retry ※\n")
        continue