"""
Computes the number of inversions in the file given, 
where the i-th row of the file indicates the i-th entry of an array.
"""

def open_file(file_path="IntegerArray.txt"):
    filename = open(file_path, 'r')
    try:
        L=[]
        for line in filename.readlines():
            L.append(int(line))
    finally:
        filename.close()
    return L


def merge(A,B):
    global numOfInversions
    C = []
    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i]<=B[j]:
            C.append(A[i])
            i += 1
        else:
            numOfInversions += len(A)- i
            C.append(B[j])
            j += 1
    if i == len(A):
        C.extend(B[j:])
    else:
        C.extend(A[i:])
    return C

def mergeSort(L):
    N = len(L)
    if N>1:
        S1 = mergeSort(L[0:N/2])
        S2 = mergeSort(L[N/2:])
        return merge(S1,S2)
    else:
        return L

if __name__ == "__main__":
    numOfInversions = 0
    lst = open_file()
    srt_lst = mergeSort(lst)
    print numOfInversions
