# uTypes Python Library: User Guide

Uncertainty is an inherent property of any measure or estimation performed in any physical setting, and therefore it needs to be considered when modeling systems that manage real data. Although several modeling languages permit the representation of measurement uncertainty for describing some system attributes, these aspects are not normally incorporated into their type systems. Thus, operating with uncertain values and propagating uncertainty are normally cumbersome processes, difficult to achieve at the model level. This library provides an extension of Python basic datatypes to incorporate data uncertainty coming from physical measurements or user estimations into the models, along with the set of operations defined for the values of these types.

``uTypes`` is a Python library that supports a set of uncertain primitive datatypes, including [``ubool``](#type-ubool), [``sbool``](#type-sbool), [``uint``](#type-uint),  [``ufloat``](#type-ufloat), [``uenum``](#type-uenum) and [``ustr``](#type-ustr).
They extend their corresponding Python types (``bool``, ``int``,  ``float``, ``enum`` and ``str``) with uncertainty. 

The ``uTypes`` library implements linear error propagation theory in Python. Uncertainty calculations are performed analytically.

## Installation and Usage

To install the ``uType`` library, use the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
pip install uncertainty-datatypes
```

You can then import all the datatypes and functions as follows:

```python
from uncertainty.utypes import *
```

---
# Basic Datatypes

## Type ubool

Type ``ubool`` is an embedding of type ``bool`` that extends traditional logic truth values (``True``, ``False``), with probabilities, and truth tables are replaced with probability expressions. Thus, an ``ubool`` value is expressed by a probability representing the degree of belief (i.e., the *confidence*) that a given statement is true. For example, ``ubool(0.7)`` means that there is a 70% chance of an event occurring. Python ``bool`` values ``True`` and ``False`` correspond to ``ubool(1.0)`` and ``ubool(0.0)``, respectively. 

```python
x = ubool(0.7) 
y = ubool('0.7')  # A str can be used if it represent a float[0, 1]
z = ubool(1)      # int 0 or 1 can be used too.
w = ubool(False)  # True or False can be also used. 
                   #True -> ubool(1.0) and False -> ubool(0.0).
```
### Type projection

``ubool`` values can be projected to ``bool`` values, using a threshold that determines when the ``ubool`` value becomes ``True`` or ``False``. This threshold is called "level of certainty" and by default is 0.9. That is, ``ubool(z)`` becomes ``True`` if ``z > 0.9``.  The level of certainty can be changed using ``ubool.setCertainty(z)`` function. 

```python
y = ubool(0.7)

# Certainty by default: 0.9
if y:   # y is ubool(0.7) < 0.9
    'not executed'

ubool.setCertainty(0.5)
if y:   # y is ubool(0.7) >= 0.5
    'executed'
```

<mark>Como se conoce el valor de certainty? Hay alguna propiedad? Alguna operacion?</mark>

In this manner, ``ubool`` values can be used as booleans in conditional statements.

```python
if x:
    'executed'
```

It is also possible to know the confidence of an ``ubool`` value using the ``confidence`` property:

<mark>Me gustan mas las properties "confidence" que las operaciones "confidence()"...</mark>


```python
x = ubool(0.7)
print (x.confidence)
# 0.7
```



### Logical operators

Operations on ``ubool`` values extend those of ``bool`` values. This means that, when working with ``bool`` values, the behavior of ``ubool`` operations is exactly the same as their boolean versions. 


``ubool`` logical operators include: ``AND``, ``OR``, ``NOT``, ``XOR``, ``IMPLIES``, and ``EQUIVALENT``. The library offers the following four ways of using logical operators: 
* Infix symbol operators: ``` x & y ``` 
* Infix textual operators: ``` x |AND| y ``` 
* Instance methods: ``` x.AND(y) ``` 
* Functions: ``` AND(x, y) ```


The table below summarizes all the possible usages.

| Operation  | Infix (symbol)       | Infix (textual)            | Method                  | Function                 |
|:----------:|:---------------:|:--------------------------:|:-----------------------:|:------------------------:|
| AND        | ``` x & y ```   | ``` x \|AND\| y ```        | ``` x.AND(y) ```        | ``` AND(x, y) ```        |
| OR         | ``` x \| y ```  | ``` x \|OR\| y ```         | ``` x.OR(y) ```         | ``` OR(x, y) ```         |
| XOR        | ``` x ^ y ```   | ``` x \|XOR\| y ```        | ``` x.XOR(y) ```        | ``` XOR(x, y) ```        |
| NOT        | ``` ~x ```      |                            | ``` x.NOT() ```         | ``` NOT(x) ```           |
| IMPLIES    | ``` x >> y ```  | ``` x \|IMPLIES\| y ```    | ``` x.IMPLIES(y) ```    | ``` IMPLIES(x, y) ```    |
| EQUIVALENT | ``` ~(x^y) ```  | ``` x \|EQUIVALENT\| y ``` | ``` x.EQUIVALENT(y) ``` | ``` EQUIVALENT(x, y) ``` |
| EQUALS     | ``` x == y ```  | ``` x \|EQUALS\| y ```     | ``` x.EQUALS(y) ```     | ``` EQUALS(x, y) ```     |
| DISTINCT   | ``` x != y ```  | ``` x \|DISTINCT\| y ```   | ``` x.DISTINCT(y) ```   | ``` DISTINCT(x, y) ```   |


<mark>Ojo: "EQUIVALENT" no es lo mismo que "=="</mark>

***IMPORTANT***: 

- This library assumes variables are independent.
- All ``ubool`` operators must be enclosed in parentheses to ensure correct operator precedence. 

``ubool`` Code example:

```python
x = ubool(0.3)
y = ubool(0.8)
z = ubool(0.5)
t = ubool(0.2)

w = (~x & y) |IMPLIES| (z | t)
# w = ubool(0.776)
```

### Using ubools with bools

``ubool`` values can be used together with ``bool`` values, but always using ``ubool`` operators. 

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

Note that Python logical operations ``(3 > 2)`` must be enclosed in paretheses. Boolean ``True`` (e.g., the result of ``3 > 2``) is automatically converted into ``ubool(1.0)`` and ``False`` into ``ubool(0.0)``.

***IMPORTANT***: The Python logical operators (``and``, ``or``, and ``not``)  have a different meaning when they are used with objects. Therefore, ***``ubool`` special logical operators must ALWAYS be used to deal with ubool values***.   

<!---
``ubool never should be used with Python logical operators`` (and, or and not keywords). ``ubool special logical operators must be used instead`` 
-->

---

## Type ufloat

An ``ufloat`` value represents a ``float`` endowed with an associated uncertainty.

```python
x = ufloat(-230.30, 0.7) 
y = ufloat(233, '0.7')  # Data can be provided as str, int or float.
# y = ufloat(233.0, 0.7)
```

This representation of uncertainty for numerical values follows the "ISO Guide to Measurement Uncertainty" ([JCMG 100:2008](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf)), where values are represented by the mean and standard deviation of the assumed probability density function representing how measurements of ground truth values are distributed. For example, if we assume that the values of a variable $X$ follow a normal distribution $N(x, \sigma)$, then we set $u = \sigma$. If we can only assume a uniform or rectangular distribution of the possible values of $X$, then the nominal value $x$ is taken as the midpoint of the interval, $x = (a + b)/2$, and its associated standard deviation as $u = (b - a)/(2 * \sqrt{3})$.


### Operators

``ufloat`` operators include: ``ADD``, ``SUB``, ``MUL``, ``DIV``, ``FLOOR DIV``, ``NEG``, and ``POWER``. The table below summarizes all the possible operations. Uncertainty propagates through all the operations performed on variables with uncertainty.

| Operation | Operator      | Method                | Function               |
|:---------:|:-------------:|:---------------------:|:----------------------:|
| ADD       | ``` x + y ``` | ``` x.add(y) ```      | ``` add(x, y) ```      |
| SUB       | ``` x - y ``` | ``` x.sub(y) ```      | ``` sub(x, y) ```      |
| MUL       | ``` x * y ``` | ``` x.mul(y) ```      | ``` mul(x, y) ```      |
| DIV       | ``` x / y ``` | ``` x.div(y) ```      | ``` div(x, y) ```      |
| FLOOR DIV | ``` x // y ```| ``` x.floordiv(y) ``` | ``` floordiv(x, y) ``` |
| NEG       | ``` -x ```    | ``` x.neg(y) ```      | ``` neg(x, y) ```      |
| POW       | ``` x ** y ```| ``` x.power(y) ```    | ``` pow(x, y) ```      |

Infix operators are recommended. When using the traditional operators, precedence is respected and it works the same as with ``float`` values. 

In addition, any ``ufloat`` variable can be interrogated for its nominal value (x) and its uncertainty (u), using properties ``value`` and ``uncertainty``, respectively.

<mark>Mejor properties que methods!</mark>

#### Examples
```python
x = ufloat(925.69, 23.8)
y = ufloat(536.50, 31.83)
z = ufloat(-3404, 4.76)

w = (x / y)**2 - z
# w = ufloat(3406.977, 5.946)

print(w.value)
# 3406.977
print(w.uncertainty)
# 5.964
```

### Specifying the covariance of variables in operations

***IMPORTANT**: Variables are assumed to be independent. Among other things, this means that expressions should be simplified and reduced in order for the results to be correct. In case of having to operate with dependent variables, it is possible to specify their covariance, as described next.*

Operations ``add``, ``sub``, ``mul``, ``div``, and ``floordiv`` allow specifying the covariance of the operands as an additional parameter.

```python
x = ufloat(92.69, 3.8)
y = ufloat(56.50, 1.83)

w = x.add(y, covariance = 0.0)
# w = ufloat(149.190, 4.218)
z = x.add(y, covariance = 12.4)
# z = ufloat(149.190, 6.526)
```


### Usage with uint, int and float.

``ufloat`` values can be used together with values of type ``uint``, as well as with Python's ``float`` and ``int`` values ("crisp" values of types ``float`` and ``int`` act as scalars in this case).

```python
x = ufloat(5.69, 23.8)
y = x + 3.1
# y = ufloat(8.790, 23.8)
```

---

## Type uint

An ``uint`` is represented by an ``int`` value and an associated uncertainty. They work basically as ``ufloat`` values, but their nominal value is an ``int``. 

```python
x = uint(-654, 2.4) 
# x = uint(-654, 2.4)
y = uint(432, '5.7')  # Data can be provided as str, int or float.
# y = uint(432, 5.7)
```

### Operators

In addition to the operators defined also for ``ufloat``, type ``uint`` also supports operator ``MOD``. 

| Operation | Operator      | Method            | Function         |
|:---------:|:-------------:|:-----------------:|:----------------:|
| MOD       | ``` x % y ``` | ``` x.mod(y) ```  | ``` mod(x, y) ```|

Again, infix operators are recommended for type ``uint``. 


#### Example

```python
x = uint(145, 3.4)
y = uint(56, 4.35)
z = uint(23, 5.2)

w = (x // y)**3 % z
# w = uint(8, 1.246)
```

### Covariance methods

Covariance can also be specified in ``uint`` operations, exactly the same as with ``ufloat`` operations.

### Usage with ufloat, int and float

``uint`` values can be used together with ``ufloat`` values and with Python's ``float`` and ``int`` values.

```python
x = uint(5, 23.8)
y = x - 3
# y = ufloat(2, 23.800)
z = y - ufloat(0.3, 10.3)
# z = ufloat(1.700, 25.933)
```

## Comparison operators between uncertain numeric values

Comparison between uncertain numerical values (of types ``uint`` or ``ufloat``) no longer return ``bool`` values, but become probabilities, i.e., values of type ``ubool``.

For example, consider the real values $x=2.0$ and $y=2.5$. Using Real arithmetic, $x<y=$ true. However, assuming some given uncertainties, namely $x=2.0\pm 0.3$ and $y=2.5\pm 0.25$, then we obtain that $x<y$ with probability 0.893. 

```python
x = ufloat(2.0,0.3)
y = ufloat(2.5,0.25)
z = x < y
# z = ubool(0.893)
``` 

Given that ``ufloat`` and ``uint`` values can be considered random variables, they are compared using *equality in distribution*: two variables are equal if their distributions are the same.

Comparisons between ``uint`` and ``ufloat`` can be performed using the traditional comparison operators: ``<``, ``<=``, ``>``, ``>=``, ``==`` and ``!=``. These operators return ``ubool`` values.


| Operation         | Operator       | Method           | Function        |
|:-----------------:|:--------------:|:----------------:|:---------------:|
| Less than             | ``` x < y ```  | ``` x.lt(y) ```  | ``` lt(x, y) ```|
| Less than or Equals    | ``` x <= y ``` | ``` x.le(y) ```  | ``` le(x, y) ```|
| Greater than          | ``` x > y ```  | ``` x.gt(y) ```  | ``` gt(x, y) ```|
| Greater than or Equals | ``` x >= y ``` | ``` x.ge(y) ```  | ``` ge(x, y) ```|
| Equals            | ``` x == y ``` | ``` x.eq(y) ```  | ``` eq(x, y) ```|
| Not Equals        | ``` x != y ``` | ``` x.ne(y) ```  | ``` ne(x, y) ```|



Again, infix operators are recommended. 

#### Example
```python
x = uint(100, 0.7)
y = ufloat(900.45, 0.6)
z = ufloat(900.00, 0.6)
if y > x:
    w = y - x # ufloat - uint
    # w = ufloat(800.450, 0.922)
b = z < y
# b = ubool(0.292)
```

## Math functions

The library provides the following math functions for ``uint`` and ``ufloat`` variables and values: 
``sqrt()``, ``sin()``, ``cos()``, ``tan()``, ``atan()``, ``acos()``, ``asin()``, ``inverse()``, ``floor()``, ``round()``, ``max()``, ``min()``.

#### Example

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
## Type ustr

Values of type ``ustr`` are used to represent Python strings with uncertainty. That is, type ``ustr`` extends type ``str``, adding to their values a degree of confidence on the contents of the string. This is useful, for example, when rendering strings obtained by inaccurate OCR devices or texts translated from other languages if there are doubts about specific words or phrases. 

Values of type ``ustr`` are pairs ``(s,c)``, where ``s`` is the string and ``c`` the associated confidence (a real number between 0 and 1). To calculate the confidence of a string ``s``, the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) is normally used. For example, ``ustr('hell0 world!',0.92)`` means that we do not trust at most one of the 12 characters of the string. Values of Python type ``str`` are embedded into ``ustr`` values as ``ustr(s,1.0)``.


```python
x = ustr('What is Lorem Ipsum?', 0.97)
```

### Accesing individual characters
Individual characters of an uncertain string can be accesed using operation ``[index]`` or method ``uAt(index)``. The character on a given position can also be obtained using method ``at(index)``.

```python
x = ustr('What is Lorem Ipsum?', 0.97)

x.uAt(0)
# ustr('W', 0.97)
x[0]
# ustr('W', 0.97)
x.at(0)
# 'W'
```

### Slicing

Both operator ``[start, stop, step]`` and method ``uSubstring(start, stop, step)`` can be used to split an uncertain string. The ``start`` and ``stop`` indexes are optional, their default values being 0 and the lenght of the string, respectively. The third parameter is also optional with a default value of 1. Negative indexes are valid, they indicate positions from the right end of the string.

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

### Concatenating ustrs

Method ``.add(ustr)``, function ``add(ustr, ustr)`` or  operator ``+`` can be used to concatenate either uncertain string, or strings, or both, as the example below shows:

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

### Comparison Operators

Comparisons between uncertain strings can also be performed using the traditional operators, which now return  ``ubool`` values.

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

### ustr Methods

Further operations available for any uncertain string ``s`` include:

- ``s.len())``: returns the size of ``s`` as an ``int``.
- ``s.uLen()``: returns the size of ``s`` as ``uint``.
- ``s.uUpper()``: returns a new ``ustr`` with all characters of ``s`` converted into upper case.
- ``s.uLower()``: returns a new ``ustr`` with all characters of ``s`` converted into lower case.
- ``s.uCapitalize()``: returns a new ``ustr`` with the first character of ``s`` capitalized.
- ``s.uFirstLower()``: returns a new ``ustr`` with the first character of ``s`` in lower case.
- ``s.index(t)``: returns the index of the uncertain string ``t`` within ``s``.
- ``s.uCharacters()``: returns a list of ``ustr`` with each character of ``s``.

<mark>Queremos metodos o properties? Lo que se use en Python para eso...</mark>

### Conversion Methods

Given an uncertain string ``s`` that represents a ``float``, ``int``, ``bool``, ``ufloat``, ``unit``, or ``ubool`` value, the following methods provide conversion operations to the corresponding types.

- ``s.tofloat()`` or ``ustr.float(s)``: converts ``s`` into a ``float`` value. 
- ``s.toufloat()``: converts ``s`` into an ``ufloat`` value. 
- ``s.toint()`` or ``ustr.int(s)``: converts ``s`` into an ``int`` value. 
- ``s.touint()``: converts ``s`` into an ``uint`` value. 
- ``s.tobool()`` or ``ustr.bool(s)``: converts ``s`` into a ``bool`` value. 
- ``s.toubool()``: converts ``s`` into an ``ubool`` value. 

<mark>Queremos metodos o properties? Lo que se use en Python para eso...</mark>

---

## Type uenum

Type ``uenum`` is the embedding supertype for Python type ``enum`` that adds uncertainty to each of its values.
A value of an
uncertain enumeration type ``enum`` is not a single literal,
but a set of pairs $\{(l_1,c_1),...,(l_n,c_n)\}$, where $\{l_1,...,l_n\}$ are the enumeration literals and $\{c_1,...,c_n\}$ are numbers in the range [0, 1] that represent
the probabilities that the variable takes each literal as its value. They should fulfil that $c_1+...+c_n=1$. Pairs whose confidence $c_i$ is 0 can be omitted.

An ``uenum`` value can be created in three ways:
1. providing a Dictionary in Python whose keys are the literals and the values are their confidences;
2. providing a list of strings with the literals and a list with the confidence of each literal; 
3. providing a list of ``ustr`` values. 

```python
x = uenum(["Red", "Blue"], [0.3, 0.453])
y = uenum({"red": 0.8, "green": 0.771})
z = uenum([ustr("blue", 0.83), ustr("yellow", 0.7)])
```

The literals of an ``uenum`` value can be accessed using the property ``literals``. A copy of the Dictionary can be obtained with the property ``elements``. A list with the ``ustr`` values of each element of the uncertain enumeration can be obtained with the property ``ustrs``.
```python
x.literals
# ['Red', 'Blue']
x.elements
# {'Red': 0.3, 'Blue': 0.453}
x.ustrs
# [ustr(Red, 0.300), ustr(Blue, 0.453)]
```



---
## Type sbool

Type ``sbool`` provides an extension of ``ubool`` to represent binomial *opinions* in [Subjective Logic](https://en.wikipedia.org/wiki/Subjective_logic). They allow expressing degrees of belief with epistemic uncertainty, and also trust. A binomial opinion about a given fact X by a belief agent A is represented as a quadruple ``sbool(b,d,u,a)`` where

- ``b`` is the degree of belief that X is True
- ``d`` is the degree of belief that X is False
- ``u`` is the amount of uncommitted belief, also interpreted as epistemic uncertainty.
- ``a`` is the prior probability in the absence of belief or disbelief.

These values are all real numbers in the range [0,1] and satisfy that *b+d+u=1*. The "*projected*" probability of a binomial opinion is defined as *P=b+au*. 

<mark>To be done...</mark>

---
# Alternative representations

Package ``uTypes`` provides two different implementations for the extended numerical types values, using their corresponding Type-A and Type-B evaluations described in the "ISO Guide to Measurement Uncertainty" ([JCMG 100:2008](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf)). 

- In **Type A** implementations, uncertain values are represented by n independent observations $X = \{x_1,...,x_n\}$ that have been obtained under the same conditions of measurement. The value of the corresponding uncertain number corresponds to the mean of the sample, and the uncertainty is given by the standard deviation.  
- In **Type B** implementation, values are represented by the mean and standard deviation of the assumed probability density function that represents how the measurements of the ground truth values are expected to distribute (in case of floats and integers) or the degree of belief that an event will occur (in case of booleans).

Types ``ubool``, ``ufloat`` and ``uint`` previously described are implemented using **Type B** evaluation, and all type operations are implemented using closed-form expressions.

This package also provides **Type A** implementations, which are represented by types [``abool``](./TypeA-implementations.md#type-abool), [``aint``](./TypeA-implementations.md#type-aint) and [``afloat``](./TypeA-implementations.md#type-afloat). They provide the extensions of Python types ``bool``, ``float`` and ``int`` with uncertainty, respectively. They are described in a separate [document](./TypeA-implementations.md).

