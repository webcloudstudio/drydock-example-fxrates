CREATE TABLE IF NOT EXISTS rates (
    date TEXT NOT NULL,
    currency TEXT NOT NULL,
    rate TEXT NOT NULL,
    PRIMARY KEY (date, currency)
);
