# Singapore rental prices


**Goal:** Help make Singapore rental price information more accessible to the global community by applying exchange rate calculations for major global currencies.

**Approach:** Identify the lowest common date denominator between the native Singaporean rental price data and the exchange rate information available in OFX.com, then calculate based on that denominator, then build a report that highlights the pricing trend in a report viewer's selected country.


## RESULT
**[My Power BI visualisation](https://community.powerbi.com/t5/Data-Stories-Gallery/Quarterly-Singapore-median-rental-prices-by-currency/m-p/2125424)**

![My Power BI visualisation](https://github.com/datamesse/datamesse.github.io/blob/main/src/assets-portfolio/img-2021-10-power-bi-quarterly-singapore-rental-prices-by-currency.gif?raw=true)

* [Wrangled data sources](https://github.com/datamesse/data-visualisation-datasets/raw/main/Singapore%20rental%20prices/Singapore%20rental%20prices.xlsx)

### Original Data Sources
* [Singapore rental prices from data.gov.sg](https://data.gov.sg/dataset/median-rent-by-town-and-flat-type)
* [Historical exchange rates from ofx.com](https://www.ofx.com/en-us/forex-news/historical-exchange-rates/ )


## POWER BI REPORT CODE

### Power Query for Median Rent By Town & Flat Type data
What makes this code interesting is the original data source has a "pre-pivoted" structure where there are columns for each exchange rate, the rent is calculated for each currency, then unpivoted using Table.UnpivotOtherColumns().

```
let
    Source = Excel.Workbook(File.Contents("C:\Singapore rental prices.xlsx"), null, true),
    tbl_RentbyTownFlatType_Table = Source{[Item="tbl_RentbyTownFlatType",Kind="Table"]}[Data],
    #"change type: all to text" = Table.TransformColumnTypes(tbl_RentbyTownFlatType_Table,{{"quarter", type text}, {"town", type text}, {"flat_type", type text}, {"median_rent", type text}}),
    #"rename columns" = Table.RenameColumns(#"change type: all to text",{{"quarter", "Year-Quarter"}, {"town", "Town "}, {"flat_type", "Flat Type "}, {"median_rent", "Median Rent "}}),
    #"add column: Year" = Table.AddColumn(#"rename columns", "Year", each Number.FromText(Text.Start([#"Year-Quarter"],4))),
    #"add column: Quarter" = Table.AddColumn(#"add column: Year", "Quarter", each Number.From(Text.End([#"Year-Quarter"],1))),
    #"add column: Town" = Table.AddColumn(#"add column: Quarter", "Town", each Text.Proper([#"Town "])),
    #"add column: Flat Type" = Table.AddColumn(#"add column: Town", "Flat Type", each if [#"Flat Type "] = "1-RM" then "1 room" else if [#"Flat Type "] = "2-RM" then "2 rooms" else if [#"Flat Type "] = "3-RM" then "3 rooms" else if [#"Flat Type "] = "4-RM" then "4 rooms" else if [#"Flat Type "] = "5-RM" then "5 rooms" else if [#"Flat Type "] = "EXEC" then "Executive" else "Unknown"),
    #"add column: Singapore Rent (SGD)" = Table.AddColumn(#"add column: Flat Type", "SGD ", each if [#"Median Rent "] = "-" then null else if [#"Median Rent "] = "na" then null else Number.FromText([#"Median Rent "])),
    #"remove other columns" = Table.SelectColumns(#"add column: Singapore Rent (SGD)",{"Year-Quarter", "Year", "Quarter", "Town", "Flat Type", "SGD "}),
    #"merge: City" = Table.NestedJoin(#"remove other columns", {"Town"}, #"Areas of Central District", {"Town"}, "Areas of Central District", JoinKind.LeftOuter),
    #"expand: City" = Table.ExpandTableColumn(#"merge: City", "Areas of Central District", {"City"}, {"City"}),
    #"add column: SGD" = Table.AddColumn(#"expand: City", "SGD", each if [Town] = "Central" then [#"SGD "] / 12 else [#"SGD "]),
    #"add column: Country" = Table.AddColumn(#"add column: SGD", "Country", each "Singapore"),
    #"add column: YearQuarter" = Table.AddColumn(#"add column: Country", "YearQuarter", each Number.FromText(Text.Combine({Text.From([Year]),Text.From([Quarter])},""))),
    #"remove column: Town SGD" = Table.SelectColumns(#"add column: YearQuarter",{"Year-Quarter", "Year", "Quarter", "Town", "Flat Type", "City", "SGD", "Country", "YearQuarter"}),
    #"reorder columns" = Table.ReorderColumns(#"remove column: Town SGD",{"Year-Quarter", "Year", "Quarter", "YearQuarter", "Country", "Town", "City", "Flat Type", "SGD"}),
    #"merge: Exchange" = Table.NestedJoin(#"reorder columns", {"Year-Quarter"}, #"Foreign Exchange Rate", {"Year-Quarter"}, "Foreign Exchange Rate", JoinKind.LeftOuter),
    #"expand merged queries" = Table.ExpandTableColumn(#"merge: Exchange", "Foreign Exchange Rate", {"FX AUD", "FX CNY", "FX EUR", "FX GBP", "FX HKD", "FX INR", "FX JPY", "FX KRW", "FX MYR", "FX USD"}, {"FX AUD", "FX CNY", "FX EUR", "FX GBP", "FX HKD", "FX INR", "FX JPY", "FX KRW", "FX MYR", "FX USD"}),
    #"add column: AUD" = Table.AddColumn(#"expand merged queries", "AUD", each [SGD] * [FX AUD]),
    #"add column: CNY" = Table.AddColumn(#"add column: AUD", "CNY", each [SGD] * [FX CNY]),
    #"add column: EUR" = Table.AddColumn(#"add column: CNY", "EUR", each [SGD] * [FX EUR]),
    #"add column: GBP" = Table.AddColumn(#"add column: EUR", "GBP", each [SGD] * [FX GBP]),
    #"add column: HKD" = Table.AddColumn(#"add column: GBP", "HKD", each [SGD] * [FX HKD]),
    #"add column: INR" = Table.AddColumn(#"add column: HKD", "INR", each [SGD] * [FX INR]),
    #"add column: JPY" = Table.AddColumn(#"add column: INR", "JPY", each [SGD] * [FX JPY]),
    #"add column: KRW" = Table.AddColumn(#"add column: JPY", "KRW", each [SGD] * [FX KRW]),
    #"add column: MYR" = Table.AddColumn(#"add column: KRW", "MYR", each [SGD] * [FX MYR]),
    #"add column: USD" = Table.AddColumn(#"add column: MYR", "USD", each [SGD] * [FX USD]),
    #"remove columns: FX columns" = Table.SelectColumns(#"add column: USD",{"Year-Quarter", "YearQuarter", "Year", "Quarter", "Country", "Town", "City", "Flat Type", "SGD", "AUD", "CNY", "EUR", "GBP", "HKD", "INR", "JPY", "KRW", "MYR", "USD"}),
    #"replace nulls" = Table.TransformColumns(#"remove columns: FX columns",{},(x) => Replacer.ReplaceValue(x,null,0)),
    #"unpivot columns" = Table.UnpivotOtherColumns(#"replace nulls", {"Year-Quarter", "YearQuarter", "Year", "Quarter", "Country", "Town", "City", "Flat Type"}, "Attribute", "Value"),
    #"replace zeroes" = Table.TransformColumns(#"unpivot columns",{},(x) => Replacer.ReplaceValue(x,0,null)),
    #"rename columns: Currency & Median Rent" = Table.RenameColumns( #"replace zeroes",{{"Attribute", "Currency"}, {"Value", "Median Rent"}}),
    #"filter: Town remove Lim Chu Kang" = Table.SelectRows(#"rename columns: Currency & Median Rent", each ([Town] <> "Lim Chu Kang"))
in
    #"filter: Town remove Lim Chu Kang"
```

### Power Query for Foreign Exchange Rate data
```
let
    Source = Excel.Workbook(File.Contents("C:\Singapore rental prices.xlsx"), null, true),
    tbl_OFX_Table = Source{[Item="tbl_OFX",Kind="Table"]}[Data],
    #"change type: text and numbers" = Table.TransformColumnTypes(tbl_OFX_Table,{{"Year", Int64.Type}, {"Quarter", Int64.Type}, {"AUD", type number}, {"CNY", type number}, {"EUR", type number}, {"GBP", type number}, {"HKD", type number}, {"INR", type number}, {"JPY", type number}, {"KRW", type number}, {"MYR", type number}, {"SGD", type number}, {"USD", type number}}),
    #"add column: Year-Quarter" = Table.AddColumn(#"change type: text and numbers", "Year-Quarter", each Text.Combine({Text.From([Year]),Text.From([Quarter])},"-Q"), type text),
    #"remove column: SGD" = Table.SelectColumns(#"add column: Year-Quarter",{"Year", "Quarter", "AUD", "CNY", "EUR", "GBP", "HKD", "INR", "JPY", "KRW", "MYR", "USD", "Year-Quarter"}),
    #"reorder column: Year-Quarter start" = Table.ReorderColumns(#"remove column: SGD",{"Year-Quarter", "Year", "Quarter", "AUD", "CNY", "EUR", "GBP", "HKD", "INR", "JPY", "KRW", "MYR", "USD"}),
    #"rename columns" = Table.RenameColumns(#"reorder column: Year-Quarter start",{{"AUD", "FX AUD"}, {"CNY", "FX CNY"}, {"EUR", "FX EUR"}, {"GBP", "FX GBP"}, {"HKD", "FX HKD"}, {"INR", "FX INR"}, {"JPY", "FX JPY"}, {"KRW", "FX KRW"}, {"MYR", "FX MYR"}, {"USD", "FX USD"}})
in
    #"rename columns"
```

### DAX measure that sets value to null (instead of 0) based on other column values
This was needed because the Filled Map visual could not apply an ongoing filter to Line Charts the same way a Slicer does. Also, other DAX functions like ISFILTERED do not capture granularity of selection. The granularity is needed to handle the Central town, which is the only one which has subset cities.

So I kept multiple null-valued rows by replacing them before and after a Power Query unpivot. Thus 1 map selection meets the if condition for chart values to appear.

```
Rent = 
IF( AND(DISTINCTCOUNT('Median Rent By Town & Flat Type'[Town])=1,
        DISTINCTCOUNT('Median Rent By Town & Flat Type'[City])=1
    ),
    SUMX(
        VALUES('Median Rent By Town & Flat Type'),
        CALCULATE(
            'Median Rent By Town & Flat Type'[Rent SUMX],
            FILTER(
                    ALLEXCEPT('Median Rent By Town & Flat Type',
                    'Median Rent By Town & Flat Type'[Country],
                    'Median Rent By Town & Flat Type'[Town],   
                    'Median Rent By Town & Flat Type'[Year-Quarter],
                    'Median Rent By Town & Flat Type'[Flat Type],
                    'Median Rent By Town & Flat Type'[Currency]),
                    'Median Rent By Town & Flat Type'[Town] = MAX('Median Rent By Town & Flat Type'[Town])
            )
        )
    ),
    BLANK()
)
```

### DAX measure that displays the town selected
If no town is specifically selected, then a message is displayed to "Select a town from map".
```
Town. = 
IF( AND(DISTINCTCOUNT('Median Rent By Town & Flat Type'[Town])=1,
        DISTINCTCOUNT('Median Rent By Town & Flat Type'[City])=1),
    UPPER(MIN('Median Rent By Town & Flat Type'[Town])),
    "Select a town from map"
)
```