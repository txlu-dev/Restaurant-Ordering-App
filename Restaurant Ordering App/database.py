import sqlite3

# Connect to the SQLite database (this will create the 'udat' database file if it doesn't exist)
conn = sqlite3.connect('udat.db')  # 'udat.db' is the name of the database file

# Create a cursor object
cursor = conn.cursor()

# Create the 'user' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    town TEXT NOT NULL
    
)
''')



# Create the 'restaurant' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS restaurant (
     restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
     restaurantname TEXT NOT NULL,
     town TEXT NOT NULL,
     description TEXT NOT NULL,
     openingTime INTEGER NOT NULL,
     closingTime INTEGER NOT NULL,
     rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
     supportsTakeaway INTEGER NOT NULL CHECK (supportsTakeaway IN (0, 1)),
     supportsDelivery INTEGER NOT NULL CHECK (supportsDelivery IN (0, 1)),
     supportsReservation INTEGER NOT NULL CHECK (supportsReservation IN (0, 1)),
     iconName TEXT NOT NULL,
     iconName2 TEXT NOT NULL
     

)
''')

# Create the 'favrestaurant' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS favrestaurant (
    favID INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    restaurant_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant (restaurant_id)
)
''')

# Create the 'restaurantmenu' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS restaurantmenu (
    mealID INTEGER PRIMARY KEY AUTOINCREMENT,
    mealName TEXT NOT NULL,
    productionTime INTEGER NOT NULL,
    price REAL NOT NULL,
    restaurant_id INTEGER,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant (restaurant_id)
)
''')

# Create the 'reservation' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS reservation (
    reservationID INTEGER PRIMARY KEY AUTOINCREMENT,
    time TIME NOT NULL,
    date DATE NOT NULL,
    tableNo INTEGER NOT NULL,
    noPeople INTEGER NOT NULL,
    user_id INTEGER,
    restaurant_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant (restaurant_id) ON DELETE CASCADE
)
''')

# Function to insert a record for each restaurant
def add_restaurants():
 conn = sqlite3.connect('udat.db')  
 cursor = conn.cursor()   
 records = [
    ("McDonalds", "Chelmsford", "Description: Located in the heart of Chelmsford, this McDonald's is a bustling hotspot for families and students alike. With its iconic golden arches, it offers a cozy atmosphere featuring free Wi-Fi and ample seating. The menu boasts classic favorites like the Big Mac and Chicken McNuggets, and the local community appreciates the special touches, like seasonal promotions and limited-edition menu items. Enjoy a quick bite, or settle in with a coffee while you watch the world go by.", 12, 12, 5, 1, 1, 0, "mcdonalds_photo.png", "mcdonalds_icon.png"),
    ("Burger King", "Southend", "Description: In the vibrant seaside town of Southend, Burger King stands out with its flame-grilled burgers and a welcoming, cheerful ambiance. This location is particularly popular for its innovative Whopper variations and mouth-watering sides like onion rings and loaded fries. With stunning views of the pier, patrons can enjoy their meals while taking in the coastal scenery. The restaurant’s friendly staff and quick service make it a perfect stop before a day of fun at the beach or a night out.", 7, 10, 5, 1, 0, 0, "burgerking_photo.png", "burgerking_icon.png"),
    ("KFC", "Basildon", "Description: Nestled in Basildon, this KFC is a favorite among fried chicken lovers. The aroma of their secret recipe chicken fills the air, enticing locals as they step inside. With a cozy dining area, families gather here to enjoy hearty meals featuring the iconic Original Recipe chicken, crispy popcorn chicken, and an array of sides. The restaurant also offers convenient drive-thru service for those on the go, ensuring that no one misses out on their finger-lickin' favorites.", 11, 6, 5, 0, 1, 0, "kfc_photo.png", "kfc_icon.png"),
    ("Nandos", "Colchester", "Description: Nando's in Colchester brings a taste of Portugal to the bustling town. Known for its peri-peri chicken, this vibrant restaurant is adorned with colorful decor and lively murals that echo the spirit of its heritage. Diners can customize their meal with various spice levels, enhancing the experience with mouth-watering sides like spicy rice and garlic bread. The casual, social atmosphere makes it an ideal place for gatherings with friends or family, all while enjoying the upbeat soundtrack in the background.", 6, 9, 5, 1, 0, 1, "nandos_photo.png", "nandos_icon.png"),
    ("Domino's", "Brentwood", "Description: The Domino's in Brentwood is a go-to destination for pizza lovers craving a cozy night in or an impromptu celebration. Known for its delicious range of toppings and the option to customize your own pizza, this location quickly becomes a local staple for quick delivery or takeout. Families and friends often order their favorites to enjoy at home, while the friendly staff is always ready to recommend their latest deals. The scent of fresh pizza wafting through the air is a constant reminder that happiness can be found in a slice.", 7, 11, 5, 1, 1, 0, "dominos_photo.png", "dominos_icon.png"),
    ("Subway", "Canvey Island", "Description: Subway in Canvey Island is the ultimate spot for a healthy yet customizable meal on the go. It offers a bright and welcoming atmosphere, perfect for lunch breaks or quick dinners. Customers can create their sandwiches or salads with a selection of fresh ingredients, including artisan breads, crisp veggies, and a variety of protein options. The emphasis on quality ingredients and fresh flavors attracts health-conscious diners, making it a valuable and convenient option for anyone looking to enjoy a meal tailored to their tastes.", 5, 5, 5, 1, 0, 0, "subway_photo.png", "subway_icon.png")
 ]

 cursor.executemany('''INSERT INTO restaurant (restaurantname, town, description, openingTime, closingTime, rating, supportsTakeaway, supportsDelivery, supportsReservation, iconName, iconName2)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', records)

 # Commit the changes to the database
 conn.commit()




# Function to add meals to each restaurant
def add_meals():
    # Connect to the database
    conn = sqlite3.connect('udat.db')
    cursor = conn.cursor()

    # Meal data (mealName, productionTime, price, restaurant_id)
    meals = [
        # McDonalds (restaurant_id = 1)
        ('Big Mac', 5, 3.99, 1),
        ('Chicken McNuggets', 6, 4.99, 1),
        ('French Fries', 3, 2.49, 1),

        # Burger King (restaurant_id = 2)
        ('Whopper', 8, 5.99, 2),
        ('Onion Rings', 4, 2.99, 2),
        ('Loaded Fries', 6, 3.49, 2),

        # KFC (restaurant_id = 3)
        ('Original Recipe Chicken', 10, 6.99, 3),
        ('Popcorn Chicken', 5, 4.49, 3),
        ('Mashed Potatoes', 7, 2.99, 3),

        # Nandos (restaurant_id = 4)
        ('Peri-Peri Chicken', 12, 8.99, 4),
        ('Spicy Rice', 6, 3.49, 4),
        ('Garlic Bread', 5, 2.99, 4),

        # Domino's (restaurant_id = 5)
        ('Pepperoni Pizza', 15, 9.99, 5),
        ('Veggie Pizza', 15, 8.99, 5),
        ('Garlic Breadsticks', 10, 4.99, 5),

        # Subway (restaurant_id = 6)
        ('Chicken Teriyaki Sub', 5, 7.49, 6),
        ('Italian BMT Sub', 6, 6.99, 6),
        ('Veggie Delight Sub', 4, 5.49, 6)
    ]

    # Insert meals into the restaurantmenu table
    cursor.executemany('''
        INSERT INTO restaurantmenu (mealName, productionTime, price, restaurant_id)
        VALUES (?, ?, ?, ?)
    ''', meals)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()





  



###




# Insert data into the 'user' table
def add_user(username, password, town):
    conn = sqlite3.connect('udat.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO user (username, password, town)
    VALUES (?, ?, ?)
    ''', (username, password, town))
    conn.commit()

# Deletes user's data from user table
def delete_user(username, password):
    conn = sqlite3.connect('udat.db')
    cursor = conn.cursor()

    # Check if the user with the given username and password exists
    cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        # If user exists, delete the record
        cursor.execute("DELETE FROM user WHERE username=? AND password=?", (username, password))
        conn.commit()
    conn.close()


# Validates username
def check_credentials(username, password):
    conn = sqlite3.connect('udat.db')
    cursor = conn.cursor()
    
    # Query to check if the username and password match a record
    cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))

    # Fetch the result
    user = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return whether the user was found
    if user:
        return True  # Credentials are correct
    else:
        return False  # Credentials are incorrect

# Function to retrieve the associated town based on username and password
def get_town(username, password):
  
    conn = sqlite3.connect('udat.db')  
    cursor = conn.cursor()

    # Query to find the record with matching username and password
    cursor.execute("SELECT town FROM user WHERE username=? AND password=?", (username, password))

    # Fetch the result
    result = cursor.fetchone()

    # If a result is found, return the town
    if result:
        town = result[0]  # Fetch the town from the tuple
        conn.close()
        return town


def get_user_id(username, password):
    
    conn = sqlite3.connect('udat.db') 
    cursor = conn.cursor()

    # Query to find the record with matching username and password
    cursor.execute("SELECT user_id FROM user WHERE username=? AND password=?", (username, password))

    result = cursor.fetchone()

    # If a result is found, return the id
    if result:
        user_id = result[0]  # Fetch the id from the tuple
        conn.close()
        return user_id


def update_user(newusername, newpassword, newtown, user_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('udat.db')  
    cursor = conn.cursor()

    # Update the user's username, password, and town based on user_id
    cursor.execute('''
    UPDATE user
    SET username = ?, password = ?, town = ?
    WHERE user_id = ?
    ''', (newusername, newpassword, newtown, user_id))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

# Function to retrieve the details of the restaurant with the associated name
def get_restaurantDetails(restaurantName):
    
    conn = sqlite3.connect('udat.db')  
    cursor = conn.cursor()
    
    cursor.execute("SELECT restaurant_id, town, description, openingTime, closingTime, rating, iconName FROM restaurant WHERE restaurantname = ?", (restaurantName,))

    # Fetch the result
    result = cursor.fetchone()

    # If a result is found, return the details individually
    if result:
        restaurant_id, town, description, openingTime, closingTime, rating, iconName = result
        conn.close()
        
        return restaurant_id, town, description, openingTime, closingTime, rating, iconName

def get_iconName2(restaurantName):
    
    conn = sqlite3.connect('udat.db')  
    cursor = conn.cursor()
    
    cursor.execute("SELECT iconName2 FROM restaurant WHERE restaurantname = ?", (restaurantName,))

    # Fetch the result
    result = cursor.fetchone()

    # If a result is found, return the icon name
    if result:
        iconName2 = result[0]  # Fetch the icon name from the tuple
        conn.close()
        return iconName2

def get_restaurantName(town):
    
    conn = sqlite3.connect('udat.db')  
    cursor = conn.cursor()
    
    cursor.execute("SELECT restaurantname FROM restaurant WHERE town = ?", (town,))

    # Fetch the results
    results = cursor.fetchall()

    # If a result is found, return the name
    if results:
        restaurantNameResults = results  # Fetch the name from the tuple
        conn.close()
        return restaurantNameResults




def get_townSearchResults(townQuery):

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('udat.db')
    c = conn.cursor()

            
    # Search database for matching items
    c.execute("SELECT restaurantname FROM restaurant WHERE town LIKE ?", ('%' + townQuery + '%',))
    results = c.fetchall()

    conn.close()
    return results




def get_nameSearchResults(nameQuery):

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('udat.db')
    c = conn.cursor()

            
    # Search database for matching items
    c.execute("SELECT restaurantname FROM restaurant WHERE restaurantname LIKE ?", ('%' + nameQuery + '%',))
    results = c.fetchall()

    conn.close()
    return results



def add_favRestaurant(user_id, restaurant_id):
 
      
    conn = sqlite3.connect('udat.db')
        
       
    cursor = conn.cursor()
        
    # Insert the user_id and restaurant_id into the favrestaurant table
    cursor.execute('''
        INSERT INTO favrestaurant (user_id, restaurant_id)
        VALUES (?, ?)
    ''', (user_id, restaurant_id))
        
    # Commit the transaction to save the changes
    conn.commit()
        
    # Close the cursor and connection
    cursor.close()
    conn.close()

def remove_favRestaurant(user_id, restaurant_id):
    # Establish a database connection
    conn = sqlite3.connect('udat.db')
    cursor = conn.cursor()
    
    # Delete the record from the favrestaurant table where both user_id and restaurant_id match
    cursor.execute('''
        DELETE FROM favrestaurant
        WHERE user_id = ? AND restaurant_id = ?
    ''', (user_id, restaurant_id))
    
    # Commit the transaction to save the changes
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()

def check_favRestaurant(user_id, restaurant_id):
    conn = sqlite3.connect('udat.db')
    cursor = conn.cursor()
    
    # SQL query to check if a record exists
    cursor.execute("SELECT EXISTS(SELECT 1 FROM favrestaurant WHERE user_id=? AND restaurant_id=?)", (user_id, restaurant_id))
    
    # Fetch the result
    exists = cursor.fetchone()[0]  # fetchone returns a tuple; extract the first element
    
    cursor.close()  
    conn.close()    
    
    return bool(exists)  # return True if exists is 1, False if 0


def get_favRestaurant(user_id):
    
    conn = sqlite3.connect('udat.db')  
    cursor = conn.cursor()
    
    cursor.execute("SELECT r.restaurantname FROM restaurant r JOIN favrestaurant f ON r.restaurant_id = f.restaurant_id WHERE f.user_id = ?", (user_id,))

    # Fetch the results
    results = cursor.fetchall()
   

    # If a result is found, return the restaurant name
    if results:
        restaurantNameResults = results  # Fetch the restaurant name from the tuple
        conn.close()
        return restaurantNameResults


# Retrieves the meal IDs of every meal associated with a given restaurant ID.
def get_restaurantMeals(restaurant_id):
   
    conn = sqlite3.connect('udat.db')  # Replace with your database file
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT mealID FROM restaurantmenu WHERE restaurant_id = ?", (restaurant_id,))
        meal_ids = cursor.fetchall()
        meal_ids = [meal_id[0] for meal_id in meal_ids]
        return meal_ids

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        conn.close()
    return None



#Retrieves details (meal name, price and time) for a given meal ID.
def get_mealDetails(meal_id):
  
    conn = sqlite3.connect('udat.db')  # Replace with your database file
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT mealName, price, productionTime FROM restaurantmenu WHERE mealID = ?", (meal_id,))
        result = cursor.fetchone()

        if result:
            return result  # Returns (mealName, price and productionTime)
        else:
            return None  # Meal not found

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None  # Handle potential errors

    finally:
        conn.close()


def get_orderOptions(restaurant_id):
    # Connect to the database
    conn = sqlite3.connect('udat.db')
    cursor = conn.cursor()
    
    # Query the restaurant table for the specified restaurant_id
    cursor.execute('''
        SELECT supportsTakeaway, supportsDelivery, supportsReservation
        FROM restaurant
        WHERE restaurant_id = ?
    ''', (restaurant_id,))
    
    # Fetch the result
    result = cursor.fetchone()
    
    # If the restaurant is found, return the options, else return None
    if result:
        supportsTakeaway, supportsDelivery, supportsReservation = result
        return supportsTakeaway, supportsDelivery, supportsReservation
    else:
        return None
    
    # Close the connection
    conn.close()

# Check if timeslot has already been booked
def check_reservation(time, date, restaurant_id):
   
    conn = sqlite3.connect('udat.db')
    cursor = conn.cursor()
    
    # Check if there is already a reservation for the given time, date, and restaurant
    cursor.execute('''
        SELECT * FROM reservation
        WHERE time = ? AND date = ? AND restaurant_id = ?
    ''', (time, date, restaurant_id))
    
    # If the query returns any rows, a reservation exists
    reservation = cursor.fetchone()

    conn.close()
    
    # If a reservation exists, return True, otherwise return False
    return reservation is not None


# Insert data into the 'reservation' table 
def add_reservation(time, date, tableNo, noPeople, user_id, restaurant_id):
   
    conn = sqlite3.connect('udat.db')
    cursor = conn.cursor()
    
    # Insert the new reservation into the reservation table
    cursor.execute('''
        INSERT INTO reservation (time, date, tableNo, noPeople, user_id, restaurant_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (time, date, tableNo, noPeople, user_id, restaurant_id))

    conn.commit()
    conn.close()


 

###


# Close the connection
conn.close()

