SELECT * FROM northwind.products
ORDER BY UnitPrice;

SELECT * FROM northwind.customers
WHERE Country = "UK" OR Country = "Spain";

SELECT * FROM northwind.products
WHERE UnitsInStock > 100 AND UnitPrice >= 25;

SELECT distinct ShipCountry FROM northwind.orders
ORDER BY ShipCountry;

select * from northwind.orders
where OrderDate >= "1996-10-1" AND OrderDate < "1996-11-1"