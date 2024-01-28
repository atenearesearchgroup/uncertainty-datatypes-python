from enum import Enum
import time
import random
import psutil
from statistics import mean,stdev,median,geometric_mean

from uncertainties import *

class TestType(Enum):
    Add = 1
    Minus = 2
    Mult = 3
    Div = 4
    Exp = 5

############ CHANGE THIS TO SELECT THE TEST TYPE:
test : TestType = TestType.Add
############

results=[]; averages=[]; medians=[]; gmeans=[]; stdevs=[]
random.seed(30)
numExecs=30
numIteraciones=5
init = 10_000; end = (init*numIteraciones)+1; step = 10_000
series : ufloat

for repetitions in range(init, end, step):
    print(repetitions)
    for n in range(numExecs):
        uf1 = ufloat(random.randrange(100, 10_000)/100, random.randrange(1_000) /100)
        uf2 = ufloat(random.randrange(100, 10_000)/100, random.randrange(1_000) /100)
        uf3 = ufloat(random.randrange(100, 10_000)/100, random.randrange(1_000) /100)
        uf4 = ufloat(random.randrange(100, 10_000)/100, random.randrange(1_000) /100)
        uf5 = ufloat(random.randrange(100, 10_000)/100, random.randrange(1_000) /100)
        uf6 = ufloat(random.randrange(100, 10_000)/100, random.randrange(1_000) /100)
        uf7 = ufloat(random.randrange(100, 10_000)/100, random.randrange(1_000) /100)
        uf8 = ufloat(random.randrange(100, 10_000)/100, random.randrange(1_000) /100)
        series = ufloat(0,0)
        start = time.process_time()
        if test == TestType.Add:
            for _ in range(repetitions):
                series = series + uf1 + uf2 + uf3 + uf4 + uf5 + uf6 + uf7 + uf8     
        elif test == TestType.Minus:
            for _ in range(repetitions):
                series = series + uf1 - uf2 - uf3 - uf4 - uf5 - uf6 - uf7 - uf8
        elif test == TestType.Mult:
            for _ in range(repetitions):
                series = series + uf1 * uf2 * uf3 * uf4 * uf5 * uf6 * uf7 * uf8
        elif test == TestType.Div:
            for _ in range(repetitions):
                series = series + uf1/uf2/uf2/uf3/uf4/uf5/uf6/uf7/uf8
        elif test == TestType.Exp:
            for _ in range(repetitions):
                series = series + uf1**2 + uf2**2 + uf3**3 + uf4**4 + uf5**5 + uf6**6 + uf7**7 + uf8**8
            # END OF COMPUTATION
        results.append(time.process_time() - start)
    averages.append(mean(results))
    medians.append(median(results))
    gmeans.append(geometric_mean(results))
    stdevs.append(stdev(results))
print('averages:' + str(averages))
print('medians:' + str(medians))
print('gmeans:' + str(gmeans))
print('stdevs:' + str(stdevs))

p = psutil.Process()
print('Memory peak: ' + str(p.memory_info().peak_wset) + ' Bytes')
