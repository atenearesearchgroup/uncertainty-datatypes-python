from uncertainty.utypes import *

a = ubool(0.3); b = ubool(0.8); c = ubool(0.5); d = ubool(0.2)
w = (~a & b) |IMPLIES| (c | d); print (w)
# w = ubool(0.776)

a = ubool(0.3); b = ubool(0.8); c = ubool(0.5); d = False
w = (~a & b) |IMPLIES| (c | d) ; print (w)  
# ubool(0.720)

x = ufloat(925.69, 23.8); y = ufloat(536.50, 31.83); z = ufloat(-3404, 4.76)
w = (x / y)**2 - z; print (w)
# w = ufloat(3406.977, 5.946)

x = ufloat(925.69, 23.8); y = ufloat(536.50, 31.83); z = -3404
print ((x / y)**2 - z)
# w = ufloat(3406.977, 3.563)

x = ufloat(2.0,0.3); y = ufloat(2.5,0.25); z = 1.5
print ((x / y)**2 + z) 
# ufloat(2.140,0.329)
print (x < y) 
# ubool(0.639)

print( max(  
    sin(ufloat(53.34, 0.8)),
    uint(23, 1), 
    floor(ufloat(24.4, 0.8)),
    23.45 )
) # ufloat(24.0, 0.800)

a = ubool(0.3); b = ubool(0.8); c = sbool(0.1, 0.4, 0.5, 0.5)
print ( (~a & b) |IMPLIES| c)
# sbool(0.496, 0.310, 0.194, 0.720)

opinions = [
    sbool(0.000, 0.400, 0.600, 0.50), 
    sbool(0.550, 0.300, 0.150, 0.380), 
    sbool(0.100, 0.750, 0.150, 0.380),
    sbool(0.151, 0.480, 0.369, 0.382) 
]
print (sbool.cbFusion(opinions))
# sbool(0.126, 0.861, 0.013, 0.393)