# Add a module docstring here explaining the purpose of the code.
"""Spreadsheet Column Printer

This script allows the user to print to the console all columns in the
spreadsheet. It is assumed that the first row of the spreadsheet is the
location of the columns.

This tool accepts comma separated value files (.csv) as well as excel
(.xls, .xlsx) files.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * get_spreadsheet_cols - returns the column headers of the file
    * main - the main function of the script
"""
import numpy as np
import pandas as pd
from numpy.random import randn

# Create a Pandas Series
mylist = np.array([10, 20, 30])
labels = ['a', 'b', 'c']
d = {'a': 10, 'b': 20, 'c': 30}

pd.Series(data=mylist)

pd.Series(data=mylist, index=labels)

pd.Series(d)

# The following line seems to have no effect, consider removing it.
# W0104: Statement seems to have no effect (pointless-statement)
pd.Series(data=labels)

pd.Series([sum, print, len])

ser1 = pd.Series([1, 2, 3, 4], index=['QW', 'AB', 'CD', 'EF'])
ser2 = pd.Series([1, 2, 5, 4], index=['AB', 'CD', 'IJ', 'KL'])

print(ser1)
print(ser2)

# Perform arithmetic operations on Series
result = ser1 + ser2
print(result)

# Create a DataFrame
np.random.seed(100)
df = pd.DataFrame(randn(5, 4), ['Q', 'W', 'E', 'R', 'T'], ['Z', 'X', 'C', 'V'])
print(df)

df = pd.DataFrame(randn(5, 4), index='Q W E R T'.split(), columns='Z X C V'.split())
print(df)


# Create a new column 'NEW'
df['NEW'] = df['Z'] + df['X']
print(df)

# Drop the 'NEW' column
df.drop('NEW', axis=1, inplace=True)
print(df)

# Access a specific row
print(df.loc['Q'])
print(df.iloc[0])

# Access specific elements
print(df.loc['Q', ['Z', 'X']])

# Conditional selection
print(df > 0)
print(df[df['Z'] > 0])
print(df[(df['Z'] > 0) & (df['C'] > 0)])
print(df[(df['X'] > 0) | (df['C'] > 0)])

# Reset and set index
print(df.reset_index())
newwind = 'AB CD EF GH IJ'.split()
df['index'] = newwind
print(df.set_index('index'))

# Create a MultiIndex DataFrame
outside = ['G1', 'G1', 'G1', 'G2', 'G2', 'G2']
inside = [1, 2, 3, 1, 2, 3]
hier_index = list(zip(outside, inside))
hier_index = pd.MultiIndex.from_tuples(hier_index)
print(hier_index)

df = pd.DataFrame(np.random.randn(6, 3), index=hier_index, columns=['C', 'D', 'E'])
print(df)


df.index.names = ['Group', 'Num']
print(df)

# Concatenate DataFrames
df1 = pd.DataFrame({'Q': ['Q0', 'Q1', 'Q2', 'Q3'],
                    'W': ['W0', 'W1', 'W2', 'W3'],
                    'E': ['E0', 'E1', 'E2', 'E3']},
                   index=[0, 1, 2, 3])
df2 = pd.DataFrame({'Q': ['Q0', 'Q5', 'Q6', 'Q7'],
                    'W': ['W4', 'W5', 'W6', 'W7'],
                    'E': ['E4', 'E5', 'E6', 'E7']},
                   index=[4, 5, 6, 7])

print(df1)
pd.concat([df1, df2])

# Merge DataFrames
merged = pd.merge(df1, df2, how='inner', on='Q')
print(merged)
