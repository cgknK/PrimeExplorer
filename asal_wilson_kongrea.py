"""
Wilson Teoremi’nin Bulunma Süreci

Wilson teoremi, o dönemde asal sayıların özelliklerini araştıran matematikçiler 
tarafından, özellikle asal sayıların bölme ve çarpma özelliklerine dikkat 
edilerek elde edilmiştir. Wilson teoremi, asal sayılarla ilişkili faktöriyel 
yapısını ortaya çıkaran ilginç ve nadir bir sonuç olarak kabul edilir. Ancak, 
teoremin matematiksel olarak doğrulanması ve kanıtlanması Joseph-Louis Lagrange 
tarafından yapılmıştır.
"""

import math

n = 511
result_511 = math.factorial(n - 1) % n
print(result_511)

n = 561
result_561 = math.factorial(n - 1) % n
print(result_561)

n = 3581
result_3581 = math.factorial(n - 1) % n
print(result_3581)