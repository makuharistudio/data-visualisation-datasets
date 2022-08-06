# Satellite overview

**[My Power BI visualisation](?????)**

Original Data Sources
* [??????](https://github.com/datamesse/data-visualisation-datasets/tree/main/Satellite%20launch%20overview)
* [??????](https://github.com/datamesse/data-visualisation-datasets/tree/main/Satellite%20launch%20overview)

https://www.browserling.com/tools/image-to-base64

**Note:** Data wrangling and cleaning takes place within the Power Query code below without reference to an external re-mapping data source.

### Power Query for Larger Dataset

```
let
    Source = Csv.Document(File.Contents("D:\Archive\Data Analysis\Dataset\Kaggle\Satellite Data (1957 - 2022)\satellite launches.csv"),[Delimiter=",", Columns=9, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"promote headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"change type 1" = Table.TransformColumnTypes(#"promote headers",{{"", Int64.Type}, {"norad_id", Int64.Type}, {"cospar_id", type text}, {"name", type text}, {"launch_date", type date}, {"flight_ended", type date}, {"status", type text}, {"destination", type text}, {"owner", type text}}),
    #"remove unneeded column" = Table.SelectColumns(#"change type 1",{"norad_id", "cospar_id", "name", "launch_date", "flight_ended", "status", "owner"}),
    #"rename columns" = Table.RenameColumns(#"remove unneeded column",{{"cospar_id", "International designator (COSPAR)"}, {"name", "Name"}, {"launch_date", "Launch date"}, {"flight_ended", "Flight end date"}, {"norad_id", "Satellite catalog number (NORAD)"}, {"status", "Status"}, {"owner", "Owner"}}),
    #"trim International designator" = Table.TransformColumns(#"rename columns",{{"International designator (COSPAR)", Text.Trim, type text}}),
    #"AllReplace" = [#"Arab Satellite Communications Organization" = "Intergovernmental: ARABSAT",
                     #"Asia Broadcast Satellite" = "Intergovernmental: ABS",
                     #"Asia Satellite Telecommunications Company (ASIASAT)" = "Intergovernmental: AsiaSat",
                     #"China/Brazil" = "Intergovernmental: CNSA &INPE",
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

### Power Query for Smaller Dataset

```
let
    Source = Csv.Document(File.Contents("D:\Archive\Data Analysis\Dataset\Union of Concerned Scientists\UCS-Satellite-Database-1-1-2022.txt"),[Delimiter="	", Columns=67, Encoding=1252, QuoteStyle=QuoteStyle.None]),
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
    #"remove redundant columns 2" = Table.SelectColumns(#"add Distance (km) column",{"NORAD Number", "COSPAR Number", "Name of Satellite, Alternate Names", "Launch Site", "Launch Vehicle", "Distance (km)", "Class of Orbit", "Purpose", "Users", "Country of Contractor", "Reference"}),
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
    #"remove redundant columns 3" = Table.SelectColumns(#"rename columns",{"Satellite catalog number (NORAD)", "International designator (COSPAR)", "Alternate names", "Launch site", "Launch vehicle", "Distance (km)", "Orbit class", "Purpose", "Users", "Contractor country", "Reference"}),
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
    #"change type 5" = Table.TransformColumnTypes(#"replace null Users with Unknown",{{"Users", type text}})
in
    #"change type 5"
```

### Power Query for Merged Dataset

```
let
    Source = Table.NestedJoin(#"Satellite launches (n2yo)", {"Satellite catalog number (NORAD)", "International designator (COSPAR)"}, #"Satellites in orbit (ucsusa)", {"Satellite catalog number (NORAD)", "International designator (COSPAR)"}, "Satellites in orbit (ucsusa)", JoinKind.LeftOuter),
    #"expand ucsusa dataset" = Table.ExpandTableColumn(Source, "Satellites in orbit (ucsusa)", {"Satellite catalog number (NORAD)", "International designator (COSPAR)", "Alternate names", "Launch site", "Launch vehicle", "Distance (km)", "Orbit class", "Purpose", "Users", "Contractor country", "Reference"}, {"(ucsusa).Satellite catalog number (NORAD)", "(ucsusa).International designator (COSPAR)", "Alternate names", "Launch site", "Launch vehicle", "Distance (km)", "Orbit class", "Purpose", "Users", "Contractor country", "Reference"}),
    #"add Record type" = Table.AddColumn(#"expand ucsusa dataset", "Record type", each if [#"Satellite catalog number (NORAD)"] <> null and [#"(ucsusa).Satellite catalog number (NORAD)"] = null
then "n2yo unmatched"
else if [#"Satellite catalog number (NORAD)"] = null and [#"(ucsusa).Satellite catalog number (NORAD)"] <> null 
then "ucsusa unmatched"
else if [#"Satellite catalog number (NORAD)"] <> null and [#"(ucsusa).Satellite catalog number (NORAD)"] <> null 
then "matched"
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
    #"remove redundant columns" = Table.SelectColumns(#"add Country column",{"Record type", "Satellite catalog number (NORAD)", "International designator (COSPAR)", "Name", "Alternate names", "Country", "Purpose", "Users", "Launch date", "Launch site", "Launch vehicle", "Orbit class", "Distance (km)", "Status", "Flight end date", "Flight life (days)", "Reference", "Flight end date?"})
in
    #"remove redundant columns"
```