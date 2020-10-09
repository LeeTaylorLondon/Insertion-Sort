from random import randint
from typing import List, NoReturn


def swap(a: List[int], i: int, i2: int) -> NoReturn:
    '''
    Swaps two elements in a list
    :param: a  -- reference to the list of integers
    :param: i  -- pointer to the element to be swapped
    :param: i2 -- pointer to the element to be swapped
    '''
    temp  = a[i]
    a[i]  = a[i2]
    a[i2] = temp

"""
Reference -- https://www.youtube.com/watch?v=JU767SDMDvA
Insertion Sort Pseudo Code: 

for i : 1 to length(A)-1
    j = i
    while j > 0 and A[j-1] > A[j]
        swap A[j] and A[j-1]
        j = j - 1
"""
def insertion_sort(a: List[int]) -> NoReturn:
    for i in range(1, len(a)):  # range is executed up until upper_limit-1
        j = i
        while (j > 0) and (a[j-1] > a[j]):
            swap(a, j, j-1)
            j = j - 1


## Functions below used for testing the user.


def return_rarray(_min=1, _max=10, size=5, duplicates=False) -> List[int]:
    '''
    Returns array of random elements [x0, x1, ..., xn]
    for each element in the range (_min >= x >= _max).
    Where the number of elements equals parameter -> size.

    :param: _min -- int
        the smallest possible integer that could be randomly generated
    :param: _max -- int
        the largest possible integer that could be randomly generated
    :param: size -- int
        the number of elements appended to the array
    :param: duplicates -- boolean
        if True, elements of equal value may be generated otherwise
        all elements are unique
    '''
    if (duplicates):
        rv = []
        for i in range(size): rv.append(randint(_min, _max))
        return rv
    elif not(duplicates):
        if not((m := 1 + _max - _min) >= size):
            raise TypeError('Size {size} too big for {m} unique values! Change _min, _max parameters!')
        rv = {}
        while (len(rv) != size): rv.update({randint(_min,_max): 0})
        return list(rv.keys())

def list_to_string(a: List[int]) -> str:
    """ Returns string of all elements in list a """
    rv = ''
    for elm in a: rv = rv + ' ' + str(elm)
    return rv[1:]

def insertion_sort_test(a: List[int]) -> NoReturn:
    """
    Insertion sort with each outer iteration trace stored
    and returned. Used to recreate questions from worksheet.
    """
    traces = []                       # init traces
    traces.append(list_to_string(a))  # append first trace
    for i in range(1, len(a)): 
        j = i
        while (j > 0) and (a[j-1] > a[j]):
            swap(a, j, j-1)
            j = j - 1
        traces.append(list_to_string(a))  # append each outter for loop trace
    return traces

def test_recognition(a: List[int], traces=4) -> NoReturn:
    """
    Based on ~ CSC2032: Tutorial 1.4.1/2.1.1 ~ Question 1

    Generates a matrix of traces in which only one corresponds
    to the insertion sort -- the user must label the correct
    trace block. 
    """
    # Init. answers, obstacles, and pointers for radomization
    actual_traces, random_traces = insertion_sort_test(a), []
    i, i2 = 0, 0
    # Populate random_traces matrix
    for i in range(traces):
        # while-loop prevents identicle pointers causing no swap
        while(i == i2): i, i2 = randint(0, len(a)-1), randint(0, len(a)-1)
        a_copy   = a.copy()
        swap(a_copy, i, i2)
        trace    = insertion_sort_test(a_copy)
        trace[0] = actual_traces[0]  # Adds more confusion
        random_traces.append(trace)
        i, i2 = 0, 0
    ow_ptr = randint(0,traces-1)  # 'ow' -> overwrite
    random_traces[ow_ptr] = actual_traces
    random_traces[randint(0,traces-1)][1] = actual_traces[1]
    # Print statements ripped from question-1
    print('Consider the following array traces which may or may not have been ')
    print('produced by different sorting algorithms when applied to the array of values:')
    print(f"{actual_traces[0]}\n")
    # Displays contents of random traces
    for i,vec in enumerate(random_traces):
        print(f"Trace [{i+1}]")
        for s in vec:
            print(s)
        print()
    # User input | answer = ow_ptr + 1
    print('Which trace above corresponds to insertion sort?')
    ua = int(input("Enter number of trace: "))
    if (ua == ow_ptr + 1): print('<Answer: Correct!>\n')
    else:
        print('<Answer: Incorrect ._. >\n')
        print(f"The right answer was: {int(ow_ptr)+1}\n")

def test_traces(a: List[int]) -> int:
    """
    Based on ~ CSC2032: Tutorial 1.4.1/2.1.1 ~ Question 2

    The user is presented with an array of integers. User
    must enter each outer iteration trace.
    User input format (i.e): 1 2 3 4 5 6 7
    
    Note: the array of integers are random unique
    values which can be customized see 'return_rarray()'
    for more details.
    """
    # init actual-traces and user-input storage
    actual_traces = insertion_sort_test(a)
    user_inp      = []
    user_inp.append(actual_traces[0])
    # First trace is always the original list
    print('Give a high-level trace of applying insertion sort to the array given below.')
    print("First trace :", actual_traces[0])
    # Take user input for each trace
    for p in range(1, len(actual_traces)):
        user_inp.append(str(input(f"Type trace-{p+1}: ")).strip())
    # Calculate and print score for matching traces
    correct = 0
    for a, ua in zip(actual_traces, user_inp):
        if (a == ua): correct += 1
    print(f"<You scored [{correct-1}/{len(actual_traces)-1}]!>\n")
    # Print answers & user input only if they got something wrong
    if (correct != len(actual_traces)):
        for a, ua in zip(actual_traces, user_inp):
            print(f"Your answer: {ua} | Actual: {a}")
        print()
    return correct

def test_iteration_recognition(a: List[int], iteration=3, lists=5) -> NoReturn:
    """
    Based on ~ CSC2032: Tutorial 1.4.1/2.1.1 ~ Question 3
    
    Displays an array partially sorted by insertion sort.
    The original array is display with others that are not
    the original array. The user must pick out the correct
    array.
    """
    # Init. obstacles, copy of list, and partial sorted version of list
    p_answers = []  # p_answers -> possible answers
    og_list   = a.copy()
    partially_sorted_array = insertion_sort_test(a)[iteration]
    # Populate p_answers with non-answers and answer
    i, i2 = 0, 0  # while-loop prevents equal ptrs causing no swap
    while (i == i2): i, i2 = randint(0,len(a)-1), randint(0,len(a)-1)
    # Swap elements in the original array and display to confuse user
    for i in range(lists):
        temp_list = og_list.copy()
        swap(temp_list, i, i2)
        p_answers.append(temp_list)
    # Sets at least one vector in p_answers to the actual answer
    p_answers[randint(0,lists-1)] = og_list
    # Dipslay question information to user
    print(f'Suppose after {int(iteration)} outer iterations of insertion')
    print('sort we have the following array:')
    print(f'{partially_sorted_array}\n')  # Display actual trace
    print('Then which of the following arrays could have been the initial')
    print('array insertion sort was applied to.\n')
    for i,vec in enumerate(p_answers): print(f"[{i+1}] {list_to_string(vec)}")
    # User input is taken and evaluated
    user_inp = int(input('\nEnter the number of any correct array: '))
    try:
        if (p_answers[user_inp-1] == og_list): print('<Answer: Correct!>\n')
        else:
            print('<Answer: Incorrect ._. >\n')
            s = 'Acceptable answers'
            for i,pa in enumerate(p_answers):
                if (pa == og_list): s = s + ' ' + f"[{str(i)}]"
            print(s)
    except IndexError:
            print('<Answer: Incorrect ._. >\n')
            s = 'Acceptable answers:'
            for i,pa in enumerate(p_answers):
                if (pa == og_list): s = s + ' ' + f"[{str(i)}]"
            print(s)

def main():
    ''' Examples '''
    #reference_example = [2, 8, 5, 3, 9, 4]
    ''' >>> <example_1 = [2, 8, 5, 3, 9, 4] (Before i.sort)> '''
    #insertion_sort(reference_example)
    ''' >>> <example_1 = [2, 3, 4, 5, 8, 9] (After i.sort)> '''
    
    ''' Testing '''
    questions = {1: test_recognition,
                 2: test_traces,
                 3: test_iteration_recognition}
    while True:
        user_inp = ''
        q = randint(1, 3)
        if (q == 3): questions.get(q)(return_rarray(size=7))
        else: questions.get(q)(return_rarray())
        while (user_inp != 'y' and user_inp != 'n'):
            user_inp = str(input('Next question (y/n): ')).lower()
            if (user_inp == 'n'): return
            

if __name__ == '__main__':
    main()
