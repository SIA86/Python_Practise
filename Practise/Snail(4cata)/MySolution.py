
def main():
    array = [[1,2,3,7,4,5],
            [4,5,6,3,6,7],
            [7,8,9,1,3,2],
            [2,4,6,8,1,5],
            [5,4,3,6,8,9],
            [7,9,1,2,3,4]
            ]

    start = 0
    end = len(array)
    str = []
    print(snail(start, end, array, str))

def snail(start, end, array, str):
    if start >= end:
        return
    else:
        str += array[start][start:end]
        #print(str)
        for row in range(start+1, end-1):
            str += [array[row][end-1]]
            #print(str)
        if start != end -1:
            str += array[end-1][-(start+1):-end-1:-1]
        else:
            pass
        #print(str)
        for row in list(reversed(range(start+1, end-1))):
            str += [array[row][start]]
            #print(str)

        start +=1
        end -=1
        snail(start, end, array, str)
        return str
        
        

if __name__ == '__main__':
    main()
        




