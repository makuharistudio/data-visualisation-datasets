## International Marketplace
**[My Power BI visualisation](https://community.powerbi.com/t5/Data-Stories-Gallery/International-Marketplace-profit-report-using-Python-and-Deneb/m-p/2480550#M7154)**

This code was used for the Power BI report I created above. Most of it is simply just importing the normalised version of the International marketplace data found here:

**[https://github.com/datamesse/data-visualisation-datasets/blob/main/International%20Marketplace%20sales/International%20Marketplace%20Normalised%20for%20Power%20BI.xlsx](https://github.com/datamesse/data-visualisation-datasets/blob/main/International%20Marketplace%20sales/International%20Marketplace%20Normalised%20for%20Power%20BI.xlsx)**

### Power Query code for the Python predicted monthly profit table

```
let
    Source = Sales,
    #"Grouped Rows" = Table.Group(Source, {"OrderDate"}, {{"Profit", each List.Sum([Profit]), type nullable number}}),
    #"change OrderDate to text" = Table.TransformColumnTypes(#"Grouped Rows",{{"OrderDate", type text}}),
    #"rename OrderDate (original)" = Table.RenameColumns(#"change OrderDate to text",{{"OrderDate", "OrderDate (original)"}}),
    #"Split Column by Delimiter" = Table.SplitColumn(#"rename OrderDate (original)", "OrderDate (original)", Splitter.SplitTextByDelimiter("/", QuoteStyle.None), {"Day", "Month", "Year"}),
    #"add OrderDate" = Table.AddColumn(#"Split Column by Delimiter", "OrderDate", each [Year] & "-"  & [Month] & "-" & 
(if Text.Length([Day]) = 1
then "0"
else "") & [Day], type text),
    #"remove unneeded columns" = Table.SelectColumns(#"add OrderDate",{"OrderDate", "Profit"}),
    #"Run Python script" = Python.Execute("import pandas as pd#(lf)import numpy as np#(lf)df = pd.DataFrame(dataset, columns = ['OrderDate','Profit'])#(lf)#(lf)df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors = 'ignore')#(lf)#(lf)df.set_index('OrderDate')#(lf)df['YearMonth'] = df['OrderDate'].dt.to_period(""M"")#(lf)groupby = df.groupby(['YearMonth'])#(lf)df['MonthlyProfit'] = groupby['Profit'].transform(np.sum)#(lf)df = df.drop(columns=['OrderDate','Profit'])#(lf)df.drop_duplicates(keep='first', inplace = True)#(lf)df.set_index('YearMonth')#(lf)df.index.freq = 'MS'#(lf)from statsmodels.tsa.holtwinters import ExponentialSmoothing#(lf)model = ExponentialSmoothing(df['MonthlyProfit'],trend='mul',seasonal='mul',seasonal_periods=12).fit()#(lf)range = pd.date_range('01-01-2024', periods=12, freq='MS')#(lf)predictions = model.forecast(12)#(lf)predictions_range = pd.DataFrame({'MonthlyProfit':predictions,'YearMonth':range})",[dataset=#"remove unneeded columns"]),
    predictions_range = #"Run Python script"{[Name="predictions_range"]}[Value],
    #"Changed Type" = Table.TransformColumnTypes(predictions_range,{{"MonthlyProfit", type number}, {"YearMonth", type date}})
in
    #"Changed Type"
```

### Power Query code for the Calendar table

```
let
    Source = Sales,
    #"Grouped Rows" = Table.Group(Source, {"OrderDate"}, {{"Profit", each List.Sum([Profit]), type nullable number}}),
    #"change OrderDate to text" = Table.TransformColumnTypes(#"Grouped Rows",{{"OrderDate", type text}}),
    #"rename OrderDate (original)" = Table.RenameColumns(#"change OrderDate to text",{{"OrderDate", "OrderDate (original)"}}),
    #"Split Column by Delimiter" = Table.SplitColumn(#"rename OrderDate (original)", "OrderDate (original)", Splitter.SplitTextByDelimiter("/", QuoteStyle.None), {"Day", "Month", "Year"}),
    #"add OrderDate" = Table.AddColumn(#"Split Column by Delimiter", "OrderDate", each [Year] & "-"  & [Month] & "-" & 
(if Text.Length([Day]) = 1
then "0"
else "") & [Day], type text),
    #"remove unneeded columns" = Table.SelectColumns(#"add OrderDate",{"OrderDate", "Profit"}),
    #"Run Python script" = Python.Execute("import pandas as pd#(lf)import numpy as np#(lf)df = pd.DataFrame(dataset, columns = ['OrderDate','Profit'])#(lf)#(lf)df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors = 'ignore')#(lf)#(lf)df.set_index('OrderDate')#(lf)df['YearMonth'] = df['OrderDate'].dt.to_period(""M"")#(lf)groupby = df.groupby(['YearMonth'])#(lf)df['MonthlyProfit'] = groupby['Profit'].transform(np.sum)#(lf)df = df.drop(columns=['OrderDate','Profit'])#(lf)df.drop_duplicates(keep='first', inplace = True)#(lf)df.set_index('YearMonth')#(lf)df.index.freq = 'MS'#(lf)from statsmodels.tsa.holtwinters import ExponentialSmoothing#(lf)model = ExponentialSmoothing(df['MonthlyProfit'],trend='mul',seasonal='mul',seasonal_periods=12).fit()#(lf)range = pd.date_range('01-01-2024', periods=12, freq='MS')#(lf)predictions = model.forecast(12)#(lf)predictions_range = pd.DataFrame({'MonthlyProfit':predictions,'YearMonth':range})",[dataset=#"remove unneeded columns"]),
    predictions_range = #"Run Python script"{[Name="predictions_range"]}[Value],
    #"Changed Type" = Table.TransformColumnTypes(predictions_range,{{"MonthlyProfit", type number}, {"YearMonth", type date}})
in
    #"Changed Type"
```