-- Auto Spare Parts Marketplace - PostgreSQL Schema
-- Run this file to initialize the database

CREATE DATABASE IF NOT EXISTS autoparts;

\c autoparts;

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    image_url VARCHAR(500),
    description TEXT,
    compatibility TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    customer_name VARCHAR(255) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending'
);

-- Seed sample products
INSERT INTO products (name, category, brand, price, stock, image_url, description, compatibility) VALUES
('High Performance Brake Pads', 'Brake', 'Brembo', 2850.00, 45, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400', 'Premium ceramic brake pads with excellent heat dissipation and low dust output. Designed for high-performance driving conditions.', 'Toyota Corolla 2015-2022, Honda Civic 2016-2023'),
('Engine Air Filter', 'Engine', 'K&N', 1200.00, 120, 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400', 'High-flow cotton gauze air filter. Washable and reusable, providing improved airflow and engine performance.', 'Universal fit - check model compatibility'),
('Shock Absorber Front', 'Suspension', 'Monroe', 4500.00, 30, 'https://images.unsplash.com/photo-1517524285303-d6fc683dddf8?w=400', 'OEM-quality shock absorber providing smooth ride and precise handling. Heavy duty construction for long service life.', 'Toyota Hilux 2010-2020, Ford Ranger 2012-2021'),
('Alternator 12V 90A', 'Electrical', 'Bosch', 8900.00, 18, 'https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=400', 'Genuine Bosch alternator ensuring reliable electrical system performance. Includes voltage regulator and brush set.', 'Honda CR-V 2012-2018, Toyota RAV4 2013-2019'),
('Timing Belt Kit', 'Engine', 'Gates', 3200.00, 55, 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400', 'Complete timing belt kit with tensioner and idler pulleys. OEM specification for precise timing and reliability.', 'Mitsubishi Lancer 2008-2017, Proton Inspira 2010-2015'),
('Radiator Coolant Fan', 'Engine', 'Denso', 5600.00, 22, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400', 'Electric cooling fan assembly with motor and blade. Maintains optimal engine temperature in all conditions.', 'Nissan X-Trail 2007-2014, Nissan Qashqai 2007-2013'),
('Disc Brake Rotor', 'Brake', 'Brembo', 3800.00, 40, 'https://images.unsplash.com/photo-1517524285303-d6fc683dddf8?w=400', 'Slotted and cross-drilled disc rotor for superior braking performance and heat dissipation. Reduces brake fade under heavy use.', 'BMW 3 Series 2012-2018, BMW 5 Series 2010-2016'),
('Spark Plug Set (4pcs)', 'Engine', 'NGK', 950.00, 200, 'https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=400', 'Iridium tipped spark plugs for improved fuel efficiency and smoother idle. Pack of 4 plugs.', 'Universal - 4 cylinder engines'),
('Power Steering Pump', 'Suspension', 'ZF', 7200.00, 15, 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400', 'Hydraulic power steering pump with reservoir. Ensures smooth and effortless steering response.', 'Toyota Camry 2006-2011, Toyota Aurion 2006-2012'),
('LED Headlight Bulbs H4', 'Electrical', 'Philips', 2100.00, 80, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400', 'Ultra-bright LED conversion kit for H4 headlights. 6000K white light, plug-and-play installation.', 'Universal H4 fitment - verify with vehicle manual'),
('CV Joint Boot Kit', 'Suspension', 'GSP', 1450.00, 65, 'https://images.unsplash.com/photo-1517524285303-d6fc683dddf8?w=400', 'Complete CV boot kit with grease and clamps. Prevents CV joint damage from contamination.', 'Most front-wheel drive vehicles - check fitment'),
('Battery 60Ah MF', 'Electrical', 'Varta', 12500.00, 25, 'https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=400', 'Maintenance-free AGM battery with superior cold cranking amps. 3-year warranty included.', 'Universal - 60Ah standard fit');
