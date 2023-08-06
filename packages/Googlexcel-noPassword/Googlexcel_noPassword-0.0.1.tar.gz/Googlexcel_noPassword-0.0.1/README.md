<h1>Googlexcel_noPassword</h1>
_____________________________________________

First package (probably) built to easily obtain the data within an entire shared Google Spreadsheet without passing Google username/ password or credentials.json.

_____________________________________________

<h2>Instructions.</h2>  

To install the package, perform:  

```python
pip install Googlexcel_noPassword
```
 
How to use the methods:  

1. To obtain the list of sheetnames:  

```python
#url_GoogleSheets = The shared url of Google Spreadsheet document. (Ensure that the privilege is set to 'Anyone with the link'.)
list_ofSheetnames = fetch_sheetnameslist(url_GoogleSheets)
```

2. To obtain the dictionary with 'Key' = Sheetname and 'Value' = DataFrame:  

```python
#Returns a dictionary with all the sheetnames and their respective data as dataframe.
dict_Dataframes = dataframe_AllSheets(url_GoogleSheets)
```

_____________________________________________

<h2>Have fun with what is possibly the first library to bypass the credentials.json and the username/ password restrictions to fetch the entire Google Spreadsheet excel document.</h2>