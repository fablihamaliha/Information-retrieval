# Calculating average precision
def get_average_precision(l1, l2):
    num = 0.0
    count = 0
    for i in range(len(l1)):
        if str(int(l1[i])) in l2:
            count = count + 1
            num = num + (count/float(i+1))
    # print(len(l2))
    return num / len(l2)


# Calculating R precision
def get_r_precision(list1, list2):
    total = 0

    for i in range(len(list1)):
        if str(int(list1[i])) in list2:
            total = total + 1

    return total/float(len(list2))



