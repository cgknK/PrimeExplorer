def isqrt(n):
    """
    Compute the integer square root of a non-negative integer n.
    
    :param n: A non-negative integer
    :return: The integer square root of n
    """
    if n < 0:
        raise ValueError('isqrt() argument must be nonnegative')
    
    if n == 0:
        return 0
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x
