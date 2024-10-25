-- 2
SELECT * FROM northwind.products
ORDER BY UnitPrice;
-- 3
SELECT * FROM northwind.customers
WHERE Country = "UK" OR Country = "Spain";
-- 4
SELECT * FROM northwind.products
WHERE UnitsInStock > 100 AND UnitPrice >= 25;
-- 5
SELECT distinct ShipCountry FROM northwind.orders
ORDER BY ShipCountry DESC;
-- 6
select * from northwind.orders
where OrderDate >= "1996-10-1" AND OrderDate < "1996-11-1";
-- 7
select * from northwind.orders
where ShipCountry = "Germany"
and ShipRegion is null
and Freight >= 100
and EmployeeID = 1
and OrderDate >= "1996-01-01" and OrderDate < "1997-01-01";
-- 8
select * from northwind.orders
where ShippedDate > RequiredDate;
-- 9
select * from northwind.orders
where ShipCountry = "Canada"
and OrderDate >= "1997-01-01" and OrderDate < "1997-05-01";
-- 10
select * from northwind.orders
where EmployeeID in (2,5,8)
and ShipRegion is not null
and ShipVia in (1,3)
order by EmployeeID, ShipVia ASC;
-- 11
select * from northwind.employees
where Region is null 
-- or reportsTo is null -- There is no "reportsTO"?
and BirthDate < "1961-01-01";