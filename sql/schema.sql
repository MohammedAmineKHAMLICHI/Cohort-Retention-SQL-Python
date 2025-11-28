
-- Minimal schema used by the cohort retention project
CREATE TABLE users (
  user_id INT PRIMARY KEY,
  signup_date DATE
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  order_date DATE,
  amount NUMERIC(10,2)
);
