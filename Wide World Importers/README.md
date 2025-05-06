Listed below are SQL scripts I created to normalise the [sample World Wide Importers database](https://github.com/Microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0), so it could be more easily used in star schema form when visualising in Power BI.
- Wrangled data source [:inbox_tray:](/Wide%20World%20Importers/Wide%20World%20Importers%20normalised%20extracts.xlsx?raw=true)
- SQL queries [:inbox_tray:](/Wide%20World%20Importers/SQL%20queries.sql)

Original data sources
- Sample World Wide Importers databases [:earth_asia:](https://github.com/Microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0)

```
use WideWorldImporters;

-- Country State City
select   c.CountryID as "Country ID",
         c.countryname as "Country",
		 c.IsoAlpha3Code as "Country Code",
		 c.continent as "Continent",
		 c.region as "Region",
		 c.subregion as "Subregion",
		 c.LatestRecordedPopulation as "Country Latest Recorded Population",
		 sp.StateProvinceID as "State ID",
		 sp.StateProvinceName as "State",
		 sp.StateProvinceCode as "State Code",
		 sp.SalesTerritory as "Sales Territory",
		 sp.LatestRecordedPopulation as "State Latest Recorded Population",
		 cy.CityID as "City ID",
		 cy.CityName as "City",
		 cy.LatestRecordedPopulation as "City Latest Recorded Population"
from     application.countries c
         left outer join Application.StateProvinces sp
		 on c.CountryID = sp.CountryID
		 left outer join Application.Cities cy
		 on sp.StateProvinceID = cy.StateProvinceID
order by c.CountryName, sp.StateProvinceName, cy.CityName;

-- Suppliers
select   s.supplierid as "Supplier ID",
         s.SupplierName as "Supplier",
		 sc.SupplierCategoryName as "Supplier Category",
		 p.FullName as "Primary Contact",
		 p.EmailAddress as "Primary Contact Email",
		 dm.DeliveryMethodName as "Delivery Method",
		 cy.CityName as "Supplier City",
		 sp.StateProvinceName as "Supplier State",
		 cnty.CountryName as "Supplier Country",
		 sp.SalesTerritory as "Supplier Territory",
		 s.BankAccountName as "Bank Account Name",
		 s.BankAccountBranch as "Bank Account Branch",
		 s.BankAccountCode as "Bank Account Code",
		 s.BankInternationalCode as "Bank International Code",
		 s.PaymentDays as "Payment Days",
		 s.PhoneNumber as "Phone",
		 s.FaxNumber as "Fax",
		 s.WebsiteURL as "Website",
		 s.DeliveryAddressLine1 as "Supplier Address 1",
		 s.DeliveryAddressLine2 as "Supplier Address 2",
		 s.DeliveryPostalCode as "Supplier Post Code"
from     Purchasing.suppliers s
         inner join Purchasing.SupplierCategories sc
		 on s.SupplierCategoryID = sc.SupplierCategoryID
		 inner join Application.People p
		 on s.PrimaryContactPersonID = p.PersonID
		 inner join Application.Cities cy
		 on s.DeliveryCityID = cy.CityID
		 inner join Application.StateProvinces sp
		 on cy.StateProvinceID = sp.StateProvinceID
		 inner join Application.Countries cnty
		 on sp.CountryID = cnty.CountryID
		 left outer join Application.DeliveryMethods dm
		 on s.DeliveryMethodID = dm.DeliveryMethodID
order by s.SupplierID asc;

-- Customer
select   c.customerid as "Customer ID",
         c.customername as "Customer",
		 bc.CustomerName as "Billing Customer",
		 cc.CustomerCategoryName as "Customer Category",
		 bg.buyinggroupname as "Buying Group",
		 p.FullName as "Primary Contact",
		 p.EmailAddress as "Primary Contact Email",
		 dm.DeliveryMethodName as "Delivery Method",
		 cy.CityName as "Customer City",
		 sp.StateProvinceName as "Customer State",
		 cnty.CountryName as "Customer Country",
		 sp.SalesTerritory as "Customer Territory",
		 c.CreditLimit as "Credit Limit",
		 c.AccountOpenedDate as "Account Open Date",
		 c.StandardDiscountPercentage as "Standard Discount %",
		 c.PhoneNumber as "Phone",
		 c.FaxNumber as "Fax",
		 c.DeliveryAddressLine1 as "Customer Address 1",
		 c.DeliveryAddressLine2 as "Customer Address 2",
		 c.DeliveryPostalCode as "Customer Post Code"		 
from     sales.customers c
		 inner join sales.Customers bc
		 on c.BillToCustomerID = bc.CustomerID
         inner join sales.CustomerCategories cc
		 on c.CustomerCategoryID = cc.CustomerCategoryID
		 inner join Application.People p
		 on c.PrimaryContactPersonID = p.PersonID
		 inner join Application.DeliveryMethods dm
		 on c.DeliveryMethodID = dm.DeliveryMethodID
		 inner join Application.Cities cy
		 on c.DeliveryCityID = cy.CityID
		 inner join Application.StateProvinces sp
		 on cy.StateProvinceID = sp.StateProvinceID
		 inner join Application.Countries cnty
		 on sp.CountryID = cnty.CountryID
		 left outer join sales.buyinggroups bg
		 on c.BuyingGroupID = bg.BuyingGroupID
order by c.customerid asc;

-- Stock Item
select   si.stockitemid as "Stock Item ID",
         si.stockitemname as "Stock Item",
		 s.SupplierID as "Supplier ID",
		 s.SupplierName as "Supplier",
		 cy.CityName as "Supplier City",
		 sp.StateProvinceName as "Supplier State",
		 cnty.CountryName as "Supplier Country",
		 sp.SalesTerritory as "Supplier Territory",
		 c.ColorName as "Colour",
		 pt1.PackageTypeName as "Unit Package Type",
		 pt2.PackageTypeName as "Outer Package Type",
		 si.Size as "Size",
		 si.LeadTimeDays as "Lead Days",
		 si.QuantityPerOuter as "Quantity per Outer Package",
		 case si.IsChillerStock
		      when 0 then 'No'
		      when 1 then 'Yes'
			  else 'N/A'
		      end as "Chilled?",
		 si.TaxRate as "Tax Rate",
		 si.UnitPrice as "Unit Price",
		 si.RecommendedRetailPrice as "RRP",
		 si.TypicalWeightPerUnit as "Weight per Unit",
		 si.SearchDetails as "Search Details",
		 sih.QuantityOnHand as "Quantity on Hand",
		 sih.BinLocation as "Bin Location",
		 sih.LastStocktakeQuantity as "Last Stocktake Quantity",
		 sih.LastCostPrice as "Last Cost Price",
		 sih.ReorderLevel as "Reorder Level",
		 sih.TargetStockLevel as "Target Stock Level"
from     Warehouse.StockItems si
         inner join Purchasing.Suppliers s
		 on si.SupplierID = s.SupplierID
		 inner join Warehouse.PackageTypes pt1
		 on si.UnitPackageID = pt1.PackageTypeID
		 inner join Warehouse.PackageTypes pt2
		 on si.OuterPackageID = pt2.PackageTypeID
		 inner join Warehouse.StockItemHoldings sih
		 on si.StockItemID = sih.StockItemID
		 inner join Application.Cities cy
		 on s.DeliveryCityID = cy.CityID
		 inner join Application.StateProvinces sp
		 on cy.StateProvinceID = sp.StateProvinceID
		 inner join Application.Countries cnty
		 on sp.CountryID = cnty.CountryID
		 left outer join Warehouse.Colors c
		 on si.ColorID = c.ColorID
order by si.StockItemID asc;

-- Stock Group
select   sg.StockGroupID as "Stock Group ID",
		 sg.StockGroupName as "Stock Group",
		 si.StockItemID as "Stock Item ID",
		 si.StockItemName as "Stock Item"
from     Warehouse.StockItemStockGroups sisg
         inner join Warehouse.StockGroups sg
		 on sisg.StockGroupID = sg.StockGroupID
		 inner join Warehouse.StockItems si
		 on sisg.StockItemID = si.StockItemID
order by si.StockItemID asc, sg.StockGroupID asc;

-- Special Deal
select   sd.SpecialDealID as "Special Deal ID",
         bg.BuyingGroupID as "Buying Group ID",
		 bg.BuyingGroupName as "Buying Group",
		 sg.StockGroupID as "Stock Group ID",
		 sg.StockGroupName as "Stock Group",
		 sd.DealDescription as "Deal Description",
		 sd.StartDate as "Start Date",
		 sd.EndDate as "End Date",
		 sd.DiscountPercentage as "Discount %"
from	 Sales.SpecialDeals sd
		 inner join Sales.BuyingGroups bg
		 on sd.BuyingGroupID = bg.BuyingGroupID
		 inner join Warehouse.StockGroups sg
		 on sd.StockGroupID = sg.StockGroupID
order by bg.BuyingGroupID asc;

-- Order
select	 o.OrderID as "Order ID",
         c.CustomerID as "Order Customer ID",
		 c.CustomerName as "Order Customer",
		 cy.CityName as "Order Customer City",
		 sp.StateProvinceName as "Order Customer State",
		 cnty.CountryName as "Order Customer Country",
		 sp.SalesTerritory as "Order Customer Territory",
		 p1.FullName as "Order Salesperson",
		 p2.FullName as "Order Picker",
		 o.BackorderOrderID as "Backorder ID",
		 o.OrderDate as "Order Date",
		 o.ExpectedDeliveryDate as "Order Expected Delivery Date",
		 o.PickingCompletedWhen as "Order Picked Date",
		 ol.OrderLineID as "OL ID",
		 ol.StockItemID as "OL Stock Item ID",
		 ol.Description as "OL Stock Item",
		 sg.StockGroupName as "OL Stock Group",
		 pt.PackageTypeName as "OL Package Type",
		 ol.Quantity as "OL Quantity",
		 ol.UnitPrice as "OL Unit Price",
		 ol.TaxRate as "OL Tax Rate",
		 ol.PickedQuantity as "OL Picked Quantity",
		 ol.PickingCompletedWhen as "OL Picked Date"
from	 Sales.Orders o
         inner join sales.Customers c
		 on o.OrderID = c.CustomerID
		 inner join Application.People p1
		 on o.SalespersonPersonID = p1.PersonID
		 inner join Sales.OrderLines ol
		 on o.OrderID = ol.OrderID
		 inner join Warehouse.PackageTypes pt
		 on ol.PackageTypeID = pt.PackageTypeID
		 inner join Application.Cities cy
		 on c.DeliveryCityID = cy.CityID
		 inner join Application.StateProvinces sp
		 on cy.StateProvinceID = sp.StateProvinceID
		 inner join Application.Countries cnty
		 on sp.CountryID = cnty.CountryID
		 inner join Warehouse.StockItemStockGroups sisg
		 on ol.StockItemID = sisg.StockItemID
		 inner join Warehouse.StockGroups sg
		 on sisg.StockGroupID = sg.StockGroupID
		 left outer join Application.People p2
		 on o.PickedByPersonID = p2.PersonID
where	 sisg.StockItemStockGroupID =
		 (select min(sisg2.StockItemStockGroupID)
		  from	 Warehouse.StockItemStockGroups sisg2
		  where  sisg.StockItemID = sisg2.StockItemID)	 
order by o.OrderID asc, ol.OrderLineID asc;

-- Sale
select   ct1.[CT ID],
		 ct1.[CT Customer ID],
		 ct1.[CT Customer],
		 ct1.[CT Customer City],
		 ct1.[CT Customer State],
		 ct1.[CT Customer Country],
         ct1.[CT Customer Territory],
		 ct1.[CT Type],
		 ct1.[CT Date],
		 ct1.[CT Amount Excluding Tax],
		 ct1.[CT Tax Amount],
		 ct1.[CT Amount],
		 ct1.[CT Outstanding Balance],
		 ct1.[CT Finalisation Date],
		 ct1.[Is CT Finalised?],
		 ct1.[CT Invoice ID],
		 i1.[Invoice Customer ID],
		 i1.[Invoice Customer],
		 i1.[Invoice Customer City],
		 i1.[Invoice Customer State],
		 i1.[Invoice Customer Country],
                 il.[Invoice Customer Territory],
		 i1.[Invoice Delivery Method],
		 i1.[Invoice Salesperson],
		 i1.[Invoice Packer],
		 i1.[Invoice Date],
		 i1.[Invoice Total Dry Items],
		 i1.[Invoice Total Chill Items],
		 i1.[Invoice Confirmed Delivery Time],
		 i1.[Invoice Confirmed Recipient],
		 i1.[Order ID],
		 il1.[IL ID],
		 il1.[IL Stock Item ID],
		 il1.[IL Stock Item],
		 il1.[IL Stock Group],
		 il1.[IL Package Type],
		 il1.[IL Quantity],
		 il1.[IL Unit Price],
		 il1.[IL Tax Rate],
		 il1.[IL Tax Amount],
		 il1.[IL Profit]
from     (select	ct.customertransactionid as "CT ID",
					c.CustomerID as "CT Customer ID", -- head offices
					c.CustomerName as "CT Customer",
					cy.CityName as "CT Customer City",
					sp.StateProvinceName as "CT Customer State",
					cnty.CountryName as "CT Customer Country",
				    sp.SalesTerritory as "CT Customer Territory",
					tt.TransactionTypeName as "CT Type",
					ct.TransactionDate as "CT Date",
					ct.AmountExcludingTax as "CT Amount Excluding Tax",
					ct.TaxAmount as "CT Tax Amount",
					ct.TransactionAmount as "CT Amount",
					ct.OutstandingBalance as "CT Outstanding Balance",
					ct.FinalizationDate as "CT Finalisation Date",
					case ct.IsFinalized
						 when 1 then 'Yes'
						 when 0 then 'No'
						 else 'N/A'
						 end as "Is CT Finalised?",
					ct.InvoiceID as "CT Invoice ID"
		  from		sales.CustomerTransactions ct
					inner join sales.customers c
					on ct.CustomerID = c.CustomerID
					inner join Application.TransactionTypes tt
					on ct.TransactionTypeID = tt.TransactionTypeID
					inner join Application.Cities cy
					on c.DeliveryCityID = cy.CityID
					inner join Application.StateProvinces sp
					on cy.StateProvinceID = sp.StateProvinceID
					inner join Application.Countries cnty
					on sp.CountryID = cnty.CountryID
		 ) as ct1
		 left outer join 
		 (select	i.invoiceid as "Invoice ID", -- duplicate
					c.CustomerID as "Invoice Customer ID", -- non-head offices i.e. transaction and invoice
					c.CustomerName as "Invoice Customer",
					cy.CityName as "Invoice Customer City",
					sp.StateProvinceName as "Invoice Customer State",
					cnty.CountryName as "Invoice Customer Country",
                    sp.SalesTerritory as "Invoice Customer Territory",
					dm.DeliveryMethodName as "Invoice Delivery Method",
					p1.FullName as "Invoice Salesperson",
					p2.FullName as "Invoice Packer",
					i.InvoiceDate as "Invoice Date",
					i.TotalDryItems as "Invoice Total Dry Items",
					i.TotalChillerItems as "Invoice Total Chill Items",
					i.ConfirmedDeliveryTime as "Invoice Confirmed Delivery Time",
					i.ConfirmedReceivedBy as "Invoice Confirmed Recipient",
					i.OrderID as "Order ID"
		  from		Sales.Invoices i
					inner join sales.Customers c
					on i.CustomerID = c.CustomerID
					inner join Application.DeliveryMethods dm
					on i.DeliveryMethodID = dm.DeliveryMethodID
					inner join Application.People p1
					on i.SalespersonPersonID = p1.PersonID
					inner join Application.People p2
					on i.PackedByPersonID = p2.PersonID
					inner join Application.Cities cy
					on c.DeliveryCityID = cy.CityID
					inner join Application.StateProvinces sp
					on cy.StateProvinceID = sp.StateProvinceID
					inner join Application.Countries cnty
					on sp.CountryID = cnty.CountryID
		 ) as i1
		 on ct1.[CT Invoice ID] = i1.[Invoice ID]
		 left outer join
		 (select	il.InvoiceID as "Invoice ID", -- duplicate
					il.InvoiceLineID as "IL ID",
					si.StockItemID as "IL Stock Item ID",
					il.Description as "IL Stock Item",
					sg.StockGroupName as "IL Stock Group",
					pt.PackageTypeName as "IL Package Type",
					il.Quantity as "IL Quantity",
					il.UnitPrice as "IL Unit Price",
					il.TaxRate as "IL Tax Rate",
					il.TaxAmount as "IL Tax Amount",
					il.LineProfit as "IL Profit"
		  from		Sales.InvoiceLines il
					inner join Warehouse.StockItems si
					on il.StockItemID = si.StockItemID
					inner join Warehouse.PackageTypes pt
					on il.PackageTypeID = pt.PackageTypeID
					inner join Warehouse.StockItemStockGroups sisg
					on il.StockItemID = sisg.StockItemID
					inner join Warehouse.StockGroups sg
					on sisg.StockGroupID = sg.StockGroupID
		   where	sisg.StockItemStockGroupID =
					(select min(sisg2.StockItemStockGroupID)
					 from	Warehouse.StockItemStockGroups sisg2
					 where  sisg.StockItemID = sisg2.StockItemID)
		 ) as il1
		 on i1.[Invoice ID] = il1.[Invoice ID]
order by ct1.[CT ID] asc, i1.[Invoice ID] asc, il1.[IL ID];

-- Purchase
select	 st1.[ST ID],
		 st1.[ST Supplier ID],
		 st1.[ST Supplier],
		 st1.[ST Supplier City],
		 st1.[ST Supplier State],
		 st1.[ST Supplier Country],
         st1.[ST Supplier Territory],
		 st1.[ST Type],
		 st1.[ST Payment Method],
		 st1.[ST Date],
		 st1.[ST Amount Excluding Tax],
		 st1.[ST Tax Amount],
		 st1.[ST Amount],
		 st1.[ST Outstanding Balance],
		 st1.[ST Finalization Date],
		 st1.[Is ST Finalised?],
		 st1.[PO ID],
		 po1.[PO Date],
		 po1.[PO Delivery Method],
		 po1.[PO Expected Delivery Date],
		 po1.[Is PO Finalised?],
		 pol1.[POL ID],
		 pol1.[POL Stock Item ID],
		 pol1.[POL Stock Item],
		 pol1.[POL Stock Group],
		 pol1.[POL Received Outers],
		 pol1.[POL Package Type],
		 pol1.[POL Expected Unit Price per Outer],
		 pol1.[POL Last Receipt Date],
		 pol1.[Is POL Finalised?]
from	 (select	st.SupplierTransactionID as "ST ID",
					s.SupplierID as "ST Supplier ID",
					s.SupplierName as "ST Supplier",
					cy.CityName as "ST Supplier City",
					sp.StateProvinceName as "ST Supplier State",
					cnty.CountryName as "ST Supplier Country",
                    sp.SalesTerritory as "ST Supplier Territory",
					tt.TransactionTypeName as "ST Type",
					pm.PaymentMethodName as "ST Payment Method",
					st.TransactionDate as "ST Date",
					st.AmountExcludingTax as "ST Amount Excluding Tax",
					st.TaxAmount as "ST Tax Amount",
					st.TransactionAmount as "ST Amount",
					st.OutstandingBalance as "ST Outstanding Balance",
					st.FinalizationDate as "ST Finalization Date",
					case st.IsFinalized
						 when 1 then 'Yes'
						 when 0 then 'No'
						 else 'N/A'
						 end as "Is ST Finalised?",
					st.PurchaseOrderID as "PO ID"
		  from		Purchasing.SupplierTransactions st
					inner join Purchasing.Suppliers s
					on st.SupplierID = s.SupplierID
					inner join Application.TransactionTypes tt
					on st.TransactionTypeID = tt.TransactionTypeID
					inner join Application.PaymentMethods pm
					on st.PaymentMethodID = pm.PaymentMethodID
					inner join Application.Cities cy
					on s.DeliveryCityID = cy.CityID
					inner join Application.StateProvinces sp
					on cy.StateProvinceID = sp.StateProvinceID
					inner join Application.Countries cnty
					on sp.CountryID = cnty.CountryID
		  ) as st1
		  left outer join 
		  (select	po.PurchaseOrderID as "PO ID", -- duplicate
					po.OrderDate as "PO Date",
					dm.DeliveryMethodName as "PO Delivery Method",
					po.ExpectedDeliveryDate as "PO Expected Delivery Date",
					case po.IsOrderFinalized
						 when 1 then 'Yes'
						 when 0 then 'No'
					     else 'N/A'
						 end as "Is PO Finalised?"
		   from		Purchasing.PurchaseOrders po
					inner join Application.DeliveryMethods dm
					on po.DeliveryMethodID = dm.DeliveryMethodID
		  ) as po1
		  on st1.[PO ID] = po1.[PO ID]
		  left outer join
		  (select	pol.PurchaseOrderID as "PO ID", -- duplicate
					pol.PurchaseOrderLineID as "POL ID",
					pol.StockItemID as "POL Stock Item ID",
					pol.Description as "POL Stock Item",
					sg.StockGroupName as "POL Stock Group",
					pol.ReceivedOuters as "POL Received Outers",
					pt.PackageTypeName as "POL Package Type",
					pol.ExpectedUnitPricePerOuter as "POL Expected Unit Price per Outer",
					pol.LastReceiptDate as "POL Last Receipt Date",
					case pol.IsOrderLineFinalized
						 when 1 then 'Yes'
						 when 0 then 'No'
						 else 'N/A'
						 end as "Is POL Finalised?"
		   from		Purchasing.PurchaseOrderLines pol
					inner join Warehouse.PackageTypes pt
					on pol.PackageTypeID = pt.PackageTypeID
					inner join Warehouse.StockItemStockGroups sisg
					on pol.StockItemID = sisg.StockItemID
					inner join Warehouse.StockGroups sg
					on sisg.StockGroupID = sg.StockGroupID
		   where	sisg.StockItemStockGroupID =
					(select min(sisg2.StockItemStockGroupID)
					 from	Warehouse.StockItemStockGroups sisg2
					 where  sisg.StockItemID = sisg2.StockItemID)
		  ) as pol1
		  on po1.[PO ID] = pol1.[PO ID]
order by  st1.[ST ID] asc, po1.[PO ID] asc, pol1.[POL ID] asc;
```