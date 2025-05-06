Nepal Hotels Database Setup

Overview

This project provides a Python script (data.py) to set up a MySQL database for a hotel management system focused on hotels in Nepal. The script creates the nepal_hotels database, defines its schema, and populates it with initial data for cities, hotels, rooms, bookings, and related entities. The database can be managed and queried using MySQL Workbench.

Prerequisites





Python 3.x: Ensure Python is installed.



MySQL Server: A running MySQL server (e.g., MySQL Community Server).



MySQL Workbench: Installed for database management and query execution.



mysql-connector-python: Python library for MySQL connectivity. Install it using:

pip install mysql-connector-python

Installation





Clone or Download the Project:





Clone the repository or download the data.py file.



Configure MySQL Credentials:





Open data.py and update the database connection settings:

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='@Psychology123'
)

Replace host, user, and password with your MySQL server credentials.



Install Python Dependencies:





Install the required library:

pip install mysql-connector-python



Set Up MySQL Workbench:





Launch MySQL Workbench and create a connection using the same credentials as in data.py.



Test the connection to ensure it works.

Usage





Run the Script:





Execute the script to create and populate the database:

python data.py



The script will:





Connect to the MySQL server.



Drop any existing nepal_hotels database.



Create a new nepal_hotels database.



Set up tables (e.g., cities, hotels, bookings, users).



Insert initial data (e.g., Nepali cities, hotels, sample bookings).



Create functions (e.g., calculate_room_price), views (e.g., room_prices), and other database objects.



Verify Output:





On successful execution, the console will display:

Event Scheduler enabled successfully.
Database and tables created successfully!
MySQL connection closed.



If errors occur, check the console for details (e.g., connection or SQL syntax issues).



Use MySQL Workbench:





Open MySQL Workbench and connect to your MySQL server.



Navigate to the nepal_hotels database under the Schemas tab.



View tables, run queries, or inspect data (e.g., SELECT * FROM hotels;).



Use the Query Tool to execute sample queries or test database functionality.

Database Structure

The nepal_hotels database includes:

Key Tables





cities: Stores Nepali cities (e.g., Kathmandu, Pokhara) with attributes like peak_rate and off_peak_rate.



hotels: Contains hotel details (e.g., name, city_id, rating).



room_types: Defines room types (Standard, Double, Family) per hotel.



bookings: Manages bookings with fields like check_in, check_out, and status.



users: Stores user data (e.g., email, role, email_verified).



payments: Tracks booking payments (e.g., amount, payment_status).



peak_seasons: Defines peak season periods for pricing adjustments.



special_offers: Stores promotional offers (e.g., Monsoon Getaway).



Additional tables include room_availability, hotel_amenities, cancellation_policies, and more.

Functions





calculate_room_price: Computes room prices based on room type and guest count.



is_peak_season: Checks if a date falls within a peak season.

Views





room_prices: Displays calculated room prices for peak and off-peak seasons.

Initial Data





Cities: Kathmandu, Pokhara, Chitwan, etc.



Hotels: Hotel Shankar, Hyatt Regency Kathmandu, etc.



Users: Sample admin and user accounts.



Bookings: Sample bookings with guests and payments.



Special Offers: Monsoon Getaway, Trekking Package.

Entity-Relationship Diagram (ERD)

The erd.pdf file provides a visual representation of the database schema, including tables, relationships, and constraints. Open it to understand the database structure and foreign key relationships.

Running Queries in MySQL Workbench





Open MySQL Workbench and connect to your server.



Select the nepal_hotels database in the Schemas panel.



Use the Query Tool to run sample queries, such as:

-- List all hotels in Kathmandu
SELECT h.name, h.rating, c.name AS city
FROM hotels h
JOIN cities c ON h.city_id = c.id
WHERE c.name = 'Kathmandu';

-- Check room availability for June 2025
SELECT rt.name, ra.date, ra.status
FROM room_availability ra
JOIN room_types rt ON ra.room_type_id = rt.id
WHERE ra.date = '2025-06-01';



Export query results or take screenshots for documentation:





Click the Export button in the result grid to save as CSV or JSON.



Use your system's screenshot tool (e.g., Snip & Sketch on Windows, Cmd+Shift+4 on Mac) to capture results.

Notes





Security: The script uses hardcoded credentials (@Psychology123). For production, store credentials in environment variables or a .env file.



Error Handling: The script handles MySQL connection and query errors. Check console output for issues.



Customization: Edit the initial_data section in data.py to modify seed data (e.g., add new hotels or cities).



Password Hashing: Placeholder passwords are used (e.g., hashed_password_123). Implement proper hashing (e.g., bcrypt) for production.



MySQL Workbench Tips:





Use the Table Inspector to verify table structures and constraints.



Enable the Event Scheduler in MySQL Workbench if needed for scheduled tasks.

Troubleshooting





Connection Errors:





Ensure MySQL server is running (mysqladmin -u root -p ping).



Verify credentials in data.py and MySQL Workbench match.



SQL Errors (e.g., Error 1064):





Check console for specific error messages.



Ensure no conflicting nepal_hotels database exists.



Validate SQL syntax in data.py (e.g., missing semicolons or incorrect constraints).



MySQL Workbench Issues:





If tables don’t appear, refresh the Schemas panel.



For query errors, verify table/column names and data existence (e.g., SELECT * FROM room_types;).



Missing Data:





Run SELECT COUNT(*) FROM table_name; to confirm data insertion.



Re-run data.py if data is missing, ensuring no errors occur.

Contributing

Maintained by Aadarsh Bhagat (Student ID: 453974). For contributions or issues:





Submit pull requests with proposed changes.



Report issues via email or the project repository.

License

This project is for educational purposes. Contact the author for licensing details.