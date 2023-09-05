# Alternative representations of uncertain types 

Package ``uTypes`` provides two different implementations for the extended numerical types values, using their corresponding Type-A and Type-B evaluations described in the "ISO Guide to Measurement Uncertainty" ([JCMG 100:2008](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf)). 

- In **Type A** implementations, uncertain values are represented by *n* independent observations X = {*x*<sub>1</sub>,...,*x*<sub>*n*</sub>} that have been obtained under the same conditions of measurement. The value of the corresponding uncertain number corresponds to the mean of the sample, and the uncertainty is given by the standard deviation.  
- In **Type B** implementation, values are represented by the mean and standard deviation of the assumed probability density function that represents how the measurements of the ground truth values are expected to distribute (in case of floats and integers) or the degree of belief that an event will occur (in case of booleans).

Types [``ubool``](./UserGuide.md#type-ubool), [``ufloat``](./UserGuide.md#type-ufloat) and [``uint``](./UserGuide.md#type-uint) are implemented using **Type B** evaluation, and all type operations are implemented using closed-form expressions.

This package also provides the **Type A** implementations of these three datatypes, which are represented by types ``abool``, ``aint`` and ``afloat``. These are described next.

1. ``u-type`` datatypes: ubool, uint, ufloat, ustr, uenum.
    Type U is a pair (x, u), noted x ± u, that represents a random variable whose average is x and standard deviation is u.
2. ``a-type`` datatypes: abool, aint, afloat.
    Type A, maintain the set of the measured values as X = {x1,...,xn}, x ± u could be calculated as the mean and standard deviation.
3. ``s-type`` datatype: sbool.
    A particular type of subjective uncertainty (Belief Uncertainty) when a user is not sure about the truth of a statement.


<!--- 
---
## Type abool

<mark>**OJO**: To be done</mark>

---
## Type afloat

<mark>**OJO**: To be done</mark>
---

## Type aint

<mark>**OJO**: To be done</mark>
-->