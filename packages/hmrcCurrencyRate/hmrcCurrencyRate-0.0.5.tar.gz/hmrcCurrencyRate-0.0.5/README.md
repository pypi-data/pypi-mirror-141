# hmrc_currency_rate module (Other Currency to GBP)
- This module convert other currencies rate to GBP from the data on HMRC
- The return result is default as pd.DataFrame
```
hmrc_to_dataframe(month, year):

dataframe

```

### How to use

Assume we would like to get the currency rate at Jan/2017
```
hmrc_to_dataframe(01, 2017):

return dataframe

```