# File Converter

This program converts CSV file into JSON file which has parent child hierarchy.
Depth of level in hierarchy is dependent on number of columns .
Input to file are : 
    inputfile name (csv file)
    delimiter( csv file delimiter)
    skip_header_rows (top n rows which are not be considered for JSON file)
    skip_columns_rows(skips columns from left in file which are not to be considered for JSON file)
    output file name (Name of Json file which needs to be created)
Output file : JSON file will created with output file name

# Prerequisites
The project requires Python 3.6 or above to run.
Apart from the  modules which need to be imported for the project to run is mentioned in requirements.txt file.
To import the prerequisites use below command from Linux machine

```bash
pip3 install -r requirements.txt
```

# Technology choices

Used pycharm community edition as the Integrated development environment

For unit-testing ,pytest have been used
Pytest - Unit testing
1. Simple to use 
2. Easy to write small test cases and focus more on unit testing
3. Fixtures are useful and simple to use.

# Unit Testing
Please ensure that you are on the location where file_converter.py , test_file_converter.py files and sample_recs2.csv are placed.
Simply type pytest
```
pytest
```

# Instructions to run the program

To run the project please use following command from Linus machine directory where files are placed

```python
python3 file_converter.py data.csv , 1 1 data.json
```
Above is an example to execute the code from command line.
In above example:
data.csv is the first input (csv filename)
, (comma) is the second input (delimiter)
1 is number of rows to be skipped. Like in data.csv file , header should be skipped
1 is number of columns to be skipped. Like in data.csv file , first column (base_url) is not required for construction of json file.Hence 1 needs to be passed
data.json is name of file to be created for json.
After script runs successfully, data.json file will be created in the same directory.
