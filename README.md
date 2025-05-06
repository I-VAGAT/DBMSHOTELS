Nepal Hotels Database Setup
Overview
The Nepal Hotels Database Setup project provides a Python script (data.py) to initialize a MySQL database (nepal_hotels) for a hotel management system tailored to hotels in Nepal. The script creates the database schema, sets up tables, and populates them with initial data, including cities, hotels, room types, bookings, and more. MySQL Workbench is recommended for managing and querying the database.
Features

Creates a MySQL database (nepal_hotels) with 30+ tables for hotel management.
Includes tables for cities, hotels, rooms, bookings, users, payments, and special offers.
Defines functions (calculate_room_price, is_peak_season) and views (room_prices).
Populates the database with sample data (e.g., hotels in Kathmandu, Pokhara).
Supports MySQL Workbench for database visualization and querying.
Includes an Entity-Relationship Diagram (ERD) in erd.pdf.

Prerequisites

Python 3.6+: Install from python.org.
MySQL Server: Install MySQL Community Server (8.0 or later).
MySQL Workbench: Install for database management (download).
mysql-connector-python: Python library for MySQL connectivity. Install via:pip install mysql-connector-python



Installation

Clone or Download the Project:
Clone the repository or download data.py and erd.pdf.


Configure MySQL Credentials:
Edit data.py to update the MySQL connection settings:connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='@Psychology123'
)

Replace host, user, and password with your MySQL server credentials.


Install Dependencies:
Install the required Python library:pip install mysql-connector-python




Set Up MySQL Workbench:
Open MySQL Workbench and create a new connection using the same credentials as in data.py.
Test the connection to confirm accessibility.



Usage

Run the Script:
Execute the script to set up the database:python data.py


The script will:
Connect to the MySQL server.
Drop any existing nepal_hotels database.
Create a new nepal_hotels database.
Create tables (e.g., cities, hotels, bookings, users).
Insert initial data (e.g., cities, hotels, sample bookings).
Define functions, views, and constraints.


Expected output:Event Scheduler enabled successfully.
Database and tables created successfully!
MySQL connection closed.




Verify in MySQL Workbench:
Open MySQL Workbench and connect to your server.
Locate the nepal_hotels database in the Schemas panel.
Inspect tables or run queries (e.g., SELECT * FROM hotels;).


Explore the ERD:
Open erd.pdf to view the database schema and relationships.



Database Structure
The nepal_hotels database includes:
Key Tables

cities: Stores city details (e.g., name, peak_rate, off_peak_rate).
hotels: Contains hotel information (e.g., name, city_id, rating).
room_types: Defines room categories (Standard, Double, Family).
bookings: Tracks bookings (e.g., check_in, check_out, status).
users: Manages user accounts (e.g., email, role).
payments: Records payment details (e.g., amount, payment_method).
peak_seasons: Defines peak season periods.
special_offers: Stores promotional offers (e.g., Monsoon Getaway).
Other tables: room_availability, hotel_amenities, cancellation_policies, etc.

Functions

calculate_room_price: Calculates room prices based on type and guest count.
is_peak_season: Determines if a date is in a peak season.

Views

room_prices: Shows peak and off-peak room prices.

Initial Data

Cities: Kathmandu, Pokhara, Chitwan, Lumbini, etc.
Hotels: Hotel Shankar, Hyatt Regency Kathmandu, Pokhara Grande, etc.
Users: Admin and sample user accounts.
Bookings: Sample bookings with guests and payments.
Special Offers: Monsoon Getaway, Trekking Package.

Sample Queries
Use MySQL Workbench’s Query Tool to run queries like:
-- List hotels in Pokhara
SELECT h.name, h.rating, c.name AS city
FROM hotels h
JOIN cities c ON h.city_id = c.id
WHERE c.name = 'Pokhara';

-- View available rooms on a specific date
SELECT rt.name, ra.date, ra.status
FROM room_availability ra
JOIN room_types rt ON ra.room_type_id = rt.id
WHERE ra.date = '2025-06-01' AND ra.is_available = TRUE;

Notes

Security: Hardcoded credentials (@Psychology123) are used for demonstration. In production, use environment variables or a secure configuration file.
Password Hashing: Placeholder passwords (hashed_password_123) are inserted. Use a library like bcrypt for secure password storage in production.
Customization: Modify the initial_data list in data.py to add or change seed data.
MySQL Workbench:
Use Table Inspector to check table structures.
Export query results as CSV/JSON via the Export button.


Event Scheduler: The script enables the MySQL Event Scheduler for potential scheduled tasks.

Troubleshooting

Connection Issues:
Verify MySQL server is running: mysqladmin -u root -p ping.
Ensure credentials match in data.py and MySQL Workbench.


SQL Errors:
Check console for error messages (e.g., Error 1064 for syntax issues).
Ensure no existing nepal_hotels database conflicts.


Data Missing:
Run SELECT COUNT(*) FROM table_name; to verify data.
Re-run data.py if needed, checking for errors.


MySQL Workbench:
Refresh the Schemas panel if tables don’t appear.
Validate table/column names in queries.



Contributing
Maintained by Aadarsh Bhagat (Student ID: 453974). To contribute:

Submit pull requests with clear descriptions of changes.
Report issues via email or the project repository (if available).

License
This project is for educational purposes. Contact the author for licensing details.
