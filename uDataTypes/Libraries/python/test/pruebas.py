import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from uncertainty.utypes import *

'''
print(
    False & ubool(0.3) | ubool("0.3") ^ ubool(0.3) & 1 & ubool() ^ 1 & (3 > 2)
)

print(
   "0.2" | (True & ubool(0.3)) & 0.2
)

print(
    False & ubool(0.3) | (ubool("0.3") ^  ubool(0.3)) & 1 & ubool() ^ 1 & (3 > 2)
)
    
print(
    False & ubool(0.3) | ubool("0.3")  ^   ubool(0.3) & 1 & ubool() ^ 1 & (3 > 2)
)

print(
    not ubool(0.3)
)

print(
    str( ubool(0.7) and ubool(0.6)) + " -> " + str(ubool(0.280))
)

print(
    -(ubool(0.7) ^ ubool(0.2))
)

print(
    ubool(0.7).equivalent(ubool(0.2))
)

print(
    max(
        uint(20, 0.7),
        uint(2, 0.76),
        ufloat(23, 0.2),
        unat(2, 0.1),
        ufloat(43, 0.6),
        uint(12, 0.3),
        unat(37, 0.373),
        uint(12, 0.3),
        uint(37, 0.73)
    )
)

print(
    (ufloat(3.3, 0.7) == ufloat(3.3, 0.7)) & (ufloat(3.3, 0.7) > 3 & (3 > 2))
)

print(ubool(0.7) & ubool(0.9))
if ubool(0.7) & ubool(0.9):
    print("True")
else:  
    print("False")

print(
    ufloat(3.3, 0.7) > 3 & (3 < 2)
)

ubool.setCertainty(0.4)
print(ubool.certainty())
if ubool(0.5):
    print("True")
else:
    print("False")

if ubool(0.51):
    print("True")
else:
    print("False")

if ubool(0.52):
    print("True")
else:
    print("False")


print(OR(ubool(0.3), ubool(0.4)))
print(ubool(0.3) |OR| ubool(0.4))
print(ubool(0.3).OR(ubool(0.4)))
print(ubool(0.3) | ubool(0.4))

print(XOR(ubool(0.3), ubool(0.4)))
print(ubool(0.3) |XOR| ubool(0.4))
print(ubool(0.3).XOR(ubool(0.4)))
print(ubool(0.3) ^ ubool(0.4))

print(IMPLIES(ubool(0.3), ubool(0.4)))
print(ubool(0.3) |IMPLIES| ubool(0.4))
print(ubool(0.3).IMPLIES(ubool(0.4)))
print(ubool(0.3) >> ubool(0.4))

print(EQUALS(ubool(0.3), ubool(0.4)))
print(EQUIVALENT(ubool(0.3), ubool(0.4)))
print(ubool(0.3) |EQUALS| ubool(0.4))
print(ubool(0.3) |EQUIVALENT| ubool(0.4))
print(ubool(0.3).EQUALS(ubool(0.4)))
print(ubool(0.3).EQUIVALENT(ubool(0.4)))
print(ubool(0.3) == True)

print(DISTINCT(ubool(0.3), ubool(0.4)))
print(ubool(0.3) |DISTINCT| ubool(0.4))
print(ubool(0.3).DISTINCT(ubool(0.4)))
print(ubool(0.3) != ubool(0.4))

print(NOT(ubool(0.3)))
print(ubool(0.3).NOT())
print(~ubool(0.3))



ubool.setCertainty(0.4)
print(ubool.certainty())

x = ubool(1.0)

if x & (3 > 2): 
    print("1")

if AND(x, 3 > 2): 
    print("2")

if x |AND| (3 > 2): 
    print("3")

if x.AND(3 > 2): 
    print("4")


x = ubool(0.3)
y = ubool(0.8)
z = ubool(0.5)

print(
    (~x & y) |IMPLIES| (y ^ z)
)

x2 = ufloat(925.69, 23.8)
y2 = ufloat(536.50, 31.83)
z2 = ufloat(-3404, 4.76)

w2 = (x2 / y2)**2 - z2
print(
    w2
)

x = uint(145, 3.4)
y = uint(56, 4.35)
z = uint(23, 5.2)

w = (x // y)**3 % z

print(
    w
)


x3 = uint(100, 0.7)
y3 = ufloat(900.45, 0.6)

if y3 > x3:
    w3 = y3 - x3

print(
    w3
)

x = uint(5, 23.8)
y = x - 3
# y = ufloat(2, 23.800)
z = y - ufloat(0.3, 10.3)
print(z)

r = max( 
    sin(ufloat(53.34, 0.8)),
    cos(uint(2, 0.6)),
    uint(23, 0.6), 
    floor(ufloat(3.4, 0.8)),
    uint(84, 0.6)
)
print(r)


x = ufloat(92.69, 3.8)
y = ufloat(56.50, 1.83)

w = x.add(y, 0.0)
print(
    w
)
z = x.add(y, 12.4)
print(
    z
)

uia = uint(-4, 3.0)
fa = -24.72

z = uia + fa

print(
    z
)

x = max(
    uint(2, 1), 
    uint(-1, 1), 
    uint(3, 1), 
    uint(3, 1), 
    uint(-2, 1), 
    uint(0, 1), 
    2000.03,
    uint(-4, 1),
    uint(5, 1),
    1991,
    uint(-4, 1)
)

print(x)
'''

'''
ubool.setCertainty(0.95)
x = ubool(0.7)                          ; print(x)
y = ubool(0.95)                         ; print(y)

# Bools
b1 = x & y                              ; print(b1)
b2 = x.OR(y)                            ; print(b2)
b3 = x |IMPLIES| ubool(0.95)            ; print(b3)
b4 = DISTINCT(x, y)                     ; print(b4)

# ufloats
uf1 = ufloat(254.540, 23.43)
uf2 = ufloat(2.324, 1.20)
r1 = uf1 * uf2                          ; print(r1)

# uints
ui1 = uint(200, 20.3)
ui2 = uint(54, 31.3)
r2 = ui1 // ui2                         ; print(r2)

#    uint / float + ufloat) power int
r3 = (ui1 / 3.0 + ufloat(2.5, 3.4)) **2 ; print(r3)

print((r1 + r2) > ufloat(999, 10.0))
if (r1 + r2) > ufloat(999, 10.0):   
    r3 = (r1 + r2) - ufloat(0.3, 10.3)  ; print(r3)
else:
    r3 = ufloat(0.3, 10.3)              ; print(r3)
'''

'''
x = ustr('What is Lorem Ipsum?', 0.97)

print(
    x[0: 4]
)
print(
    x[: 4]
)
#ustr('What', 0.97)
print(
    x[16:]
)

print(
    x.uSubstring(0, 4)
)
#ustr('What', 0.97)

print(
    x[-6: ]
)
#ustr('Ipsum?', 0.97)

print(
    x.uSubstring(-6)
)
#ustr('Ipsum?', 0.97)
'''

'''
x = uenum(["Red", "Blue"], [0.3, 0.453])
print(
    x.literals
)
# 
print(
    x.elements
)
# 
print(
    x.ustrs
)


x = ustr('What is Lorem Ipsum?', 0.97)
y = ustr('What is', 0.7)

print(x >= y)
print(x <= y)
print(x < y)
'''
'''
x = ustr('What is Lorem Ipsum?', 0.97)
y = ustr(' Lorem Ipsum is simply dummy text', 0.7)

r = x + y
print(r)
r = concat(x, y)
print(r)
r = x.concat(y)
print(r)
# 

r = r = x + ' Lorem Ipsum is simply dummy text'
print(r)
r = concat(x, ' Lorem Ipsum is simply dummy text')
print(r)
r = x.concat(' Lorem Ipsum is simply dummy text')
print(r)
# 

'''
'''
import numpy as np

x = np.empty(shape=10, dtype=bool)
x[0] = True
print(x)

c = [ True, False, False, False, False, False, False, False, False, False ]
y = np.array(c, dtype=bool)
y[0] = True
print(y)
'''

'''
x1 = abool([True, True, True])
print(x1.c)
x2 = abool([False, True, True])
print(x2.c)
x3 = abool([True, False, True])
print(x3.c)
x4 = abool([False, True, False])
print(x4.c)
x5 = abool([False, False, False])
print(x5.c)

xy = abool([True, False, True, False])
print(xy.c)
'''

'''
ar = abool(0.623)
br = abool('0.823')
cr = abool([True, False, True, False])

arb = ar.toubool()
print(arb)
brb = br.toubool()
print(brb)


eb = abool(ar.toubool().XOR(br.toubool()))
print('u == u: ' + str(eb.c))

r = ar.XOR(br)
print('a == a: ' + str(r.c))
'''

'''

## ubool(0.623) XOR ubool(0.823)
# Result      # Implementation
ubool(0.200)  # XOR1 :   ubool(abs(a.c - other.c))
ubool(0.200)  # XOR2 :   a.EQUIVALENT1(other).NOT()
              #          ---->EQUIVALENT1 :    XOR(o).NOT()
ubool(0.386)  # XOR3 :   a.EQUIVALENT2(other).NOT()
              #          ---->EQUIVALENT2 :    a.IMPLIES(other).AND(o.IMPLIES(self))
ubool(0.386)  # XOR4 :   ( a.AND(other.NOT()) ).OR( a.NOT().AND(other) )

## abool(0.623) XOR abool(0.823)
# Result      # 
ubool(0.4174) # XOR1 :   a.EQUIVALENT1(other).NOT()
ubool(0.4145) # XOR2 :   ( a.AND(other.NOT()) ).OR( a.NOT().AND(other) )





## ubool(0.623) EQUIVALENT ubool(0.823)
# Result      # Implementation
ubool(0.8)    # EQUIVALENT1 :  XOR(o).NOT()
ubool(0.6136) # EQUIVALENT2 :  a.IMPLIES(other).AND(o.IMPLIES(self))

## abool(0.623) EQUIVALENT abool(0.823)
# Result      # Implementation
ubool(0.5751) # EQUIVALENT1 :  a.IMPLIES(other).AND(other.IMPLIES(self))
ubool(0.5717) # EQUIVALENT2 :  (a.AND(other)).OR(a.NOT().AND(other.NOT()))
ubool(0.5702) # EQUIVALENT3 :  a.XOR2(other).NOT()
              #                ---->XOR2 :   ( a.AND(other.NOT()) ).OR( a.NOT().AND(other) )

'''

'''
x = sbool()
print(x)

y = sbool(x)
print(y)

z = sbool(ubool(0.75))
print(z)

w = sbool(0.7, 0.1, 0.2, 0.5)
print(w)
'''

x = sbool()
print(x)
x2 = sbool(True)
print(x2)
y = sbool(False)
print(y)
z = sbool(0.7, 0.1, 0.2, 0.5, 20)
print(z)
w = sbool(ubool(0.7))
print(w)

z = sbool(0.7, 0.1, 0.2, 0.5)
# sbool(0.700, 0.100, 0.200, 0.500)
print(z.belief)
# 0.700
print(z.disbelief)
# 0.100
print(z.uncertainty)
# 0.200
print(z.base_rate)
# 0.500


opinions = [
    sbool(0.0, 0.40, 0.6, 0.5), 
    sbool(0.55, 0.3, 0.15, 0.38), 
    sbool(0.1, 0.75, 0.15, 0.38),
    sbool(0.151, 0.48, 0.369, 0.382) 
]
i = sbool.beliefConstraintFusion(opinions)
print(i)

x1 = sbool(0.0, 0.40, 0.6, 0.5)
y1 = sbool(0.55, 0.3, 0.15, 0.38)
z1 = x1.bcFusion(y1)
print(z1)


x = sbool(0.95, 0, 0.05, 0.20) 
y = sbool(0.0, 0.0, 1, 0.9) 
z = x.discount(y)
print(z)

# sbool(0.855, 0, 0.145, 0.2)


print(3.5 // 4.5)

beliefConstraintFusion(opinions)