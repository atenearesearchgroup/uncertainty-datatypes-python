# Uncertainty Python Library

Uncertainty Datatypes is a Python library providing uncertainty datatypes including u-type, a-type and s-type.

The library provides three kinds of datatypes: 
1. **u-type** datatypes: ubool, uint, ufloat, ustr, uenum.
    Type U is a pair (x, u), noted x ± u, that represents a random variable whose average is x and standard deviation is u.
2. **a-type** datatypes: abool, aint, afloat.
    Type A, maintain the set of the measured values as X = {x1,...,xn}, x ± u could be calculated as the mean and standard deviation.
3. **s-type** datatype: sbool.
    A particular type of subjective uncertainty (Belief Uncertainty) when a user is not sure about the truth of a statement.

Math functions with the datatypes are also provided.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install uncertainty-datatypes
```
<sub>Note pip3 may be used instead of pip</sub> 

## Usage

Import all the datatypes and functions using:
```python
from udatatypes.utypes import *
```

---

## The ubool type

A ubool can be instantiated providing the certainty, that is, a float[0, 1] where 1 is the highest possible certainty while 0 is the lowest.

```python
x = ubool(0.7) 
y = ubool('0.7')  # A str can be used if it represent a float[0, 1]
z = ubool(1)      # int 0 or 1 can be used too.
w = ubool(False)  # True or False can be also used. 
                   #True -> ubool(1.0) and False -> ubool(0.0).
```

ubools can be used as conditional statements.
```python
if x:
    'executed'
```
**ubool never should be used with python logical operators** (and, or and not keywords). **ubool special logical operators must be used** (see below.)

#### Logical operators
The python logical operators ('and', 'or', and 'not' keywords)  have a different meaning when they are being used with objects. Therefore, **ubool special logical operators must be used**. 

ubool logical operators include: *AND*, *OR*, *NOT*, *XOR*, *IMPLIES, and *EQUIVALENT*. The library offers the following four ways of using logical operators: 
* Operator: ``` x & y ``` 
* Special operator: ``` x |AND| y ``` 
* The ubool method: ``` x.AND(y) ``` 
* A function: ``` AND(x, y) ```

The table below summarizes all the possible usages.

| Logical <br/> Operation | Operator      | Special <br/> Operator  | Method | Function |
|:-----------:|:---------------:|:-------------------:|:-------------:|:----------:|
| AND      | ``` x & y ``` | ``` x |AND| y ``` | ``` x.AND(y) ```  | ``` AND(x, y) ```|
| OR       | ``` x | y ``` | ``` x |OR| y ``` | ``` x.OR(y) ```  | ``` OR(x, y) ```|
| XOR      | ``` x ^ y ``` | ``` x |XOR| y ```| ``` x.XOR(y) ``` | ``` XOR(x, y) ```|
| NOT      | ``` ~ x ``` | | ``` x.NOT() ``` | ``` NOT(x) ```|
| IMPLIES      | ``` x >> y ``` | ``` x |IMPLIES| y ```| ``` x.IMPLIES(y) ``` | ``` IMPLIES(x, y) ```|
| EQUIVALENT      | ``` x == y ``` | ``` x |EQUIVALENT| y ```<br />``` x |EQUALS| y ```| ``` x.EQUIVALENT(y) ```<br />``` x.EQUALS(y) ```| ``` EQUIVALENT(x, y) ```<br />``` EQUALS(x, y) ```|
| DISTINCT      | ``` x != y ``` | ``` x |DISTINCT| y ```| ``` x.DISTINCT(y) ```| ``` DISTINCT(x, y) ```|

Operators or special operators must be surrounded by parentheses due operator precedence. Meanwhile, using a method or the function provides the highest precedence.

*Code example:*
```python
x = ubool(0.3)
y = ubool(0.8)
z = ubool(0.5)

w = (~x & y) |IMPLIES| (y ^ z)
# w = ubool(0.608)
```

#### Usage with bool
ubools can be used together with python's bools, but ubool operators must be used. 

```python
if x & (3 > 2): 
    # do something
elif OR(x, 3 > 2): 
    # do something
elif x |XOR| (3 > 2):
    # do something
while x.AND(3 > 2):
    # do something
```
<sub>Note that, python logical operations (3 > 2) must be enclosed by paretheses. True values (result of 3 > 2) are converted into a ubool(1.0) and False into ubool(0.0).</sub>

#### Level of certainty
The level of certainty changes when a ubool is evaluated to True. 
The level of certainty can be set using **ubool.setCertainty()** function. By default, 0.9 is used.

```python
y = ubool(0.7)

# Certainty by default: 0.9
if y:   # y is ubool(0.7) < 0.9
    'not executed'

ubool.setCertainty(0.5)
if y:   # y is ubool(0.7) >= 0.5
    'executed'
```
---

## The ufloat type

A ufloat can be instantiated providing the value and the certainty. Value is any float and Certainty is a float[0, 1] where 1 is the highest possible certainty while 0 is the lowest.

```python
x = ufloat(-230.30, 0.7) 
y = ufloat(233, '0.7')  # Data can be provided as str, int or float.
# y = ufloat(233.0, 0.7)
```

#### Operators
ufloat operators include: *ADD*, *SUB*, *MUL*, *DIV*, *FLOOR DIV*, *NEG*, *POWER*. The table below summarizes all the possible operations.

| Operation | Operator      | Method | Function |
|:---------:|:------------:|:-----------------:|:----------------:|
| ADD      | ``` x + y ``` | ``` x.add(y) ```  | ``` add(x, y) ```|
| SUB      | ``` x - y ``` | ``` x.sub(y) ```  | ``` sub(x, y) ```|
| MUL      | ``` x * y ``` | ``` x.mul(y) ```  | ``` mul(x, y) ```|
| DIV      | ``` x / y ``` | ``` x.div(y) ```  | ``` div(x, y) ```|
| FLOOR DIV| ``` x // y ```| ``` x.floordiv(y) ``` | ``` floordiv(x, y) ```|
| NEG      | ``` ~ x ```   | ``` x.neg(y) ```  | ``` neg(x, y) ```|
| POW      | ``` x ** y ```| ``` x.power(y) ```| ``` pow(x, y) ```|

<sub>Arithmetic operators are recommended. The usage of methods or functions changes the precedence of the operation at execution as if it were enclosed in parentheses.</sub>

##### Covariance methods
Methods *add*, *sub*, *mul*, *div*, *floordiv* allows the usage of the covariance as an additional parameter.
```python
x = ufloat(92.69, 3.8)
y = ufloat(56.50, 1.83)

w = x.add(y, covariance = 0.0)
# w = ufloat(149.190, 4.218)
z = x.add(y, covariance = 12.4)
# z = ufloat(149.190, 6.526)
```

*ufloat operators Code example:*
```python
x = ufloat(925.69, 23.8)
y = ufloat(536.50, 31.83)
z = ufloat(-3404, 4.76)

w = (x / y)**2 - z
# w = ufloat(3406.977, 5.946)
```

#### Usage with uint, int and float.
ufloats can be used together uint and with python's float and int.

```python
x = ufloat(5.69, 23.8)
y = x + 3.1
# y = ufloat(8.790, 23.800)
```

---

## The uint type

A uint can be instantiated in the same way as for ufloat, providing the value and certainty. Value is any float and Certainty is a float[0, 1] where 1 is the highest possible certainty while 0 is the lowest.

```python
x = uint(-654, 2.4) 
# y = uint(-654, 2.4)
y = uint(432, '5.7')  # Data can be provided as str, int or float.
# y = uint(432, 5.7)
```

#### Operators
The operator MOD is included for uint. The rest of the operators available for uint are the same than those provided for ufloat: *ADD*, *SUB*, *MUL*, *DIV*, *FLOOR DIV*, *NEG*, *POWER*. 

| Operation | Operator      | Method | Function |
|:---------:|:------------:|:-----------------:|:----------------:|
| MOD      | ``` x % y ``` | ``` x.mod(y) ```  | ``` mod(x, y) ```|
<sub>Arithmetic operators are recommended. The usage of methods or functions changes the precedence of the operation at execution as if it were enclosed in parentheses.</sub>

##### Covariance methods
Covariance methods are also provided for the uint type.

*uint operators Code example:*
```python
x = uint(145, 3.4)
y = uint(56, 4.35)
z = uint(23, 5.2)

w = (x // y)**3 % z
# w = uint(8, 1.246)
```

#### Usage with ufloat, int and float.
uints can be used together ufloat and with python's float and int.

```python
x = uint(5, 23.8)
y = x - 3
# y = ufloat(2, 23.800)
z = y - ufloat(0.3, 10.3)
# z = ufloat(1.700, 25.933)
```
--- 

## Comparison Operators
Comparison between uint and ufloat can be made using the comparison operators: <, <=, >, >=, == and != and the methods.


| Operation | Operator      | Method | Function |
|:-----------:|:---------------:|:-------------------:|:-------------:|
| Less      | ``` x < y ``` | ``` x.lt(y) ```  | ``` lt(x, y) ```|
| Less or Equals | ``` x <= y ``` | ``` x.le(y) ```  | ``` le(x, y) ```|
| Greater | ``` x > y ``` | ``` x.gt(y) ```  | ``` gt(x, y) ```|
| Greater or Equals | ``` x >= y ``` | ``` x.ge(y) ```  | ``` ge(x, y) ```|
| Equals | ``` x == y ``` | ``` x.eq(y) ```  | ``` eq(x, y) ```|
| Not Equals | ``` x != y ``` | ``` x.ne(y) ```  | ``` ne(x, y) ```|

<sub>Operators are recommended. The usage of methods or functions changes the precedence of the operation at execution as if it were enclosed in parentheses.</sub>

*Code example:*
```python
x = uint(100, 0.7)
y = ufloat(900.45, 0.6)

if y > x:
    w = y - x # ufloat - uint
    # w = ufloat(800.450, 0.922)
```
---

## Math functions

The library provides the following math functions for uint and ufloat types: 
*sqrt*(), *sin*(), *cos*(), *tan*(), *atan*(), *acos*(), *asin*(), *inverse*(), *floor*(), *round*(), *max*(...), *min*(...)

Example usage of max for uint and ufloat.
```python
m = max( 
    sin(ufloat(53.34, 0.8)),
    cos(uint(2, 0.6)),
    uint(23, 0.6), 
    floor(ufloat(3.4, 0.8)),
    uint(84, 0.6)
)
# m = uint(84, 0.600)
``` 

---
## The abool type

---

## The afloat type

---

## The aint type

---
## sbool

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Atenea Research Group
For more information, please visit our research group's websites: http://atenea.lcc.uma.es/projects/UncertainOCLTypes.html and http://atenea.lcc.uma.es/projects/SubjectiveLogic.html