"""
CMPS 2200  Assignment 2.
See assignment-02.md for details.
"""
from collections import defaultdict
import math

#### Iterative solution
def parens_match_iterative(mylist):
    """
    Implement the iterative solution to the parens matching problem.
    This function should call `iterate` using the `parens_update` function.
    
    Params:
      mylist...a list of strings
    Returns
      True if the parenthesis are matched, False otherwise
      
    e.g.,
    >>>parens_match_iterative(['(', 'a', ')'])
    True
    >>>parens_match_iterative(['('])
    False
    """
    final_count = iterate(parens_update, 0, mylist)
    return final_count == 0


def parens_update(current_output, next_input):
    """
    This function will be passed to the `iterate` function to 
    solve the balanced parenthesis problem.
    
    Like all functions used by iterate, it takes in:
    current_output....the cumulative output thus far (e.g., the running sum when doing addition)
    next_input........the next value in the input
    
    Returns:
      the updated value of `current_output`
    """
    if current_output < 0:  
        return current_output
    if next_input == '(':
        return current_output + 1
    elif next_input == ')':
        return current_output - 1
    else:
        return current_output


def iterate(f, x, a):
    """
    Apply function f iteratively to sequence a starting with initial value x.
    """
    result = x
    for item in a:
        result = f(result, item)
    return result


#### Scan solution

def parens_match_scan(mylist):
    """
    Implement a solution to the parens matching problem using `scan`.
    This function should make one call each to `scan`, `map`, and `reduce`
    
    Params:
      mylist...a list of strings
    Returns
      True if the parenthesis are matched, False otherwise
      
    e.g.,
    >>>parens_match_scan(['(', 'a', ')'])
    True
    >>>parens_match_scan(['('])
    False
    
    """
    if not mylist:
        return True
        
    # Map parentheses to values
    mapped = list(map(paren_map, mylist))
    
    # Get prefix sums using scan
    prefix_sums, total = scan(plus, 0, mapped)
    
    # Check if total is 0 and all prefix sums are non-negative
    all_non_negative = reduce(min_f, float('inf'), prefix_sums) >= 0
    
    return total == 0 and all_non_negative


def scan(f, id_, a):
    """
    This is a horribly inefficient implementation of scan
    only to understand what it does.
    We saw a more efficient version in class. You can assume
    the more efficient version is used for analyzing work/span.
    """
    return (
            [reduce(f, id_, a[:i+1]) for i in range(len(a))],
             reduce(f, id_, a)
           )

def paren_map(x):
    """
    Returns 1 if input is '(', -1 if ')', 0 otherwise.
    This will be used by your `parens_match_scan` function.
    
    Params:
       x....an element of the input to the parens match problem (e.g., '(' or 'a')
       
    >>>paren_map('(')
    1
    >>>paren_map(')')
    -1
    >>>paren_map('a')
    0
    """
    if x == '(':
        return 1
    elif x == ')':
        return -1
    else:
        return 0

def min_f(x,y):
    """
    Returns the min of x and y. Useful for `parens_match_scan`.
    """
    if x < y:
        return x
    return y

def plus(a, b):
    """
    Returns the sum of a and b.
    """
    return a + b

def reduce(f, id_, a):
    """
    Reduce a sequence a using function f with identity id_.
    """
    if len(a) == 0:
        return id_
    result = id_
    for item in a:
        result = f(result, item)
    return result


#### Divide and conquer solution

def parens_match_dc(mylist):
    """
    Calls parens_match_dc_helper. If the result is (0,0),
    that means there are no unmatched parentheses, so the input is valid.
    
    Returns:
      True if parens_match_dc_helper returns (0,0); otherwise False
    """
    n_unmatched_left, n_unmatched_right = parens_match_dc_helper(mylist)
    return n_unmatched_left == 0 and n_unmatched_right == 0

def parens_match_dc_helper(mylist):
    """
    Recursive, divide and conquer solution to the parens match problem.
    
    Returns:
      tuple (R, L), where R is the number of unmatched right parentheses, and
      L is the number of unmatched left parentheses. This output is used by 
      parens_match_dc to return the final True or False value
    """
    # Base cases
    if len(mylist) == 0:
        return (0, 0)
    elif len(mylist) == 1:
        if mylist[0] == '(':
            return (0, 1)  # one unmatched (
        elif mylist[0] == ')':
            return (1, 0)  # one unmatched )    
        else:
            return (0, 0)
    
    # Divide
    mid = len(mylist) // 2
    left_R, left_L = parens_match_dc_helper(mylist[:mid])
    right_R, right_L = parens_match_dc_helper(mylist[mid:])
    
    # Combine
    # The unmatched left parens from left can match with unmatched right parens from right
    matches = min(left_L, right_R)
    total_R = left_R + (right_R - matches)
    total_L = (left_L - matches) + right_L
    
    return (total_R, total_L)



    

