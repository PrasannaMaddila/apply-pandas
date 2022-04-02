# apply-pandas 
## Generic Apply Function for Pandas DataFrames

This repo demonstrates a powerful, simple and generic way to make an `apply` function for Pandas DataFrames. `apply` takes in a list of conditions (**as strings**) to apply to a dataframe, and returns the result of those applications.

This can be useful when you want to avoid writing huge chunks of code to filter data, or when you want to construct code based on other factors to give you a properly formatted result. Case in point - user input can be turned into well-defined string queries/filters on your DataFrame, with which you can return the appropriate data, *without* knowing those queries in advance.

## Overview and Usage
--- 
Import statement is 

```python 
from apply_pandas.apply import Apply 
```

The Apply function is wrapped in a functor so that we can cleanly separate verification and application. Furthermore, this also allows us to clearly bind the target DatFrame and the desired conditions together; something that might not always be easy when dealing with rapidly changing variables, while giving the programmer the option to call it when desired. 

In effect, you can bind at creation, but can safely get the computation much, much later. Here's a code snippet that illustrates the usage of this method.

```python 
# First, we create our dummy data
df = pd.DataFrame(list(range(0, 100)), columns=["Slice"])

# Then a list of conditions to apply.
list_condns = ["frame['Slice']<5", "frame['Slice']%3==1"]

# To use the Apply() class,
# First create an object that binds DataFrame and conditions,
Applicator = Apply(df, list_condns)

# Call for the result when needed.
result = Applicator() #<--- returns pandas DataFrame
``` 

**Notice** that in `list_condns`, all of our conditions are made out to `frame`, regardless of the actual name of the actual target frame. This means that when you generate these conditions in real-time, you do not ever have to worry about getting the name of the variable - just make out the filter for `frame`, and we'll take care of the rest :)

## Bugfixes and Improvements 

This code is always ready for improvements, and to get rid of bugs - so please let me know if you've found anything, or how you've used this project! Hope you have fun with it :)
