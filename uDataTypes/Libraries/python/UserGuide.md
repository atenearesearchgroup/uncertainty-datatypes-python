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

Type ``ubool`` is an embedding of type ``bool`` that extends traditional logic truth values (``True``, ``False``) with probabilities, and replaces truth tables with probability expressions. Thus, an ``ubool`` value is expressed by a probability (i.e., a number between 0 and 1) representing the degree of belief (i.e., the *confidence*) that a given statement is true. For example, ``ubool(0.7)`` means that there is a 70% chance of an event occurring. Python ``bool`` values ``True`` and ``False`` correspond to ``ubool(1.0)`` and ``ubool(0.0)``, respectively. 

```python
x = ubool(0.7) 
y = ubool('0.7')  # A str can be used if it represent a float[0, 1]
z = ubool(1)      # int 0 or 1 can be used too.
w = ubool(False)  # True or False can be also used. 
                   #True -> ubool(1.0) and False -> ubool(0.0).
```
It is always possible to know the confidence of an ``ubool`` value using the ``confidence`` property:

```python
x = ubool(0.7)
print (x.confidence)
# 0.7
```

### Type conversion and projection

``ubool`` values can be converted to ``bool`` values, using a threshold that determines when the ``ubool`` value is evaluated as ``True`` or ``False``. This threshold is called "*level of certainty*" and its default value is ``0.9``.  The *level of certainty* can be changed using ``ubool.setCertainty(c: float)`` and queried using ``ubool.getCertainty()``. 

```python
y = ubool(0.7)

# Certainty by default: 0.9
if y:   # y is ubool(0.7) < 0.9
    'not executed'

ubool.setCertainty(0.5)
if y:   # y is ubool(0.7) >= 0.5
    'executed'

# Get certainty
ubool.getCertainty()
# 0.5
```

In this way, ``ubool`` values and variables can be used as booleans in conditional statements.

```python
if x:
    'executed'
```
In addition, method ``u.tobool() -> bool`` explicitly converts an ``ubool`` variable into a ``bool``, using the level of certainty: ``u.tobool() = (x.confidence > ubool.getCertainty())``.

### Logical operators

Operations on ``ubool`` values are proper extensions of those of type ``bool``. This means that, when working with ``bool`` values, the behavior of ``ubool`` operations is exactly the same as their boolean versions. 

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

Note that ``equal`` and ``equivalent`` operations are not the same. Equivalence corresponds to ``~(x^y)`` (i.e., the negation of ``xor``), while the equal operation (``==``) requires that the two values are the same.

***IMPORTANT***: 

- This library assumes variables are independent.
- All ``ubool`` operators must be enclosed in parentheses to ensure correct operator precedence. 

``ubool`` code example:

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

Note that Python logical operations ``(3 > 2)`` must be enclosed in parentheses. Boolean ``True`` (e.g., the result of ``3 > 2``) is automatically converted into ``ubool(1.0)`` and ``False`` into ``ubool(0.0)``.

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

``ufloat`` operators include: ``ADD``, ``SUB``, ``MUL``, ``DIV``, ``FLOOR DIV``, ``NEG``, and ``POW``. The table below summarizes all the possible operations. Uncertainty propagates through all the operations performed on variables with uncertainty.

| Operation | Infix operator| Method                | Function               |
|:---------:|:-------------:|:---------------------:|:----------------------:|
| ADD       | ``` x + y ``` | ``` x.add(y) ```      | ``` add(x, y) ```      |
| SUB       | ``` x - y ``` | ``` x.sub(y) ```      | ``` sub(x, y) ```      |
| MUL       | ``` x * y ``` | ``` x.mul(y) ```      | ``` mul(x, y) ```      |
| DIV       | ``` x / y ``` | ``` x.div(y) ```      | ``` div(x, y) ```      |
| FLOOR DIV | ``` x // y ```| ``` x.floordiv(y) ``` | ``` floordiv(x, y) ``` |
| NEG       | ``` -x ```    | ``` x.neg() ```       | ``` neg(x) ```         |
| POW       | ``` x ** y ```| ``` x.pow(y) ```      | ``` pow(x, y) ```      |

<!-- Infix operators are recommended.--> 
When using the traditional *infix* operators, precedence is respected and it works the same as with ``float`` values. 

In addition, any ``ufloat`` variable can be interrogated for its nominal value (``x``) and its uncertainty (``u``), using properties ``value`` and ``uncertainty``, respectively.

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

By default, variables are assumed to be independent. Among other things, this means that expressions should be simplified and reduced in order for the results to be correct. <!--  (for example, ``x-x`` is not the same as ``ufloat(0,0)``, but ``ufloat(0,1.4142*x.uncertainty)``). -->

In case of having to operate with dependent variables, it is possible to specify their covariance. In particular, operations ``add``, ``sub``, ``mul``, ``div``, and ``floordiv`` allow specifying the covariance of the operands as an additional parameter.

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

| Operation | Infix operator      | Method            | Function         |
|:---------:|:-------------:|:-----------------:|:----------------:|
| MOD       | ``` x % y ``` | ``` x.mod(y) ```  | ``` mod(x, y) ```|

<!-- Again, infix operators are recommended for type ``uint``.--> 


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

For example, consider the real values $x=2.0$ and $y=2.5$. Using Real arithmetic, $x < y$ = true. However, assuming some given uncertainties, namely $x=2.0\pm 0.3$ and $y=2.5\pm 0.25$, then we obtain that $x < y$ with probability 0.893. 

```python
x = ufloat(2.0,0.3)
y = ufloat(2.5,0.25)
z = x < y
# z = ubool(0.893)
``` 

Comparisons between ``uint`` and ``ufloat`` can be performed using the traditional comparison operators: ``<``, ``<=``, ``>``, ``>=``, ``==`` and ``!=``. These operators return ``ubool`` values.


| Operation               | Infix operator       | Method           | Function        |
|:-----------------------:|:--------------:|:----------------:|:---------------:|
| Less than               | ``` x < y ```  | ``` x.lt(y) ```  | ``` lt(x, y) ```|
| Less than or Equals     | ``` x <= y ``` | ``` x.le(y) ```  | ``` le(x, y) ```|
| Greater than            | ``` x > y ```  | ``` x.gt(y) ```  | ``` gt(x, y) ```|
| Greater than or Equals  | ``` x >= y ``` | ``` x.ge(y) ```  | ``` ge(x, y) ```|
| Equals                  | ``` x == y ``` | ``` x.eq(y) ```  | ``` eq(x, y) ```|
| Not Equals              | ``` x != y ``` | ``` x.ne(y) ```  | ``` ne(x, y) ```|

Given that ``ufloat`` and ``uint`` values can be considered random variables, they are compared using *equality in distribution*: two variables are equal (``==``) if their probability distributions are the same. 

<!-- Again, infix operators are recommended. -->

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

Values of type ``ustr`` are pairs ``(s, c)``, where ``s`` is the string and ``c`` the associated confidence (a real number between 0 and 1). To calculate the confidence of a string ``s``, the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) is normally used. For example, ``ustr('hell0 world!', 0.92)`` means that we do not trust at most one of the 12 characters of the string. Values of Python type ``str`` are embedded into ``ustr`` values as ``ustr(s, 1.0)``.


```python
x = ustr('What is Lorem Ipsum?', 0.97)
```

### Accesing individual characters
Individual characters of an uncertain string can be accesed using operation ``[index]`` or method ``at(index)``.

```python
x = ustr('What is Lorem Ipsum?', 0.97)

x[0]
# 'W'

x.at(0)
# 'W'
```

### Slicing

Both operator ``[start, stop, step]`` and method ``uSubstring(start, stop, step)`` can be used to split an uncertain string. ``start`` indicates the starting index of the substring. The character at this index is included in the substring. The default value is 0. ``end`` indicates the terminating index of the substring. The character at this index is not included in the substring. If ``end`` is not indicated, or if the specified value exceeds the string length, it is assumed to be equal to the length of the string by default. ``step`` indicates that every "step" character after the current character is to be included. The default value is 1.

Negative indexes are valid, they indicate positions from the right end of the string. Note that the ``confidence`` is adjusted according to the length of the substring. 

```python
x = ustr('What is Lorem Ipsum?', 0.97)

x[0: 4]
x[: 4]
x.uSubstring(0, 4)
# ustr(What, 0.993)

x[-6: ]
x.uSubstring(-6)
# ustr(Ipsum?, 0.979)
```


### Concatenating ustrs

Method ``add(ustr)``, function ``add(ustr, ustr)``, or  operator ``+`` can be used to concatenate uncertain strings, strings, or both, as the example below shows:

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

### Comparison operators

Comparisons between uncertain strings can also be performed using the traditional comparison operators (using their infix versions, as methods, or as functions), which now return  ``ubool`` values.

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

### ustr methods

Further operations available for any uncertain string ``s`` include:

- ``s.len() -> int`` returns the size of ``s`` as an ``int``.
- ``s.uLen() -> uint`` returns the size of ``s`` as ``uint``.
- ``s.uUpper() -> ustr`` returns a new ``ustr`` with all characters of ``s`` converted into upper case.
- ``s.uLower() -> ustr`` returns a new ``ustr`` with all characters of ``s`` converted into lower case.
- ``s.uCapitalize() -> ustr`` returns a new ``ustr`` with the first character of ``s`` capitalized.
- ``s.uFirstLower() -> ustr`` returns a new ``ustr`` with the first character of ``s`` in lower case.
- ``s.index(t: str) -> int`` returns the index of string ``t`` within ``s``.
<!-- - ``s.uCharacters()`` method returns a list of ``ustr`` with each character of ``s``. -->

### Conversion methods

Given an uncertain string ``s`` that represents a ``float``, ``int``, ``bool``, ``ufloat``, ``unit``, or ``ubool`` value, the following methods provide conversion operations to the corresponding types.

- ``s.tofloat() -> float`` converts ``s`` into a ``float`` value. 
- ``s.toufloat() -> ufloat`` converts ``s`` into an ``ufloat`` value. 
- ``s.toint()`` converts ``s`` into an ``int`` value. 
- ``s.touint()`` converts ``s`` into an ``uint`` value. 
- ``s.tobool()``  converts ``s`` into a ``bool`` value. 
- ``s.toubool()``  converts ``s`` into an ``ubool`` value. 

These instance methods also have their *function* counterparts: ``float(s: ustr) -> float``, ``int(s: ustr) -> int``, ``bool(s: ustr) -> bool``, ``ufloat(s: str) -> ufloat``, ``uint(s: ustr) -> uint``, ``ubool(s: ustr) -> ubool``.

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

Type ``sbool`` provides an extension of ``ubool`` to represent binomial *opinions* in [Subjective Logic](https://en.wikipedia.org/wiki/Subjective_logic). They allow expressing degrees of belief with epistemic uncertainty, and also trust.

A binomial opinion $w_X^A=(b,d,u,a)$ about a given fact $X$ by a belief agent $A$ is represented as a quadruple ``sbool(b, d, u, a)`` where

- Belief: ``b`` is the degree of belief that $X$ is True
- Disbelief: ``d`` is the degree of belief that $X$ is False
- Uncertainty: ``u`` is the amount of uncommitted belief, also interpreted as epistemic uncertainty.
- Base rate: ``a`` is the prior probability in the absence of belief or disbelief.

These values are all real numbers in the range [0,1], and satisfy that ``b+d+u=1``. The "*projected*" probability of a binomial opinion is defined as ``P=b+au``. 

Type ``sbool`` can be initialized providing the four ``float`` values, a ``bool`` or an ``ubool``.
```python
x = sbool() # Same as: sbool(True)
# sbool(1.000, 0.000, 0.000, 1.000)
y = sbool(False)
# sbool(0.000, 1.000, 0.000, 0.000)
z = sbool(0.7, 0.1, 0.2, 0.5)
# sbool(0.700, 0.100, 0.200, 0.500)
w = sbool(ubool(0.7))
# sbool(0.700, 0.300, 0.000, 0.700)
```

The four components of an opinion can be known using the corresponding properties:
```python
z = sbool(0.7, 0.1, 0.2, 0.5)
# sbool(0.700, 0.100, 0.200, 0.500)
z.belief
# 0.700
z.disbelief
# 0.100
z.uncertainty
# 0.200
z.base_rate
# 0.500
```

All information about Subjective Logic and the operations it defines to reason about opinions and trust can be found in Audun Jøsang's book "[Subjective Logic: A formalism to reason about uncertainty](https://link.springer.com/book/10.1007/978-3-319-42337-1)". 

### Conversion methods

Values of type ``sbool`` can be converted into ``ubool`` or ``bool`` values as follows:

- Method ``s.toubool() -> ubool`` converts an ``sboolean`` variable ``s`` into an ``ubool`` value by projecting it. That is, ``s.toubool() = s.projection()``

- Method ``s.tobool() -> bool`` converts an ``sboolean`` variable ``s`` into a ``bool`` value by projecting it and then using the degree of certainty: ``s.tobool() = (s.projection() >= ubool.getCertainty())``.


Sometimes, an ``sbool`` value needs to be converted into an equivalent one but with maximized uncertainty (i.e., with either null belief or disbelief):

- ``s.uncertaintyMaximized() -> sbool`` returns an ``sbool`` that is equivalent to ``s`` but with maximum uncertainty. 



<!--
The following conversion operations are provided for ``sbool``.

- ``createDogmaticOpinion``: convert a ``sbool`` into a dogmatic opinion: an opinion with complete certainty (uncertainty = 0).
- ``createVacuousOpinion``: convert a ``sbool`` into a vacuous opinion: an opinion with a uncertainty of 1.
- ``uncertainOpinion``: returns the equivalent ``sbool`` with maximum uncertainty. 
- ``s.tobool()`` or ``bool(s)``: converts an ``sbool`` into a ``bool`` value. 
- ``s.toubool()``: converts a ``sbool`` into an ``ubool`` value. 
-->

### Information access methods

In addition, type ``sbool`` supports the following query methods.

- ``s.projection() -> bool`` returns the projected probability of opinon ``s``, i.e., ``s.projection() = s.belief + s.uncertainty*s.base_rate``.
- ``s.isAbsolute() -> bool``  returns ``True`` iff ``s.belief == 1 or s.disbelief == 1``.
- ``s.isMaximizedUncertainty() -> bool``  returns ``True`` iff ``s.belief == 0 or s.disbelief == 0``.
- ``s.isVacuous() -> bool`` returns ``True`` iff ``s.uncertainty == 1``.
- ``s.isDogmatic() -> bool``  returns ``True`` iff ``s.uncertainty == 0``.
<!-- 
- ``s.isCertain(threshold) -> bool`` method returns ``True`` if the ``sbool`` has ``uncertainty >= threshold``.
- ``s.isUncertain(threshold) -> bool`` method returns ``True`` if the ``sbool`` has ``uncertainty < threshold``.
- ``s.certainty() ->`` method returns the certainty. (i.e., 1 - u).
-->


### Logical operators

Type ``sbool`` extends all the logical operations that type ``bool`` supports. This is a proper extension, which means that the behavior of ``sbool`` operations is exactly the same as their ``ubool`` and ``bool`` versions when applied to values of these latter types, although they now return ``sbool`` values.

Basic operations include ``AND``, ``OR``, ``NOT``, ``XOR``, ``IMPLIES``, and ``EQUIVALENT``. The same four ways of using these logical operators are supported: Infix symbol operators (``` x & y ```), Infix textual operators (``` x |AND| y ```), Instance methods (``` x.AND(y) ```) and functions (``` AND(x, y) ```).

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

Note that equal and equivalent operations are not the same. Equivalence corresponds to ``~(x^y)``, while the equal operation ``=='' requires all four components of the two opinions to be the same.

<!-- Infix operator are recommended.-->

### Union operations
<!--
- ``s.applyOn(sbool)`` Returns the ``sbool`` that results from adjusting the base rate to be the one given in the parameter.
- ``s.deduceY(sboolyGivenX, sboolyGivenNotX)``:  Deduction, returns Y, acting "self sbool" as X.
-->

The *addition* (or *union*)  operation defined in Subjective logic ($w_{X\cup Y}^A = w_X^A + w_Y^A$) is supported:


- ``s.union(y: sbool) -> sbool`` returns a ``sbool`` with the union of ``s`` and ``y``.

Moreover, we have defined a new operation that performs the weighted union of two opinions:

- ``s.weightedUnion(y: sbool) -> sbool`` returns a ``sbool`` with the weighted union of ``s`` and ``y``.

These two methods also have versions that allow calculating the union and weighted union of two or more opinions, as functions: 

- ``union(opinions: Collection[sbool]) -> sbool``
- ``weightedUnion(opinions: Collection[sbool]) -> sbool``

   
### Belief Fusion operations

[Belief fusion](https://www.mn.uio.no/ifi/english/people/aca/josang/publications/jwz2017-fusion.pdf) is a central concept in subjective logic. It allows opinions from different source agents $A_1,...A_n$ about the same fact $X$ to be merged, in order to provide an opinion representing a consensus agreement, or at least a single compromise opinion.

The ``uTypes`` Python library provides all the [fusion operations](https://www.mn.uio.no/ifi/english/people/aca/josang/publications/jwz2017-fusion.pdf) defined in Subjective logic. 


#### Binary fusion operators

Given two ``sbool`` opinions ``o1`` and ``o2``, the following methods return their fusion using the different operators.

| Fusion operation | Binary version (method) | 
|----------------|-----------------------|
| Constraint Belief Fusion (CBF) | ``o1.cbFusion(o2: sbool) -> sbool`` |
| Consensus & Compromise Fusion (CCF) | ``o1.ccFusion(o2: sbool) -> sbool`` |
| Aleatory Cumulative Fusion (aCBF) | ``o1.aleatoryCumulativeFusion(o2: sbool) -> sbool`` |
| Epistemic Cumulative Fusion (eCBF) | ``o1.epistemicCumulativeFusion(o2: sbool) -> sbool`` |
| Averaging Belief Fusion (ABF) | ``o1.averagingFusion(o2: sbool) -> sbool`` |
| Weighted Belief Fusion (WBF) | ``o1.weightedFusion(o2: sbool) -> sbool`` |
| Minimum Belief Fusion (MinBF) | ``o1.minimumFusion(o2: sbool) -> sbool`` |
| Majority Belief Fusion (MajBF) | ``o1.majorityFusion(o2: sbool) -> sbool`` |

Example of use of ``cbFusion()`` operator:
```python
x = sbool(0.0, 0.40, 0.6, 0.5)
y = sbool(0.55, 0.3, 0.15, 0.38)
x.cbFusion(y)
# sbool(0.423, 0.462, 0.115, 0.418)
```

#### Fusion of collections of opions

The ``uTypes`` Python library also supports the following *functions* that allow to fuse two or more opinions:

| Fusion operation | Collection version (function) | 
|----------------|-----------------------|
| Constraint Belief Fusion (CBF) | ``cbFusion(c: Collection[sbool]) -> sbool`` |
| Consensus & Compromise Fusion (CCF) | ``ccFusion(c: Collection[sbool]) -> sbool`` |
| Aleatory Cumulative Fusion (aCBF) | ``aleatoryCumulativeFusion(c: Collection[sbool]) -> sbool`` |
| Epistemic Cumulative Fusion (eCBF) | ``epistemicCumulativeFusion(c: Collection[sbool]) -> sbool`` |
| Averaging Belief Fusion (ABF) | ``averagingFusion(c: Collection[sbool]) -> sbool`` |
| Weighted Belief Fusion (WBF) | ``weightedFusion(c: Collection[sbool]) -> sbool`` |
| Minimum Belief Fusion (MinBF) | ``minimumFusion(c: Collection[sbool]) -> sbool`` |
| Majority Belief Fusion (MajBF) | ``majorityFusion(c: Collection[sbool]) -> sbool`` |

Example of Belief Constraint Fusion:
```python
opinions = [
    sbool(0.0, 0.40, 0.6, 0.5), 
    sbool(0.55, 0.3, 0.15, 0.38), 
    sbool(0.1, 0.75, 0.15, 0.38),
    sbool(0.151, 0.48, 0.369, 0.382) 
]
cbFusion(opinions)
# sbool(0.126, 0.861, 0.013, 0.393)
```

### Discount operator

Subjective logic can also be used to represent and reason about trust. In this context, *trust discounting* is used to express degrees of trust in an information source and then to discount it from all the information provided by that source. The ``discount()`` method is used to compute the trust-discounted opinion. 

Thus, given an opinion ``b_X`` that represents the opinion (i.e., the *functional trust*) of an agent $B$ about a statement $X$, i.e., $[B:X]$, and an opinion ``trustofAOnB`` that represents the *trust referral* that Agent $A$ has on agent $B$, i.e., $[A\ ;B]$, then,

- ``b_X.discount(trustOfAonB: sbool) -> sbool``

returns the derived opinion of $A$ about $X$, i.e., $[A:X]=[A\ ;B]\otimes[B:X]$. This operation follows the defintion given in [Jøsang's book](https://link.springer.com/book/10.1007/978-3-319-42337-1) (Section 14.3.2). 

We also provide the alternative defintion of the discount operator given by [Hardi et al.](https://www.hindawi.com/journals/wcmc/2018/1073216/), which uses the degree of belief instead of the projection of the opinion to compute the discounted opinion:

- ``b_X.discountB(trustOfAonB: sbool) -> sbool``

### Discount operator on multi-edge paths

We also implement the discounting operator on multi-edge paths, using the "probability-sensitive trust discounting operator" (section 14.3.4 of [Jøsang's book](https://link.springer.com/book/10.1007/978-3-319-42337-1)). 

We assume that ``An_X`` represents the opinion (functional trust) of an agent $A_n$ on statement $X$, i.e., $[A_n:X]$, and that ``agentsTrusts`` is a collection of opinions with the *trust referrals* that Agent $A_i$ has on Agent $A_{i+1}$, i.e., $[A_i\ ;A_{i+1}]$. Then,

- ``An_X.discount(agentsTrusts: Collection[sbool]) -> sbool``

returns an ``sbool`` value that represents the resulting opinion of $A_1$ on $X$, i.e., $[A_1:X]=[A_1;A_2;...;A_n]\otimes[A_n:X]$.

The alternative implementation by [Hardi et al.](https://www.hindawi.com/journals/wcmc/2018/1073216/) is also supported in the ``uTypes`` library:

- ``An_X.discountB(agentsTrusts: Collection[sbool]) -> sbool``

Discount code example:
```python
b_x = sbool(0.95, 0, 0.05, 0.20) 
a_on_b = sbool(0.0, 0.0, 1, 0.9) 
b_x.discount(a_on_b)
# sbool(0.855, 0.000, 0.145, 0.200)
```

<!--

---
# Alternative representations

Package ``uTypes`` provides two different implementations for the extended numerical types values, using their corresponding Type-A and Type-B evaluations described in the "ISO Guide to Measurement Uncertainty" ([JCMG 100:2008](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf)). 

- In **Type A** implementations, uncertain values are represented by n independent observations $X = \{x_1,...,x_n\}$ that have been obtained under the same conditions of measurement. The value of the corresponding uncertain number corresponds to the mean of the sample, and the uncertainty is given by the standard deviation.  
- In **Type B** implementation, values are represented by the mean and standard deviation of the assumed probability density function that represents how the measurements of the ground truth values are expected to distribute (in case of floats and integers) or the degree of belief that an event will occur (in case of booleans).

Types ``ubool``, ``ufloat`` and ``uint`` previously described are implemented using **Type B** evaluation, and all type operations are implemented using closed-form expressions.

This package also provides **Type A** implementations, which are represented by types [``abool``](./TypeA-implementations.md#type-abool), [``aint``](./TypeA-implementations.md#type-aint) and [``afloat``](./TypeA-implementations.md#type-afloat). They provide the extensions of Python types ``bool``, ``float`` and ``int`` with uncertainty, respectively. They are described in a separate [document](./TypeA-implementations.md).

-->
