"""
Create a function that takes a positive integer and returns the next bigger number that can be formed by rearranging its digits. For example:
12 ==> 21
513 ==> 531
2017 ==> 2071

If the digits can't be rearranged to form a bigger number, return -1
9 ==> -1
111 ==> -1
531 ==> -1
"""

num = input('Enter the number: ')
len_num = len(num)
new = '-1'
for i in range(len_num-1):
    if int(num[len_num-1-i]) > int(num[len_num-2-i]):
        new = num[:len_num-2-i] + num[len_num-1-i] + num[len_num-2-i] + num[len_num-i:]
        len_new = len(num[len_num-2-i] + num[len_num-i:])
        for j in range(len_new-1):
            if int(new[len_num-1-j]) < int(new[len_num-2-j]):
                new = new[:len_num-2-j] + new[len_num-1-j] + new[len_num-2-j] + new[len_num-j:]
        break

print(new)



            
        
    


    
            
            

#print(num)
    