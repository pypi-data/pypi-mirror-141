Default Mutable
==========

### *Prevent mutable default value behavior*

Default Mutable is a Python decorator that overrides default mutable values and prevents object mutation from one call to another. More info on https://docs.python-guide.org/writing/gotchas/

## Features

- Easy to use
- Preset default value

## Advantages

- Highly flexible
- Lightweight and independent
- Open-source
- Real use cases
- Support & documentation

## Authors

- Rudy Fernandez

## Install
The easiest way to install default_mutable using pip:
`pip install default_mutable`

## [Examples](https://github.com/roodrepo/default_mutable/blob/v0-dev/examples/example1.py)


Python’s default arguments are evaluated once when the function is defined, not each time the function is called (like it is in say, Ruby). This means that if you use a mutable default argument and mutate it, you will and have mutated that object for all future calls to the function as well.
```python
def function1(idx, dict1 = {}, list1 = [], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function1:')
function1(idx= 1)   # 1 {'a1': 'a1'} ['a']
function1(idx= 2)   # 2 {'a1': 'a1', 'a2': 'a2'} ['a', 'a']
```

---

Setting all the arguments with mutable default arguments to an **EMPTY** dictionary or list
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable
def function2(idx, dict1 = {}, list1 = [], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function2:')
function2(1)    # 1 {'a1': 'a1'} ['a']
function2(2)    # 2 {'a2': 'a2'} ['a']
```

---

Setting all the arguments with mutable default arguments to an **EMPTY** dictionary or list
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable
def function2_2(idx, dict1 = {}, list1 = ['list_init'], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function2_2:')
function2_2(1)    # 1 {'a1': 'a1'} ['a']
function2_2(2)    # 2 {'a2': 'a2'} ['a']
```

---

When the decorator is executed with not arguments, we get the default behavior (same as "function1")
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable()
def function3(idx, dict1 = {}, list1 = [], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function3:')
function3(idx= 1)   # 1 {'a1': 'a1'} ['a']
function3(idx= 2)   # 2 {'a1': 'a1', 'a2': 'a2'} ['a', 'a']
```

---

As no value is passed, the decorator set the default value for "dict1" and "list1" an empty dictionary and empty list
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable('dict1', 'list1')
def function4(idx, dict1 = {}, list1 = [], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function4:')
function4(idx= 1)   # 1 {'a1': 'a1'} ['a']
function4(idx= 2)   # 2 {'a2': 'a2'} ['a']
```

---

As no value is passed, the decorator set the default value for "dict1" and "list1" an empty dictionary and empty list
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable('dict1', 'list1')
def function4_2(idx, dict1 = {}, list1 = ['init'], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function4_2:')
function4_2(idx= 1)   # 1 {'a1': 'a1'} ['a']
function4_2(idx= 2)   # 2 {'a2': 'a2'} ['a']
```

---
As no value is passed, the decorator set the default value for "list1" an empty list. "dict1" has the default behavior
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable('list1')
def function4_3(idx, dict1 = {}, list1 = [], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function4_3:')
function4_3(idx= 1) # 1 {'a1': 'a1'} ['a']
function4_3(idx= 2) # 2 {'a1': 'a1', 'a2': 'a2'} ['a']
```

---
The default values are mutable and "list1" get incremented from one function to the other
```python
def function5(idx, dict1 = {}, list1 = ['init'], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function5:')
function5(idx= 1)   # 1 {'a1': 'a1'} ['init', 'a']
function5(idx= 2)   # 2 {'a1': 'a1', 'a2': 'a2'} ['init', 'a', 'a']
```

---
Default value for "list1" is not an empty list
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable('dict1', list1= ['init'])
def function6(idx, dict1 = {}, list1 = ['init'], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function6:')
function6(idx= 1)   # 1 {'a1': 'a1'} ['init', 'a']
function6(idx= 2)   # 2 {'a2': 'a2'} ['init', 'a']
```

---
Default value for "list1" is not an empty list
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable('dict1', list1= ['init'])
def function7(idx, dict1 = {}, list1 = [], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function7:')
function7(idx= 1)   # 1 {'a1': 'a1'} ['init', 'a']
function7(idx= 2)   # 2 {'a2': 'a2'} ['init', 'a']
```

---
Default value are empty dictionary and empty list
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable('dict1', list1= [])
def function7_2(idx, dict1 = {}, list1 = ['init'], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function7_2:')
function7_2(idx= 1) # 1 {'a1': 'a1'} ['a']
function7_2(idx= 2) # 2 {'a2': 'a2'} ['a']
```
---
Default value are empty dictionary and empty list
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable('dict1', 'list1')
def function7_3(idx, dict1 = {}, list1 = ['init'], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function7_3:')
function7_3(idx= 1) # 1 {'a1': 'a1'} ['a']
function7_3(idx= 2) # 2 {'a2': 'a2'} ['a']
```

---
Default value for "dict1" and "list1" are preset
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable(dict1= {'dict_init': 'dict_init'}, list1= ['init'])
def function8(idx, dict1 = {}, list1 = [], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function8:')
function8(idx= 1)   # 1 {'dict_init': 'dict_init', 'a1': 'a1'} ['init', 'a']
function8(idx= 2)   # 2 {'dict_init': 'dict_init', 'a2': 'a2'} ['init', 'a']
```

---
Passed values are not overridden
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable(dict1= {'dict_init': 'dict_init'}, list1= ['init'])
def function9(idx, dict1 = {}, list1 = [], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function9:')
function9(idx= 1, dict1= {'dict_value': 'dict_value'}, list1= ['list_value'])   # 1 {'dict_value': 'dict_value', 'a1': 'a1'} ['list_value', 'a']
function9(idx= 2, dict1= {'dict_value': 'dict_value'}, list1= ['list_value'])   # 2 {'dict_value': 'dict_value', 'a2': 'a2'} ['list_value', 'a']

```

---
Passed values are not overridden
```python
from default_mutable.DefaultMutable import defaultMutable

@defaultMutable(dict1= {'dict_init': 'dict_init'}, list1= ['init'])
def function10(idx, dict1 = {}, list1 = [], element = 'a'):
    list1.append(element)
    dict1[f'{element}{idx}'] = f'{element}{idx}'
    print('', idx, dict1, list1)

print('')
print('function10:')
function10(1, {'dict_value': 'dict_value'}, ['list_value']) # 1 {'dict_value': 'dict_value', 'a1': 'a1'} ['list_value', 'a']
function10(2, {'dict_value': 'dict_value'}, ['list_value']) # 2 {'dict_value': 'dict_value', 'a2': 'a2'} ['list_value', 'a']
```

