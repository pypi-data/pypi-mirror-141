## ULOWA MODULE 
Please, read carefully before using this library.

This module implements the ULOWA aggregation operator: Unbalanced Linguistic Ordered Weighted Average. 
Aggregation operators for linguistic variables usually assume uniform and symmetrical distribution of 
the linguistic terms that define the variable. However, there are some problems where an unbalanced set 
of linguistic terms is more appropriate to describe the objects. ULOWA accepts a set of linguistic labels 
defined with unbalanced fuzzy sets. The fuzzy sets must define a fuzzy partition on the set of reference values. 
They can be defined by trapezoidal or triangular membership functions.



This module has been made for academic purposes. If you want to use it, cite the author.

### 1. Installation
First, you can simpy install it by using the pip comand: `pip install ulowa`
### 2. Usage
#### 2.1. ULOWA
It is necessary to define a **fuzzy set**, each one with 4 points, e.g:
`fuzzyNumbers = [[0.0, 0.0, 1.0, 2.0], [1.0, 2.0, 4.0, 5.0], [4.0, 5.0, 5.0, 6.0], [5.0, 6.0, 6.0, 7.0],
                [6.0, 7.0, 8.0, 8.5], [8.0, 8.5, 9.0, 9.5], [9.0, 9.5, 10.0, 10.0]]`

*Note that the scale may vary, it isn't compulsory to be from 0 to 10*

Then, you must define the weights and the labels for the scale, e.g:
`weights = [0.6, 0.2, 0.2, 0.0, 0.0]`
`labels = ["VL", "L", "M", "AH", "H", "VH", "P"]`

*Note that the weights must sum up to 1, and the scale must be ordered from worst to best tag.*

Now, we should define the labels for our specific problem, e.g:
`problem_labels = ["VL", "VL", "L", "M", "L"]`

Eventually, we call the ULOWA function:
`ulowaOperation(problem_labels, weights, fuzzyNumbers, labels)`

In case you need to analyze more alternatives, you may need to establish a performance table e.g: `performance_table` in which you will include several problem labels, such as:
`performance_table = [["VL", "VL", "P", "H", "VL"], ["VL", "VL", "H", "P", "P"], ["VL", "VL", "L", "M", "L"],
                     ["VH", "L", "H", "H", "AH"], ["P", "L", "H", "L", "AH"]]`

*Note that the tags doesn't need to be sorted, since a specific method will do so.*

Now, in order to get a table with all the results, you should execute a code like the following:
```
fuzzyNumbers = [[0.0, 0.0, 1.0, 2.0], [1.0, 2.0, 4.0, 5.0], [4.0, 5.0, 5.0, 6.0], [5.0, 6.0, 6.0, 7.0], 
                [6.0, 7.0, 8.0, 8.5], [8.0, 8.5, 9.0, 9.5], [9.0, 9.5, 10.0, 10.0]]
 
labels = ["VL", "L", "M", "AH", "H", "VH", "P"]

weights = [0.6, 0.2, 0.2, 0.0, 0.0]
 
performance_table = [["VL", "VL", "P", "H", "VL"], ["VL", "VL", "H", "P", "P"], ["VL", "VL", "L", "M", "L"],
                     ["VH", "L", "H", "H", "AH"], ["P", "L", "H", "L", "AH"]]
results = []
for alternative in performance_table:
    results.append(ulowaOperation(alternative, weights, fuzzyNumbers, labels))
print(results)

```
#### 2.2. Specificity and Fuzziness
This module also allows you to calculate the specificity and fuzziness of a given fuzzy set.
In this case, a code like the shown below must be executed:
```
a = fuzzyNumbers[0][0]
b = fuzzyNumbers[len(fuzzyNumbers) - 1][3]
order=1
for i in fuzzyNumbers:
    print(f"\nThe specificity of the {order} fuzzy set is: {specificity(i, a, b)}")
    print(f"\nThe fuzziness of the {order} fuzzy set is: {fuzziness(i, a, b)}")
    order = order + 1
```
#### 2.3. Defuzzification
There are three methods that can be used in this package: `defuzzifyCOG(fuzzyNumbers, labels, tag)`, `defuzzifyOrdinal(scale, tag)` and `defuzzifyCOM(fuzzyNumbers, labels, tag)`.
Here is an example code of their usage:
```  
tag = "VL"           

print(f"The center of gravity of the first fuzzy set is: {defuzzifyCOG(fuzzyNumbers, labels, tag)}")
print(f"The center of maximum of the first fuzzy set is: {defuzzifyCOM(fuzzyNumbers, labels, tag)}")


# Those will give us the COG and COM of the first fuzzy number, since we specified tag VL


print(f"The ordinal value for tag {tag} is {defuzzifyOrdinal(labels, tag)}")

```
*The code shown above can be done in a loop so that we can get for example the ordinal values for all the results of the ULOWA operation.*

**Author:** Universitat Rovira i Virgili (URV) - [ITAKA research group](https://deim.urv.cat/~itaka/itaka2/index.html) (Ignacio Miguel Rodríguez)

**Reference:** A. Valls, The Unbalanced Linguistic Ordered Weighted Averaging Operator, In: Proc. IEEE International Conference on Fuzzy Systems, FUZZ-IEEE 2010, IEEE Computer Society, Barcelona, Catalonia, 2010, pp. 3063-3070. [ULOWA article](https://ieeexplore.ieee.org/document/5584199)

**Contact:** [Send e-mail](mailto:aida.valls@urv.cat)