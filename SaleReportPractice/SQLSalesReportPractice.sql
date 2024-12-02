SELECT * FROM PortfolioProject..IntSalesRep



-- Just by looking at our data, I see our date format changes from DATE column and Months column, I want to make it universally the same so we can order by one date

--ALTER TABLE PortfolioProject..IntSalesRep
--ADD UnifiedDate VARCHAR(20);

UPDATE PortfolioProject..IntSalesRep 
    SET UnifiedDate = ISNULL(CONVERT(VARCHAR, DATE, 101), Months);



SELECT * 
FROM PortfolioProject..IntSalesRep
ORDER BY TRY_CONVERT(DATE, UnifiedDate, 101);


SELECT 
    CONVERT(VARCHAR, TRY_CONVERT(DATE, UnifiedDate, 101), 101) AS StandardizedDate
FROM 
    PortfolioProject..IntSalesRep


SELECT *
FROM PortfolioProject..IntSalesRep
WHERE ISDATE(UnifiedDate) = 0;

UPDATE PortfolioProject..IntSalesRep
SET UnifiedDate = 
    CONVERT(VARCHAR, 
            COALESCE(TRY_CONVERT(DATE, DATE, 101),
                     TRY_CONVERT(DATE, Months, 101),
                     TRY_CONVERT(DATE, Months, 110)), 
            101)
WHERE ISDATE(UnifiedDate) = 0 OR UnifiedDate IS NULL;

UPDATE PortfolioProject..IntSalesRep
SET UnifiedDate = NULL
WHERE ISDATE(UnifiedDate) = 0;

DELETE FROM PortfolioProject..IntSalesRep
WHERE UnifiedDate IS NULL;


-- Here, we can now see that UnifiedDate gets our dates from the two columns and excludes all nulls, now I will delete the two columns as they are not necessary
SELECT * FROM PortfolioProject..IntSalesRep
ORDER BY UnifiedDate

-- If I wanted to access these later, I can backup to another table using SELECT INTO 
ALTER TABLE PortfolioProject..IntSalesRep
DROP COLUMN DATE, Months;

-- I also want to drop all rows where PCS is null, as we cannot make the assumption someone ordered no pieces of an item 

DELETE FROM PortfolioProject..IntSalesRep
WHERE PCS IS NULL;

-- PCS is in time format, we need it to be in decimals, then drop the old column
ALTER TABLE PortfolioProject..IntSalesRep
ADD PCS_Int INT;
UPDATE PortfolioProject..IntSalesRep
SET PCS_Int = DATEPART(HOUR, PCS);


ALTER TABLE PortfolioProject..IntSalesRep
DROP COLUMN PCS;

