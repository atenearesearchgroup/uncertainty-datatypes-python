# uTypes Uncertainty Python Library

``uTypes`` is a Python library that supports uncertain primitive datatypes, including [``ubool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ubool), [``sbool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-sbool), [``uint``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-uint),  [``ufloat``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ufloat), [``uenum``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-uenum) and [``ustr``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ustr). They extend their corresponding Python types (``bool``, ``int``,  ``float``, ``enum`` and ``str``) with uncertainty. The ``uTypes`` library implements linear error propagation theory in Python.

Uncertain numerical values, [``ufloat``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ufloat) and [``uint``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-uint), are represented by pairs ``(x,u)`` where ``x`` is the numerical (nominal) value and ``u`` is its associated uncertainty. For example, ``ufloat(3.5, 0.1)`` represents the uncertain real number 3.5 $\pm$ 0.1, and ``uint(30, 1)`` represents the uncertain integer 30 $\pm$ 1. 

This representation of uncertainty for numerical values follows the "ISO Guide to Measurement Uncertainty" ([JCMG 100:2008](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf)), where values are represented by the mean and standard deviation of the assumed probability density function representing how measurements of the ground truth value are distributed. For example, if we assume that the values of a variable $X$ follow a normal distribution $N(x, \sigma)$, then we set $u = \sigma$. If we can only assume a uniform or rectangular distribution of the possible values of $X$, then the nominal value $x$ is taken as the midpoint of the interval, $x = (a + b)/2$, and its associated standard deviation as $u = (b - a)/(2 * \sqrt{3})$.

Type [``ubool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ubool) extends type ``bool`` by using propabilities instead of the traditional logical truth values (``True``, ``False``), and by replacing truth tables with probability expressions. Thus, an [``ubool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ubool) value is expressed by a probability representing the degree of belief (i.e., the *confidence*) that a given statement is true. For example, ``ubool(0.7)`` means that there is a 70% chance of an event occurring. Python ``bool`` values ``True`` and ``False`` correspond to ``ubool(1.0)`` and ``ubool(0.0)``, respectively. ``ubool`` values can be used instead of ``bool`` values, by *projecting* the probability using a [``certainty`` threshold](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-projection). 

Type [``sbool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-sbool) provides an extension of [``ubool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ubool) to represent binomial *opinions* in [Subjective Logic](https://en.wikipedia.org/wiki/Subjective_logic). They allow expressing degrees of belief with epistemic uncertainty, and also trust. 

A binomial opinion $w_X^A=(b,d,u,a)$ about a given fact $X$ by a belief agent $A$ is represented as a quadruple ``sbool(b,d,u,a)`` where

- ``b`` is the degree of belief that X is True
- ``d`` is the degree of belief that X is False
- ``u`` is the amount of uncommitted belief, also interpreted as epistemic uncertainty.
- ``a`` is the prior probability in the absence of belief or disbelief.

These values are all real numbers in the range [0,1], and satisfy that ``b+d+u=1``. The "*projected*" probability of a binomial opinion is defined as ``P=b+au``. 

Type [``ustr``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ustr) can be used to represent Python strings with uncertainty. I.e., type [``ustr``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ustr) extends type ``str``, adding to their values a degree of confidence on the contents of the string. This is useful, for example, when rendering strings obtained by inaccurate OCR devices or texts translated from other languages if there are doubts about specific words or phrases. Therefore, values of type [``ustr``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ustr)  are
pairs ``(s, c)``, where ``s`` is the nominal string and ``c`` the associated confidence (a real number between 0 and 1). To calculate the confidence of a string ``s``, the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) is normally used. For example, ``ustr('hell0 world!', 0.92)`` means that we do not trust at most one of the 12 characters of the string. Values of Python type ``str`` are embedded into [``ustr``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ustr) values as ``ustr(s, 1.0)``.


Finally, type [``uenum``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-uenum) is the embedding supertype for Python type ``enum`` that adds uncertainty to each of its values. A value of an
uncertain enumeration type ``enum`` is not a single literal,
but a set of pairs $\{(l_1,c_1),...,(l_n,c_n)\}$, where $\{l_1,...,l_n\}$ are the enumeration literals and $\{c_1,...,c_n\}$ are numbers in the range [0, 1] that represent
the probabilities that the variable takes each literal as its value. They should fulfil that $c_1+...+c_n=1$. Pairs whose confidence $c_i$ is 0 can be omitted. 

All related operations and Mathematical functions on these datatypes are supported. Check the [uTypes User Guide](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md) for details.

## Main features

The ``uTypes`` library provides a simple implementation of uncertainty for Python primitive datatypes, and implements linear error propagation theory in Python. Uncertainty calculations are performed analytically.
The goal of the library is to support the basic mechanisms for the expression and propagation of uncertainty, in a lightweight and efficient manner. 

A distinguishing feature of the ``uTypes`` library is that comparison operators return [``ubool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ubool) values. This is essential when comparing uncertain numerical values, since their comparison is also subject to uncertainty and this fact must be taken into account. Unfortunately, this feature is not supported by the rest of the related uncertainty libraries, such as the [uncertainties package](https://pythonhosted.org/uncertainties), "[soerp](https://pypi.python.org/pypi/soerp)" or "[mcerp](https://pypi.python.org/pypi/mcerp)".

Another distinctive feature of  ``uTypes`` library is that it naturally incorporates Subjective logic (type [``sbool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-sbool)) into the type system, as a natural extension of probabilistic logic (type [``ubool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ubool)). This enables the seamless combination of different types of uncertainties under the same library, and in particular the representation of both second-order uncertainty and trust. The type embedding mechanisms used in ``uTypes`` allow operations to be closed in the algebra of types, and where the extended operations work as expected when values of original types are given as input parameters.

Correlations between expressions are not automatically taken into account in ``uTypes``. This saves keeping track at all times of all correlations between quantities (variables and functions), improving the performance of the calculations. However, this implies that, ***by default, we assume that variables are independent***. Otherwise, the correlation between dependent variables must be explicitly specified, or dependencies between variables in numerical expressions must be eliminated when possible. For instance, users are expected to simplify numerical expressions as much as possible to avoid duplication of uncertain variables.

In any case, should there be a need to deal with dependent variables, [``uint``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-uint) and 
[``ufloat``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ufloat) mathematical operations allow specifying the correlation between them (see the [User Guide](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md/#covariance-methods)).

The derivatives of mathematical expressions are not automatically handled by the ``uTypes`` library, either. Again, this saves keeping track of the value of derivatives, something that also impacts performance. Other unsuported features include automatic handling of arrays of uncertain numbers, or higher-order analysis to error propagation.

In case derivatives or these further features are needed, other libraries that provide these features could be used instead. 
 
 - For example, the [uncertainties package](https://pythonhosted.org/uncertainties) supports uncertainty progagation, variable correlation, derivatives, and integration with the [NumPy](https://numpy.org/) package for scientific computation in Python. 
  
 - [soerp](https://pypi.python.org/pypi/soerp) is another uncertainty calculation package for Python that provides higher-order approximations of uncertainty. In particular, it supports a second-order analysis to error propagation. Mathematical functions, similar to those in the standard [math](http://docs.python.org/library/math.html) module, can also be evaluated directly using this package.

-  [mcerp](https://pypi.python.org/pypi/mcerp) provides a stochastic calculator for Monte Carlo methods that uses 
latin-hypercube sampling to perform non-order specific error propagation (or uncertainty analysis).

The problem is that these implementations are sometimes too slow, e.g., when used in iterative methods. Furthermore, their comparison operations are too basic and not expressive enough: they return *crisp* boolean values, disregarding the inherent uncertainty that occurs in the comparison between uncertain numerical values. The ``uTypes`` package successfully addresses these limitations.

In summary, the uncertain datatypes provided by the ``uTypes`` library is well suited for applications that require the basic mechanisms for the propagation of uncertainty, efficient computation, and a closed algebra of datatypes. In particular, the comparison of two uncertain numeric values returns a probability, i.e., an [``ubool``](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md#type-ubool) value, and subjective logic is implemented as a natural extension of probabilistic logic, and in turn of Boolean logic. More precisely, we implement the following type hierarchy:  ``bool`` <: ``ubool`` <: ``sbool``. 


## Installation

To install the ``uType`` library, use the package manager [pip](https://pip.pypa.io/en/stable/):

```bash
pip install uncertainty-datatypes
```

<sub>Note: pip3 may be used instead of pip</sub> 

## Usage

You can import all the datatypes and functions defined by ``uTypes`` as follows:

```python
from uncertainty.utypes import *
```

The companion [uTypes User Guide](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/python/UserGuide.md) provides details about all supported datatypes and its associated operations.

## Contributing

Pull requests are welcome. For major changes, please open an issue to discuss what you would like to change.

## License

[MIT Licence](https://choosealicense.com/licenses/mit/)


<ul> <li style="list-style-type: none;"> 

Copyright (c) 2023 Atenea Research group:

*Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.*</li>
</uL>

## Version control

The ``uTypes`` library was initially [developed in Java](https://github.com/atenearesearchgroup/uncertainty/blob/master/uDataTypes/Libraries/Java/README.md). This is the first version of this Python library (July 2023).

---

## References and further information


The following papers contain all the details about these datatypes:

- Manuel F. Bertoa, Loli Burgueño, Nathalie Moreno, Antonio Vallecillo. "Incorporating measurement uncertainty into OCL/UML primitive datatypes" Softw. Syst. Model. 19(5):1163-1189, 2020. https://doi.org/10.1007/s10270-019-00741-0
- Paula Muñoz, Loli Burgueño, Victor Ortiz, Antonio Vallecillo. "Extending OCL with Subjective Logic" J. Object Technol. 19(3): 3:1-15, 2020. https://doi.org/10.5381/jot.2020.19.3.a1

Examples of applications of the uncertainty datatypes presented here can be found in the following papers:

- Jean-Marc Jézéquel, Antonio Vallecillo. "Uncertainty-aware Simulation of Adaptive Systems"  ACM Transactions on Modeling and Computer Simulation, 33(3):8:1-8:19, 2023. https://doi.org/10.1145/3589517
- Lola Burgueño, Paula Muñoz, Robert Clarisó, Jordi Cabot, Sébastien Gérard, Antonio Vallecillo. "Dealing with Belief Uncertainty in Domain Models" ACM Trans. Softw. Eng. Methodol. 32(2):31:1-31:34, 2023. https://doi.org/10.1145/3542947
- Francisco J. Navarrete, Antonio Vallecillo.
"Introducing Subjective Knowledge Graphs" In Proc. of EDOC 2021. pp. 61-70, 2021. https://doi.org/10.1109/EDOC52215.2021.00017
- Nathalie Moreno, Manuel F. Bertoa, Loli Burgueño, Antonio Vallecillo. "Managing Measurement and Occurrence Uncertainty in Complex Event Processing Systems" IEEE Access 7:88026-88048, 2019. https://doi.org/10.1109/ACCESS.2019.2923953
- Victor Ortiz, Loli Burgueño, Antonio Vallecillo, Martin Gogolla. "Native Support for UML and OCL Primitive Datatypes Enriched with Uncertainty in USE" In Proc. of OCL@MoDELS 2019:59-66, 2019. https://ceur-ws.org/Vol-2513/paper5.pdf 
- Nathalie Moreno, Manuel F. Bertoa, Gala Barquero, Loli Burgueño, Javier Troya, Adrián García-López, Antonio Vallecillo. "Managing Uncertain Complex Events in Web of Things Applications". In Proc. of ICWE 2018:349-357, 2018. https://doi.org/10.1007/978-3-319-91662-0_28
- Loli Burgueño, Manuel F. Bertoa, Nathalie Moreno, Antonio Vallecillo. "Expressing Confidence in Models and in Model Transformation Elements" In Proc. of MoDELS 2018: 57-66, 2018. https://doi.org/10.1145/3239372.3239394


For more information, please visit our research group's website: 
- [Atenea Research Group](http://atenea.lcc.uma.es/) 
- [Atenea: Uncertain UML/OCL Types](http://atenea.lcc.uma.es/projects/UncertainOCLTypes.html) 
- [Atenea: Subjective Logic](http://atenea.lcc.uma.es/projects/SubjectiveLogic.html)
