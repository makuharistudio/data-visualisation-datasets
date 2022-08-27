# Satellite launch overview


**Goal:** Having read several online articles with varied numbers of satellites in orbit, I want to see how many were launched historically versus the number that are functional and actively monitored.

**Approach:** Merge the UCSUSA dataset for actively monitored satellites (which has been referenced in several articles and Tableau Public dashboards), with data webscraped from n2yo.com for all historical launches of satellites, the build a Power BI report that compares those numbers and overall launch trend.


## RESULT
**[My Power BI visualisation](https://community.powerbi.com/t5/Data-Stories-Gallery/Satellite-launch-overview/m-p/2730077)**

![My Power BI visualisation](https://github.com/datamesse/datamesse.github.io/blob/main/src/assets-portfolio/img-2022-08-satellite-launch-overview.gif?raw=true)

### Original Data Sources
* [Actively monitored satellites from ucsusa.org](https://www.ucsusa.org/resources/satellite-database)
* [Historical satellites n2yo.com webscraped dataset by Robin S. from kaggle.com](https://www.kaggle.com/datasets/heyrobin/satellite-data-19572022)

**Note:** Data wrangling and cleaning takes place within the Power Query code below without reference to an external re-mapping data source, but summary Excel files for the remaps performed on each data source is available here:
* [Remapping n2yo.com to match UCSUSA](https://github.com/datamesse/data-visualisation-datasets/blob/main/Satellite%20launch%20overview/Excel%20files%20for%20value%20remapping/Remapping%20n2yo.com%20to%20match%20ucsusa%20dataset.xlsx)
* [Remapping UCSUSA to match n2yo.com](https://github.com/datamesse/data-visualisation-datasets/blob/main/Satellite%20launch%20overview/Excel%20files%20for%20value%20remapping/Remapping%20ucsusa%20to%20match%20n2yo.com%20dataset.xlsx)


## POWER BI REPORT CODE

### Power Query to clean n2yo.com historic satellite data

* [Satellite Data (1957-2022) by Robin S. (scraped from n2yo.com) via Kaggle](https://www.kaggle.com/datasets/heyrobin/satellite-data-19572022)

```
let
    Source = Csv.Document(File.Contents("C:\satellites-n2yo.csv"),[Delimiter=",", Columns=9, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"promote headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"change type 1" = Table.TransformColumnTypes(#"promote headers",{{"", Int64.Type}, {"norad_id", Int64.Type}, {"cospar_id", type text}, {"name", type text}, {"launch_date", type date}, {"flight_ended", type date}, {"status", type text}, {"destination", type text}, {"owner", type text}}),
    #"remove unneeded column" = Table.SelectColumns(#"change type 1",{"norad_id", "cospar_id", "name", "launch_date", "flight_ended", "status", "owner"}),
    #"rename columns" = Table.RenameColumns(#"remove unneeded column",{{"cospar_id", "International designator (COSPAR)"}, {"name", "Name"}, {"launch_date", "Launch date"}, {"flight_ended", "Flight end date"}, {"norad_id", "Satellite catalog number (NORAD)"}, {"status", "Status"}, {"owner", "Owner"}}),
    #"trim International designator" = Table.TransformColumns(#"rename columns",{{"International designator (COSPAR)", Text.Trim, type text}}),
    #"AllReplace" = [#"Arab Satellite Communications Organization" = "Intergovernmental: ARABSAT",
                     #"Asia Broadcast Satellite" = "Intergovernmental: ABS",
                     #"Asia Satellite Telecommunications Company (ASIASAT)" = "Intergovernmental: AsiaSat",
                     #"China/Brazil" = "Intergovernmental: CNSA & INPE",
                     #"Commonwealth of Independent States (former USSR)" = "Russia",
                     #"Czech Republic (former Czechoslovakia)" = "Czech Republic",
                     #"Democratic People's Republic of Korea" = "North Korea",
                     #"European Organization for the Exploitation of Meteorological Satellites (EUMETSAT)" = "Intergovernmental: EUMETSAT",
                     #"European Space Agency" = "Intergovernmental: ESA",
                     #"European Space Research Organization" = "Intergovernmental: ESRO",
                     #"European Telecommunications Satellite Organization (EUTELSAT)" = "Intergovernmental: EUTELSAT",
                     #"France/Germany" = "Multinational: Symphonie",
                     #"France/Italy" = "Intergovernmental: CNES & ASI",
                     #"Globalstar" = "United States",
                     #"International Mobile Satellite Organization (INMARSAT)" = "United Kingdom",
                     #"International Space Station" = "Intergovernmental: ISS",
                     #"International Telecommunications Satellite Organization (INTELSAT)" = "Multinational: Intelsat",
                     #"New ICO" = "United States",
                     #"North Atlantic Treaty Organization" = "Intergovernmental: NATO",
                     #"O3b Networks" = "United States",
                     #"ORBCOMM" = "United States",
                     #"People's Republic of China" = "China",
                     #"Philippines (Republic of the Philippines)" = "Philippines",
                     #"RascomStar-QAF" = "Multinational: Thales Alenia Space",
                     #"Republic of Korea" = "South Korea",
                     #"Sea Launch" = "Multinational: Sea Launch",
                     #"SES" = "Luxembourg",
                     #"Singapore/Taiwan" = "Multinational: Singtel & Chunghwa Telecom",
                     #"Taiwan (Republic of China)" = "Taiwan",
                     #"United States/Brazil" = "Brazil"],
    #"replace various Owners" = Table.TransformColumns(#"trim International designator",{{"Owner", each Record.FieldOrDefault(AllReplace,_,_)}}),
    #"change type 2" = Table.TransformColumnTypes(#"replace various Owners",{{"Owner", type text}})
in
    #"change type 2"
```

### Power Query to clean UCSUSA actively monitored satellite data

* [Union of Concerned Scientists' (UCSUSA) satellite database](https://www.ucsusa.org/resources/satellite-database)

```
let
    Source = Csv.Document(File.Contents("C:\satellites-ucsusa.txt"),[Delimiter="	", Columns=67, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"promote headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"change type 1" = Table.TransformColumnTypes(#"promote headers",{{"Name of Satellite, Alternate Names", type text}, {"Current Official Name of Satellite", type text}, {"Country/Org of UN Registry", type text}, {"Country of Operator/Owner", type text}, {"Operator/Owner", type text}, {"Users", type text}, {"Purpose", type text}, {"Detailed Purpose", type text}, {"Class of Orbit", type text}, {"Type of Orbit", type text}, {"Longitude of GEO (degrees)", type number}, {"Perigee (km)", Int64.Type}, {"Apogee (km)", Int64.Type}, {"Eccentricity", type number}, {"Inclination (degrees)", type number}, {"Period (minutes)", type number}, {"Launch Mass (kg.)", Int64.Type}, {" Dry Mass (kg.) ", Int64.Type}, {"Power (watts)", type text}, {"Date of Launch", type text}, {"Expected Lifetime (yrs.)", type number}, {"Contractor", type text}, {"Country of Contractor", type text}, {"Launch Site", type text}, {"Launch Vehicle", type text}, {"COSPAR Number", type text}, {"NORAD Number", Int64.Type}, {"Comments", type text}, {"", type text}, {"Source Used for Orbital Data", type text}, {"Source", type text}, {"Source_1", type text}, {"Source_2", type text}, {"Source_3", type text}, {"Source_4", type text}, {"Source_5", type text}, {"Source_6", type text}, {"_7", type text}, {"_8", type text}, {"_9", type text}, {"_10", type text}, {"_11", type text}, {"_12", type text}, {"_13", type text}, {"_14", type text}, {"_15", type text}, {"_16", type text}, {"_17", type text}, {"_18", type text}, {"_19", type text}, {"_20", type text}, {"_21", type text}, {"_22", type text}, {"_23", type text}, {"_24", type text}, {"_25", type text}, {"_26", type text}, {"_27", type text}, {"_28", type text}, {"_29", type text}, {"_30", type text}, {"_31", type text}, {"_32", type text}, {"_33", type text}, {"_34", type text}, {"_35", type text}, {"_36", type text}}),
    #"replace errors" = Table.ReplaceErrorValues(#"change type 1", {{" Dry Mass (kg.) ", 1900}}),
    #"remove redundant columns 1" = Table.RemoveColumns(#"replace errors",{"Source_5", "Source_6", "_7", "_8", "_9", "_10", "_11", "_12", "_13", "_14", "_15", "_16", "_17", "_18", "_19", "_20", "_21", "_22", "_23", "_24", "_25", "_26", "_27", "_28", "_29", "_30", "_31", "_32", "_33", "_34", "_35", "_36"}),
    #"add Reference column" = Table.AddColumn(#"remove redundant columns 1", "Reference", each if [Source] <> ""
        then [Source]
        else if [Source_1] <> ""
        then [Source_1]
        else if [Source_2] <> ""
        then [Source_2]
        else if [Source_3] <> ""
        then [Source_3]
        else if [Source_4] <> ""
        then [Source_4]
else null, type text),
    #"add Launch date column" = Table.AddColumn(#"add Reference column", "Launch date", each Date.From([Date of Launch],"en-US"), type date),
    #"add Distance (km) column" = Table.AddColumn(#"add Launch date column", "Distance (km)", each Number.RoundUp(Value.Divide(([#"Perigee (km)"] + [#"Apogee (km)"]), 2)), Int64.Type),
    #"remove redundant columns 2" = Table.SelectColumns(#"add Distance (km) column",{"NORAD Number", "COSPAR Number", "Name of Satellite, Alternate Names", "Launch Site", "Launch Vehicle", "Perigee (km)", "Apogee (km)", "Distance (km)", "Class of Orbit", "Purpose", "Users", "Country of Contractor", "Reference"}),
    #"trim COSPAR Number" = Table.TransformColumns(#"remove redundant columns 2",{{"COSPAR Number", Text.Trim, type text}}),
    #"add n2yo remapped NORAD column" = Table.AddColumn(#"trim COSPAR Number", "n2yo remapped NORAD", each if ([NORAD Number] =  22491 and [COSPAR Number] = "1993-009B") then 22490
        else if ([NORAD Number] =  28541 and [COSPAR Number] = "2005-004B") then 28538
        else if ([NORAD Number] =  28908 and [COSPAR Number] = "2005-048B") then 28909
        else if ([NORAD Number] =  28945 and [COSPAR Number] = "2006-007B") then 28946
        else if ([NORAD Number] =  28946 and [COSPAR Number] = "2006-007A") then 28945
        else if ([NORAD Number] =  31708 and [COSPAR Number] = "2007-027B") then 31702
        else if ([NORAD Number] =  37736 and [COSPAR Number] = "2021-017Q") then 47736
        else if ([NORAD Number] =  38908 and [COSPAR Number] = "2021-059AF") then 48908
        else if ([NORAD Number] =  40914 and [COSPAR Number] = "2015-049R") then null
        else if ([NORAD Number] =  43245 and [COSPAR Number] = "2018-029B") then 43246
        else if ([NORAD Number] =  43246 and [COSPAR Number] = "2018-029A") then 43245
        else if ([NORAD Number] =  44058 and [COSPAR Number] = "2019-010D") then 44060
        else if ([NORAD Number] =  44060 and [COSPAR Number] = "2019-010B") then 44058
        else if ([NORAD Number] =  44209 and [COSPAR Number] = "2019-024B") then 44208
        else if ([NORAD Number] =  44495 and [COSPAR Number] = "2018-054A") then 44495
        else if ([NORAD Number] =  44759 and [COSPAR Number] = "2019-074Y") then 44759
        else if ([NORAD Number] =  44853 and [COSPAR Number] = "2019-089G") then 44858
        else if ([NORAD Number] =  45123 and [COSPAR Number] = "2020-012R") then 45193
        else if ([NORAD Number] =  45253 and [COSPAR Number] = "2020-014D") then 45252
        else if ([NORAD Number] =  45393 and [COSPAR Number] = "2020--019AK") then 45393
        else if ([NORAD Number] =  45417 and [COSPAR Number] = "2020--019BK") then 45417
        else if ([NORAD Number] =  45598 and [COSPAR Number] = "1998-067RK") then 45597
        else if ([NORAD Number] =  45611 and [COSPAR Number] = "2020-032B") then 45612
        else if ([NORAD Number] =  46326 and [COSPAR Number] = "2020-062C") then 46327
        else if ([NORAD Number] =  46498 and [COSPAR Number] = "2020-068AN") then 46498
        else if ([NORAD Number] =  46499 and [COSPAR Number] = "2020-068AP") then 46499
        else if ([NORAD Number] =  46621 and [COSPAR Number] = "2020-061BJ") then 46612
        else if ([NORAD Number] =  46809 and [COSPAR Number] = "2020-076D") then 46810
        else if ([NORAD Number] =  46825 and [COSPAR Number] = "2020-061PQ") then 46825
        else if ([NORAD Number] =  46956 and [COSPAR Number] = "2020-085D") then 46932
        else if ([NORAD Number] =  46957 and [COSPAR Number] = "2020-085E") then 46957
        else if ([NORAD Number] =  46958 and [COSPAR Number] = "2020-085F") then 46958
        else if ([NORAD Number] =  46959 and [COSPAR Number] = "2020-085G") then 46959
        else if ([NORAD Number] =  46960 and [COSPAR Number] = "2020-085H") then 46960
        else if ([NORAD Number] =  47349 and [COSPAR Number] = "2021-005") then 47349
        else if ([NORAD Number] =  47446 and [COSPAR Number] = "2021-026AK") then 47446
        else if ([NORAD Number] =  47454 and [COSPAR Number] = "2021-026AT") then 47454
        else if ([NORAD Number] =  47666 and [COSPAR Number] = "2021-021G") then 47866
        else if ([NORAD Number] =  47925 and [COSPAR Number] = "1998-067RV") then 46925
        else if ([NORAD Number] =  48261 and [COSPAR Number] = "2021-043A") then 48621
        else if ([NORAD Number] =  48275 and [COSPAR Number] = "2021-035A") then 48274
        else if ([NORAD Number] =  48868 and [COSPAR Number] = "1998-067SN") then 48868
        else if ([NORAD Number] =  48874 and [COSPAR Number] = "2021-058E") then 48874
        else if ([NORAD Number] =  48875 and [COSPAR Number] = "2021-058D") then 48875
        else if ([NORAD Number] =  48877 and [COSPAR Number] = "2021-056G") then 48877
        else if ([NORAD Number] =  48906 and [COSPAR Number] = "2021-059D") then 48906
        else if ([NORAD Number] =  48909 and [COSPAR Number] = "2021-059G") then 48909
        else if ([NORAD Number] =  48965 and [COSPAR Number] = "2021-059CR") then 48966
        else if ([NORAD Number] =  49055 and [COSPAR Number] = "2021-095A") then 49332
        else if ([NORAD Number] =  49056 and [COSPAR Number] = "2021-095B") then 49333
        else if ([NORAD Number] =  49070 and [COSPAR Number] = "2021-072E") then 49070
        else if ([NORAD Number] =  49434 and [COSPAR Number] = "2021-091K") then 49324
        else if ([NORAD Number] =  49818 and [COSPAR Number] = "2021-118A") then 49817
        else if ([NORAD Number] =  54940 and [COSPAR Number] = "2020-051B") then 45940
        else if ([NORAD Number] =  57759 and [COSPAR Number] = "2021-017AP") then 47759
        else [NORAD Number], Int64.Type),
    #"add n2yo remapped COSPAR column" = Table.AddColumn(#"add n2yo remapped NORAD column", "n2yo remapped COSPAR", each if ([NORAD Number] =  22491 and [COSPAR Number] = "1993-009B") then "1993-009B"
        else if ([NORAD Number] =  28541 and [COSPAR Number] = "2005-004B") then "2005-004B"
        else if ([NORAD Number] =  28908 and [COSPAR Number] = "2005-048B") then "2005-048B"
        else if ([NORAD Number] =  28945 and [COSPAR Number] = "2006-007B") then "2006-007B"
        else if ([NORAD Number] =  28946 and [COSPAR Number] = "2006-007A") then "2006-007A"
        else if ([NORAD Number] =  31708 and [COSPAR Number] = "2007-027B") then "2007-027B"
        else if ([NORAD Number] =  37736 and [COSPAR Number] = "2021-017Q") then "2021-017Q"
        else if ([NORAD Number] =  38908 and [COSPAR Number] = "2021-059AF") then "2021-059AF"
        else if ([NORAD Number] =  40914 and [COSPAR Number] = "2015-049R") then null
        else if ([NORAD Number] =  43245 and [COSPAR Number] = "2018-029B") then "2018-029B"
        else if ([NORAD Number] =  43246 and [COSPAR Number] = "2018-029A") then "2018-029A"
        else if ([NORAD Number] =  44058 and [COSPAR Number] = "2019-010D") then "2019-010D"
        else if ([NORAD Number] =  44060 and [COSPAR Number] = "2019-010B") then "2019-010B"
        else if ([NORAD Number] =  44209 and [COSPAR Number] = "2019-024B") then "2019-024B"
        else if ([NORAD Number] =  44495 and [COSPAR Number] = "2018-054A") then "2019-054A"
        else if ([NORAD Number] =  44759 and [COSPAR Number] = "2019-074Y") then "2019-074AY"
        else if ([NORAD Number] =  44853 and [COSPAR Number] = "2019-089G") then "2019-089G"
        else if ([NORAD Number] =  45123 and [COSPAR Number] = "2020-012R") then "2020-012R"
        else if ([NORAD Number] =  45253 and [COSPAR Number] = "2020-014D") then "2020-014D"
        else if ([NORAD Number] =  45393 and [COSPAR Number] = "2020--019AK") then "2020-019AK"
        else if ([NORAD Number] =  45417 and [COSPAR Number] = "2020--019BK") then "2020-019BK"
        else if ([NORAD Number] =  45598 and [COSPAR Number] = "1998-067RK") then "1998-067RK"
        else if ([NORAD Number] =  45611 and [COSPAR Number] = "2020-032B") then "2020-032B"
        else if ([NORAD Number] =  46326 and [COSPAR Number] = "2020-062C") then "2020-062C"
        else if ([NORAD Number] =  46498 and [COSPAR Number] = "2020-068AN") then "2020-068N"
        else if ([NORAD Number] =  46499 and [COSPAR Number] = "2020-068AP") then "2020-068P"
        else if ([NORAD Number] =  46621 and [COSPAR Number] = "2020-061BJ") then "2020-061BJ"
        else if ([NORAD Number] =  46809 and [COSPAR Number] = "2020-076D") then "2020-076D"
        else if ([NORAD Number] =  46825 and [COSPAR Number] = "2020-061PQ") then "2020-061BQ"
        else if ([NORAD Number] =  46956 and [COSPAR Number] = "2020-085D") then "2020-085D"
        else if ([NORAD Number] =  46957 and [COSPAR Number] = "2020-085E") then "2020-085AE"
        else if ([NORAD Number] =  46958 and [COSPAR Number] = "2020-085F") then "2020-085AF"
        else if ([NORAD Number] =  46959 and [COSPAR Number] = "2020-085G") then "2020-085AG"
        else if ([NORAD Number] =  46960 and [COSPAR Number] = "2020-085H") then "2020-085AH"
        else if ([NORAD Number] =  47349 and [COSPAR Number] = "2021-005") then "2021-005A"
        else if ([NORAD Number] =  47446 and [COSPAR Number] = "2021-026AK") then "2021-006AK"
        else if ([NORAD Number] =  47454 and [COSPAR Number] = "2021-026AT") then "2021-006AT"
        else if ([NORAD Number] =  47666 and [COSPAR Number] = "2021-021G") then "2021-021G"
        else if ([NORAD Number] =  47925 and [COSPAR Number] = "1998-067RV") then "1998-067RV"
        else if ([NORAD Number] =  48261 and [COSPAR Number] = "2021-043A") then "2021-043A"
        else if ([NORAD Number] =  48275 and [COSPAR Number] = "2021-035A") then "2021-035A"
        else if ([NORAD Number] =  48868 and [COSPAR Number] = "1998-067SN") then "1998-067SP"
        else if ([NORAD Number] =  48874 and [COSPAR Number] = "2021-058E") then "2021-058D"
        else if ([NORAD Number] =  48875 and [COSPAR Number] = "2021-058D") then "2021-058E"
        else if ([NORAD Number] =  48877 and [COSPAR Number] = "2021-056G") then "2021-058G"
        else if ([NORAD Number] =  48906 and [COSPAR Number] = "2021-059D") then "2021-059AD"
        else if ([NORAD Number] =  48909 and [COSPAR Number] = "2021-059G") then "2021-059AG"
        else if ([NORAD Number] =  48965 and [COSPAR Number] = "2021-059CR") then "2021-059CR"
        else if ([NORAD Number] =  49055 and [COSPAR Number] = "2021-095A") then "2021-095A"
        else if ([NORAD Number] =  49056 and [COSPAR Number] = "2021-095B") then "2021-095B"
        else if ([NORAD Number] =  49070 and [COSPAR Number] = "2021-072E") then "2021-073E"
        else if ([NORAD Number] =  49434 and [COSPAR Number] = "2021-091K") then "2021-091K"
        else if ([NORAD Number] =  49818 and [COSPAR Number] = "2021-118A") then "2021-118A"
        else if ([NORAD Number] =  54940 and [COSPAR Number] = "2020-051B") then "2020-051B"
        else if ([NORAD Number] =  57759 and [COSPAR Number] = "2021-017AP") then "2021-017AP"
        else [COSPAR Number], type text),
    #"rename columns" = Table.RenameColumns(#"add n2yo remapped COSPAR column",{{"n2yo remapped NORAD", "Satellite catalog number (NORAD)"}, {"n2yo remapped COSPAR", "International designator (COSPAR)"}, {"Name of Satellite, Alternate Names", "Alternate names"}, {"Launch Site", "Launch site"}, {"Launch Vehicle", "Launch vehicle"}, {"Class of Orbit", "Orbit class"}, {"Country of Contractor", "Contractor country"}}),
    #"remove redundant columns 3" = Table.SelectColumns(#"rename columns",{"Satellite catalog number (NORAD)", "International designator (COSPAR)", "Alternate names", "Launch site", "Launch vehicle", "Perigee (km)", "Apogee (km)", "Distance (km)", "Orbit class", "Purpose", "Users", "Contractor country", "Reference"}),
    #"AllReplace1" = [ #"ESA" = "Intergovernmental: ESA",
                       #"France/Belgium/Spain/Italy" = "Multinational: Thales Alenia Space",
                       #"France/Italy" = "Multinational: Thales Alenia Space",
                       #"France/UK/Germany/Spain/Italy" = "Multinational: Thales Alenia Space",
                       #"Japan/Singapore" = "Multinational: KIT & NTU",
                       #"South Ko" = "Russia",
                       #"Turkmenistan/Monaco" = "Turkey",
                       #"UK/Finland/Belgium" = "Belgium",
                       #"USA" = "United States"],
    #"replace various Contractor countries" = Table.TransformColumns(#"remove redundant columns 3",{{"Contractor country", each Record.FieldOrDefault(AllReplace1,_,_)}}),
    #"change type 2" = Table.TransformColumnTypes(#"replace various Contractor countries",{{"Contractor country", type text}}),
    #"AllReplace2" = [ #"Elliptical" = "Geostationary Transfer Orbit",
                       #"GEO" = "Geosynchronous Equatorial Orbit",
                       #"LEO" = "Low Earth Orbit",
                       #"MEO" = "Medium Earth Orbit"],
    #"replace Orbit classes" = Table.TransformColumns(#"change type 2",{{"Orbit class", each Record.FieldOrDefault(AllReplace2,_,_)}}),
    #"replace null Orbit class with Unknown" = Table.ReplaceValue(#"replace Orbit classes","","Unknown",Replacer.ReplaceValue,{"Orbit class"}),
    #"change type 3" = Table.TransformColumnTypes(#"replace null Orbit class with Unknown",{{"Orbit class", type text}}),
    #"AllReplace3" = [ #"Communication" = "Communications",
                       #"Communications/Maritime Tracking" = "Communications",
                       #"Communications/Navigation" = "Communications",
                       #"Communications/Technology Development" = "Communications",
                       #"Earth Observarion" = "Earth observation",
                       #"Earth Observation" = "Earth observation",
                       #"Earth Observation/Communications" = "Earth observation",
                       #"Earth Observation/Communications/Space Science" = "Earth observation",
                       #"Earth Observation/Earth Science" = "Education & demonstration",
                       #"Earth Observation/Space Science" = "Education & demonstration",
                       #"Earth Observation/Technology Development" = "Earth observation",
                       #"Earth Science" = "Earth science",
                       #"Earth Science/Earth Observation" = "Earth science",
                       #"Earth/Space Observation" = "Space surveillance",
                       #"Educational" = "Education & demonstration",
                       #"Mission Extension Technology" = "Other",
                       #"Navigation/Global Positioning" = "Navigation & positioning",
                       #"Navigation/Regional Positioning" = "Navigation & positioning",
                       #"Platform" = "Other",
                       #"Satellite Positioning" = "Navigation & positioning",
                       #"Signals Intelligence" = "Navigation & positioning",
                       #"Space Observation" = "Space surveillance",
                       #"Space Science" = "Space science",
                       #"Space Science/Technology Demonstration" = "Space science",
                       #"Space Science/Technology Development" = "Space science",
                       #"Surveillance" = "Earth surveillance",
                       #"Technology Demonstration" = "Education & demonstration",
                       #"Technology Development" = "Technology development",
                       #"Technology Development/Educational" = "Education & demonstration",
                       #"Unknown" = "Other"],
    #"replace Purposes" = Table.TransformColumns(#"change type 3",{{"Purpose", each Record.FieldOrDefault(AllReplace3,_,_)}}),
    #"replace null Purpose with Unknown" = Table.ReplaceValue(#"replace Purposes","","Unknown",Replacer.ReplaceValue,{"Purpose"}),
    #"change type 4" = Table.TransformColumnTypes(#"replace null Purpose with Unknown",{{"Purpose", type text}}),
    #"trim Users" = Table.TransformColumns(#"change type 4",{{"Users", Text.Trim, type text}}),
    #"AllReplace4" = [ #"Civil" = "Commercial and civil",
                       #"Commercial" = "Commercial and civil",
                       #"Civil/Government" = "Government / Commercial and civil",
                       #"Civil/Military" = "Military / Commercial and civil",
                       #"Commercial/Civil" = "Commercial and civil",
                       #"Commercial/Government" = "Government / Commercial and civil",
                       #"Commercial/Military" = "Military / Commercial and civil",
                       #"Earth Observation" = "Military",
                       #"Government/Civil" = "Government / Commercial and civil",
                       #"Government/Commercial" = "Government / Commercial and civil",
                       #"Government/Commercial/Military" = "Government / Commercial and civil",
                       #"Government/Military" = "Government / military",
                       #"Military" = "Military",
                       #"Military/Civil" = "Military / Commercial and civil",
                       #"Military/Commercial" = "Military / Commercial and civil",
                       #"Military/Government" = "Government / military"],
    #"replace Users" = Table.TransformColumns(#"trim Users",{{"Users", each Record.FieldOrDefault(AllReplace4,_,_)}}),
    #"replace null Users with Unknown" = Table.ReplaceValue(#"replace Users","","Unknown",Replacer.ReplaceValue,{"Users"}),
    #"change type 5" = Table.TransformColumnTypes(#"replace null Users with Unknown",{{"Users", type text}}),
    #"trim Launch site" = Table.TransformColumns(#"change type 5",{{"Launch site", Text.Trim, type text}}),
    #"AllReplace5" = [ #"Antares" = "Wallops Island Flight Facility",
                       #"Cygnus" = "Wallops Island Flight Facility",
                       #"Dragon CRS-17" = "Tyuratam Missile and Space Complex",
                       #"FANTM-RAiL (Xtenti)" = "Vandenberg Space Force Base",
                       #"FANTM-RAiL [Xtenti]" = "Vandenberg Space Force Base",
                       #"International Space Station" = "Tyuratam Missile and Space Complex",
                       #"International Space Station - Antares" = "Tyuratam Missile and Space Complex",
                       #"International Space Station - Cygnus" = "Unknown",
                       #"Orbital ATK L-1011" = "Eastern Range Air Space",
                       #"Satish Dhawan" = "Satish Dhawan Space Centre",
                       #"Stargazer L-1011" = "Eastern Range Air Space",
                       #"Vandenberg AFB" = "Vandenberg Space Force Base",
                       #"Virgin Orbit" = "Vandenberg Space Force Base",
                       #"Wenchang Space Center" = "Wenchang Space Launch Site",
                       #"Wenchang Satellite Launch Center" = "Wenchang Space Launch Site" ],
    #"replace Launch sites" = Table.TransformColumns(#"trim Launch site",{{"Launch site", each Record.FieldOrDefault(AllReplace5,_,_)}}),
    #"change type 6" = Table.TransformColumnTypes(#"replace Launch sites",{{"Launch site", type text}})
in
    #"change type 6"
```

### Power Query to merge n2yo.com historic and UCSUSA actively monitored satellite data

```
let
    Source = Table.NestedJoin(#"Satellite launches (n2yo)", {"Satellite catalog number (NORAD)", "International designator (COSPAR)"}, #"Satellites in orbit (ucsusa)", {"Satellite catalog number (NORAD)", "International designator (COSPAR)"}, "Satellites in orbit (ucsusa)", JoinKind.LeftOuter),
    #"expand ucsusa dataset" = Table.ExpandTableColumn(Source, "Satellites in orbit (ucsusa)", {"Satellite catalog number (NORAD)", "International designator (COSPAR)", "Alternate names", "Launch site", "Launch vehicle", "Perigee (km)", "Apogee (km)", "Distance (km)", "Orbit class", "Purpose", "Users", "Contractor country", "Reference"}, {"(ucsusa).Satellite catalog number (NORAD)", "(ucsusa).International designator (COSPAR)", "Alternate names", "Launch site", "Launch vehicle", "Perigee (km)", "Apogee (km)", "Distance (km)", "Orbit class", "Purpose", "Users", "Contractor country", "Reference"}),
    #"add Record type" = Table.AddColumn(#"expand ucsusa dataset", "Record type", each if [#"Satellite catalog number (NORAD)"] <> null and [#"(ucsusa).Satellite catalog number (NORAD)"] = null
then "n2yo.com historic observation"
else if [#"Satellite catalog number (NORAD)"] = null and [#"(ucsusa).Satellite catalog number (NORAD)"] <> null 
then "ucsusa unmatched"
else if [#"Satellite catalog number (NORAD)"] <> null and [#"(ucsusa).Satellite catalog number (NORAD)"] <> null 
then "UCSUSA active observation"
else "N/A", type text),
    #"add Flight life (days)" = Table.AddColumn(#"add Record type", "Flight life (days)", each if ([Launch date] <> null and [Flight end date] <> null) then Duration.Days([Flight end date] - [Launch date])
else null, Int64.Type),
    #"add Flight end date?" = Table.AddColumn(#"add Flight life (days)", "Flight end date?", each if [Flight end date] <> null
then "Satellite has end date"
else if [Flight end date] = null
then "No flight end date"
else "Check this data", type text),
    #"replace null Status with Unknown" = Table.ReplaceValue(#"add Flight end date?","","Unknown",Replacer.ReplaceValue,{"Status"}),
    #"AllReplace" = [#"Backup/Standby" = "Operational", 
                     #"Extended mission" = "Operational", 
                     #"Partially operational" = "Operational", 
                     #"Spare" = "Operational"],
    #"replace various Statuses with Operational" = Table.TransformColumns(#"replace null Status with Unknown",{{"Status", each Record.FieldOrDefault(AllReplace,_,_)}}),
    #"change type Status to text" = Table.TransformColumnTypes(#"replace various Statuses with Operational",{{"Status", type text}}),
    #"add Country column" = Table.AddColumn(#"change type Status to text", "Country", each if ([Owner] = "" and [#"Contractor country"] = null)
then "Unknown"
else if [Owner] <> ""
then [Owner]
else if ([Owner] = "" and [#"Contractor country"] <> null)
then [#"Contractor country"]
else "N/A", type text),
    #"remove redundant columns" = Table.SelectColumns(#"add Country column",{"Record type", "Satellite catalog number (NORAD)", "International designator (COSPAR)", "Name", "Alternate names", "Country", "Purpose", "Users", "Launch date", "Launch site", "Launch vehicle", "Orbit class", "Perigee (km)", "Apogee (km)", "Distance (km)", "Status", "Flight end date", "Flight life (days)", "Reference", "Flight end date?"}),
    #"replace null Users with Unknown" = Table.ReplaceValue(#"remove redundant columns",null,"Unknown",Replacer.ReplaceValue,{"Users"}),
    #"replace null Purposes with Unknown" = Table.ReplaceValue(#"replace null Users with Unknown",null,"Unknown",Replacer.ReplaceValue,{"Purpose"}),
    #"replace null Orbit classes with Unknown" = Table.ReplaceValue(#"replace null Purposes with Unknown",null,"Unknown",Replacer.ReplaceValue,{"Orbit class"}),
    #"replace null Launch sites with Unknown" = Table.ReplaceValue(#"replace null Orbit classes with Unknown",null,"Unknown",Replacer.ReplaceValue,{"Launch site"}),
    #"replace blank Launch sites with Unknown" = Table.ReplaceValue(#"replace null Launch sites with Unknown","","Unknown",Replacer.ReplaceValue,{"Launch site"}),
    #"replace null Launch vehicles with Unknown" = Table.ReplaceValue(#"replace blank Launch sites with Unknown",null,"Unknown",Replacer.ReplaceValue,{"Launch vehicle"}),
    #"add Flight life (years) column" = Table.AddColumn(#"replace null Launch vehicles with Unknown", "Flight life (years)", each if [#"Flight end date?"] = "Satellite has end date"
then Number.IntegerDivide([#"Flight life (days)"],365)
else null, Int64.Type),
    #"add Launch site latitude column" = Table.AddColumn(#"add Flight life (years) column", "Launch site latitude", each if [Launch site] = "Cape Canaveral" then 28.4926884
else if [Launch site] = "Baikonur Cosmodrome" then 45.96494307
else if [Launch site] = "Guiana Space Center" then 5.16776515
else if [Launch site] = "Vandenberg Space Force Base" then 34.74226912
else if [Launch site] = "Vostochny Cosmodrome" then 51.85023838
else if [Launch site] = "Satish Dhawan Space Centre" then 13.72612064
else if [Launch site] = "Jiuquan Satellite Launch Center" then 40.958056
else if [Launch site] = "Taiyuan Launch Center" then 38.84879055
else if [Launch site] = "Xichang Satellite Launch Center" then 28.24696212
else if [Launch site] = "Plesetsk Cosmodrome" then 62.92795254
else if [Launch site] = "Rocket Lab Launch Complex 1" then -39.26021649
else if [Launch site] = "Wallops Island Flight Facility" then 37.93403169
else if [Launch site] = "Tanegashima Space Center" then 30.3750677
else if [Launch site] = "Dombarovsky Air Base" then 51.0994718
else if [Launch site] = "Sea Launch Odyssey" then 6.34419062823554
else if [Launch site] = "Tyuratam Missile and Space Complex" then 44.1385718192634
else if [Launch site] = "Uchinoura Space Center" then 31.25199903
else if [Launch site] = "Yellow Sea Launch Platform" then 35.3327650833263
else if [Launch site] = "Wenchang Space Launch Site" then 19.61861916
else if [Launch site] = "Eastern Range Air Space" then 28.23672
else if [Launch site] = "Palmachim Launch Complex" then 31.89992763
else if [Launch site] = "Kodiak Launch Complex" then 57.4357406
else if [Launch site] = "Kwajalein Island" then 8.716667
else if [Launch site] = "Svobodny Cosmodrome" then 51.7186549
else if [Launch site] = "Naro Space Center" then 34.44194243
else if [Launch site] = "Shahroud Missile Base" then 36.2061063
else null, type number),
    #"add Launch site longitude column" = Table.AddColumn(#"add Launch site latitude column", "Launch site longitude", each if [Launch site] = "Cape Canaveral" then -80.57279338
else if [Launch site] = "Baikonur Cosmodrome" then 63.30528572
else if [Launch site] = "Guiana Space Center" then -52.68324688
else if [Launch site] = "Vandenberg Space Force Base" then -120.5724297
else if [Launch site] = "Vostochny Cosmodrome" then 128.3553151
else if [Launch site] = "Satish Dhawan Space Centre" then 80.22656523
else if [Launch site] = "Jiuquan Satellite Launch Center" then 100.291111
else if [Launch site] = "Taiyuan Launch Center" then 111.6080259
else if [Launch site] = "Xichang Satellite Launch Center" then 102.0267277
else if [Launch site] = "Plesetsk Cosmodrome" then 40.57486226
else if [Launch site] = "Rocket Lab Launch Complex 1" then 177.8662063
else if [Launch site] = "Wallops Island Flight Facility" then -75.4795783
else if [Launch site] = "Tanegashima Space Center" then 130.9576342
else if [Launch site] = "Dombarovsky Air Base" then 59.84147987
else if [Launch site] = "Sea Launch Odyssey" then -10.8012012676391
else if [Launch site] = "Tyuratam Missile and Space Complex" then 60.1237156206004
else if [Launch site] = "Uchinoura Space Center" then 131.0761933
else if [Launch site] = "Yellow Sea Launch Platform" then 123.201025386553
else if [Launch site] = "Wenchang Space Launch Site" then 110.951529
else if [Launch site] = "Eastern Range Air Space" then -80.609528
else if [Launch site] = "Palmachim Launch Complex" then 34.690556
else if [Launch site] = "Kodiak Launch Complex" then -152.3394517
else if [Launch site] = "Kwajalein Island" then 167.733333
else if [Launch site] = "Svobodny Cosmodrome" then 128.0031326
else if [Launch site] = "Naro Space Center" then 127.5341107
else if [Launch site] = "Shahroud Missile Base" then 55.33477795
else null, type number)
in
    #"add Launch site longitude column"
```

### Deneb code for the zoomable scatterplot of actively monitored satellites in orbit

See my blog post on how I created the Vega-Lite code for this visual:

* **[https://datamesse.github.io/#/post/1661522400](https://datamesse.github.io/#/post/1661522400)**

```
{"background": "null",
 "view": {"fill": "#0B0D14", 
          "fillOpacity": 0 },
 "data": {"name": "dataset"},
 "layer": [
     { "transform": [
            { "aggregate": [{"op": "max", "field": "Sin", "as": "max_sin"}] },
            { "calculate": "datum.max_sin * 0", "as": "x-axis zero" },
            { "calculate": "abs(datum.max_sin) * 0.5", "as": "y-axis top year" } ],
       "mark": {"type": "text",
                "style": "label",
                "angle": 0,
                "baseline": "top",
                "align": "center",
                "fontSize": 30 },
       "encoding": { "x": {"field": "x-axis zero",
                           "type":  "quantitative"},
                     "y": {"field": "y-axis top year",
                           "type":  "quantitative"},
                     "text": {"value": "1974"},
                     "color": {"value": "#9DA4AC"} }
     },
     { "transform": [
            { "aggregate": [{"op": "max", "field": "Sin", "as": "max_sin"}] },
            { "calculate": "datum.max_sin * 0", "as": "x-axis zero" },
            { "calculate": "abs(datum.max_sin) * -1 * 0.6", "as": "y-axis bottom year" } ],
       "mark": {"type": "text",
                "style": "label",
                "angle": 0,
                "baseline": "bottom",
                "align": "center",
                "fontSize": 30 },
       "encoding": { "x": {"field": "x-axis zero",
                           "type":  "quantitative"},
                     "y": {"field": "y-axis bottom year",
                           "type":  "quantitative"},
                     "text": {"value": "2006"},
                     "color": {"value": "#9DA4AC"} }
     },
     { "transform": [
            { "aggregate": [{"op": "max", "field": "Sin", "as": "max_sin"}] },
            { "calculate": "datum.max_sin * 0", "as": "y-axis zero" },
            { "calculate": "abs(datum.max_sin) * 0.5", "as": "x-axis right year" } ],
       "mark": {"type": "text",
                "style": "label",
                "angle": 0,
                "baseline": "middle",
                "align": "center",
                "fontSize": 30 },
       "encoding": { "y": {"field": "y-axis zero",
                           "type":  "quantitative"},
                     "x": {"field": "x-axis right year",
                           "type":  "quantitative"},
                     "text": {"value": "1990"},
                     "color": {"value": "#9DA4AC"} }
     },
     { "transform": [
            { "aggregate": [{"op": "max", "field": "Sin", "as": "max_sin"}] },
            { "calculate": "datum.max_sin * 0", "as": "y-axis zero" },
            { "calculate": "abs(datum.max_sin) * -1 * 0.5", "as": "x-axis left year" } ],
       "mark": {"type": "text",
                "style": "label",
                "angle": 0,
                "baseline": "middle",
                "align": "center",
                "fontSize": 30 },
       "encoding": { "y": {"field": "y-axis zero",
                           "type":  "quantitative"},
                     "x": {"field": "x-axis left year",
                           "type":  "quantitative"},
                     "text": {"value": "2021"},
                     "color": {"value": "#9DA4AC"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 1974"},
         { "filter": {"field": "Orbit class", "equal": "Low Earth Orbit"}},
         { "aggregate": [{"op": "min", "field": "Cos", "as": "min_sin_LEO"}] },
         { "calculate": "datum.min_sin_LEO * 0", "as": "x-axis zero" },
         { "calculate": "abs(round(datum.min_sin_LEO)) + 'km'", "as": "display LEO max 1974 kms"}, 
         { "calculate": "abs(datum.min_sin_LEO)", "as": "y-axis LEO max 1974 distance" } ],
       "mark": { "type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "left", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis LEO max 1974 distance", "type":  "quantitative"},
                     "x": {"field": "x-axis zero", "type":  "quantitative"},
                     "text": {"field": "display LEO max 1974 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 1990"},
         { "filter": {"field": "Orbit class", "equal": "Low Earth Orbit"}},
         { "aggregate": [{"op": "min", "field": "Sin", "as": "min_sin_LEO"}] },
         { "calculate": "datum.min_sin_LEO * 0", "as": "y-axis zero" },
         { "calculate": "abs(round(datum.min_sin_LEO)) + 'km'", "as": "display LEO max 1990 kms"}, 
         { "calculate": "abs(datum.min_sin_LEO)", "as": "x-axis LEO max 1990 distance" } ],
       "mark": {"type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "center", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis zero", "type":  "quantitative"},
                     "x": {"field": "x-axis LEO max 1990 distance", "type": "quantitative"},
                     "text": {"field": "display LEO max 1990 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 1990"},
         { "filter": {"field": "Orbit class", "equal": "Geosynchronous Equatorial Orbit"}},
         { "aggregate": [{"op": "min", "field": "Sin", "as": "min_sin_GEO"}] },
         { "calculate": "datum.min_sin_GEO * 0", "as": "y-axis zero" },
         { "calculate": "abs(round(datum.min_sin_GEO)) + 'km'", "as": "display GEO max 1990 kms"}, 
         { "calculate": "abs(datum.min_sin_GEO)", "as": "x-axis GEO max 1990 distance" } ],
       "mark": {"type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "center", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis zero", "type":  "quantitative"},
                     "x": {"field": "x-axis GEO max 1990 distance", "type": "quantitative"},
                     "text": {"field": "display GEO max 1990 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2006"},
         { "filter": {"field": "Orbit class", "equal": "Low Earth Orbit"}},
         { "aggregate": [{"op": "max", "field": "Cos", "as": "max_sin_LEO"}] },
         { "calculate": "datum.max_sin_LEO * 0", "as": "x-axis zero" },
         { "calculate": "abs(round(datum.max_sin_LEO)) + 'km'", "as": "display LEO min 2006 kms"}, 
         { "calculate": "abs(datum.max_sin_LEO) * -1", "as": "y-axis LEO min 2006 distance" } ],
       "mark": { "type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "left", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis LEO min 2006 distance", "type":  "quantitative"},
                     "x": {"field": "x-axis zero", "type":  "quantitative"},
                     "text": {"field": "display LEO min 2006 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2006"},
         { "filter": {"field": "Orbit class", "equal": "Low Earth Orbit"}},
         { "aggregate": [{"op": "median", "field": "Cos", "as": "med_sin_LEO"}] },
         { "calculate": "datum.med_sin_LEO * 0", "as": "x-axis zero" },
         { "calculate": "abs(round(datum.med_sin_LEO)) + 'km'", "as": "display LEO med 2006 kms"}, 
         { "calculate": "abs(datum.med_sin_LEO) * -1", "as": "y-axis LEO med 2006 distance" } ],
       "mark": { "type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "left", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis LEO med 2006 distance", "type":  "quantitative"},
                     "x": {"field": "x-axis zero", "type":  "quantitative"},
                     "text": {"field": "display LEO med 2006 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2006"},
         { "filter": {"field": "Orbit class", "equal": "Low Earth Orbit"}},
         { "aggregate": [{"op": "min", "field": "Cos", "as": "min_sin_LEO"}] },
         { "calculate": "datum.min_sin_LEO * 0", "as": "x-axis zero" },
         { "calculate": "abs(round(datum.min_sin_LEO)) + 'km'", "as": "display LEO max 2006 kms"}, 
         { "calculate": "abs(datum.min_sin_LEO) * -1", "as": "y-axis LEO max 2006 distance" } ],
       "mark": { "type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "left", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis LEO max 2006 distance", "type":  "quantitative"},
                     "x": {"field": "x-axis zero", "type":  "quantitative"},
                     "text": {"field": "display LEO max 2006 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2006"},
         { "filter": {"field": "Orbit class", "equal": "Medium Earth Orbit"}},
         { "aggregate": [{"op": "min", "field": "Cos", "as": "min_sin_MEO"}] },
         { "calculate": "datum.min_sin_MEO * 0", "as": "x-axis zero" },
         { "calculate": "abs(round(datum.min_sin_MEO)) + 'km'", "as": "display MEO max 2006 kms"}, 
         { "calculate": "abs(datum.min_sin_MEO) * -1", "as": "y-axis MEO max 2006 distance" } ],
       "mark": { "type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "left", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis MEO max 2006 distance", "type":  "quantitative"},
                     "x": {"field": "x-axis zero", "type":  "quantitative"},
                     "text": {"field": "display MEO max 2006 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2006"},
         { "filter": {"field": "Orbit class", "equal": "Geosynchronous Equatorial Orbit"}},
         { "aggregate": [{"op": "min", "field": "Cos", "as": "min_sin_GEO"}] },
         { "calculate": "datum.min_sin_GEO * 0", "as": "x-axis zero" },
         { "calculate": "abs(round(datum.min_sin_GEO)) + 'km'", "as": "display GEO max 2006 kms"}, 
         { "calculate": "abs(datum.min_sin_GEO) * -1", "as": "y-axis GEO max 2006 distance" } ],
       "mark": {"type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "left", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis GEO max 2006 distance", "type": "quantitative"},
                     "x": {"field": "x-axis zero", "type":  "quantitative"},
                     "text": {"field": "display GEO max 2006 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2021"},
         { "filter": {"field": "Orbit class", "equal": "Low Earth Orbit"}},
         { "aggregate": [{"op": "max", "field": "Sin", "as": "max_sin_LEO"}] },
         { "calculate": "datum.max_sin_LEO * 0", "as": "y-axis zero" },
         { "calculate": "abs(round(datum.max_sin_LEO)) + 'km'", "as": "display LEO min 2021 kms"}, 
         { "calculate": "abs(datum.max_sin_LEO) * -1", "as": "x-axis LEO min 2021 distance" } ],
       "mark": {"type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "center", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis zero", "type":  "quantitative"},
                     "x": {"field": "x-axis LEO min 2021 distance", "type": "quantitative"},
                     "text": {"field": "display LEO min 2021 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2021"},
         { "filter": {"field": "Orbit class", "equal": "Low Earth Orbit"}},
         { "aggregate": [{"op": "median", "field": "Sin", "as": "med_sin_LEO"}] },
         { "calculate": "datum.med_sin_LEO * 0", "as": "y-axis zero" },
         { "calculate": "abs(round(datum.med_sin_LEO)) + 'km'", "as": "display LEO med 2021 kms"}, 
         { "calculate": "abs(datum.med_sin_LEO) * -1", "as": "x-axis LEO med 2021 distance" } ],
       "mark": {"type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "center", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis zero", "type": "quantitative"},
                     "x": {"field": "x-axis LEO med 2021 distance", "type": "quantitative"},
                     "text": {"field": "display LEO med 2021 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2021"},
         { "filter": {"field": "Orbit class", "equal": "Low Earth Orbit"}},
         { "aggregate": [{"op": "min", "field": "Sin", "as": "min_sin_LEO"}] },
         { "calculate": "datum.min_sin_LEO * 0", "as": "y-axis zero" },
         { "calculate": "abs(round(datum.min_sin_LEO)) + 'km'", "as": "display LEO max 2021 kms"}, 
         { "calculate": "abs(datum.min_sin_LEO) * -1", "as": "x-axis LEO max 2021 distance" } ],
       "mark": {"type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "center", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis zero", "type": "quantitative"},
                     "x": {"field": "x-axis LEO max 2021 distance", "type": "quantitative"},
                     "text": {"field": "display LEO max 2021 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2021"},
         { "filter": {"field": "Orbit class", "equal": "Medium Earth Orbit"}},
         { "aggregate": [{"op": "min", "field": "Sin", "as": "min_sin_MEO"}] },
         { "calculate": "datum.min_sin_MEO * 0", "as": "y-axis zero" },
         { "calculate": "abs(round(datum.min_sin_MEO)) + 'km'", "as": "display MEO max 2021 kms"}, 
         { "calculate": "abs(datum.min_sin_MEO) * -1", "as": "x-axis MEO max 2021 distance" } ],
       "mark": {"type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "center", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis zero", "type":  "quantitative"},
                     "x": {"field": "x-axis MEO max 2021 distance", "type": "quantitative"},
                     "text": {"field": "display MEO max 2021 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
         { "timeUnit": "year", "field": "Launch date", "as": "date"},
         { "filter": "year(datum.date) == 2021"},
         { "filter": {"field": "Orbit class", "equal": "Geosynchronous Equatorial Orbit"}},
         { "aggregate": [{"op": "min", "field": "Sin", "as": "min_sin_GEO"}] },
         { "calculate": "datum.min_sin_GEO * 0", "as": "y-axis zero" },
         { "calculate": "abs(round(datum.min_sin_GEO)) + 'km'", "as": "display GEO max 2021 kms"}, 
         { "calculate": "abs(datum.min_sin_GEO) * -1", "as": "x-axis GEO max 2021 distance" } ],
       "mark": {"type": "text", "style": "label", "angle": 0, "baseline": "bottom", "align": "center", "fontSize": 16 },
       "encoding": { "y": {"field": "y-axis zero", "type":  "quantitative"},
                     "x": {"field": "x-axis GEO max 2021 distance", "type": "quantitative"},
                     "text": {"field": "display GEO max 2021 kms", "type": "nominal"},
                     "color": {"value": "#AAB6C4"} }
     },
     { "transform": [
            { "aggregate": [{"op": "max", "field": "Sin", "as": "max_sin"}] },
            { "calculate": "datum.max_sin * 0", "as": "x-axis zero for vertical rule" } ],
       "mark": {"type": "rule",
                "strokeDash": [1, 10],
                "strokeDashOffset": 50000},
       "encoding": { "x": { "field": "x-axis zero for vertical rule",
                            "type": "quantitative"},
                            "color": {"value": "#9DA4AC"},
                            "size": {"value": 1} }
     },
     { "transform": [
            { "aggregate": [{"op": "max", "field": "Sin", "as": "max_sin"}] },
            { "calculate": "datum.max_sin * 0", "as": "y-axis zero for horizontal rule" } ],
       "mark": {"type": "rule",
                "strokeDash": [1, 10],
                "strokeDashOffset": 50000},
       "encoding": { "y": { "field": "y-axis zero for horizontal rule",
                            "type": "quantitative"},
                            "color": {"value": "#9DA4AC"},
                            "size": {"value": 1} }
     },
     { "transform": [
            { "aggregate": [{"op": "max", "field": "Sin", "as": "max_sin"}] },
            { "calculate": "datum.max_sin * 0", "as": "origin zero" } ],
       "mark": {"type": "image",
                "width": 75,
                "height": 75},
       "encoding": { "x": { "aggregate": "median",
                            "field": "origin zero",
                            "type": "quantitative"},
                     "y": { "aggregate": "median",
                            "field": "origin zero",
                            "type": "quantitative"},
                     "url": { "datum": "data:image/png;base64,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",
                              "type":  "nominal"}
                   }
     },
     { "params": [{ "name": "grid",
                    "select": "interval",
                    "bind": "scales"},
                  { "name": "legend",
                    "select": {"type": "point", "fields": ["Orbit class"]},
                    "bind": "legend"} ],
       "mark": { "type": "point", 
                 "shape": "circle",
                 "tooltip": true,
                 "filled": true,
                 "fillOpacity": 0.75},
       "encoding": { "x": { "field": "Sin", 
                            "type": "quantitative",
                            "title": false, 
                            "axis": {"disable": true,
                                     "grid": false,
                                     "labels": false},
                                     "scale": {"domain": [-70400,70050]}},
                      "y": { "field": "Cos", 
                             "type": "quantitative",
                             "title": false, 
                             "axis": {"disable": true,
                                      "grid": false,
                                      "labels": false},
                                      "scale": {"domain": [-69540,60370]}},
                      "size": {"value": 50},
                      "color": { "field": "Orbit class",
                                 "type":  "nominal",
                                 "sort": [ "Geostationary Transfer Orbit", "Geosynchronous Equatorial Orbit", "Medium Earth Orbit", "Low Earth Orbit"],
                                 "scale": {"range": ["#C8F6FF", "#8DECFF", "#2DDBFF", "#11BBDE" ]} },
                      "opacity": { "condition": {"param": "legend", "value": 1},
                                   "value": 0.025 },
                      "tooltip": [ {"field": "Satellite catalog number (NORAD)", "type": "nominal", "title": "NORAD"},
                                   {"field": "International designator (COSPAR)", "title": "COSPAR"},
                                   {"field": "Name", "title": "SATELLITE"},
                                   {"field": "Country", "title": "COUNTRY"},
                                   {"field": "Purpose", "title": "PURPOSE"},
                                   {"field": "Users", "title": "USERS"},
                                   {"field": "Launch date", "title": "LAUNCH DATE", "type": "temporal", "format": "%d-%m-%Y (DMY)"},
                                   {"field": "Status", "title": "STATUS"},
                                   {"field": "Orbit class", "title": "ORBIT CLASS"},
                                   {"field": "Distance (km)", "title": "AVERAGE DISTANCE (km)", "type": "nominal", "format": ",.0f"},
                                   {"field": "Apogee (km)", "title": "APOGEE (km)", "type": "nominal", "format": ",.0f"},
                                   {"field": "Perigee (km)", "title": "PERIGEE (km)", "type": "nominal", "format": ",.0f"},
                                   {"field": "Launch site", "title": "LAUNCH SITE"},
                                   {"field": "Launch vehicle", "title": "LAUNCH VEHICLE"}] }
     }
    ],
    "config": {
      "legend": {"title": "null",
                 "titleColor": "#ffffff",
                 "labelColor": "#ffffff",
                 "labelFontSize": 10,
                 "labelFont": "Consolas",
                 "orient": "top-left",
                 "labelLimit": 260  }
    }
}
```