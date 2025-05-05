#<!-- Aadarsh Bhagat, Student Id: 453974-->
import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Psychology123'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            print("Event Scheduler enabled successfully.")

            # Drop database if exists and create new
            cursor.execute("DROP DATABASE IF EXISTS nepal_hotels")
            cursor.execute("CREATE DATABASE nepal_hotels")
            cursor.execute("USE nepal_hotels")

            # Create tables
            tables = [
                """
                CREATE TABLE cities (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    capacity INT,
                    peak_rate DECIMAL(10,2),
                    off_peak_rate DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE peak_seasons (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100),
                    start_date DATE,
                    end_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(100) UNIQUE,
                    password VARCHAR(255),
                    phone VARCHAR(20),
                    profile_image VARCHAR(255) DEFAULT 'default-profile.jpg',
                    role ENUM('user', 'admin') DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE hotels (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    city_id INT,
                    name VARCHAR(100) NOT NULL,
                    tagline VARCHAR(200),
                    hero_image VARCHAR(255),
                    about_image VARCHAR(255),
                    distance_to_center VARCHAR(50),
                    description TEXT,
                    location VARCHAR(100),
                    rating INT,
                    reviews INT,
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    address TEXT,
                    years_operation INT,
                    map_embed TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    status ENUM('active', 'archived') DEFAULT 'active',
                    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE SET NULL
                )
                """,
                """
                CREATE TABLE room_types (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    hotel_id INT,
                    name VARCHAR(100),
                    category ENUM('Standard', 'Double', 'Family') NOT NULL,
                    size VARCHAR(20),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE room_capacities (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    room_type_id INT,
                    min_guests INT,
                    max_guests INT,
                    extra_guest_charge DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE bookings (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    booking_reference VARCHAR(50) UNIQUE NOT NULL,
                    user_id INT NOT NULL,
                    hotel_id INT NOT NULL,
                    room_type_id INT NOT NULL,
                    check_in DATE NOT NULL,
                    check_out DATE NOT NULL,
                    num_guests INT NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL,
                    special_requests TEXT,
                    status ENUM('pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled', 'completed') DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (hotel_id) REFERENCES hotels(id),
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id)
                )
                """,
                """
                CREATE TABLE booking_guests (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    booking_id INT NOT NULL,
                    guest_order INT NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    is_primary BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE payments (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    booking_id INT NOT NULL,
                    payment_reference VARCHAR(50) UNIQUE NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    payment_method ENUM('credit_card', 'debit_card', 'paypal') DEFAULT 'credit_card',
                    payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
                    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE hotel_highlights (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    hotel_id INT,
                    highlight TEXT,
                    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
                )
                """,
                """
                ALTER TABLE users
                ADD COLUMN email_verified BOOLEAN DEFAULT FALSE,
                ADD COLUMN email_verified_at TIMESTAMP NULL
                """,
                """
                ALTER TABLE users
                ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                """,
                """
                CREATE TABLE email_verifications (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    verification_code VARCHAR(6) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE password_resets (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    reset_code VARCHAR(6) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    used BOOLEAN DEFAULT FALSE,
                    used_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_active_reset (user_id, used)
                )
                """,
                """
                CREATE TABLE room_images (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    room_type_id INT,
                    image_url VARCHAR(255),
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE room_amenities (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    room_type_id INT,
                    amenity VARCHAR(100),
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE hotel_amenities (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    hotel_id INT,
                    name VARCHAR(100),
                    description TEXT,
                    icon VARCHAR(50),
                    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE testimonials (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    hotel_id INT,
                    name VARCHAR(100),
                    avatar VARCHAR(255),
                    rating INT,
                    comment TEXT,
                    date VARCHAR(50),
                    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE special_offers (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    discount VARCHAR(50),
                    image VARCHAR(255),
                    link VARCHAR(255),
                    badge_color VARCHAR(50),
                    hover_color VARCHAR(50),
                    hover_bg VARCHAR(50),
                    booking_window VARCHAR(50),
                    cancellation_policy TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                ALTER TABLE special_offers
                ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                """,
                """
                CREATE TABLE offer_tags (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    offer_id INT,
                    tag VARCHAR(50),
                    FOREIGN KEY (offer_id) REFERENCES special_offers(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE offer_features (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    offer_id INT,
                    feature TEXT,
                    FOREIGN KEY (offer_id) REFERENCES special_offers(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE booking_constraints (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    min_days INT DEFAULT 1,
                    max_days INT DEFAULT 30,
                    max_advance_days INT DEFAULT 90,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE advance_booking_discounts (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    min_days INT,
                    max_days INT,
                    discount_percentage DECIMAL(5,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE user_roles (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name ENUM('admin', 'user') NOT NULL,
                    permissions JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE room_availability (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    room_type_id INT,
                    date DATE,
                    is_available BOOLEAN DEFAULT true,
                    status ENUM('available', 'booked', 'maintenance', 'blocked') DEFAULT 'available',
                    price_override DECIMAL(10,2),
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id),
                    UNIQUE KEY unique_room_date (room_type_id, date)
                )
                """,
                """
                CREATE TABLE report_types (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100),
                    description TEXT,
                    query_template TEXT,
                    parameters JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE generated_reports (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    report_type VARCHAR(50) NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    generated_by INT NOT NULL,
                    format VARCHAR(10) NOT NULL,
                    file_path VARCHAR(255) NOT NULL,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (generated_by) REFERENCES users(id)
                )
                """,
                """
                CREATE TABLE hotel_config (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    check_in_time TIME DEFAULT '14:00:00',
                    check_out_time TIME DEFAULT '11:00:00',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                INSERT INTO hotel_config (check_in_time, check_out_time)
                VALUES ('14:00:00', '11:00:00')
                """,
                """
                CREATE TABLE currencies (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    code VARCHAR(3) UNIQUE,
                    name VARCHAR(50),
                    symbol VARCHAR(5),
                    exchange_rate DECIMAL(10,4),
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE audit_logs (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT,
                    action VARCHAR(100),
                    entity_type VARCHAR(50),
                    entity_id INT,
                    old_values JSON,
                    new_values JSON,
                    ip_address VARCHAR(45),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """,
                """
                CREATE TABLE room_inventory (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    hotel_id INT,
                    room_type_id INT,
                    total_rooms INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE FUNCTION calculate_room_price(base_price DECIMAL(10,2), room_type VARCHAR(20), guest_count INT)
                RETURNS DECIMAL(10,2)
                DETERMINISTIC
                BEGIN
                    DECLARE final_price DECIMAL(10,2);
                    CASE room_type
                        WHEN 'Standard' THEN SET final_price = base_price;
                        WHEN 'Double' THEN SET final_price = base_price * 1.2;
                        WHEN 'Family' THEN SET final_price = base_price * 1.5;
                    END CASE;
                    IF room_type = 'Double' AND guest_count = 2 THEN
                        SET final_price = final_price + (base_price * 0.1);
                    END IF;
                    RETURN final_price;
                END
                """,
                """
                CREATE FUNCTION is_peak_season(check_date DATE)
                RETURNS BOOLEAN
                DETERMINISTIC
                BEGIN
                    DECLARE month_num INT;
                    SET month_num = MONTH(check_date);
                    RETURN (
                        month_num BETWEEN 3 AND 5 OR
                        month_num BETWEEN 9 AND 11
                    );
                END
                """,
                """
                CREATE VIEW room_prices AS
                SELECT
                    r.id as room_type_id,
                    r.hotel_id,
                    r.name as room_name,
                    r.category as room_type,
                    c.peak_rate,
                    c.off_peak_rate,
                    calculate_room_price(c.peak_rate, r.category, 1) as peak_price,
                    calculate_room_price(c.off_peak_rate, r.category, 1) as off_peak_price,
                    calculate_room_price(c.peak_rate, r.category, 2) as peak_price_two_guests,
                    calculate_room_price(c.off_peak_rate, r.category, 2) as off_peak_price_two_guests
                FROM room_types r
                JOIN hotels h ON r.hotel_id = h.id
                JOIN cities c ON h.city_id = c.id
                """,
                """
                CREATE TABLE daily_room_availability (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    room_type_id INT,
                    date DATE,
                    total_rooms INT,
                    available_rooms INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id),
                    UNIQUE KEY unique_room_date (room_type_id, date)
                )
                """,
                """
                CREATE TABLE rooms (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    room_type_id INT,
                    room_number VARCHAR(10) UNIQUE,
                    floor INT,
                    wing VARCHAR(1),
                    status ENUM('active', 'maintenance', 'inactive') DEFAULT 'active',
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id)
                )
                """,
                """
                ALTER TABLE room_inventory
                ADD COLUMN available_rooms INT AFTER total_rooms
                """,
                """
                CREATE TABLE room_bookings (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    booking_id INT,
                    room_id INT,
                    check_in DATE,
                    check_out DATE,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id),
                    FOREIGN KEY (room_id) REFERENCES rooms(id)
                )
                """,
                """
                ALTER TABLE room_bookings
                ADD COLUMN assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ADD COLUMN assigned_by INT,
                ADD FOREIGN KEY (assigned_by) REFERENCES users(id)
                """,
                """
                CREATE TABLE cancellation_charges (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    booking_id INT NOT NULL,
                    charge_amount DECIMAL(10,2) NOT NULL,
                    charge_percentage INT NOT NULL,
                    reason TEXT,
                    refund_amount DECIMAL(10,2),
                    refund_status ENUM('pending', 'processed', 'completed') DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed_at TIMESTAMP NULL,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id)
                )
                """,
                """
                CREATE TABLE cancellation_policies (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    min_days INT NOT NULL,
                    max_days INT NOT NULL,
                    charge_percentage INT NOT NULL,
                    description TEXT,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE refunds (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    booking_id INT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    payment_reference VARCHAR(50),
                    payment_method VARCHAR(20),
                    status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed_at TIMESTAMP NULL,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id)
                )
                """,
                """
                CREATE TABLE room_pricing (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    room_type_id INT,
                    season_id INT,
                    base_price DECIMAL(10,2),
                    capacity_percentage DECIMAL(5,2),
                    rate_multiplier DECIMAL(5,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE,
                    FOREIGN KEY (season_id) REFERENCES peak_seasons(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE confirmation_views (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    booking_reference VARCHAR(50) NOT NULL,
                    user_id INT NOT NULL,
                    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    UNIQUE KEY unique_booking_view (booking_reference, user_id)
                )
                """,
                """
                CREATE TABLE booking_status_history (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    booking_id INT NOT NULL,
                    status ENUM('pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled', 'completed') NOT NULL,
                    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    changed_by INT,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
                    FOREIGN KEY (changed_by) REFERENCES users(id)
                )
                """
            ]

            # Execute table creation
            for table in tables:
                cursor.execute(table)

            # Insert initial data
            initial_data = [
                # Insert Nepali cities
                """
                INSERT INTO cities (name, capacity, peak_rate, off_peak_rate) VALUES
                ('Kathmandu', 120, 100.00, 50.00),
                ('Pokhara', 100, 90.00, 45.00),
                ('Chitwan', 80, 80.00, 40.00),
                ('Lumbini', 70, 70.00, 35.00),
                ('Bhaktapur', 60, 75.00, 37.50),
                ('Biratnagar', 50, 65.00, 32.50),
                ('Janakpur', 50, 60.00, 30.00),
                ('Nagarkot', 40, 85.00, 42.50)
                """,
                # Insert hotels
                """
                INSERT INTO hotels (city_id, name, tagline, hero_image, about_image, distance_to_center, description, location, rating, reviews, phone, email, address, years_operation, map_embed, status) VALUES
                (1, 'Hotel Shankar', 'Heritage and Comfort', 'shankar_hero.jpg', 'shankar_about.jpg', '2 km', 'A historic hotel in a converted Rana Palace, offering luxury and tradition.', 'Lazimpat, Kathmandu', 4, 1200, '+977-1-4410151', 'info@shankarhotel.com', 'Lazimpat, Kathmandu, Nepal', 60, '<iframe src="https://maps.google.com/maps?q=Hotel+Shankar+Kathmandu&t=&z=13&ie=UTF8&iwloc=&output=embed"></iframe>', 'active'),
                (1, 'Hyatt Regency Kathmandu', 'Luxury in the Capital', 'hyatt_hero.jpg', 'hyatt_about.jpg', '5 km', 'A luxurious hotel with modern amenities and proximity to cultural sites.', 'Boudha, Kathmandu', 5, 2500, '+977-1-4491234', 'kathmandu.regency@hyatt.com', 'Taragaon, Boudha, Kathmandu, Nepal', 20, '<iframe src="https://maps.google.com/maps?q=Hyatt+Regency+Kathmandu&t=&z=13&ie=UTF8&iwloc=&output=embed"></iframe>', 'active'),
                (2, 'Hotel Middle Path & Spa', 'Serenity by Phewa Lake', 'middlepath_hero.jpg', 'middlepath_about.jpg', '1 km', 'A cozy hotel with stunning lake views and excellent service.', 'Lakeside, Pokhara', 4, 800, '+977-61-465678', 'info@middlepath.com', 'Lakeside, Pokhara, Nepal', 15, '<iframe src="https://maps.google.com/maps?q=Hotel+Middle+Path+Pokhara&t=&z=13&ie=UTF8&iwloc=&output=embed"></iframe>', 'active'),
                (2, 'Pokhara Grande', 'Grandeur in the Himalayas', 'grande_hero.jpg', 'grande_about.jpg', '3 km', 'A premium hotel with modern facilities and mountain views.', 'Birauta, Pokhara', 4, 1500, '+977-61-460210', 'reservations@pokharagrande.com', 'Birauta, Pokhara, Nepal', 18, '<iframe src="https://maps.google.com/maps?q=Pokhara+Grande&t=&z=13&ie=UTF8&iwloc=&output=embed"></iframe>', 'active'),
                (3, 'Green Park Chitwan', 'Jungle Retreat', 'greenpark_hero.jpg', 'greenpark_about.jpg', '10 km', 'An eco-friendly resort near Chitwan National Park.', 'Sauraha, Chitwan', 4, 600, '+977-56-580123', 'info@greenparkchitwan.com', 'Sauraha, Chitwan, Nepal', 12, '<iframe src="https://maps.google.com/maps?q=Green+Park+Chitwan&t=&z=13&ie=UTF8&iwloc=&output=embed"></iframe>', 'active')
                """,
                # Insert room types for each hotel
                """
                INSERT INTO room_types (hotel_id, name, category, size, description)
                SELECT
                    h.id,
                    CASE
                        WHEN types.category = 'Standard' THEN CONCAT(h.name, ' Standard Room')
                        WHEN types.category = 'Double' THEN CONCAT(h.name, ' Double Room')
                        ELSE CONCAT(h.name, ' Family Suite')
                    END,
                    types.category,
                    CASE
                        WHEN types.category = 'Standard' THEN '20 m²'
                        WHEN types.category = 'Double' THEN '30 m²'
                        ELSE '45 m²'
                    END,
                    CASE
                        WHEN types.category = 'Standard' THEN 'Comfortable room with essential amenities'
                        WHEN types.category = 'Double' THEN 'Spacious room with added comfort'
                        ELSE 'Luxurious suite ideal for families'
                    END
                FROM hotels h
                CROSS JOIN (
                    SELECT 'Standard' as category
                    UNION SELECT 'Double'
                    UNION SELECT 'Family'
                ) types
                """,
                # Insert room capacities
                """
                INSERT INTO room_capacities (room_type_id, min_guests, max_guests, extra_guest_charge)
                SELECT
                    id,
                    CASE category
                        WHEN 'Standard' THEN 1
                        WHEN 'Double' THEN 2
                        ELSE 3
                    END,
                    CASE category
                        WHEN 'Standard' THEN 2
                        WHEN 'Double' THEN 4
                        ELSE 6
                    END,
                    10.00
                FROM room_types
                """,
                # Insert users
                """
                INSERT INTO users (first_name, last_name, email, password, phone, role, email_verified) VALUES
                ('Admin', 'User', 'admin@worldhotels.com', 'hashed_password_123', '+977-9841000001', 'admin', TRUE),
                ('Sita', 'Rai', 'sita.rai@gmail.com', 'hashed_password_456', '+977-9841000002', 'user', TRUE),
                ('Ram', 'Shrestha', 'ram.shrestha@gmail.com', 'hashed_password_789', '+977-9841000003', 'user', FALSE)
                """,
                # Insert bookings
                """
                INSERT INTO bookings (booking_reference, user_id, hotel_id, room_type_id, check_in, check_out, num_guests, total_amount, special_requests, status) VALUES
                ('BOOK001', 2, 1, 1, '2025-06-01', '2025-06-05', 2, 200.00, 'Extra pillows', 'confirmed'),
                ('BOOK002', 3, 3, 7, '2025-07-10', '2025-07-12', 3, 180.00, 'Vegetarian meals', 'pending')
                """,
                # Insert booking guests
                """
                INSERT INTO booking_guests (booking_id, guest_order, first_name, last_name, email, phone, is_primary) VALUES
                (1, 1, 'Sita', 'Rai', 'sita.rai@gmail.com', '+977-9841000002', TRUE),
                (1, 2, 'Hari', 'Rai', 'hari.rai@gmail.com', '+977-9841000004', FALSE),
                (2, 1, 'Ram', 'Shrestha', 'ram.shrestha@gmail.com', '+977-9841000003', TRUE)
                """,
                # Insert payments
                """
                INSERT INTO payments (booking_id, payment_reference, amount, payment_method, payment_status) VALUES
                (1, 'PAY001', 200.00, 'credit_card', 'completed'),
                (2, 'PAY002', 180.00, 'paypal', 'pending')
                """,
                # Insert hotel highlights
                """
                INSERT INTO hotel_highlights (hotel_id, highlight) VALUES
                (1, 'Historic Rana Palace architecture'),
                (1, 'Rooftop dining with city views'),
                (2, 'Close to Boudhanath Stupa'),
                (3, 'Lakeside location with mountain views'),
                (4, 'Spa and wellness facilities')
                """,
                # Insert room images
                """
                INSERT INTO room_images (room_type_id, image_url)
                SELECT id, CONCAT('room_', id, '_image.jpg') FROM room_types
                """,
                # Insert room amenities
                """
                INSERT INTO room_amenities (room_type_id, amenity)
                SELECT id, 'Free WiFi' FROM room_types
                UNION
                SELECT id, 'Air Conditioning' FROM room_types
                UNION
                SELECT id, 'Minibar' FROM room_types WHERE category IN ('Double', 'Family')
                """,
                # Insert hotel amenities
                """
                INSERT INTO hotel_amenities (hotel_id, name, description, icon) VALUES
                (1, 'Swimming Pool', 'Outdoor pool with city views', 'fa-swimmer'),
                (1, 'Restaurant', 'Authentic Nepali cuisine', 'fa-utensils'),
                (2, 'Spa', 'Traditional Himalayan treatments', 'fa-spa'),
                (3, 'Bar', 'Lakeside bar with cocktails', 'fa-cocktail'),
                (4, 'Gym', 'Modern fitness center', 'fa-dumbbell')
                """,
                # Insert testimonials
                """
                INSERT INTO testimonials (hotel_id, name, avatar, rating, comment, date) VALUES
                (1, 'John Doe', 'john.jpg', 5, 'Amazing heritage experience!', '2025-01-15'),
                (2, 'Jane Smith', 'jane.jpg', 4, 'Luxurious stay near Boudha.', '2025-02-10'),
                (3, 'Arjun Thapa', 'arjun.jpg', 4, 'Perfect lakeside retreat.', '2025-03-01')
                """,
                # Insert special offers
                """
                INSERT INTO special_offers (title, description, discount, image, link, badge_color, hover_color, hover_bg, booking_window, cancellation_policy) VALUES
                ('Monsoon Getaway', 'Enjoy a relaxing stay with 20% off.', '20%', 'monsoon_offer.jpg', '/offers/monsoon', 'blue', 'white', 'blue', 'Book by July 2025', 'Free cancellation up to 7 days'),
                ('Trekking Package', 'Stay and trek with guided tours.', '15%', 'trekking_offer.jpg', '/offers/trekking', 'green', 'white', 'green', 'Book by August 2025', 'Non-refundable')
                """,
                # Insert offer tags
                """
                INSERT INTO offer_tags (offer_id, tag) VALUES
                (1, 'Monsoon'),
                (1, 'Discount'),
                (2, 'Adventure'),
                (2, 'Trekking')
                """,
                # Insert offer features
                """
                INSERT INTO offer_features (offer_id, feature) VALUES
                (1, 'Complimentary breakfast'),
                (1, 'Spa discount'),
                (2, 'Guided trekking tour'),
                (2, 'Free airport pickup')
                """,
                # Insert booking constraints
                """
                INSERT INTO booking_constraints (min_days, max_days, max_advance_days) VALUES
                (1, 30, 90)
                """,
                # Insert advance booking discounts
                """
                INSERT INTO advance_booking_discounts (min_days, max_days, discount_percentage) VALUES
                (80, 90, 30.00),
                (60, 79, 20.00),
                (45, 59, 10.00)
                """,
                # Insert user roles
                """
                INSERT INTO user_roles (name, permissions) VALUES
                ('admin', '{"manage_users": true, "manage_bookings": true, "view_reports": true}'),
                ('user', '{"view_bookings": true, "make_bookings": true}')
                """,
                # Insert room availability
                """
                INSERT INTO room_availability (room_type_id, date, is_available, status, price_override)
                SELECT id, '2025-06-01', TRUE, 'available', NULL FROM room_types
                """,
                # Insert report types
                """
                INSERT INTO report_types (name, description, query_template, parameters) VALUES
                ('Booking Summary', 'Summary of bookings by date range', 'SELECT * FROM bookings WHERE created_at BETWEEN :start_date AND :end_date', '{"start_date": "date", "end_date": "date"}')
                """,
                # Insert currencies
                """
                INSERT INTO currencies (code, name, symbol, exchange_rate) VALUES
                ('NPR', 'Nepalese Rupee', '₨', 1.0000),
                ('USD', 'US Dollar', '$', 0.0075),
                ('EUR', 'Euro', '€', 0.0065),
                ('INR', 'Indian Rupee', '₹', 0.6250)
                """,
                # Insert room inventory
                """
                INSERT INTO room_inventory (hotel_id, room_type_id, total_rooms, available_rooms)
                SELECT hotel_id, id, 10, 10 FROM room_types
                """,
                # Insert rooms
                """
                INSERT INTO rooms (room_type_id, room_number, floor, wing, status)
                SELECT
                    rt.id,
                    CONCAT('R', rt.id, LPAD(ROW_NUMBER() OVER (PARTITION BY rt.id ORDER BY n.num), 3, '0')),
                    CEIL(n.num / 5),
                    CASE WHEN n.num % 2 = 0 THEN 'A' ELSE 'B' END,
                    'active'
                FROM room_types rt
                CROSS JOIN (
                    SELECT a.N + b.N * 10 + 1 AS num
                    FROM
                        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
                        (SELECT 0 AS N UNION SELECT 1) b
                    ORDER BY num
                    LIMIT 10
                ) n
                """,
                # Insert room bookings
                """
                INSERT INTO room_bookings (booking_id, room_id, check_in, check_out, assigned_by) VALUES
                (1, 1, '2025-06-01', '2025-06-05', 1),
                (2, 7, '2025-07-10', '2025-07-12', 1)
                """,
                # Insert cancellation policies
                """
                INSERT INTO cancellation_policies (min_days, max_days, charge_percentage, description) VALUES
                (61, 999, 0, 'No cancellation charge if cancelled more than 60 days before check-in'),
                (31, 60, 50, '50% cancellation charge if cancelled between 30-60 days before check-in'),
                (0, 30, 100, '100% cancellation charge if cancelled within 30 days of check-in')
                """,
                # Insert peak seasons
                """
                INSERT INTO peak_seasons (name, start_date, end_date) VALUES
                ('Spring 2025', '2025-03-01', '2025-05-31'),
                ('Autumn 2025', '2025-09-01', '2025-11-30')
                """,
                # Insert room pricing
                """
                INSERT INTO room_pricing (room_type_id, season_id, base_price, capacity_percentage, rate_multiplier)
                SELECT rt.id, ps.id,
                    CASE rt.category
                        WHEN 'Standard' THEN 50.00
                        WHEN 'Double' THEN 75.00
                        ELSE 100.00
                    END,
                    100.00,
                    1.2
                FROM room_types rt
                CROSS JOIN peak_seasons ps
                """
            ]

            # Execute initial data insertion
            for query in initial_data:
                cursor.execute(query)

            # Update room_inventory available_rooms
            cursor.execute("""
                UPDATE room_inventory
                SET available_rooms = total_rooms
                WHERE available_rooms IS NULL
            """)

            connection.commit()
            print("Database and tables created successfully!")

    except Error as e:
        print(f"Error: {e}")
        if connection.is_connected():
            connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    setup_database()
