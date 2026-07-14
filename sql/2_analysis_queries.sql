-- ============================================================================
-- 2_analysis_queries.sql
-- ============================================================================
-- Questions we ask the data, written as SQL queries, ordered from simplest to
-- most advanced. Each has a plain-English comment explaining what it answers
-- and how it works.
--
-- The overall question the project answers is: what makes a car fuel efficient?
--
-- Key SQL ideas used here:
--   SELECT / FROM        choose columns and the table
--   WHERE                keep only rows matching a condition
--   GROUP BY             collapse rows into one per category
--   COUNT / AVG / MAX    do maths across a group
--   ROUND                tidy up decimals
--   ORDER BY / LIMIT     sort and trim the results
-- ============================================================================


-- ----------------------------------------------------------------------------
-- Query 1: The 10 most fuel efficient cars.
-- A simple sort on our headline figure, then keep the top 10.
-- ----------------------------------------------------------------------------
SELECT manufacturer, model, year, class, cty, hwy, avg_mpg
FROM cars
ORDER BY avg_mpg DESC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- Query 2: The 10 least fuel efficient cars.
-- The same idea, sorted the other way.
-- ----------------------------------------------------------------------------
SELECT manufacturer, model, year, class, cty, hwy, avg_mpg
FROM cars
ORDER BY avg_mpg ASC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- Query 3: Average efficiency by vehicle class.
-- Groups every car by its class, then averages the economy in each group.
-- This shows the obvious but important point that small cars beat large ones.
-- ----------------------------------------------------------------------------
SELECT class,
       COUNT(*)              AS number_of_cars,
       ROUND(AVG(avg_mpg), 1) AS average_mpg
FROM cars
GROUP BY class
ORDER BY average_mpg DESC;


-- ----------------------------------------------------------------------------
-- Query 4: Average efficiency by number of cylinders.
-- Engine size and cylinder count are the usual suspects for fuel use. This is
-- the clearest single relationship in the data.
-- ----------------------------------------------------------------------------
SELECT cyl AS cylinders,
       COUNT(*)              AS number_of_cars,
       ROUND(AVG(avg_mpg), 1) AS average_mpg
FROM cars
GROUP BY cyl
ORDER BY cylinders;


-- ----------------------------------------------------------------------------
-- Query 5: Does drivetrain matter?
-- Compares front, rear and four wheel drive.
-- ----------------------------------------------------------------------------
SELECT drive,
       COUNT(*)              AS number_of_cars,
       ROUND(AVG(avg_mpg), 1) AS average_mpg
FROM cars
GROUP BY drive
ORDER BY average_mpg DESC;


-- ----------------------------------------------------------------------------
-- Query 6: Automatic versus manual.
-- A common question. We compare the average economy of the two gearbox types.
-- ----------------------------------------------------------------------------
SELECT transmission_type,
       COUNT(*)              AS number_of_cars,
       ROUND(AVG(avg_mpg), 1) AS average_mpg
FROM cars
GROUP BY transmission_type
ORDER BY average_mpg DESC;


-- ----------------------------------------------------------------------------
-- Query 7: Did fuel economy improve from 1999 to 2008?
-- Averages economy for each of the two model years in the data.
-- ----------------------------------------------------------------------------
SELECT year,
       COUNT(*)              AS number_of_cars,
       ROUND(AVG(cty), 1)     AS average_city_mpg,
       ROUND(AVG(hwy), 1)     AS average_highway_mpg,
       ROUND(AVG(avg_mpg), 1) AS average_mpg
FROM cars
GROUP BY year
ORDER BY year;


-- ----------------------------------------------------------------------------
-- Query 8: Which manufacturers make the most efficient cars on average?
-- HAVING is like WHERE but for groups: here we only keep manufacturers with at
-- least five cars in the data, so the averages are not based on one or two models.
-- ----------------------------------------------------------------------------
SELECT manufacturer,
       COUNT(*)              AS number_of_cars,
       ROUND(AVG(avg_mpg), 1) AS average_mpg
FROM cars
GROUP BY manufacturer
HAVING COUNT(*) >= 5
ORDER BY average_mpg DESC;


-- ----------------------------------------------------------------------------
-- Query 9: Sort cars into simple efficiency bands using CASE.
-- CASE works like an "if / else": it labels each car by its average economy,
-- and then we count how many cars fall into each band.
-- ----------------------------------------------------------------------------
SELECT
    CASE
        WHEN avg_mpg >= 30 THEN 'Efficient (30+ mpg)'
        WHEN avg_mpg >= 20 THEN 'Average (20 to 29 mpg)'
        ELSE                    'Thirsty (under 20 mpg)'
    END AS efficiency_band,
    COUNT(*) AS number_of_cars
FROM cars
GROUP BY efficiency_band
ORDER BY number_of_cars DESC;


-- ----------------------------------------------------------------------------
-- Query 10 (the most advanced one): the most efficient car in each class.
-- This uses a window function. RANK() numbers the cars inside each class from
-- most efficient (1) downwards, without collapsing the rows the way GROUP BY
-- would. The outer query then keeps only the number 1 in each class.
--
-- Read it inside out: the inner query tags every car with its rank within its
-- class, and the outer query keeps the top ranked car per class.
-- This is the one query worth practising until you can explain it out loud.
-- ----------------------------------------------------------------------------
SELECT class, manufacturer, model, year, avg_mpg
FROM (
    SELECT class,
           manufacturer,
           model,
           year,
           avg_mpg,
           RANK() OVER (PARTITION BY class ORDER BY avg_mpg DESC) AS rank_in_class
    FROM cars
)
WHERE rank_in_class = 1
ORDER BY avg_mpg DESC;
