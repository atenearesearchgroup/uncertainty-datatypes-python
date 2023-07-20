# Uncertainty Python Library

Uncertainty is a Python library providing uncertain primitive datatypes, including booleans, reals and integers endowed with uncertainty. 

  including u-type, a-type and s-type: 
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
from uncertainty.utypes import *
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

ubool logical operators include: *AND*, *OR*, *NOT*, *XOR*, *IMPLIES*, and *EQUIVALENT*. The library offers the following four ways of using logical operators: 
* Operator: ``` x & y ``` 
* Special operator: ``` x |AND| y ``` 
* The ubool method: ``` x.AND(y) ``` 
* A function: ``` AND(x, y) ```

The table below summarizes all the possible usages.

| Operation  | Operator        | Special Operator           | Method                  | Function                 |
|:----------:|:---------------:|:--------------------------:|:-----------------------:|:------------------------:|
| AND        | ``` x & y ```   | ``` x \|AND\| y ```        | ``` x.AND(y) ```        | ``` AND(x, y) ```        |
| OR         | ``` x \| y ```  | ``` x \|OR\| y ```         | ``` x.OR(y) ```         | ``` OR(x, y) ```         |
| XOR        | ``` x ^ y ```   | ``` x \|XOR\| y ```        | ``` x.XOR(y) ```        | ``` XOR(x, y) ```        |
| NOT        | ``` ~x ```      |                            | ``` x.NOT() ```         | ``` NOT(x) ```           |
| IMPLIES    | ``` x >> y ```  | ``` x \|IMPLIES\| y ```    | ``` x.IMPLIES(y) ```    | ``` IMPLIES(x, y) ```    |
| EQUIVALENT | ``` x == y ```  | ``` x \|EQUIVALENT\| y ``` | ``` x.EQUIVALENT(y) ``` | ``` EQUIVALENT(x, y) ``` |
| EQUALS     | ``` x == y ```  | ``` x \|EQUALS\| y ```     | ``` x.EQUALS(y) ```     | ``` EQUALS(x, y) ```     |
| DISTINCT   | ``` x != y ```  | ``` x \|DISTINCT\| y ```   | ``` x.DISTINCT(y) ```   | ``` DISTINCT(x, y) ```   |

<sub> Operators or special operators must be surrounded by parentheses due operator precedence. Meanwhile, using a method or the function provides the highest precedence. </sub>

*ubool Code example:*
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

The level of certainty changes when a ubool is evaluated to True. The level of certainty can be set using **ubool.setCertainty()** function. By default, 0.9 is used.

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

A ufloat value represents a float endowed with its asscciated uncertainty.

```python
x = ufloat(-230.30, 0.7) 
y = ufloat(233, '0.7')  # Data can be provided as str, int or float.
# y = ufloat(233.0, 0.7)
```

#### Operators

ufloat operators include: *ADD*, *SUB*, *MUL*, *DIV*, *FLOOR DIV*, *NEG*, *POWER*. The table below summarizes all the possible operations.

| Operation | Operator      | Method                | Function               |
|:---------:|:-------------:|:---------------------:|:----------------------:|
| ADD       | ``` x + y ``` | ``` x.add(y) ```      | ``` add(x, y) ```      |
| SUB       | ``` x - y ``` | ``` x.sub(y) ```      | ``` sub(x, y) ```      |
| MUL       | ``` x * y ``` | ``` x.mul(y) ```      | ``` mul(x, y) ```      |
| DIV       | ``` x / y ``` | ``` x.div(y) ```      | ``` div(x, y) ```      |
| FLOOR DIV | ``` x // y ```| ``` x.floordiv(y) ``` | ``` floordiv(x, y) ``` |
| NEG       | ``` -x ```    | ``` x.neg(y) ```      | ``` neg(x, y) ```      |
| POW       | ``` x ** y ```| ``` x.power(y) ```    | ``` pow(x, y) ```      |

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

A uint can be instantiated in the same way as for ufloat, providing the value and the uncertainty. 

```python
x = uint(-654, 2.4) 
# x = uint(-654, 2.4)
y = uint(432, '5.7')  # Data can be provided as str, int or float.
# y = uint(432, 5.7)
```

#### Operators

The operator MOD is included for uint. The rest of the operators available for uint are the same than those provided for ufloat: *ADD*, *SUB*, *MUL*, *DIV*, *FLOOR DIV*, *NEG*, *POWER*. 

| Operation | Operator      | Method            | Function         |
|:---------:|:-------------:|:-----------------:|:----------------:|
| MOD       | ``` x % y ``` | ``` x.mod(y) ```  | ``` mod(x, y) ```|

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
Comparison between uint and ufloat can be made using the comparison operators: <, <=, >, >=, == and !=. These perators return uboolean values.


| Operation         | Operator       | Method           | Function        |
|:-----------------:|:--------------:|:----------------:|:---------------:|
| Less              | ``` x < y ```  | ``` x.lt(y) ```  | ``` lt(x, y) ```|
| Less or Equals    | ``` x <= y ``` | ``` x.le(y) ```  | ``` le(x, y) ```|
| Greater           | ``` x > y ```  | ``` x.gt(y) ```  | ``` gt(x, y) ```|
| Greater or Equals | ``` x >= y ``` | ``` x.ge(y) ```  | ``` ge(x, y) ```|
| Equals            | ``` x == y ``` | ``` x.eq(y) ```  | ``` eq(x, y) ```|
| Not Equals        | ``` x != y ``` | ``` x.ne(y) ```  | ``` ne(x, y) ```|

<sub>Operators are recommended. The usage of methods or functions changes the precedence of the operation at execution as if it were enclosed in parentheses.</sub>

*ufloat Comparison Code example:*
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

*Example usage of max for uint and ufloat:*
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

## The ustr type

A ustr can be instantiated providing the string value and the certainty. Certainty is a float[0, 1] where 1 is the highest possible certainty while 0 is the lowest.

```python
x = ustr('What is Lorem Ipsum?', 0.97)
```

#### Accesing elements
Elements of the ustr can be accesed using *uAt(index)* or *[index]* operator. The character on the position can be obtained using *
at(index)*

```python
x = ustr('What is Lorem Ipsum?', 0.97)

x.uAt(0)
# ustr('W', 0.97)
x[0]
# ustr('W', 0.97)
x.at(0)
# 'W'
```

#### Slicing

The *[start, stop, step]* operator and the uSubstring(start, stop, step) method can be used to split the ustr. The start and stop indexes are optional, their default values are 0 and the lenght of the string. The third parameter is also optional with a default value of 1. Negative indexes are valid.

```python
x = ustr('What is Lorem Ipsum?', 0.97)

x[0: 4]
x[: 4]
x.uSubstring(0, 4)
#ustr('What', 0.97)

x[-6: ]
x.uSubstring(-6)
#ustr('Ipsum?', 0.97)
```

#### Concatenating ustrs

The method *.add(ustr)*, function *add(ustr, ustr)* or the operator + can be used to concat diferent ustrs or strings, example below:

```python
x = ustr('What is Lorem Ipsum?', 0.97)
y = ustr(' Lorem Ipsum is simply dummy text', 0.7)

x + y
concat(x, y)
x.concat(y)
# ustr(What is Lorem Ipsum? Lorem Ipsum is simply dummy text, 0.802)

x + ' Lorem Ipsum is simply dummy text'
concat(x, ' Lorem Ipsum is simply dummy text')
x.concat(' Lorem Ipsum is simply dummy text')
# ustr(What is Lorem Ipsum? Lorem Ipsum is simply dummy text, 0.989)
```

#### Comparison Operators

Comparisions between ustrs can be performed using the methods, functions and operators defined for booleans. A ubool is returned in coparison operations.

```python
x = ustr('What is Lorem Ipsum?', 0.97)
y = ustr('What is', 0.7)

x >= y
# ubool(0.679)

x.lt(y)
# ubool(0.321)

le(x, y)
# ubool(0.321)
```

#### ustr Methods

- *uLen()*: returns the size of the ustr as uint.
<sub> len(ustr) function can be used to obtain the length of the string as int. </sub>
- *uUpper()* returns a new ustr with all characters converted into upper case.
- *uLower()* returns a new ustr with all characters converted into lower case.
- *uCapitalize()* returns a new ustr with first character as capital letter.
- *uFirstLower()* returns a new ustr with first character as lower case.
- *index(s: str)* return the index of the string 's'.
- *uCharacters()* return a list of ustr with each character.

#### Conversion Methods

- *tofloat()* Convert the ustr into a float. *float(ustr) function can be used.*
- *toufloat()* Convert the ustr into a ufloat. 
- *toint()* Convert the ustr into a int. *int(ustr) function can be used.*
- *touint()* Convert the ustr into a uint. 
- *tobool()* Convert the ustr into a bool. *int(ustr) function can be used.*
- *toubool()* Convert the ustr into a ubool. 

---

## The uenum type

A uenum can be instantiated in three ways:
1. providing a dic where the key is the literal and the value the certainty;
2. providing a list of strings with the literals and a list with certainties of each string; 
3. providing a list of ustr. Certainty is a float[0, 1] where 1 is the highest possible certainty while 0 is the lowest.

```python
x = uenum(["Red", "Blue"], [0.3, 0.453])
y = uenum({"red": 0.8, "green": 0.771})
z = uenum([ustr("blue", 0.83), ustr("yellow", 0.7)])
```

literals can be accessed using the property 'literals'. A copy of the dict can be obtained with the property 'elements'. A list of ustr with each element can be obtained with the property 'ustrs'
```python
x.literals
# ['Red', 'Blue']
x.elements
# {'Red': 0.3, 'Blue': 0.453}
x.ustrs
# [ustr(Red, 0.300), ustr(Blue, 0.453)]
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
For more information, please visit our research group's websites: 
- [Atenea Research Group](http://atenea.lcc.uma.es/) 
- [Atenea: Uncertain OCL Types](http://atenea.lcc.uma.es/projects/UncertainOCLTypes.html) 
- [Atenea: Subjective Logic](http://atenea.lcc.uma.es/projects/SubjectiveLogic.html)
