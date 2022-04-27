## International Marketplace
**[My Power BI visualisation](https://community.powerbi.com/t5/Data-Stories-Gallery/International-Marketplace-profit-report-using-Python-and-Deneb/m-p/2480550#M7154)**

This code was used for the Power BI report I created above.

The dataset I used was the normalised version of the International Marketplace dataset, found here:

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

This is the code used for the custom Deneb visuals

### Vega-Lite code for the Deneb visual of the combined circle and bar chart

```
{
  "data": {"name": "dataset"},
  "bounds": "flush",
  "spacing": 6,
  "params": [{"name": "pts",
              "select": "interval"
            }],
  "hconcat": [
     {"mark": { "type": "circle",
                "size": 50,
                "tooltip": true
     },
      "width": 150,
      "height": 530,
      "encoding": {
                   "y": {"field": "Subcategory",
                         "type": "nominal",
                         "title": null,
                         "axis": {"labelFontSize": 9, "grid": true, "tickBand": "extent", "gridColor": "#f6f6f6", "gridWidth": 1},
                         "sort": {"op": "sum", "field": "Total quantity", "order": "descending"}
                        },
                   "x": {"timeUnit": "month",
                         "field": "OrderDate",
                         "title": null,
                         "axis": { "labelAlign": "center",
                                   "labelExpr": "datum.label[0]" }
                        },
                   "color": {
                             "aggregate": "sum",
                             "field": "Total quantity",
                             "scale":  {
                               "domainMin": 0, "domainMax": 100000,
                               "range": ["#cbf2f2", "#82e0e0", "#90dfdf", "#32c9c9", "#19abab", "#048e8e"] }
                            },
                   "tooltip": [{"timeUnit": "year", "field": "OrderDate", "title": "YEAR"},
                               {"timeUnit": "month", "field": "OrderDate", "title": "MONTH"},
                               {"field": "Category", "type": "nominal", "title": "CATEGORY"},
                               {"field": "Subcategory", "type": "nominal", "title": "SUBCATEGORY"},
                               {"aggregate": "sum", "field": "Total quantity", "title": "QUANTITY"}]
                  }
     },
     {"mark": { "type": "bar", "tooltip": true},
      "width": 100,
      "height": 530,
      "encoding": {
                   "y": {"field": "Subcategory",
                         "type": "nominal",
                         "title": null,
                         "sort": {"op": "sum", "field": "Total quantity", "order": "descending"},
                         "axis": {"labelFontSize": 9, "labels": false, "grid": true, "gridColor": "#f6f6f6", "gridWidth": 1}
                        },
                   "x": {"field": "Total quantity",
                         "type": "quantitative",
                         "aggregate": "sum",
                         "title": null,
                         "axis": {"labels": false,
                                  "gridColor": "white"
                         }
                        },
                   "color": {"aggregate": "sum",
                             "field": "Total quantity",
                             "scale":  {"range": ["#cbf2f2", "#82e0e0", "#90dfdf", "#32c9c9", "#19abab", "#048e8e"] }
                            },
                   "tooltip": [{"timeUnit": "year", "field": "OrderDate", "title": "YEAR"},
                               {"field": "Category", "type": "nominal", "title": "CATEGORY"},
                               {"field": "Subcategory", "type": "nominal", "title": "SUBCATEGORY"},
                               {"aggregate": "sum", "field": "Total quantity", "title": "QUANTITY"}]
                   }
     },
     {"mark": {"type": "text", "align": "left", "x": 0, "fontSize": 9},
      "width": 50,
      "height": 530,
      "encoding": {"text": {"aggregate": "sum",
                            "field": "Total quantity"
                           },
                   "y": {"field": "Subcategory",
                         "type": "nominal",
                         "title": null,
                         "sort": {"op": "sum", "field": "Total quantity", "order": "descending"},
                         "axis": {"labels": false, "labelFontSize": 9}
                        }
                  }
     }
  ],
  "config": {"legend": {"disable": true} }
}
```

### Vega-Lite code for the Deneb visual of the zoomable scatterplot

```
{
  "data": {"name": "dataset"},
  "layer": [
    {
      "params": [{
        "name": "grid",
        "select": "interval",
        "bind": "scales"}],
      "transform": [
        {
          "aggregate": [
            {"op": "sum", "field": "Total profit", "as": "sum_profit"},
            {"op": "sum", "field": "Total sales", "as": "sum_sales"} ],
            "groupby": ["CustomerID"]
        },
        {
          "calculate": "datum.sum_profit", "as": "Profit"
        },
        {
          "calculate": "datum.sum_sales", "as": "Sales"
        },
        {
          "calculate": "datum.sum_profit/datum.sum_sales * 100", "as": "Profit margin"
        },
        {
          "calculate": "(datum.sum_profit/datum.sum_sales) * (datum.sum_profit/datum.sum_sales)", "as": "Point size"
        }],
      "mark": {
        "type": "point", 
        "shape": "M-3.671-1.9184L-.5855-3.875l3.0856 1.9566v2.837L-.5855 2.875-3.671.9186z",
        "tooltip": true,
        "color":"#33cbcb",
        "filled": false},
      "encoding": {
        "x": {
          "field": "Profit margin",
          "type": "quantitative",
          "scale": {
            "domain": [-25, 25],
            "domainMax": 100,
            "domainMin": -150},
          "axis": {"format": ".0f", "titleFontSize": 11},
          "title": "PROFIT MARGIN  (%)"},
        "y": {
          "field": "Profit",
          "type": "quantitative",
          "axis": {
            "titleFontSize": 11,
            "titleAngle": 360,
            "titlePadding": 30},
          "title": "PROFIT  ($)",
          "scale": {
            "domain": [-100, 100],
            "domainMax": 12000,
            "domainMin": -850 }},
        "color": {
          "condition": {
            "test": "datum['Profit'] < 0 || datum['Profit margin'] < 0",
            "value": "#ff0000"}},
        "size": {
          "field": "Point size",
          "type": "quantitative"},
        "tooltip": [
          {"field": "CustomerID", "type": "nominal", "title": "CUSTOMER ID"},
          {"field": "Profit", "title": "PROFIT ($)"},
          {"field": "Sales", "title": "SALES ($)"},
          {"field": "Profit margin", "format": ".1f", "title": "PROFIT MARGIN (%)"}]}
    },
    {
      "transform": [
        {
          "aggregate": [
            {"op": "sum", "field": "Total profit", "as": "sum_profit"},
            {"op": "sum", "field": "Total sales", "as": "sum_sales"} ],
          "groupby": ["CustomerID"]
        },
        {
          "calculate": "datum.sum_profit", "as": "Profit"
        },
        {
          "calculate": "datum.sum_sales", "as": "Sales"
        },
        {
          "calculate": "datum.sum_profit/datum.sum_sales * 100", "as": "Profit margin"
        }],
      "mark": {
        "type": "rule",
        "strokeDash": [7, 6]},
      "encoding": {
        "x": {
          "aggregate": "median",
          "field": "Profit margin",
          "type": "quantitative"},
        "color": {"value": "#b3b3b3"},
        "size": {"value": 2}
      }
    },
    {
      "transform": [
        {
          "aggregate": [
            {"op": "sum", "field": "Total profit", "as": "sum_profit"}],
          "groupby": ["CustomerID"]
        },
        {
          "calculate": "datum.sum_profit", "as": "Profit"
        }],
      "mark": {
        "type": "rule",
        "strokeDash": [7, 6]},
      "encoding": {
        "y": {
          "aggregate": "median",
          "field": "Profit",
          "type": "quantitative"},
        "color": {"value": "#b3b3b3"},
        "size": {"value": 2}
      }
    }
  ],
  "config": {"legend": {"disable": true} }
}
```

### Vega-Lite code for the Deneb visual of the country-level boxplot

```
{
  "data": {"name": "dataset"},
  "layer": [
    {
      "transform": [
        {
          "aggregate": [
            {"op": "median", "field": "Delivery", "as": "median_delivery"}],
          "groupby": ["OrderID", "Country"]}],
      "mark": {
        "type": "boxplot",
        "extent": 1.5,
        "ticks": false,
        "size": 8},
      "encoding": {
        "x": {
          "field": "median_delivery",
          "type": "quantitative",
          "scale": {"zero": false},
          "axis": {"titleFontSize": 9},
          "title": null },
        "color": {"value": "#33cbcb", "legend": null},
        "y": {
          "field": "Country",
          "type": "nominal",
          "axis":{
            "titleFontSize":9,
            "titleAngle": 360,
            "titlePadding": 30,
            "labelFontSize": 9},
          "title": null}}},
    {
      "transform": [
        {
          "aggregate": [
              {"op": "median", "field": "Delivery", "as": "median_delivery"}],
          "groupby": ["OrderID"]
        }],
        "mark": {
            "type": "rule",
            "strokeDash": [1, 0]},
          "encoding": {
            "x": {
              "aggregate": "median",
              "field": "median_delivery",
              "type": "quantitative"},
            "color": {"value": "#b3b3b3"},
            "size": {"value": 2}
          }
    }]
}
```