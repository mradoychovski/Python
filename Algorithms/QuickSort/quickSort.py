# PROBLEM 1
def quicksort_first(L, start, end) :
    """ 
    Computes the number of comparisons, using 
    the first element of the given array as the pivot element.  
    """
    count = 0
    if end <= start + 1:
		return 0
    else:
        split = partition(L, start, end)
        count = end - start - 1
        lc = quicksort_first(L, start, split)				
        rc = quicksort_first(L, split+1, end)
        return count + lc + rc

# PROBLEM 2
def quicksort_last(L, start, end) :
    """
    Compute the total number of comparisons (as in Problem 1),
    always using the final element of the given array as the pivot element. 
    """
    count = 0
    if end <= start + 1:
        return 0
    else:
        # swap
        L[start], L[end-1] = L[end-1] , L[start]
        split = partition(L, start, end)
        count = end - start - 1
        lc = quicksort_last(L, start, split)				
        rc = quicksort_last(L, split+1, end)
        return count + lc + rc


# PROBLEM 3
def median_element(a,b,c):
	return ( a <= b and b <= c ) or (c <= b and b <= a )

def quicksort_median(L, start, end) :
    """
    Compute the number of comparisons (as in Problem 1), using the "median-of-three" pivot rule.
    """
    count = 0
    if end <= start + 1:
        return 0
    else :
        med = start + (end - start + 1)/2 - 1
        if median_element(L[start], L[med], L[end-1]) :
            L[start], L[med] = L[med] , L[start]
        elif median_element(L[start], L[end-1], L[med]) :
            L[start], L[end-1] = L[end-1], L[start]	

        split = partition(L, start, end)
        count = end - start - 1
        lc = quicksort_median(L, start, split)				
        rc = quicksort_median(L, split+1, end)
        return count + lc + rc

def partition(L, start, end) :
	pivot = L[start]
	i = start + 1

	for j in range(start + 1, end) :
		if L[j] < pivot :					
			L[i], L[j] = L[j], L[i]
			i = i + 1			

	L[i-1], L[start] = L[start], L[i-1]
	return i-1


def open_file(file_path="QuickSort.txt"):
    filename = open(file_path, 'r')
    try:
        L = []
        for line in filename.readlines():	
	        L.append(int(line))
    finally:
        filename.close()
    return L


if __name__ == "__main__":
    first, last, median = open_file(), open_file(), open_file()
    print quicksort_first(first, 0, len(first))
    print quicksort_last(last, 0, len(last))
    print quicksort_median(median, 0, len(median))

