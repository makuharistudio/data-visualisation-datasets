# International Marketplace sales
* [Normalised dataset for Power BI](https://github.com/datamesse/data-visualisation-datasets/raw/main/International%20Marketplace%20sales/International%20Marketplace%20Normalised%20for%20Power%20BI.xlsx)
* [Denormalised dataset for Tableau](https://github.com/datamesse/data-visualisation-datasets/raw/main/International%20Marketplace%20sales/International%20Marketplace%20Denormalised%20for%20Tableau.xlsx)

![Excel files](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/01.png?raw=true)

Original Data Sources
* APAC Superstore dataset can be found and extracted from Tableau Desktop's *Saved Data Sources*.
* [Contoso Data Warehouse](https://www.microsoft.com/en-us/download/details.aspx?id=18279)
* [Wide World Importers](https://github.com/Microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0)

Remapping files used in SSIS ETL
* [Unicode text files that remap original data source values to new values](https://github.com/datamesse/data-visualisation-datasets/tree/main/International%20Marketplace%20sales/Text%20files%20for%20value%20remapping%20in%20SSIS)

To get some hands-on experience with SQL Server Integration Services (SSIS), I created this fictional sales dataset, which is a merge and transformation/alteration of the 3 original data sources bullet pointed above. This included changing the dates to cover specific years, remapping some United States sales to new countries, and renaming customers to more realistically reflect their country of origin using a **[name randomiser](https://github.com/datamesse/data-visualisation-datasets/tree/main/Support%20ticket%20updates)**.

This is a collapsed view of the project from Visual Studio.
![Visual Studio of SSIS project](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/02.png?raw=true)

Once deployed to SQL Server, the main tables and views created are as below.

The Power BI dataset is from the following views:
 - v_Dim_City
 - v_Dim_Customer
 - v_Dim_Product
 - v_Fact_Sales

The Tableau dataset is from this view:
 - v_Denormalised_Sales

![SQL Server of views to export dataset to Excel](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/03.png?raw=true)


# SQL Server Integration Services Project code

## Scripts for initial comparison of datasets

Listed below are the 2 key scripts used to match as close as possible, the Microsoft Wide World Importers and Contoso DW datasets, with the Tableau APAC Superstore dataset's schema. If you would like to learn more details about the planning behind this SSIS project, visit this blog post.

### Wide World Importers (Database)
```
select
   N'Wide World Importers' "Data Source",
   trim(c.CustomerName) "Customer",
   trim(cnty.CountryName) "Country",
   trim(sp.StateProvinceName) "State",
   trim(cy.CityName) "City",
   convert(varchar,o.OrderDate,103) "Order Date",
   trim(s.SupplierName) "Supplier",
   trim(il.Description) "Product",
   floor( il.LineProfit / 200 ) * 200 "Profit (bin)",
   convert(varchar,dateadd(day,(abs(checksum(newid())) % 8),o.OrderDate),103) "Ship Date",
   case
      when sd.DiscountPercentage is null then 0
      else sd.DiscountPercentage/100 end as "Discount",
   il.LineProfit "Profit",
   il.Quantity "Quantity",
   il.Quantity * il.UnitPrice "Sales"
from   Sales.Customers c
   inner join Application.Cities cy
      on c.DeliveryCityID = cy.CityID
   inner join Application.StateProvinces sp
      on cy.StateProvinceID = sp.StateProvinceID
   inner join Application.Countries cnty
      on sp.CountryID = cnty.CountryID
   inner join Sales.Invoices i
      on c.CustomerID = i.CustomerID
   inner join Sales.Orders o
      on i.OrderID = o.OrderID
   inner join Sales.InvoiceLines il
      on i.InvoiceID = il.InvoiceID
   inner join Warehouse.StockItems si
      on il.StockItemID = si.StockItemID
   inner join Purchasing.Suppliers s
      on si.SupplierID = s.SupplierID
   left outer join Sales.SpecialDeals sd
      on c.BuyingGroupID = sd.BuyingGroupID
      and o.OrderDate between sd.startdate and sd.enddate;
```

### Contoso BI Demo Dataset for Retail Industry (Data Warehouse)
**Important:** The max(SalesOrderNumber) inner join is used to significantly reduce the number of Contoso records that will be used, otherwise the final dataset may be too large to upload to Power BI or Tableau's community galleries.
```
select
   N'Contoso' as "Data Source",
   case
      when c.FirstName is null and c.LastName is null and c.CompanyName is not null
         then c.CompanyName
         else c.FirstName + ' ' + c.LastName end "Customer",
   trim(g.RegionCountryName) "Country",
   trim(g.StateProvinceName) "State",
   trim(g.CityName) "City",
   convert(varchar,s.DateKey,103) "Order Date",
   trim(p.Manufacturer) "Supplier",
   trim(p.ProductName) "Product",
   floor( sum(s.UnitPrice - s.TotalCost - s.DiscountAmount) / 200 ) * 200 "Profit (bin)",
   convert(varchar, (dateadd(day,(abs(checksum(newid())) % 18),s.Datekey)),103) "Ship Date",
   sum(s.DiscountAmount)/sum(s.UnitPrice) as "Discount",
   sum(s.UnitPrice - s.TotalCost - s.DiscountAmount) "Profit",
   sum(s.SalesQuantity) "Quantity",
   sum(s.UnitPrice) "Sales"
from   DimCustomer c
   inner join DimGeography g
      on c.GeographyKey = g.GeographyKey
   inner join FactOnlineSales s
      on c.CustomerKey = s.CustomerKey
   inner join DimProduct p
      on s.ProductKey = p.ProductKey
   inner join DimProductSubCategory psc
      on p.ProductSubcategoryKey = psc.ProductSubcategoryKey
   inner join DimProductCategory pc
      on psc.ProductCategoryKey = pc.ProductCategoryKey
   inner join (
      select CustomerKey,
      max(SalesOrderNumber) SalesOrderNumber
      from   FactOnlineSales
      group by CustomerKey
   ) as lso
      on s.SalesOrderNumber = lso.SalesOrderNumber
      where s.ReturnQuantity = 0
group by   
   c.CompanyName,
   c.FirstName,
   c.LastName,
   g.RegionCountryName,
   g.StateProvinceName,
   g.CityName,
   s.DateKey,
   s.SalesOrderNumber,
   pc.ProductCategoryName,
   psc.ProductSubcategoryName,
   p.Manufacturer,
   p.ProductName,
   c.CustomerType;
```

## Preparation / Extract

I used SQL Server 2019 Developer Edition with Visual Studio Community 2019 and the SSIS Extension (all of which are free). I have Tableau Desktop Professional Edition, where I extracted their APAC Superstore data. I won't be providing that original dataset, but I believe it should be available in the free version, as there are thousands of dashboards in their community gallery using that dataset.

![APAC Superstore in Tableau Public](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/04.png?raw=true)

Only key information is outlined, not general SSIS steps. If you are unfamiliar with SSIS, I recommend the LinkedIn Learning course **["SQL Server Integration Services" by Adam Wilbert](https://www.linkedin.com/learning/sql-server-integration-services-2)**.


**Step 1.** Copy the APAC Superstore data to a tabl delimited Unicode text file.

From Tableau Desktop, open the APAC Superstore dataset, and in a new sheet, add all the fields from the Orders table, being mindful to convert all the date-related fields to Discrete and Exact Date formats to render them properly.

![Tableau Desktop Saved Data Source Connect to Sample - APAC Superstore](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/05.png?raw=true)

Then from the dropdown menu, select Worksheet > Copy > Crosstab
![APAC Superstore Copy Crosstab data](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/06.png?raw=true)

Open a new Excel worksheet, paste the data, then Save As a Unicode .txt file. The columns should end up delimited by tabs.

**Note:** Tableau does contain a built-in export to Excel feature, but when testing this, I found that it stalls for this dataset, which is only 10k+ rows by 20 columns. However, copying the data to Excel is near instantaneous. This is a known performance issue.

[https://kb.tableau.com/articles/issue/exporting-a-crosstab-to-excel-2016-takes-a-long-time](https://kb.tableau.com/articles/issue/exporting-a-crosstab-to-excel-2016-takes-a-long-time)

**Step 2.** Restore the Wide World Importers .bak file into your SQL Server instance.

**Step 3.** Restore the Contoso data warehouse .bak file into your SQL Server instance.

**Step 4.** Download all the following data remapping files.

Download all the Unicode files from this folder
https://github.com/datamesse/data-visualisation-datasets/tree/main/International%20Marketplace%20sales/Text%20files%20for%20value%20remapping%20in%20SSIS

**Step 5.** Create a new SSIS project and connections.

Create OLE DB connections to both Contoso and Wide World Importers, and flat file connections to APAC Superstore and all the text remapping files.

I named my project "International Marketplace", but you can name your project and solution however you like.

![Connection Managers](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/07.png?raw=true)

## Creating SSIS package and T-SQL

Below are screenshots of expanded views of the package package with each element numbered, and T-SQL scripts used in each.

### 1  Country using World Wide Importers as the base

![Country using World Wide Importers as the base](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/08.png?raw=true)

**1-1  Create Country main & staging tables**
Connection: International Marketplace
```
drop table if exists Country;
create table Country (
   CountryID int identity(1,1) not null,
   Region nvarchar(30) not null,
   Subregion nvarchar(30) not null,
   Country nvarchar(60) not null
);
drop table if exists z_country;
create table z_country (
   Region nvarchar(30) not null,
   Subregion nvarchar(30) not null,
   Country nvarchar(60) not null
);
```

**1-2  Populate Country staging table**

* **1-2-1  Extract countries from World Wide Importers**
Connection: Wide World Importers Database
```
select
   region "Region",
   subregion "Subregion",
   countryname "Country"
from
   application.countries
group by
   region,
   subregion,
   countryname;
```

* **1-2-2  Load to Country staging table**
Connection: International Marketplace
Table/View: z_country

**1-3  Insert and updates to clean records**
Connection: International Marketplace
```
update z_country set country = N'England'
where country = N'United Kingdom';
update z_country set country = N'South Korea'
where country = N'Korea';
insert into z_country (region,subregion,country)
values (N'Asia',N'Eastern Asia',N'Hong Kong');
insert into z_country (region,subregion,country)
values (N'Europe',N'Northern Europe',N'Scotland');
insert into z_country (region,subregion,country)
values (N'Asia',N'Eastern Asia',N'Taiwan');
```

**1-4  Load from Country staging to main table**

* **1-4-1  Extract countries from staging**
Connection: International Marketplace
Table/View: z_country

* **1-4-2  Sort by Country name ascending**
*Country* ascending, *Subregion* ascending, *Region* ascending

* **1-4-3  Load to Country main table**
Connection: International Marketplace
Table/View: Country

### 2  State and City combine and remap all 3 data sources

![State and City combine and remap all 3 data sources](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/09.png?raw=true)

**2-1  Create State & City main and staging tables, and views**
Connection: International Marketplace
```
drop table if exists State;
create table State (
   StateID int identity(1,1) not null,
   CountryID int not null,
   State nvarchar(35) not null
);
drop table if exists City;
create table City (
   CityID int identity(1,1) not null,
   StateID int not null,
   City nvarchar(35) not null
);
drop table if exists z_statecity;
create table z_statecity (
   DataSource nvarchar(20),
   FromCountry nvarchar(100) not null,
   FromState nvarchar(100) not null,
   FromCity nvarchar(100) not null,
   ToCountry nvarchar(100),
   ToState nvarchar(100),
   ToCity nvarchar(100),
   FinalCityID int
);
drop table if exists zx_statecity_remap;
create table zx_statecity_remap (
   DataSource nvarchar(20) not null,
   FromCountry nvarchar(100) not null,
   FromState nvarchar(100) not null,
   FromCity nvarchar(100) not null,
   ToCountry nvarchar(100),
   ToState nvarchar(100),
   ToCity nvarchar(100)
);
```

**2-2  Populate StateCity staging and remapping tables**

* **2-2-1  Extract states and cities from Wide World Importers**
Connection: Wide World Importers Database
```
select
   N'World Wide Importers' "Data Source",
   cnty.countryname "Country",
   sp.stateprovincename "State",
   cty.cityname "City"
from
   application.countries cnty
   inner join application.stateprovinces sp
   on cnty.countryid = sp.countryid
   inner join application.cities cty
   on sp.stateprovinceid = cty.stateprovinceid;
```

* **2-2-2  Extract states and cities from Contoso**
Connection: Contoso Retail Data Warehouse
```
select
   N'Contoso' as "Data Source",
   trim(g.regioncountryname) "Country",
   trim(g.stateprovincename) "State",
   trim(g.cityname) "City"
from   DimCustomer c
   inner join DimGeography g
   on c.GeographyKey = g.GeographyKey
   inner join FactOnlineSales s
   on c.CustomerKey = s.CustomerKey
   inner join DimProduct p
   on s.ProductKey = p.ProductKey
   inner join DimProductSubCategory psc
   on p.ProductSubcategoryKey = psc.ProductSubcategoryKey
   inner join DimProductCategory pc
   on psc.ProductCategoryKey = pc.ProductCategoryKey
   inner join (
      select
         CustomerKey,
         max(SalesOrderNumber) SalesOrderNumber
      from   FactOnlineSales
      group by CustomerKey
   ) as lso 
   on s.SalesOrderNumber = lso.SalesOrderNumber
where
   s.ReturnQuantity = 0
   and g.cityname is not null
group by
   trim(g.regioncountryname),
   trim(g.stateprovincename),
   trim(g.cityname);
```

* **2-2-3  Union All**
*Data Source*, *From Country*, *From State*, *From City*

* **2-2-4  Sort**
*Data Source* ascending, *From Country* ascending, *From State* ascending, *From City* ascending

* **2-2-5  Load to StateCity staging table 1**
Connection: International Marketplace
Table/View: z_statecity

* **2-2-6  Extract state and cities from APAC Superstore**
Flat file connection manager: APAC Superstore.txt

* **2-2-7  Sort 1**
*Country Region* ascending, *State* ascending, *City* ascending

* **2-2-8  Group By all fields**
*From Country* Group by, *From State* Group by, *From City* Group by

* **2-2-9  Load to StateCity staging table 2**
Connection: International Marketplace
Table/View: z_statecity

* **2-2-10  Extract State and City remapping**
Flat file connection manager: SSIS Remapping for APAC Superstore and Contoso geography.txt

* **2-2-11  Load to StateCity remapping table**
Connection: International Marketplace
Table/View: zx_statecity_remap

**2-3  Replace Data Source field NULLs with APAC Superstore**
Connection: International Marketplace
```
update z_statecity set datasource = N'APAC Superstore' where datasource is null;
```

**2-4  Update StateCity staging using the StateCity remappng table**
Connection: International Marketplace
```
update   zsc
set
   zsc.ToCountry = zxsc.ToCountry,
   zsc.ToState = zxsc.ToState,
   zsc.ToCity = zxsc.ToCity
from   z_statecity zsc
inner join   zx_statecity_remap zxsc
on   zsc.DataSource = zxsc.DataSource
   and zsc.FromCountry = zxsc.FromCountry
   and zsc.FromState = zxsc.FromState
   and zsc.FromCity = zxsc.FromCity;
```

**2-5  Create StateCity remapped view**
Connection: International Marketplace
```
drop view if exists zv_statecity_remapped;
go
create view zv_statecity_remapped as
select
   DataSource,
   FromCountry,
   FromState,
   FromCity,
   case
      when ToCountry is null then FromCountry
      when ToCountry = '' then FromCountry
      when ToCountry = '	' then FromCountry
      else ToCountry end "ToCountry",
   case
      when ToState is null then FromState
      when ToState = '' then FromState
      when ToState = '	' then FromState
      else ToState end "ToState",
   case
      when ToCity is null then FromCity
      when ToCity = '' then FromCity
      when ToCity = '	' then FromCity
      else ToCity end "ToCity"
from   z_statecity;
```

**2-6  Populate State main table from remapped view**

* **2-6-1  Extract StateCity remapped view with Group By 1**
Connection: International Marketplace
```
select
   c.CountryID "CountryID",
   zvsc.ToState "State"
from
   zv_statecity_remapped zvsc
   inner join country c
   on zvsc.ToCountry = c.Country
group by
   c.CountryID,
   zvsc.ToState
order by
   c.CountryID,
   zvsc.ToState;
```

* **2-6-2  Load to State main table**
Connection: International Marketplace
Table/View: State

**2-7  Populate City main table from remapped view**

* **2-7-1  Extract StateCity remapped view with Group By 2**
Connection: International Marketplace
```
select
   s.StateID,
   zvsc.ToCity
from
   zv_statecity_remapped zvsc
   inner join country c
   on zvsc.ToCountry = c.Country
   inner join state s
   on c.CountryID = s.CountryID and zvsc.ToState = s.State
group by
   s.StateID,
   zvsc.ToCity
order by 1, 2;
```

* **2-7-2  Load to City main table  (OLE DB Destination)**
Connection: International Marketplace
Table/View: City

**2-8  Update StateCity staging table with main table CityID**
Connection: International Marketplace
```
update   zsc
set
   zsc.FinalCityID = final.CityID
from (   select
      cny.Country,
      sta.State,
      cty.City,
      cty.CityID
   from city cty
   inner join state sta
   on cty.StateID = sta.StateID
   inner join country cny
   on sta.CountryID = cny.CountryID) as final
inner join zv_statecity_remapped zvsc
on final.Country = zvsc.ToCountry and final.State = zvsc.ToState and final.City = zvsc.ToCity
inner join z_statecity zsc
on zvsc.DataSource = zsc.DataSource and zvsc.FromCountry = zsc.FromCountry and zvsc.FromState = zsc.FromState and zvsc.FromCity = zsc.FromCity;
```

### 3  Customer combine and remap all 3 sources

![Customer combine and remap all 3 sources](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/10.png?raw=true)

**3-1  Create Customer main and staging tables**
Connection: International Marketplace
```
drop table if exists Customer;
create table Customer (
   CustomerID int identity(1,1) not null,
   CityID int not null,
   Customer nvarchar(50) not null,
   SegmentID int not null
);
drop table if exists z_customer;
create table z_customer (
   DataSource nvarchar(20),
   FromCountry nvarchar(100) not null,
   FromState nvarchar(100) not null,
   FromCity nvarchar(100) not null,
   FromCustomer nvarchar(50) not null,
   FromSegment nvarchar(15),
   ToCustomer nvarchar(50),
   ToSegment nvarchar(15)
);
drop table if exists zx_customer_remap;
create table zx_customer_remap (
   DataSource nvarchar(20),
   FromCountry nvarchar(100) not null,
   FromCustomer nvarchar(50) not null,
   ToCustomer nvarchar(50)
);
```

**3-2  Populate Customer staging and remapping tables**

* **3-2-1  Extract Customer from Wide World Importers**
Connection: Wide World Importers Database
```
select
   N'Wide World Importers' "Data Source",
   case
      when c.CustomerName like '%(%' then trim(left(c.CustomerName,charindex(' (',c.CustomerName)))
      else trim(c.CustomerName) end as "Customer",
   cnty.CountryName "Country",
   sp.StateProvinceName "State",
   cy.CityName "City",
   case
      when c.CustomerName like '%(%' then N'Corporate'
      else N'Consumer' end as "Segment"
from       Sales.Customers c
inner join Application.Cities cy
           on c.DeliveryCityID = cy.CityID
inner join Application.StateProvinces sp
           on cy.StateProvinceID = sp.StateProvinceID
inner join Application.Countries cnty
           on sp.CountryID = cnty.CountryID
inner join Sales.Invoices i
           on c.CustomerID = i.CustomerID
group by   c.CustomerName,
           cnty.CountryName,
           sp.StateProvinceName,
           cy.CityName
order by 1, 2, 3, 4;
```

* **3-2-2  Extract Customer from Contoso**
Connection: Contoso Retail Data Warehouse
```
select
   N'Contoso' "Data Source",
   case
      when c.FirstName is null and c.LastName is null and c.CompanyName is not null
         then trim(c.CompanyName)
         else trim(c.FirstName) + ' ' + trim(c.LastName) 
   end "Customer",
   trim(g.RegionCountryName) "Country",
   trim(g.StateProvinceName) "State",
   trim(g.CityName) "City",
   case
      when c.CustomerType = 'Person' then N'Consumer'
      when c.CustomerType = 'Company' then N'Corporate'
   else null end as "Segment"
from   DimCustomer c
inner join DimGeography g
on c.GeographyKey = g.GeographyKey
inner join FactOnlineSales s
on c.CustomerKey = s.CustomerKey
inner join (
   select   CustomerKey,
   max(SalesOrderNumber) SalesOrderNumber
   from   FactOnlineSales
   group by CustomerKey
   ) as lso 
on s.SalesOrderNumber = lso.SalesOrderNumber
where      s.ReturnQuantity = 0
group by   
   c.CompanyName,
   c.FirstName,
   c.LastName,
   trim(g.RegionCountryName),
   trim(g.StateProvinceName),
   trim(g.CityName),
   c.CustomerType;
```

* **3-2-3  Union All**
*Data Source*, *Country*, *State*, *City*, *Customer*, *Segment*

* **3-2-4  Sort 1**
*Data Source* ascending, *From Country* ascending, *From State* ascending, *From City* ascending

* **3-2-5  Load to Customer staging table 1**
Connection: International Marketplace
Table/View: z_customer

* **3-2-6  Extract Customer from APAC Superstore**
Flat file connection manager: APAC Superstore.txt

* **3-2-7  Data Conversion**
*Customer*, *Segment*, *Country*, *State*, *City* convert to Data Type: Unicode string DT_WSTR

* **3-2-8  Sort 2**
*Customer* ascending, *From Country* ascending, *From State* ascending, *From City* ascending, *Segment* ascending

* **3-2-9  Aggregate**
*Customer*, *Segment*, *Country*, *State*, *City*

* **3-2-10  Load to Customer staging table 2**
Connection: International Marketplace
Table/View: z_customer

* **3-2-11  Extract Customer remapping**
Flat file connection manager: SSIS Remapping for APAC Superstore and Contoso names.txt

* **3-2-12  Load to Customer remapping table**
Connection: International Marketplace
Table/View: zx_customer_remap

**3-3  Replace Data Source field NULLs with APAC Superstore**
Connection: International Marketplace
```
update z_customer set datasource = N'APAC Superstore' where datasource is null;
```

**3-4  Update Customer staging using the Customer remapping table**
Connection: International Marketplace
```
update zc
set
   zc.ToCustomer = zxc.ToCustomer,
   zc.ToSegment = N'Consumer'
from
   z_customer zc
inner join   zx_customer_remap zxc
on   zc.DataSource = zxc.DataSource
   and zc.FromCountry = zxc.FromCountry
   and zc.FromCustomer = zxc.FromCustomer;
update zc
   set
      zc.ToSegment =
      case
         when zc.FromSegment = N'Home Office' then N'Consumer'
      else zc.FromSegment end
from z_customer zc
where zc.ToSegment is null;
update zc
   set zc.ToCustomer = zc.FromCustomer
from z_customer zc
where zc.ToCustomer is null;
```

**3-5  Create Customer remapped CityID view**
Connection: International Marketplace
```
drop view if exists zv_customercity_remapped;
go
create view zv_customercity_remapped as
select
   new.CityID,
   trim(zc.ToCustomer) "ToCustomer",
   case
      when zc.ToSegment = N'Consumer' then 0
      when zc.ToSegment = N'Corporate' then 1
      else null end as "Segment ID"
from z_customer zc
inner join
( select
     zvsc.DataSource,
     zvsc.FromCountry,
     zvsc.FromState,
     zvsc.FromCity,
     csc.CityID
  from zv_statecity_remapped zvsc
  inner join 
     ( select
          cny.Country,
          sta.State,
          cty.City,
          cty.CityID
       from city cty
       inner join state sta
       on cty.StateID = sta.StateID
       inner join country cny
       on sta.CountryID = cny.CountryID) as csc
  on zvsc.ToCountry = csc.Country
     and zvsc.ToState = csc.State
     and zvsc.ToCity = csc.City) as new
on  zc.FromCountry = new.FromCountry
   and zc.FromState = new.FromState
   and zc.FromCity = new.FromCity
group by
   new.CityID,
   trim(zc.ToCustomer),
   zc.ToSegment;
```

**3-6  Populate Customer main table from remapped view**

* **3-6-1  Extract Customer remapped view**
Connection: International Marketplace
Table/View: zv_customercity_remapped

* **3-6-2  Load to Customer main table**
Connection: International Marketplace
Table/View: Customer

### 4  Supplier, Category and Product combine and remap all 3 sources**

![Supplier, Category and Product combine and remap all 3 sources](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/11.png?raw=true)

**4-1  Create Supplier, Category, and Product main and staging tables**
Connection: International Marketplace
```
drop table if exists Supplier;
create table Supplier (
   SupplierID int identity(1,1) not null,
   Supplier nvarchar(25) not null
);
drop table if exists Category;
create table Category (
   CategoryID int identity(1,1) not null,
   Category nvarchar(20) not null
);
drop table if exists Subcategory;
create table Subcategory (
   SubcategoryID int identity(1,1) not null,
   CategoryID int not null,
   Subcategory nvarchar(20) not null
);
drop table if exists Product;
create table Product (
   ProductID int identity(1,1) not null,
   SupplierID int not null,
   CategoryID int not null,
   SubcategoryID int not null,
   Product nvarchar(100) not null
);
drop table if exists z_supplier;
create table z_supplier (
   DataSource nvarchar(20),
   FromSupplier nvarchar(100) not null,
   ToSupplier nvarchar(100),
   SupplierID int   
);
drop table if exists z_categorysubcategory;
create table z_categorysubcategory (
   DataSource nvarchar(20),
   FromCategory nvarchar(100),
   FromSubcategory nvarchar(100),
   ToCategory nvarchar(100),
   ToSubcategory nvarchar(100)
);
drop table if exists z_product;
create table z_product (
   DataSource nvarchar(20),
   FromCategory nvarchar(100),
   FromSubcategory nvarchar(100),
   FromSupplier nvarchar(100),
   FromProduct nvarchar(100) not null,
   ToSupplier nvarchar(100),
   ToCategory nvarchar(100),
   ToSubcategory nvarchar(100),
   ToProductID int,
   ToSupplierID int,
   ToCategoryID int,
   ToSubcategoryID int
);
drop table if exists zx_supplier_remap;
create table zx_supplier_remap (
   DataSource nvarchar(20),
   FromSupplier nvarchar(100) not null,
   ToSupplier nvarchar(100)
);
drop table if exists zx_categorysubcategory_remap;
create table zx_categorysubcategory_remap (
   DataSource nvarchar(20),
   FromCategory nvarchar(100) not null,
   FromSubcategory nvarchar(100) not null,
   ToCategory nvarchar(100),
   ToSubcategory nvarchar(100),
);
drop table if exists zx_product_remap;
create table zx_product_remap (
   DataSource nvarchar(20) not null,
   FromSupplier nvarchar(100),
   FromCategory nvarchar(100),
   FromSubcategory nvarchar(100),
   FromProduct nvarchar(100) not null,
   ToCategory nvarchar(100),
   ToSubcategory nvarchar(100)
);
```

**4-2  Populate Supplier, Category, and Product staging and remapping tables**

This data flow has the largest number of elements of the SSIS package. In hindsight, a lot of them may be unnecessary, such as the sorts, so feel free to exclude those.
![Supplier, Category and Product combine and remap all 3 sources](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/12.png?raw=true)

* **4-2-1  Extract Category and Subcategory from Contoso**
Connection: Wide World Importers Database
```
select
   N'Contoso' "Data Source",
   trim(pc.ProductCategoryName) "Category",
   trim(psc.ProductSubcategoryName) "Sub-Category"
from   DimCustomer c
   inner join DimGeography g
   on c.GeographyKey = g.GeographyKey
   inner join FactOnlineSales s
   on c.CustomerKey = s.CustomerKey
   inner join DimProduct p
   on s.ProductKey = p.ProductKey
   inner join DimProductSubCategory psc
   on p.ProductSubcategoryKey = psc.ProductSubcategoryKey
   inner join DimProductCategory pc
   on psc.ProductCategoryKey = pc.ProductCategoryKey
   inner join (
      select CustomerKey,
      max(SalesOrderNumber) SalesOrderNumber
      from   FactOnlineSales
      group by CustomerKey
   ) as lso
   on s.SalesOrderNumber = lso.SalesOrderNumber
where   s.ReturnQuantity = 0
group by
   pc.ProductCategoryName,
   psc.ProductSubcategoryName;
```

* **4-2-2  Load to CategorySubcategory staging table 1**
Connection: International Marketplace
Table/View: z_categorysubcategory

* **4-2-3  Extract Supplier from Contoso**
Connection: Contoso Retail Data Warehouse
```
select
   N'Contoso' "Data Source",
   trim(p.Manufacturer) "Supplier"
from   DimCustomer c
   inner join DimGeography g
   on c.GeographyKey = g.GeographyKey
   inner join FactOnlineSales s
   on c.CustomerKey = s.CustomerKey
   inner join DimProduct p
   on s.ProductKey = p.ProductKey
   inner join DimProductSubCategory psc
   on p.ProductSubcategoryKey = psc.ProductSubcategoryKey
   inner join DimProductCategory pc
   on psc.ProductCategoryKey = pc.ProductCategoryKey
   inner join (
      select CustomerKey,
      max(SalesOrderNumber) SalesOrderNumber
      from   FactOnlineSales
      group by CustomerKey
   ) as lso
   on s.SalesOrderNumber = lso.SalesOrderNumber
where   s.ReturnQuantity = 0
group by
   trim(p.Manufacturer);
```

* **4-2-4  Extract Supplier from World Wide Importers**
Connection: Wide World Importers Database
```
select
   N'Wide World Importers' "Data Source",
   SupplierName "Supplier"
from Purchasing.Suppliers
group by SupplierName;
```

* **4-2-5  Union All 1**
*Data Source*, *Supplier*

* **4-2-6  Load to Supplier staging table 1**
Connection: International Marketplace
Table/View: z_supplier

* **4-2-7  Extract Product from Wide World Importers**
Connection: Wide World Importers Database
```
select
   N'Wide World Importers' "Data Source",
   null "Category",
   null "Subcategory",
   s.SupplierName "Supplier",
   il.Description "Product"
from Sales.InvoiceLines il
inner join Warehouse.StockItems si
on il.StockItemID = si.StockItemID
inner join Purchasing.Suppliers s
on si.SupplierID = s.SupplierID
group by
   s.SupplierName,
   il.Description;
```

* **4-2-8  Extract Product from Contoso**
Connection: Contoso Retail Data Warehouse
```
select
   N'Contoso' "Data Source",
   trim(pc.ProductCategoryName) "Category",
   trim(psc.ProductSubcategoryName) "Subcategory",
   trim(p.Manufacturer) "Supplier",
   trim(p.ProductName) "Product"
from   DimCustomer c
   inner join DimGeography g
   on c.GeographyKey = g.GeographyKey
   inner join FactOnlineSales s
   on c.CustomerKey = s.CustomerKey
   inner join DimProduct p
   on s.ProductKey = p.ProductKey
   inner join DimProductSubCategory psc
   on p.ProductSubcategoryKey = psc.ProductSubcategoryKey
   inner join DimProductCategory pc
   on psc.ProductCategoryKey = pc.ProductCategoryKey
   inner join (
      select CustomerKey,
      max(SalesOrderNumber) SalesOrderNumber
      from FactOnlineSales
      group by CustomerKey
   ) as lso 
   on s.SalesOrderNumber = lso.SalesOrderNumber
   where s.ReturnQuantity = 0
group by
   trim(pc.ProductCategoryName),
   trim(psc.ProductSubcategoryName),
   trim(p.Manufacturer),
   trim(p.ProductName);
```

* **4-2-9  Union All 2**
*Data Source*, *Category*, *Subcategory*, *Supplier*, *Product*

* **4-2-10  Remove double quotes 6**
Derived Column Expressions:
 - REPLACE(Category,"\"","")
 - REPLACE(Subcategory,"\"","")
 - REPLACE(Supplier,"\"","")
 - REPLACE(Product,"\"","")

* **4-2-11  Load to Product staging table 1**
Connection: International Marketplace
Table/View: z_product

* **4-2-12  Extract Category and Subcategory from APAC Superstore**
Flat file connection manager: APAC Superstore.txt

* **4-2-13  Data Conversion 1**
*Category*, *Subcategory* convert to Data Type: Unicode string DT_WSTR

* **4-2-14  Sort 1**
*Category* ascending, *Subcategory* ascending

* **4-2-15  Aggregate 1**
*Category* Group by, *Subcategory* Group by

* **4-2-16  Load to CategorySubcategory staging table 2**
Connection: International Marketplace
Table/View: z_categorysubcategory

* **4-2-17  Extract Supplier from APAC Superstore**
Flat file connection manager: APAC Superstore.txt

* **4-2-18  Data Conversion 2**
*Supplier* convert to Data Type: Unicode string DT_WSTR

* **4-2-19  Sort 2**
*Supplier* ascending

* **4-2-20  Aggregate 2**
*Supplier* Group by

* **4-2-21  Load to Supplier staging table 2**
Connection: International Marketplace
Table/View: z_supplier

* **4-2-22  Extract Product remapping APAC Superstore**
Flat file connection manager: SSIS Remapping for APAC Superstore products.txt

* **4-2-23  Remove double quotes 4**
Derived Column Expressions:
 - REPLACE([From Product],"\"","")
 - REPLACE([From Supplier],"\"","")
 - REPLACE([From Category],"\"","")
 - REPLACE([From Subcategory],"\"","")
 - REPLACE([To Subcategory],"\"","")
 - REPLACE([To Category],"\"","")

* **4-2-24  Sort 6**
*Data Source* ascending, *From Supplier* ascending, *From Category* ascending, *From Subcategory* ascending, *From Product* ascending, *To Category* ascending, *To Subcategory* ascending

* **4-2-25  Load to Product remapping table 1**
Connection: International Marketplace
Table/View: zx_product_remap

* **4-2-26  Extract Product from APAC Superstore**
Flat file connection manager: APAC Superstore.txt

* **4-2-27  Data Conversion 3**
*Category*, *Product*, *Subcategory*, *Supplier* convert to Data Type: Unicode string DT_WSTR

* **4-2-28  Remove double quotes 1**
 - REPLACE([4-2-27  Data Conversion 3].Product,"\"","")
 - REPLACE([4-2-27  Data Conversion 3].Category,"\"","")
 - REPLACE([4-2-27  Data Conversion 3].Subcategory,"\"","")
 - REPLACE([4-2-27  Data Conversion 3].Supplier,"\"","")

* **4-2-29  Sort 3**
*Supplier* ascending, *Category* ascending, *Subcategory* ascending, *Product* ascending

* **4-2-30  Aggregate 3**
*Supplier*, *Category*, *Subcategory*, *Product*,  Group by

* **4-2-31  Load to Product staging table 2**
Connection: International Marketplace
Table/View: z_product

* **4-2-32  Extract CategorySubcategory remapping**
Flat file connection manager: SSIS Remapping for APAC Superstore and Contoso categories.txt

* **4-2-33  Remove double quotes 2**
 - REPLACE([From Category],"\"","")
 - REPLACE([From Subcategory],"\"","")
 - REPLACE([To Category],"\"","")
 - REPLACE([To Subcategory],"\"","")

* **4-2-34  Sort 4**
*Data Source* ascending, *From Category* ascending, *From Subcategory* ascending, *To Category* ascending, *To Subcategory* ascending

* **4-2-35  Load to CategorySubcategory remapping table**
Connection: International Marketplace
Table/View: zx_categorysubcategory_remap

* **4-2-36  Extract Supplier remapping**
Flat file connection manager: SSIS Remapping for all suppliers.txt

* **4-2-37  Remove double quotes 3**
 - REPLACE([From Supplier],"\"","")
 - REPLACE([To Supplier],"\"","")

* **4-2-38  Sort 5**
*Data Source* ascending, *From Supplier* ascending, *To Supplier* ascending

* **4-2-39  Load to Supplier remapping table**
Connection: International Marketplace
Table/View: zx_supplier_remap

* **4-2-40  Extract Product remapping WWI**
Flat file connection manager: SSIS Remapping for Wide World Importers products.txt

* **4-2-41  Remove double quotes 5**
 - REPLACE([From Product],"\"","")
 - REPLACE([To Category],"\"","")
 - REPLACE([To Subcategory],"\"","")
 - REPLACE([From Supplier],"\"","")

* **4-2-42  Sort 7**
*Data Source* ascending, *From Supplier* ascending, *From Product* ascending, *To Category* ascending, *To Subcategory* ascending

* **4-2-43  Load to Product remapping 2**
Connection: International Marketplace
Table/View: zx_product_remap

**4-3  Replace Data Source field NULLs with APAC Superstore**
Connection: International Marketplace
```
update z_supplier set datasource = N'APAC Superstore' where datasource is null;
update z_categorysubcategory set datasource = N'APAC Superstore' where datasource is null;
update z_product set datasource = N'APAC Superstore' where datasource is null;
```

**4-4  Update Supplier and Category staging tables with remapping tables**
Connection: International Marketplace
```
update zs
   set zs.ToSupplier = zxs.ToSupplier
   from z_supplier zs
   inner join zx_supplier_remap zxs
   on zs.DataSource = zxs.DataSource
      and zs.FromSupplier = zxs.FromSupplier;
update zs
   set zs.ToSupplier = zs.FromSupplier
   from z_supplier zs
   where zs.ToSupplier is null;
update zcs
   set zcs.ToCategory = zxcs.ToCategory,
       zcs.ToSubcategory = zxcs.ToSubcategory
from z_categorysubcategory zcs
left outer join zx_categorysubcategory_remap zxcs
on zcs.DataSource = zxcs.DataSource
   and zcs.FromCategory = zxcs.FromCategory
   and zcs.FromSubcategory = zxcs.FromSubcategory;
update zcs
   set zcs.ToCategory = zcs.FromCategory
   from z_categorysubcategory zcs
   where zcs.ToCategory is null;
update zcs
   set zcs.ToSubcategory = zcs.FromSubcategory
   from z_categorysubcategory zcs
   where zcs.ToSubcategory is null;
```

**4-5  Insert new records for CategorySubcategory staging table**
Connection: International Marketplace
```
insert into z_categorysubcategory(datasource,tocategory,tosubcategory)
   values
      (N'APAC Superstore',N'Appliances',N'Blenders'),
      (N'APAC Superstore',N'Appliances',N'Stoves'),
      (N'APAC Superstore',N'Appliances',N'Toasters'),
      (N'Wide World Importers',N'Clothes and shoes',N'Jackets and jumpers'),
      (N'Wide World Importers',N'Clothes and shoes',N'Shirts'),
      (N'Wide World Importers',N'Clothes and shoes',N'Slippers'),
      (N'Wide World Importers',N'Clothes and shoes',N'Socks'),
      (N'Wide World Importers',N'Food',N'Confectionery'),
      (N'Wide World Importers',N'Games and toys',N'Action figures'),
      (N'Wide World Importers',N'Games and toys',N'Novelty gifts'),
      (N'Wide World Importers',N'Games and toys',N'RC toys'),
      (N'Wide World Importers',N'Games and toys',N'Ride on toys');
```

**4-6  Update Product staging with remapping tables**
Connection: International Marketplace
```
update zp
   set zp.ToSupplier = zs.ToSupplier
   from z_product zp
      inner join z_supplier zs
      on zp.DataSource = zs.DataSource
         and zp.FromSupplier = zs.FromSupplier;
update zp
   set zp.ToCategory = zcs.ToCategory,
       zp.ToSubcategory = zcs.ToSubcategory
   from z_product zp
     inner join z_categorysubcategory zcs
      on zp.DataSource = zcs.DataSource
      and zp.FromCategory = zcs.FromCategory
      and zp.FromSubcategory = zcs.FromSubcategory
      where zp.DataSource in (N'Contoso',N'APAC Superstore');
update zp
   set zp.ToCategory = zxp.ToCategory,
       zp.ToSubcategory = zxp.ToSubcategory
   from z_product zp
      inner join zx_product_remap zxp
      on zp.DataSource = zxp.DataSource
      and zp.FromProduct = zxp.FromProduct;
update zs2
   set zs2.FromShipMode = 'Same Day'
   from z_sales zs2
   inner join
      (select cast((ABS(CHECKSUM(NewId()))%3) as bigint) as "random", zs1.SalesStagingID
       from  z_sales zs1
       where zs1.FromOrderDate = zs1.FromShipDate and zs1.FromShipMode is null) as rzs
      on zs2.SalesStagingID = rzs.SalesStagingID
   where rzs.random < 2;
update zs2
   set zs2.FromShipMode =
      case
         when rzs.random between 0 and 5 then N'Standard Class'           
         when rzs.random between 6 and 8 then N'Second Class'
         else N'First Class' end
   from z_sales zs2
   inner join
      (select cast((ABS(CHECKSUM(NewId()))%10) as bigint) as "random", zs1.SalesStagingID
       from  z_sales zs1
       where zs1.FromShipMode is null) as rzs
      on zs2.SalesStagingID = rzs.SalesStagingID;
```

**4-7  Populate Supplier and Category main tables from staging tables**

* **4-7-1  Extract Supplier staging table**
Connection: International Marketplace
```
select tosupplier
from z_supplier
group by tosupplier
order by 1;
```

* **4-7-2  Load to Supplier main table**
Connection: International Marketplace
Table/View: Supplier

* **4-7-3  Extract Category staging table**
Connection: International Marketplace
```
select tocategory
from z_categorysubcategory
group by tocategory
order by 1;
```

* **4-7-4  Load to Category main table**
Connection: International Marketplace
Table/View: Category

**4-8  Populate Subcategory main table from staging table**

* **4-8-1  Extract Subcategory staging table**
Connection: International Marketplace
```
select
   c.categoryid,
   zcs.tosubcategory as "subcategory"
from z_categorysubcategory zcs
left outer join category c
on zcs.tocategory = c.category
group by
   c.categoryid,
   zcs.tosubcategory
order by 1, 2;
```

* **4-8-2  Load to Subcategory main table**
Connection: International Marketplace
Table/View: Subcategory

**4-9  Update Product staging with IDs from other main tables**
Connection: International Marketplace
```
update zp
   set zp.ToSupplierID = s.SupplierID,
       zp.ToCategoryID = c.CategoryID,
       zp.ToSubcategoryID = sc.SubcategoryID
from z_product zp
   inner join supplier s
   on zp.ToSupplier = s.Supplier
   inner join Category c
   on zp.ToCategory = c.Category
   inner join Subcategory sc
   on zp.ToSubcategory = sc.Subcategory;
```

**4-10  Populate Product main table from staging table**

* **4-10-1  Extract Product staging table**
Connection: International Marketplace
Table/View: z_product

* **4-10-2  Sort**
*FromProduct* ascending, *ToSupplierID* ascending, *ToCategoryID* ascending, *ToSubcategoryID* ascending

* **4-10-3  Load to Product main table**
Connection: International Marketplace
Table/View: Product

**4-11  Update Product staging with Product IDs from main table**
Connection: International Marketplace
```
update zp
   set zp.ToProductID = p.ProductID
from z_product zp
   inner join product p
   on zp.FromProduct = p.Product;
```

### 5  Create Sales fact table and combine all 3 sources

![Create Sales fact table and combine all 3 sources](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/13.png?raw=true)

**5-1  Create Sales main and staging tables**
Connection: International Marketplace
```
drop table if exists Sales;
create table Sales (
   SalesID int identity(1,1) not null,
   OrderID int,
   CustomerID int not null,
   ProductID int not null,
   OrderDate date not null,
   ProfitBin decimal(18,2) not null,
   ShipDate date not null,
   ShipModeID int,
   DiscountPercentage  decimal(18,3) not null,
   DiscountAmount  decimal(18,2) not null,
   Profit decimal(18,2) not null,
   Quantity int not null,
   Sales decimal(18,2) not null
);
drop table if exists z_sales;
create table z_sales (
   SalesStagingID int identity(1,1) not null,
   DataSource nvarchar(20),
   FromCustomer nvarchar(100),
   FromCountry nvarchar(100),
   FromState nvarchar(100),
   FromCity nvarchar(100),
   FromOrderDate date,
   FromSupplier nvarchar(100),
   FromProduct nvarchar(100),
   FromProfitBin decimal(18,2),
   FromShipDate date,
   FromShipMode nvarchar(100),
   FromDiscountPercent decimal(18,3),
   FromDiscountAmount decimal(18,2),
   FromProfit decimal(18,2),
   FromQuantity int,
   FromSales decimal(18,2),
   ToOrderDate date,
   ToShipDate date,
   ToSalesID int,
   ToCustomerID int,
   ToProductID int,
   ToShipModeID int
);
```

**5-2  Populate Sales staging table with Contoso and WWI**

* **5-2-1  Extract Sales from World Wide Importers**
Connection: Wide World Importers Database
```
select
   N'Wide World Importers' "Data Source",
   trim(c.CustomerName) "Customer",
   trim(cnty.CountryName) "Country",
   trim(sp.StateProvinceName) "State",
   trim(cy.CityName) "City",
   convert(varchar,o.OrderDate,103) "Order Date",
   trim(s.SupplierName) "Supplier",
   trim(il.Description) "Product",
   floor( il.LineProfit / 200 ) * 200 "Profit (bin)",
   convert(varchar,dateadd(day,(abs(checksum(newid())) % 8),o.OrderDate),103) "Ship Date",
   case
      when sd.DiscountPercentage is null then 0
      else sd.DiscountPercentage/100 end as "Discount",
   il.LineProfit "Profit",
   il.Quantity "Quantity",
   il.Quantity * il.UnitPrice "Sales"
from   Sales.Customers c
   inner join Application.Cities cy
      on c.DeliveryCityID = cy.CityID
   inner join Application.StateProvinces sp
      on cy.StateProvinceID = sp.StateProvinceID
   inner join Application.Countries cnty
      on sp.CountryID = cnty.CountryID
   inner join Sales.Invoices i
      on c.CustomerID = i.CustomerID
   inner join Sales.Orders o
      on i.OrderID = o.OrderID
   inner join Sales.InvoiceLines il
      on i.InvoiceID = il.InvoiceID
   inner join Warehouse.StockItems si
      on il.StockItemID = si.StockItemID
   inner join Purchasing.Suppliers s
      on si.SupplierID = s.SupplierID
   left outer join Sales.SpecialDeals sd
      on c.BuyingGroupID = sd.BuyingGroupID
      and o.OrderDate between sd.startdate and sd.enddate;
```

* **5-2-2  Remove double quotes 1**
  - REPLACE(Product,"\"","")

* **5-2-3  Load to Sales staging table 1**
Connection: International Marketplace
Table/View: z_Sales

* **5-2-4  Extract Sales from Contoso**
Connection: Contoso Retail Data Warehouse
```
select
   N'Contoso' as "Data Source",
   case
      when c.FirstName is null and c.LastName is null and c.CompanyName is not null
         then c.CompanyName
         else c.FirstName + ' ' + c.LastName end "Customer",
   trim(g.RegionCountryName) "Country",
   trim(g.StateProvinceName) "State",
   trim(g.CityName) "City",
   convert(varchar,s.DateKey,103) "Order Date",
   trim(p.Manufacturer) "Supplier",
   trim(p.ProductName) "Product",
   floor( sum(s.UnitPrice - s.TotalCost - s.DiscountAmount) / 200 ) * 200 "Profit (bin)",
   convert(varchar, (dateadd(day,(abs(checksum(newid())) % 18),s.Datekey)),103) "Ship Date",
   sum(s.DiscountAmount)/sum(s.UnitPrice) as "Discount",
   sum(s.UnitPrice - s.TotalCost - s.DiscountAmount) "Profit",
   sum(s.SalesQuantity) "Quantity",
   sum(s.UnitPrice) "Sales"
from   DimCustomer c
   inner join DimGeography g
      on c.GeographyKey = g.GeographyKey
   inner join FactOnlineSales s
      on c.CustomerKey = s.CustomerKey
   inner join DimProduct p
      on s.ProductKey = p.ProductKey
   inner join DimProductSubCategory psc
      on p.ProductSubcategoryKey = psc.ProductSubcategoryKey
   inner join DimProductCategory pc
      on psc.ProductCategoryKey = pc.ProductCategoryKey
   inner join (
      select CustomerKey,
      max(SalesOrderNumber) SalesOrderNumber
      from   FactOnlineSales
      group by CustomerKey
   ) as lso 
      on s.SalesOrderNumber = lso.SalesOrderNumber
      where      s.ReturnQuantity = 0
group by   
   c.CompanyName,
   c.FirstName,
   c.LastName,
   g.RegionCountryName,
   g.StateProvinceName,
   g.CityName,
   s.DateKey,
   s.SalesOrderNumber,
   pc.ProductCategoryName,
   psc.ProductSubcategoryName,
   p.Manufacturer,
   p.ProductName,
   c.CustomerType;
```

* **5-2-5  Remove double quotes 2**
  - REPLACE(Product,"\"","")

* **5-2-6  Load to Sales staging table 2**
Connection: International Marketplace
Table/View: z_Sales

**5-3  Populate Sales staging table with APAC Superstore**

 * **5-3-1  Extract Sales from APAC Superstore**
Flat file connection manager: APAC Superstore.txt

* **5-3-2  Convert to Unicode**
  - *Customer*, *Country*, *State*, *City*, *Supplier*, *Product*, *Ship Mode* convert to Data Type: Unicode string DT_WSTR
  - *Ship Mode*, *Order Date* convert to Data Type: database date DT_DBDATE
  - *Profit (bin)*, *Profit*, *Sales* convert to Data Type: decimal DT_DECIMAL, scale 2
  - *Quantity* convert to Data Type: single-byte signed integer DT_I1

* **5-3-3  Remove double quotes and percentage character from Discount**
  - REPLACE([5-3-2  Convert to Unicode].Customer,"\"","")
  - REPLACE([5-3-2  Convert to Unicode].Country,"\"","")
  - REPLACE([5-3-2  Convert to Unicode].State,"\"","")
  - REPLACE([5-3-2  Convert to Unicode].City,"\"","")
  - REPLACE([5-3-2  Convert to Unicode].Supplier,"\"","")
  - REPLACE([5-3-2  Convert to Unicode].Product,"\"","")
  - REPLACE([5-3-2  Convert to Unicode].[Ship Mode],"\"","")
  - REPLACE(Discount,"%","")

* **5-3-4  Convert Discount to decimal data type**
  - *Discount* convert to Data Type: decimal DT_DECIMAL, scale 2

* **5-3-5  Convert Discount to decimal value**
  - [5-3-4  Convert Discount to decimal data type].Discount / 100

* **5-3-6  Load to Sales staging table**
Connection: International Marketplace
Table/View: z_sales

**5-4  Replace Data Source field NULLs with APAC Superstore populate outstanding values**
Connection: International Marketplace
```
update z_sales set datasource = N'APAC Superstore' where datasource is null;
update zs
   set
      zs.FromDiscountAmount =
         case
            when zs.FromDiscountPercent = round(0,2) then 0
            else cast( ((zs.FromSales/(1-FromDiscountPercent))-zs.FromSales) as decimal(18,2)) end
   from z_sales zs;
update zs2
   set zs2.FromShipMode = 'Same Day'
   from z_sales zs2
   inner join
      (select cast((ABS(CHECKSUM(NewId()))%3) as bigint) as "random", zs1.SalesStagingID
       from  z_sales zs1
       where zs1.FromOrderDate = zs1.FromShipDate and zs1.FromShipMode is null) as rzs
      on zs2.SalesStagingID = rzs.SalesStagingID
   where rzs.random < 2;
update zs2
   set zs2.FromShipMode =
      case
         when rzs.random between 0 and 5 then N'Standard Class'           
         when rzs.random between 6 and 8 then N'Second Class'
         else N'First Class' end
   from z_sales zs2
   inner join
      (select cast((ABS(CHECKSUM(NewId()))%10) as bigint) as "random", zs1.SalesStagingID
       from  z_sales zs1
       where zs1.FromShipMode is null) as rzs
      on zs2.SalesStagingID = rzs.SalesStagingID;
update zs2
   set
      zs2.toshipdate = dateadd(year,(2022-cast(convert(varchar(4),zs2.fromshipdate,112) as int)),zs2.fromshipdate),
      zs2.toorderdate = dateadd(year,(2022-cast(convert(varchar(4),zs2.fromorderdate,112) as int)),zs2.fromorderdate)
   from z_sales zs2
   inner join
      (select cast((ABS(CHECKSUM(NewId()))%2) as bigint) as "random", zs1.SalesStagingID
       from  z_sales zs1 where zs1.toorderdate is null and zs1.toshipdate is null) as rzs
       on zs2.SalesStagingID = rzs.SalesStagingID
   where rzs.random < 1;
update zs
   set
      zs.toshipdate = dateadd(year,(2022-cast(convert(varchar(4),zs.fromshipdate,112) as int)+1),zs.fromshipdate),
      zs.toorderdate = dateadd(year,(2022-cast(convert(varchar(4),zs.fromorderdate,112) as int)+1),zs.fromorderdate)
   from z_sales zs
   where zs.toorderdate is null and zs.toshipdate is null;
```

**5-5  Populate Sales staging table with Customer, Product, and ShipMode IDs from main tables**
Connection: International Marketplace
```
update zs
   set zs.ToProductID = p.ProductID
from z_sales zs
inner join product p
on zs.FromProduct = p.Product;
update zs
   set zs.ToShipModeID =
      case
         when zs.FromShipMode = N'Same Day' then 0
         when zs.FromShipMode = N'First Class' then 1
         when zs.FromShipMode = N'Second Class' then 2
         when zs.FromShipMode = N'Standard Class' then 3
      else null end
from z_sales zs;
update zs
   set zs.ToCustomerID = rmp.CustomerID
from z_sales zs
inner join
   ( select
        SalesStagingID,
        DataSource,
        FromCountry,
        FromState,
        FromCity,
        case
           when FromCustomer like '%(%' then trim(left(FromCustomer,charindex(' (',FromCustomer)))
           else trim(FromCustomer) end as "FromCustomer"
        from z_sales) as zs2
   on zs.SalesStagingID = zs2.SalesStagingID
inner join
   ( select
        remap.DataSource,
        remap.FromCountry,
        remap.FromState,
        remap.FromCity,
        remap.FromCustomer,
        c.CustomerID
     from
        ( select
             zc.DataSource,
             zc.FromCountry,
             zc.FromState,
             zc.FromCity,
             zc.FromCustomer,
             new.CityID,
             case
                when zc.ToSegment = N'Consumer' then 0
                when zc.ToSegment = N'Corporate' then 1
                else null end as "SegmentID",
             trim(zc.ToCustomer) "ToCustomer"
          from z_customer zc
          inner join
             ( select
                  zvsc.DataSource,
                  zvsc.FromCountry,
                  zvsc.FromState,
                  zvsc.FromCity,
                  csc.CityID
               from zv_statecity_remapped zvsc
               inner join 
                  ( select
                       cny.Country,
                       sta.State,
                       cty.City,
                       cty.CityID
                   from city cty
                   inner join state sta
                   on cty.StateID = sta.StateID
                   inner join country cny
                   on sta.CountryID = cny.CountryID) as csc
               on zvsc.ToCountry = csc.Country
               and zvsc.ToState = csc.State
               and zvsc.ToCity = csc.City) as new
          on  zc.FromCountry = new.FromCountry
          and zc.FromState = new.FromState
          and zc.FromCity = new.FromCity
          group by
             zc.DataSource,
             zc.FromCountry,
             zc.FromState,
             zc.FromCity,
             zc.FromCustomer,
             new.CityID,
             zc.ToSegment,
             trim(zc.ToCustomer)
     ) as remap
     inner join customer c
        on remap.CityID = c.CityID
        and remap.SegmentID = c.SegmentID
        and remap.ToCustomer = c.Customer ) as rmp
   on zs.DataSource = rmp.DataSource
      and zs.FromCountry = rmp.FromCountry
      and zs.FromState = rmp.FromState
      and zs.FromCity = rmp.FromCity
      and zs2.FromCustomer = rmp.FromCustomer;
```

**5-6  Populate Sales main table from staging table**

* **5-6-1  Extract Sales from staging table**
Connection: International Marketplace
Table/View: z_sales

* **5-6-2  Sort by Order Date, Ship Date, then other random columns**
*ToOrderDate* ascending, *ToShipDate* ascending, *ToCustomerID* ascending, *ToShipModeID* ascending, *ToProductID* ascending

* **5-6-3  Load to Sales main table**
Connection: International Marketplace
Table/View: Sales

**5-7  Create temp table to populate Sales main table with Order ID**
Connection: International Marketplace
```
if object_id(N'tempdb..#SalesOrderID') is not null
begin
drop table #SalesOrderID
end
go
create table #SalesOrderID
   ( OrderID int identity(1,1) not null,
     CustomerID int,
	 OrderDate date,
	 ShipDate date,
	 ShipModeID int )
insert into #SalesOrderID
select
   s.CustomerID,
   s.OrderDate,
   s.ShipDate,
   s.ShipModeID
from sales s
inner join customer c
on s.CustomerID = c.CustomerID
group by
   s.CustomerID,
   s.OrderDate,
   s.ShipDate,
   s.ShipModeID
order by 
   s.OrderDate asc,
   s.ShipDate asc,
   s.ShipModeID desc,
   s.CustomerID asc;
update s
   set s.OrderID = tmp.OrderID
from sales s
inner join #SalesOrderID tmp
   on s.CustomerID = tmp.CustomerID
      and s.OrderDate = tmp.OrderDate
      and s.ShipDate = tmp.ShipDate
      and s.ShipModeID = tmp.ShipModeID;
begin
drop table if exists #SalesOrderID
end;
```

### 6  Add Ship Mode and Segment tables
Connection: International Marketplace
```
drop table if exists Segment;
create table Segment (
   SegmentID int identity(0,1) not null,
   Segment nvarchar(10)
);
insert into Segment (Segment)
   values (N'Consumer'),(N'Corporate');
drop table if exists ShipMode;
create table ShipMode (
   ShipModeID int identity(0,1) not null,
   ShipMode nvarchar(15)
);
insert into ShipMode (ShipMode)
   values (N'Same Day'),(N'First Class'),(N'Second Class'),(N'Standard Class');
```

### 7  Create denormalised view for Tableau and normalised views for Power BI

![Create denormalised view for Tableau and normalised views for Power BI](https://raw.githubusercontent.com/datamesse/data-visualisation-datasets/main/International%20Marketplace%20sales/screenshots/14.png?raw=true)

**7-1  Sales for Tableau**
Connection: International Marketplace
```
drop view if exists v_Denormalised_Sales;
go
create view v_Denormalised_Sales as
   select
      s.OrderID,
      s.SalesID as "OrderLineID",
      c.Customer,
      seg.Segment,
      cny.Country,
      sta.State,
      cty.City,
      p.Product,
      sup.Supplier,
      cat.Category,
      sc.Subcategory,
      shp.ShipMode,
      s.Quantity,
      s.DiscountPercentage,
      s.DiscountAmount,
      s.Sales,
      s.Profit,
      s.ProfitBin,
      s.OrderDate,
      s.ShipDate
   from Sales s
   inner join Customer c
      on s.CustomerID = c.CustomerID
   inner join Segment seg
      on c.SegmentID = seg.SegmentID
   inner join City cty
      on c.CityID = cty.CityID
   inner join State sta
      on cty.StateID = sta.StateID
   inner join Country cny
      on sta.CountryID = cny.CountryID
   inner join Product p
      on s.ProductID = p.ProductID
   inner join Supplier sup
      on p.SupplierID = sup.SupplierID
   inner join Subcategory sc
      on p.SubcategoryID = sc.SubcategoryID
   inner join Category cat
      on sc.CategoryID = cat.CategoryID
   inner join ShipMode shp
      on s.ShipModeID = shp.ShipModeID;
```
**7-2  DimCustomer for Power BI**
Connection: International Marketplace
```
drop view if exists v_Dim_Customer;
go
create view v_Dim_Customer as
   select
      c.CustomerID,
      c.Customer,
      seg.Segment
   from Customer c
   inner join Segment seg
      on c.SegmentID = seg.SegmentID;
```

**7-3  DimCity for Power BI**
 - Connection: International Marketplace
```
drop view if exists v_Dim_City;
go
create view v_Dim_City as
   select
      cty.CityID,
      cty.City,
      sta.State,
      cny.Country
   from City cty
   inner join State sta
      on cty.StateID = sta.StateID
   inner join Country cny
      on sta.CountryID = cny.CountryID;
```
**7-4  DimProduct for Power BI**
 - Connection: International Marketplace
```
drop view if exists v_Dim_Product;
go
create view v_Dim_Product as
   select
      p.ProductID,
      p.Product,
      sup.Supplier,
      cat.Category,
      sc.Subcategory
   from Product p
   inner join Supplier sup
      on p.SupplierID = sup.SupplierID
   inner join Subcategory sc
      on p.SubcategoryID = sc.SubcategoryID
   inner join Category cat
      on sc.CategoryID = cat.CategoryID;
```
**7-5  FactSales for Power BI**
 - Connection: International Marketplace
```
drop view if exists v_Fact_Sales;
go
create view v_Fact_Sales as
   select
      s.OrderID,
      s.SalesID as "OrderLineID",
      s.CustomerID,
      c.CityID,
      s.ProductID,      
      shp.ShipMode,
      s.Quantity,
      s.DiscountPercentage,
      s.DiscountAmount,
      s.Sales,
      s.Profit,
      s.ProfitBin,
      s.OrderDate,
      s.ShipDate
   from Sales s
   inner join Customer c
      on s.CustomerID = c.CustomerID
   inner join City cty
      on c.CityID = cty.CityID
   inner join ShipMode shp
      on s.ShipModeID = shp.ShipModeID;
```
