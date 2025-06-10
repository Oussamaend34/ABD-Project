USE demo;

-- Sales regions (you can join with sales.region_id)
CREATE TABLE regions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50)
);

INSERT INTO regions (name) VALUES
  ('North'),
  ('South'),
  ('East'),
  ('West');

-- Salespeople (who make sales)
CREATE TABLE salespeople (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  region_id INT,
  FOREIGN KEY (region_id) REFERENCES regions(id)
);

INSERT INTO salespeople (name, region_id) VALUES
  ('Alice', 1),
  ('Bob', 2),
  ('Charlie', 3),
  ('Diana', 4);

-- Sales table (with foreign keys to salesperson and region)
CREATE TABLE sales (
  id INT AUTO_INCREMENT PRIMARY KEY,
  salesperson_id INT,
  region_id INT,
  sales_amount FLOAT,
  sale_date DATE,
  FOREIGN KEY (salesperson_id) REFERENCES salespeople(id),
  FOREIGN KEY (region_id) REFERENCES regions(id)
);

INSERT INTO sales (salesperson_id, region_id, sales_amount, sale_date) VALUES
  (1, 1, 1200, '2025-01-10'),
  (2, 2, 900, '2025-01-11'),
  (3, 3, 1400, '2025-01-12'),
  (4, 4, 1100, '2025-01-13'),
  (1, 1, 1500, '2025-02-10'),
  (2, 2, 700, '2025-02-11');

-- Products
CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  price FLOAT
);

INSERT INTO products (name, price) VALUES
  ('Product A', 50),
  ('Product B', 75),
  ('Product C', 100);

-- Sales items (line items in a sale, joining sales and products)
CREATE TABLE sales_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sale_id INT,
  product_id INT,
  quantity INT,
  FOREIGN KEY (sale_id) REFERENCES sales(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO sales_items (sale_id, product_id, quantity) VALUES
  (1, 1, 10),
  (1, 2, 5),
  (2, 1, 7),
  (3, 3, 3),
  (4, 2, 2),
  (5, 1, 20),
  (6, 3, 1);
