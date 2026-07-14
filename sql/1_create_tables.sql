-- ============================================================================
-- 1_create_tables.sql
-- ============================================================================
-- Creates the table that holds the cleaned car fuel economy data.
--
-- A table is like a sheet in a spreadsheet: named columns, and one row per
-- record (here, one row per car model and configuration). Describing each
-- column's type lets the database check the data and lets us query it with SQL.
--
-- We drop the table first if it exists, so this script can be run again cleanly.
-- ============================================================================

DROP TABLE IF EXISTS cars;

CREATE TABLE cars (
    manufacturer       TEXT,      -- the car maker, for example audi
    model              TEXT,      -- the model name, for example a4
    year               INTEGER,   -- model year (1999 or 2008)
    class              TEXT,      -- vehicle class, for example compact or suv
    displ              REAL,      -- engine size in litres
    cyl                INTEGER,   -- number of cylinders
    transmission_type  TEXT,      -- auto or manual
    gears              INTEGER,   -- number of gears (blank for variable gearboxes)
    drive              TEXT,      -- Front-wheel, Rear-wheel or Four-wheel
    fuel               TEXT,      -- Premium, Regular, Diesel and so on
    cty                INTEGER,   -- city fuel economy, miles per gallon
    hwy                INTEGER,   -- highway fuel economy, miles per gallon
    avg_mpg            REAL       -- average of city and highway, our headline figure
);

-- Indexes help the database group and filter faster. On a small table the
-- speed gain is tiny, but including them shows the idea and is a good habit.
CREATE INDEX idx_cars_class  ON cars (class);
CREATE INDEX idx_cars_cyl    ON cars (cyl);
CREATE INDEX idx_cars_year   ON cars (year);
