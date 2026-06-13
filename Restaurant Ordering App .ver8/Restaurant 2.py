# Toluwanimi Awosanya
# Restaurant Booking App

# Import Libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import check_credentials, add_user, delete_user, get_town, get_user_id, \
     update_user, get_restaurantDetails, get_iconName2, get_restaurantName, get_townSearchResults, \
     get_nameSearchResults, add_favRestaurant, remove_favRestaurant, check_favRestaurant, get_favRestaurant, \
     get_restaurantMeals, get_mealDetails, get_orderOptions, check_reservation, add_reservation
from datetime import datetime, timedelta


#######################################################################


#Creates class for user
class User:
    def __init__(self, username, password, town):
        self.username = username
        self.password = password
        self.town = town
        self.user_id = get_user_id(self.username, self.password)

    def get_town(self):
        return self.town # Returns user's town


    def delete_account(self):
        delete_user(self.username, self.password)

    def update_account(self, newusername, newpassword, newtown):
        update_user(newusername, newpassword, newtown, self.user_id) #Updates 'user' database
        self.username = newusername #Updates attributes
        self.password = newpassword
        self.town = newtown

    def get_ID(self):
        return self.user_id # Returns user's id

    
#Creates class for restaurant      
class Restaurant:
    def __init__(self, restaurant_id, restaurantName, restaurant_town, openingTime, closingTime, rating):
        self.restaurant_id = restaurant_id
        self.restaurantName = restaurantName
        self.restaurant_town = restaurant_town
        self.openingTime = openingTime
        self.closingTime = closingTime
        self.rating = rating

    def get_ID(self):
        return self.restaurant_id # Returns restaurant's id


#######################################################################

#Manages pages and user sessions
class App:

    def __init__(self, window):
        # Creates window and it's properties
        self.window = window
        self.window.geometry("912x600")
        self.window.minsize(912, 600)
        self.window.title("Restaurant Booking App")
        icon = tk.PhotoImage(file='img.png')
        self.window.iconphoto(True, icon)

        # User data
        self.user_details = None  # Current user object
        

        # Create pages (instances of our Page subclasses)
        self.loginpage = LoginPage(self.window, self)
        self.regpage = RegistrationPage(self.window, self)
        self.homepage = HomePage(self.window, self)
        self.accsettings = AccountSettingsPage(self.window, self)
        self.restaurant_page = RestaurantPage(self.window, self)
        self.search_results_page = SearchResultsPage(self.window, self)
        self.menupage = MenuPage(self.window, self)
        self.orderpage = OrderPage(self.window, self)
        self.purchasepage = PurchasePage(self.window, self)
        self.reservationpage = ReservationPage(self.window, self)
        self.res_purchasepage = ReservationPurchasePage(self.window, self)

        # Store pages in a dictionary for easy access
        self.pages = {
            "loginpage": self.loginpage,
            "regpage": self.regpage,
            "homepage": self.homepage,
            "accsettings": self.accsettings,
            "restaurantpage": self.restaurant_page,
            "searchResultsPage": self.search_results_page,
            "menupage": self.menupage,
            "orderpage": self.orderpage,
            "purchasepage": self.purchasepage,
            "reservationpage": self.reservationpage,
            "res_purchasepage": self.res_purchasepage,
        }

        # Initially show the login page
        self.show_page("loginpage")

    def show_page(self, page_name):
        #Shows the selected page
        self.pages[page_name].show()

   


    

#Superclass defining common behavior for all pages in an app
class Page(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app  # Store a reference to the main App instance
        self.create_widgets()

    def create_widgets(self):
        #Abstract method: should be overridden by subclasses to define the page's content
        raise NotImplementedError("Subclasses must implement create_widgets() method.")

    def show(self):
        #Shows the page by packing it and hiding all other pages
        for page in self.app.pages.values():
            page.pack_forget()  # Hide all other pages
        self.pack(fill="both", expand=True)

        
#######################################################################


class LoginPage(Page):

    def create_widgets(self):

        # Title labels
        title_label = tk.Label(self,
              text="Restaurant Booking App",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        title_label.pack()
        
        title_label2 = tk.Label(self,
              text="Login or Register:",
              font=('Arial',20),
              bd = 5,
              padx=20)
        title_label2.pack(pady=10)
        
        # Create and place the username label and entry
        username_label = tk.Label(self, text="Username:")
        username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        
        # Create and place the password label and entry
        password_label = tk.Label(self, text="Password:")
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*")  # Show asterisks for password
        self.password_entry.pack()
        
        # Create and place the login button
        login_button = tk.Button(self, text="Login", command=self.validate_login)
        login_button.pack(pady=20)
        
        # Creating delete button
        delete_button = tk.Button(self, text="Delete", command=self.delete_login)
        delete_button.pack()

        # Creating reigster button
        register_button = tk.Button(self, text="Register", command=self.register_login)
        register_button.pack(pady=20)



    # Function to validate the login
    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()  

        # Validation
        if check_credentials(username, password):
            self.app.show_page("homepage")
            
            town = get_town(username,password)
            self.app.user_details = User(username, password, town) # Creates user object from details in self
            self.app.homepage.update_homepage() #Updates homepage contents and displays homepage to the user

        elif username and password:
            messagebox.showerror("Login Failed", "Invalid username or password")
                   
        else:
            messagebox.showerror("Login Failed", "Insufficient data entered")
            

      
    # Function to delete the login details
    def delete_login(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


    # Function to validate the user details and send user to register screen
    def register_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        
        if check_credentials(username, password):
            messagebox.showerror("Register Failed","Username and Password already exists")
        elif username and password:
            self.app.show_page("regpage")
        else:
            messagebox.showerror("Register Failed","Insufficient data entered")


#######################################################################

class HomePage(Page):

    def create_widgets(self):

        
        # Create labels and buttons for the home page
        title_label = tk.Label(self,
              text="Home Menu",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        title_label.pack()
        

        title_label2 = tk.Label(self,
              text=("Welcome!"),
              font=('Arial',20),
              bd = 5,
              padx=20)
        title_label2.pack(pady=10)



        # Create the local restaurants frame
        self.restaurant_bar = tk.Frame(self, width=600, bg="lightgrey")
        self.restaurant_bar.pack(fill=tk.X)


        title_label2 = tk.Label(self.restaurant_bar,
              text=("Restaurants near you:"),
              font=(15),
              bd = 5,
              padx=20)
        title_label2.pack(side=tk.LEFT, pady=10)




        # Create the favourite restaurant frame
        self.fav_bar = tk.Frame(self, width=600, bg="lightgrey")
        self.fav_bar.pack(fill=tk.X)


        self.title_label2 = tk.Label(self.fav_bar,
              text=("Your favourite restaurants:"),
              font=(15),
              bd = 5,
              padx=20)
        self.title_label2.pack(side=tk.LEFT, pady=10)
        
        

        # Create a frame to hold the entry, button, and combo box together
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5, anchor="w", padx=10)  # Align frame to the left


        # Create the search entry widget (the search bar)
        self.search_entry = tk.Entry(search_frame, width=30)
        
        # Create the combo box with options and set it to readonly (non-editable)
        options = ["Chelmsford", "Southend", "Basildon", "Colchester", "Brentwood", "Canvey Island"]
        self.search_combo = ttk.Combobox(search_frame, values=options, width=27, state="readonly")
        self.search_combo.set(options[0])
        
        # Start with entry bar visible, combo box hidden
        self.is_combo = False
        self.search_entry.pack(side="left", padx=5)



        # Create a button to toggle between entry bar and combo box
        self.toggle_button = tk.Button(search_frame, text="Search by Location", command=self.toggle_input)
        self.toggle_button.pack(side="right", padx=5)
        
        # Create a button that will trigger the search function
        search_button = tk.Button(search_frame, text="Search", command=self.search)
        search_button.pack(side="right", padx=5)
        
        


        # Create the settings frame
        settings_bar = tk.Frame(self, width=600)
        settings_bar.pack(side=tk.BOTTOM )

        # Button taking you to settings screen
        settings_button = tk.Button(settings_bar, text="Settings", command=lambda: self.app.show_page("accsettings"))
        settings_button.pack(side=tk.LEFT, padx=5)

        # Logout button taking you to loginscreen
        logout = tk.Button(settings_bar, text="Logout", command=self.logout)
        logout.pack(side=tk.LEFT, padx=5, pady=20)

        





    # Function to update local and favourite restaurants then open homepage
    def update_homepage(self):

        self.local_Restaurants() # Displays restaurants near the user
        self.favourite_Restaurants() # Displays the user's favourite restaurants
        self.app.show_page("homepage") # Opens home page


    def local_Restaurants(self):
        if self.app.user_details:
            self.town = self.app.user_details.town # Gets user's town from object

        restaurantNameResults = get_restaurantName(self.town) # Gets the names of the restaurants associated with the user's town
        self.local_icons = []   # Store references to all loaded images

        # Destroy only buttons (skip other widgets like labels)
        for widget in self.restaurant_bar.winfo_children():
            if isinstance(widget, tk.Button):  # Check if the widget is a button
                widget.destroy()



       
                
        # Create a button for each restaurant name
        for index, restaurantNameResult in enumerate(restaurantNameResults):
         
            
            iconName2 = get_iconName2(restaurantNameResult[0]) # Gets the filename of the icon with that restaurant name stored in the database and saves it 
            iconName2 = tk.PhotoImage(file=iconName2) # Load the icons
            iconName2 = iconName2.subsample(4, 4) # Resizing the image to 25% of its original size
            self.local_icons.append(iconName2) #Adds icons to list

            

      
            restaurant_button = tk.Button(self.restaurant_bar, image=iconName2, text=restaurantNameResult[0], compound="top", 
                                      command=lambda r=restaurantNameResult[0]: self.app.restaurant_page.open_Restaurant(r)) 
            restaurant_button.pack(side="left")


    # Function to display the user's favourite restaurants on the home page
    def favourite_Restaurants(self):

        if self.app.user_details:
            user_id = self.app.user_details.get_ID() # Gets user's ID from object
        


        restaurantNameResults = get_favRestaurant(user_id) # Gets the names of the favourite restaurants associated with the user's id
        self.fav_icons = []   # Store references to all loaded images
       

        # Destroy every other label aside from the title label
        for widget in self.fav_bar.winfo_children():
            if widget !=  self.title_label2: # Check if the widget isn't the title label
                widget.destroy()


        if restaurantNameResults == None: # Display "No favourites"
            noFavs_label = tk.Label(self.fav_bar, text="No favourites") 
            noFavs_label.pack(side="left")

            

        else:
                    
            # Create a button for each restaurant name
            for index, restaurantNameResult in enumerate(restaurantNameResults):
                     
                iconName2 = get_iconName2(restaurantNameResult[0]) # Gets the filename of the icon with that restaurant name stored in the database and saves it 
                iconName2 = tk.PhotoImage(file=iconName2) # Load the icons
                iconName2 = iconName2.subsample(4, 4) # Resizing the image to 25% of its original size
                self.fav_icons.append(iconName2) #Adds icons to list
    
                favRestaurant_button = tk.Button(self.fav_bar, image=iconName2, text=restaurantNameResult[0], compound="top", 
                                      command=lambda r=restaurantNameResult[0]: self.app.restaurant_page.open_Restaurant(r)) 
                favRestaurant_button.pack(side="left")

        self.app.show_page("homepage")


    


    def search(self):
        # Check if the combo box is visible and get its selected value
        if self.is_combo:
            townQuery = self.search_combo.get()  # Get the selected value from the combo box
            if townQuery:
                
                results = get_townSearchResults(townQuery) # Get search results from the database

                if results:
                    self.app.search_results_page.display_results(results)
                    
                else:
                    self.display_results(results)
                    # Displays results not found
                    results_label = tk.Label(self.app.search_results_page.results_frame, text="No matches found!")
                    results_label.grid(row=1, column=0, padx=5, pady=5)

                results_label2 = tk.Label(self.app.search_results_page.results_frame, text=f"Showing results for: {townQuery}")
                results_label2.grid(row=0, column=0, padx=5, pady=5)
                    
            else:
                messagebox.showwarning("Input required", "Please enter a search term.")
            
            
        else:
            nameQuery = self.search_entry.get()  # Get text from the entry bar
            if nameQuery:
                
                results = get_nameSearchResults(nameQuery)

                if results:
                    self.app.search_results_page.display_results(results)
                    
                else:
                    self.app.search_results_page.display_results(results)
                    # Displays results not found
                    results_label = tk.Label(self.app.search_results_page.results_frame, text="No matches found!")
                    results_label.grid(row=1, column=0, padx=5, pady=5)

                results_label2 = tk.Label(self.app.search_results_page.results_frame, text=f"Showing results for: {nameQuery}") 
                results_label2.grid(row=0, column=0, padx=5, pady=5)
                    
            else:
                messagebox.showwarning("Input required", "Please enter a search term.")
        

        

    # Function to toggle between entry and combo box
    def toggle_input(self):
        global is_combo
        if self.is_combo:
            # Replace combo box with entry bar
            self.search_combo.pack_forget()
            self.search_entry.pack(side="left", padx=5)
            self.toggle_button.config(text="Search by Location")
        else:
            # Replace entry bar with combo box
            self.search_entry.pack_forget()
            self.search_combo.pack(side="left", padx=5)
            self.toggle_button.config(text="Search by Name")
        self.is_combo = not self.is_combo


        
    # Function to reset user inputs and send user back to login screen
    def logout(self):
        
        # Reset entry boxes 
        self.app.loginpage.username_entry.delete(0, tk.END)
        self.app.loginpage.password_entry.delete(0, tk.END)
        self.app.accsettings.newusername_entry.delete(0, tk.END)
        self.app.accsettings.newpassword_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

        # Reset combo boxes 
        options = ["Chelmsford", "Southend", "Basildon", "Colchester", "Brentwood", "Canvey Island"]
        self.app.regpage.combo_box.set(options[0])
        self.app.accsettings.newcombo_box.set(options[0])
        self.search_combo.set(options[0])

        # Set search bar to "Search by name"
        self.is_combo = True
        self.toggle_input()

        self.user_details = None  # Clear user details on logout
        self.app.show_page("loginpage")
               



#######################################################################



class RegistrationPage(Page):

    def create_widgets(self):
        
        # Title labels
        title_label = tk.Label(self,
              text="Restaurant Booking App",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        title_label.pack()
        
        title_label2 = tk.Label(self,
              text="Register:",
              font=('Arial',20),
              bd = 5,
              padx=20)
        title_label2.pack(pady=10)

        

        # Create a label for the dropdown menu
        label = tk.Label(self, text="Select your location:")
        label.pack(pady=10)

        # Create a Combobox (dropdown menu) with options
        options = ["Chelmsford", "Southend", "Basildon", "Colchester", "Brentwood", "Canvey Island"]
        self.combo_box = ttk.Combobox(self, values=options, state="readonly")  # Set state to "readonly"
        self.combo_box.set(options[0])  # Set default selection to "Chelmsford"
        self.combo_box.pack(pady=10)

        # Sign up button to add user details to udat
        sign_up = tk.Button(self, text="Sign Up", command=self.sign_up)
        sign_up.pack(pady=10)

        # Backwards button to go to the login page
        backward_button = tk.Button(self, text="Back", command=lambda: self.app.show_page("loginpage"))
        backward_button.pack(pady=10)


       


    # Function to add add details to udat then return user to login screen
    def sign_up(self):
        username = self.app.loginpage.username_entry.get()
        password = self.app.loginpage.password_entry.get()
        town = self.combo_box.get()
    
        # added details to database
        add_user(username, password, town)

        # created user object from details in self
        self.app.user_details = User(username, password, town) 
        
        self.app.show_page("loginpage")


#######################################################################
        

class AccountSettingsPage(Page):

    def create_widgets(self):

        # Title labels
        title_label = tk.Label(self,
              text="Account Settings",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        title_label.pack()
        
        title_label2 = tk.Label(self,
              text="Enter new details:",
              font=('Arial',20),
              bd = 5,
              padx=20)
        title_label2.pack(pady=10)

        # Create and place the new username label and entry
        newusername_label = tk.Label(self, text="New username:")
        newusername_label.pack()
        self.newusername_entry = tk.Entry(self)
        self.newusername_entry.pack()
        
        # Create and place the new password label and entry
        newpassword_label = tk.Label(self, text="New password:")
        newpassword_label.pack()
        self.newpassword_entry = tk.Entry(self, show="*")  # Show asterisks for password
        self.newpassword_entry.pack()

        # Creates a dropdown for the new location
        newlocation_label = tk.Label(self, text="New location:")
        newlocation_label.pack()
        options = ["Chelmsford", "Southend", "Basildon", "Colchester", "Brentwood", "Canvey Island"]
        self.newcombo_box = ttk.Combobox(self, values=options, state="readonly")  
        self.newcombo_box.set(options[0]) 
        self.newcombo_box.pack(pady=10)
        
        # Create and place the confirm button to update settings
        confirm_button = tk.Button(self, text="Confirm", command=self.user_update_account)
        confirm_button.pack(pady=10)
        
        # Creating delete account button
        delete_account = tk.Button(self, text="Delete Account", command=self.user_delete_account )
        delete_account.pack()


        # Backwards button to go to the home page
        backward_button = tk.Button(self, text="Back", command=lambda: self.app.show_page("homepage"))
        backward_button.pack(pady=10)




    # Function to delete account details from database
    def user_delete_account(self):
        if self.app.user_details:
            self.app.user_details.delete_account()
        self.app.homepage.logout()
        self.app.show_page("loginpage")

    # Function to update account details in database
    def user_update_account(self):
        
        self.newusername = self.newusername_entry.get()
        self.newpassword = self.newpassword_entry.get()
        self.newtown = self.newcombo_box.get()

        if check_credentials(self.newusername, self.newpassword):
            messagebox.showerror("Register Failed","Username and Password already exists")
        elif self.newusername and self.newpassword:
            if self.app.user_details:
                self.app.user_details.update_account(self.newusername, self.newpassword, self.newtown)
            self.app.show_page("homepage")
            self.newusername_entry.delete(0, tk.END)
            self.newpassword_entry.delete(0, tk.END)
            self.app.homepage.local_Restaurants() # Updates user's nearby restaurants
        else:
            messagebox.showerror("Register Failed","Insufficient data entered")
        


#######################################################################
        

class RestaurantPage(Page):

    def create_widgets(self):
        
        self.restaurantName_label = tk.Label(self,
              text="Restaurant Name",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        self.restaurantName_label.pack()




        # Create the left frame
        self.left_frame = tk.Frame(self, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        # Backwards button to go to the home page
        backward_button = tk.Button(self.left_frame, text="Back", command=self.app.homepage.favourite_Restaurants)
        backward_button.pack(pady=10)

        # Confirm Button
        confirm_button = tk.Button(self.left_frame, text="Confirm", command = lambda: self.app.show_page("menupage"))
        confirm_button.pack(pady=10)

        # Create the favourite button
        self.favourite_button = tk.Button(self.left_frame, text="Favourite", command=self.add_favourite)
        self.favourite_button.pack(pady=10)    



        # Photo of the restaurant
        self.restaurant_icon = tk.PhotoImage(file='mcdonalds_icon.png')

        self.restaurantPhoto = tk.Label(self.left_frame, image=self.restaurant_icon)
        self.restaurantPhoto.pack()

        self.restaurantPhoto.image = self.restaurant_icon

        
        
        
        self.rating_label = tk.Label(self,
              text="Rating: ",
              font=('Arial',20),
              bd = 5,
              padx=20)
        self.rating_label.pack(pady=10)

        self.openingTimes_label = tk.Label(self,
              text="Opening Times: ",
              font=('Arial',20),
              bd = 5,
              padx=20)
        self.openingTimes_label.pack(pady=10)

        self.town_label = tk.Label(self,
              text="Town:",
              font=('Arial',20),
              bd = 5,
              padx=20)
        self.town_label.pack(pady=10)

        self.description_label = tk.Text(self, wrap=tk.WORD, width=45, height=15)
        self.description_label.pack()
        

        
    #returns the information saved in the database about the restaurant selected then displays it on the restaurant home page
    def open_Restaurant(self, restaurantName):
        
        restaurant_id, restaurant_town, description, openingTime, closingTime, rating, iconName = get_restaurantDetails(restaurantName) 

        self.restaurant_icon.config(file=iconName)
        self.restaurantName_label.config(text=restaurantName)
        
        self.rating_label.config(text=f"Rating: {rating}") 
        self.openingTimes_label.config(text=f"Opening Times: {openingTime}am - {closingTime}pm")
        self.town_label.config(text=f"Town: {restaurant_town}")
        
        self.description_label.config(state=tk.NORMAL)
        self.description_label.delete('1.0', tk.END)
        self.description_label.insert(tk.END, description)
        self.description_label.config(state=tk.DISABLED)

        # created restaurant object from details in self
        self.app.restaurant_details = Restaurant(restaurant_id, restaurantName, restaurant_town, openingTime, closingTime, rating)

        self.check_favourite()# Check if restauranted has been favourited already
        self.app.menupage.reset_basket() # Refreshes the basket and displays the meals in the restaurant menu bar
        
        self.app.show_page("restaurantpage")


    # Function to mark a restaurant as a user's favourite
    def add_favourite(self):
        if self.app.user_details:
            user_id = self.app.user_details.get_ID()
        if self.app.restaurant_details:
            restaurant_id = self.app.restaurant_details.get_ID()
        add_favRestaurant(user_id, restaurant_id)

        self.favourite_button.config(text="Unfavourite", command=self.remove_favourite) # Update button text and command to "Unfavourite"
            



        
    # Function to unmark a restaurant as a user's favourite
    def remove_favourite(self):
        if self.app.user_details:
            user_id = self.app.user_details.get_ID()
        if self.app.restaurant_details:
            restaurant_id = self.app.restaurant_details.get_ID()
        remove_favRestaurant(user_id, restaurant_id)
        
        self.favourite_button.config(text="Favourite", command=self.add_favourite) # Update button text and command to "Favourite"

        
    # Function to check if a restaurant is a user's favourite
    def check_favourite(self):
        if self.app.user_details:
            user_id = self.app.user_details.get_ID()
        if self.app.restaurant_details:
            restaurant_id = self.app.restaurant_details.get_ID()

      
        if check_favRestaurant(user_id, restaurant_id): #Check favRestaurant database to see if both user and and restaurant's id can be found           
            self.favourite_button.config(text="Unfavourite", command=self.remove_favourite) #Update button text and command to "Unfavourite"
            
        else:
            self.favourite_button.config(text="Favourite", command=self.add_favourite)  # Update button text and command to "Favourite"
            

#######################################################################
            

class SearchResultsPage(Page):

  

    def create_widgets(self):

        
        resultsTitle_label = tk.Label(self,
              text="Search Results:",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        resultsTitle_label.pack()
       

        # Frame to display search results (hidden initially)
        self.results_frame = None

        

        # Create the bottom frame
        back_bar = tk.Frame(self, width=600)
        back_bar.pack(side=tk.BOTTOM )

        # Backwards button to go to the home page
        backward_button = tk.Button(back_bar, text="Back", command=lambda: self.app.show_page("homepage"))
        backward_button.pack(pady=10)





    def display_results(self, results):
        
        # Remove the existing results frame if it exists
        if self.results_frame:
            self.results_frame.destroy()

        # Create a new frame to display search results
        self.results_frame = tk.Frame(self, bg="lightgrey")
        self.results_frame.pack(padx=10, pady=10)
      

        self.icons = []   # Store references to all loaded images


        # Create a button for each result
        for index, result in enumerate(results):

            iconName2 = get_iconName2(result[0]) # Gets the filename of the icon with that restaurant name stored in the database and saves it as iconName2
            iconName2 = tk.PhotoImage(file=iconName2) # Load the icons
            iconName2 = iconName2.subsample(4, 4) # Resizing the image to 25% of its original size
            self.icons.append(iconName2) #Adds icons to list

      
            result_button = tk.Button(self.results_frame, image=iconName2, text=result[0], compound="top", 
                                      command=lambda r=result[0]: self.app.restaurant_page.open_Restaurant(r))
            result_button.grid(row=index+1, column=0, pady=5)
            
        self.app.show_page("searchResultsPage")



#######################################################################
        
        
class MenuPage(Page):

    def __init__(self, master, app):
        super().__init__(master, app)
        self.basket = {}  # Initialize the basket as a dictionary
        self.total_production_time = 0  # Variable to track the total production time

    def create_widgets(self):

        title_label = tk.Label(self,
              text="Menu",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        title_label.pack()

       
        # Create the info frame
        info_bar = tk.Frame(self, width=600)
        info_bar.pack()

        # Label displaying amount of items in basket
        self.basket_label = tk.Label(info_bar, text="Basket: 0 items", font=('Arial',15))
        self.basket_label.pack(side=tk.LEFT, padx=5, pady=20)

        # Label displaying the total cost of the user's basket
        self.price_label = tk.Label(info_bar, text="Total price: £0.00", font=('Arial',15))
        self.price_label.pack(side=tk.LEFT, padx=5)

        # Create the meal frame to hold the restaurant's meals
        self.meal_bar = tk.Frame(self, width=600, bg="lightgrey")
        self.meal_bar.pack(fill=tk.X)
        

        # Create the bottom frame
        back_bar = tk.Frame(self, width=600)
        back_bar.pack(side=tk.BOTTOM, pady=20)

        # Backwards button to go back to the restaurant home page
        backward_button = tk.Button(back_bar, text="Back", command=lambda: self.app.show_page("restaurantpage"))
        backward_button.pack(side=tk.LEFT, padx=5)

        # Delete button to remove most recently added meal from basket
        self.delete_button = tk.Button(back_bar, text="Delete", command=self.remove_from_basket)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Confirm Button to confirm order
        confirm_button = tk.Button(back_bar, text="Confirm", command=self.confirm_order)
        confirm_button.pack(side=tk.LEFT, padx=5)

        # Label displaying total production time
        self.time_label = tk.Label(info_bar, text="Total time: 0 mins", font=('Arial', 15))
        self.time_label.pack(side=tk.LEFT, padx=5)


       
        

   #Displays the number of items in and the total cost of the user's basket
    def display_basket(self):
        # Calculate total items by summing the quantities (first element in each list)
        total_items = sum(meal[0] for meal in self.basket.values())
        # Calculate total cost by summing (price * quantity) for each meal
        total_cost = sum(meal_price * meal[0] for meal_price, meal in self.basket.items())

        self.basket_label.config(text=f"Basket: {total_items} items")
        self.price_label.config(text=f"Total price: £{total_cost:.2f}")

        # Update the total time label
        self.time_label.config(text=f"Total time: {self.total_production_time} mins")


    #Displays the restaurant's meals as buttons in the meal frame
    def display_meals(self):

        if self.app.restaurant_details:
            restaurant_id = self.app.restaurant_details.restaurant_id #Gets the restaurant's id from the restaurant details object
        mealResults = get_restaurantMeals(restaurant_id)  #Retrieves the meal IDs of every meal associated with that restaurant id
        
        # Destroy existing meal buttons
        for widget in self.meal_bar.winfo_children():
                widget.destroy()

        
        #Display no meals if the restaurant doesn't have any meals addded to the database
        if not mealResults: 
            no_meals_label = tk.Label(self.meal_bar, text="No meals available for this restaurant.")
            no_meals_label.pack(pady=10)
            return

      
        meal_icon = tk.PhotoImage(file="meal_icon.png")  # Load the meal icon
        meal_icon_resized = meal_icon.subsample(4, 4)  # Resizing the image to 25% of its original size
    
        # Keep a reference to the image to prevent garbage collection
        self.meal_icon = meal_icon_resized  # Store it as an instance variable
       
                
        # Create a button for each meal ID
        for index, mealResult in enumerate(mealResults):

            mealName, mealPrice, mealTime = get_mealDetails(mealResult) #Retrieves the information about the meal

            
            
            
                    
            meal_button = tk.Button(self.meal_bar, image=self.meal_icon, text=f"{mealName} Price: £{mealPrice:.2f}", compound="top",
                                    command=lambda meal_price=mealPrice, meal_time=mealTime: self.add_to_basket(meal_price, meal_time))
            meal_button.pack(padx=5, side="left")

        
        self.app.show_page("menupage")



    # Adds meal to basket
    def add_to_basket(self, meal_price, meal_time):
        meal_price = float(meal_price)
        if meal_price in self.basket:
            self.basket[meal_price][0] += 1  # Update quantity
        else:
            self.basket[meal_price] = [1, meal_time]  # [quantity, production time]
        
        # Update the total production time
        self.total_production_time += meal_time

        self.display_basket() #Update the basket labels

    # Removes meal from basket
    def remove_from_basket(self):
        if self.basket:
            # Remove the most recently added item.
            # Iterate through keys to get the most recent price added
            most_recent_price = next(iter(self.basket.keys())) #retrieves the key of the most recently added meal
            meal_quantity, meal_time = self.basket[most_recent_price]

            if meal_quantity > 1:
                self.basket[most_recent_price][0] -= 1
                self.total_production_time -= meal_time
            else:
                del self.basket[most_recent_price]
                self.total_production_time -= meal_time

            self.display_basket() #Update the basket labels
        else:
            messagebox.showinfo("Basket Empty", "Your basket is already empty.")
            
    #Takes user to order page
    def confirm_order(self):
        if not self.basket: # Check if basket is empty
            messagebox.showinfo("Order Confirmation", "Your basket is empty. Please add items before confirming.") 
            return

        self.total_cost = sum(meal_price * meal_quantity[0] for meal_price, meal_quantity in self.basket.items()) 
        self.total_items = sum(meal_quantity[0] for meal_quantity in self.basket.values())
        
        self.app.show_page("orderpage")
        self.app.orderpage.order_options()#Displays the restaurants ordering options
        
        

        
    # Reset basket and production time 
    def reset_basket(self):
                
        self.basket = {}
        self.total_production_time = 0
        self.display_basket() # Reset the basket labels
        self.display_meals()  # Refresh the menu to reset the added items


    
        
    
        
        
    
class OrderPage(Page):

    def create_widgets(self):

        # Title labels
        title_label = tk.Label(self,
              text="Order",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        title_label.pack()

        title_label2 = tk.Label(self,
              text="How do you want to order?",
              font=('Arial',20),
              bd = 5,
              padx=20)
        title_label2.pack(pady=10)
      
        # Frame to store order option buttons button
        self.order_frame = tk.Frame(self, bg="lightgrey")
        self.order_frame.pack() 
    
        backward_button = tk.Button(self, text="Back", command=lambda: self.app.show_page("menupage"))
        backward_button.pack(side=tk.BOTTOM, padx=5, pady=20)

    # Displays the ordering options to the user
    def order_options(self):

        if self.app.restaurant_details:
            restaurant_id = self.app.restaurant_details.restaurant_id

        supportsTakeaway, supportsDelivery, supportsReservation = get_orderOptions(restaurant_id) #Retrieves the ordering options about the restaurant with that associated id

        # Destroy the current frame 
        self.order_frame.destroy()

        # Create the new frame
        self.order_frame = tk.Frame(self)
        self.order_frame.pack()
        

        if supportsTakeaway == 1:
            takeaway_button = tk.Button(self.order_frame, text="Takeaway", command= lambda: self.app.purchasepage.purchase_info("Takeaway"))
            takeaway_button.pack(pady=5)

        if supportsDelivery == 1:
            delivery_button = tk.Button(self.order_frame, text="Delivery", command= lambda: self.app.purchasepage.purchase_info("Delivery"))
            delivery_button.pack(pady=5)

        if supportsReservation == 1:
            reservation_button = tk.Button(self.order_frame, text="Book Reservation", command=  self.app.reservationpage.get_timeslots )
            reservation_button.pack(pady=5)

        else:
            eatIn_button = tk.Button(self.order_frame, text="Eat In", command= lambda: self.app.purchasepage.purchase_info("Eat In"))
            eatIn_button.pack(pady=5)


class PurchasePage(Page):

    def create_widgets(self):

        # Title labels
        self.title_label = tk.Label(self,
              text="Order for restaurant:",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        self.title_label.pack()

        # Frame to store labels displaying purchase info
        self.purchaseInfo_frame = tk.Frame(self, bg="lightgrey")
        self.purchaseInfo_frame.pack() 

      
        # Create the bottom frame
        back_bar = tk.Frame(self, width=600)
        back_bar.pack(side=tk.BOTTOM, pady=20)

        backward_button = tk.Button(back_bar, text="Back", command=lambda: self.app.show_page("orderpage"))
        backward_button.pack(side=tk.LEFT, padx=5)

        #Button to make final purchase
        purchase_button = tk.Button(back_bar, text="Purchase", command=self.purchase)
        purchase_button.pack(side=tk.LEFT, padx=5)


    # Creates the labels displaying the purchase info to the user
    def purchase_info(self, orderType):
        if self.app.restaurant_details:
            restaurantName = self.app.restaurant_details.restaurantName #Gets the restaurant's id from the restaurant details object
            
        # Changes the title label depending on the restaurant name and order type
        self.title_label.config(text=f"{orderType} order for restaurant: {restaurantName}")

        # Destroy the current frame 
        self.purchaseInfo_frame.destroy()

        # Create the new frame
        self.purchaseInfo_frame = tk.Frame(self)
        self.purchaseInfo_frame.pack()

        #Stores values from the menupage as variables
        self.total_price = self.app.menupage.total_cost 
        self.total_time = self.app.menupage.total_production_time


       
               
        if orderType == "Delivery":
            self.total_price += 1 # Update price with delivery fee
            self.total_time += 5 # Update time with delivery time

            fee_label = tk.Label(self.purchaseInfo_frame, # Display delivery fee
              text="Delivery Fee: £1.00",
              font=('Arial',15),
              bd = 5,
              padx=20)
            fee_label.pack(pady=10)

            deliveryTime_label = tk.Label(self.purchaseInfo_frame, # Display delivery time
              text="Delivery Time: 5 mins",
              font=('Arial',15),
              bd = 5,
              padx=20)
            deliveryTime_label.pack(pady=10)
   
    

        # Creates price, quantity and time labels to display the purchase information
        price_label = tk.Label(self.purchaseInfo_frame,
              text=f"Final Price: £{self.total_price:.2f}",
              font=('Arial',15),
              bd = 5,
              padx=20)
        price_label.pack(pady=10)

        quantity_label = tk.Label(self.purchaseInfo_frame,
              text=f"Number of meals purchased: {self.app.menupage.total_items}",
              font=('Arial',15),
              bd = 5,
              padx=20)
        quantity_label.pack(pady=10)

        time_label = tk.Label(self.purchaseInfo_frame,
              text=f"Food will be ready in: {self.total_time} mins",
              font=('Arial',15),
              bd = 5,
              padx=20)
        time_label.pack(pady=10)
        
        # Edit text to fit the delivery option
        if orderType == "Delivery":
            time_label.config(text=f"Food will be delivered in: {self.total_time} mins")
             
        self.app.show_page("purchasepage")

    #Displays price and time to use then returns them to homepage
    def purchase(self):

        current_time = datetime.now() #Get current time
        ready_time = current_time + timedelta(minutes=self.total_time)# Adds the time meal will be ready/delivered to current time

        
        messagebox.showinfo("Order Confirmation",
        f'''Your order has been placed!
        Total cost: £{self.total_price:.2f}
        Meals purchased: {self.app.menupage.total_items}
        Food will be ready at: {ready_time.strftime('%H:%M %d/%m/%Y ')}''')
        self.app.show_page("homepage")


class ReservationPage(Page):

    def create_widgets(self):

        # Title labels
        self.title_label = tk.Label(self,
              text="Reservation",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        self.title_label.pack()

        title_label2 = tk.Label(self,
              text="Make a reservation:",
              font=('Arial',20),
              bd = 5,
              padx=20)
        title_label2.pack(pady=10)
        
        # Create Comboboxes (dropdown menus) with options
        people_label = tk.Label(self, text="Number of people:")
        people_label.pack()
        people_options = [1, 2, 3, 4, 5]
        self.people_combo_box = ttk.Combobox(self, values=people_options, state="readonly")  # Set state to "readonly"
        self.people_combo_box.set(people_options[0])  # Set default selection to 1
        self.people_combo_box.pack(pady=10)
       
        table_label = tk.Label(self, text="Table Number:")
        table_label.pack()
        table_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.table_combo_box = ttk.Combobox(self, values=table_options, state="readonly")  
        self.table_combo_box.set(table_options[0]) 
        self.table_combo_box.pack(pady=10)
        
        time_label = tk.Label(self, text="Timeslot:")
        time_label.pack()
        self.time_options = [""]
        self.time_combo_box = ttk.Combobox(self, values=self.time_options, state="readonly")  
        self.time_combo_box.pack(pady=10)
    
        date_label = tk.Label(self, text="Date:")
        date_label.pack()
        self.date_options = [""]
        self.date_combo_box = ttk.Combobox(self, values=self.date_options, state="readonly") 
        self.date_combo_box.pack(pady=10)  
        
        # Create the bottom frame
        back_bar = tk.Frame(self, width=600)
        back_bar.pack(side=tk.BOTTOM, pady=20)

        backward_button = tk.Button(back_bar, text="Back", command=lambda: self.app.show_page("orderpage"))
        backward_button.pack(side=tk.LEFT, padx=5)

        #Button to make reservation
        submit_button = tk.Button(back_bar, text="Submit",command= self.check_reservation)
        submit_button.pack(side=tk.LEFT, padx=5)
        

    # Edits the available reservation timeslots to match the restaurant's opening and closing times
    def get_timeslots(self):
        if self.app.restaurant_details:
            openingTime = self.app.restaurant_details.openingTime #Gets the restaurant's opening time from the restaurant details object
            closingTime = self.app.restaurant_details.closingTime #Gets the restaurant's closing time from the restaurant details object
            
        #Converts the times to 24hr format
        if openingTime == 12:
            openingTime = 0  # Convert to 0 for midnight
        if closingTime != 12:
            closingTime += 12
        closingTime -= 1 #Ensures last timeslot doesn't show

        # Create start and end time as datetime objects
        start_time = datetime.strptime(f"{openingTime:02d}:00", "%H:%M")
        end_time = datetime.strptime(f"{closingTime:02d}:00", "%H:%M")

        # Create a timedelta for 1 hour
        time_interval = timedelta(hours=1)

        # Initialize the current time variable
        current_time = start_time

        # Clear previous time options
        self.time_options.clear()

        # Collect times in increments of 1 hour
        while current_time <= end_time:
            self.time_options.append(current_time.strftime("%H:%M"))  # Format time to 24-hour format
            current_time += time_interval
            
        # Update the time options Combobox with new times
        self.time_combo_box['values'] = self.time_options
        if self.time_options:
            self.time_combo_box.set(self.time_options[0])  # Set the first available time as the default



        # Clear previous date options
        self.date_options.clear()

        # Get the current date and time
        today = datetime.now()  
       
        for i in range(7):
            next_day = today + timedelta(days=i)  # Add 'i' days to today
            self.date_options.append(next_day.strftime("%d/%m/%Y"))  # Format the date and add to thedate options list

        # Update the date options Combobox with new times
        self.date_combo_box['values'] = self.date_options
        if self.date_options:
            self.date_combo_box.set(self.date_options[0])  # Set the first available date as the default

        self.people_combo_box.set(1) #Reset people number
        self.table_combo_box.set(1) #Reset table number
    

        self.app.show_page("reservationpage")

        
        
    #Checks for reservation clashes
    def check_reservation(self):
        
        if self.app.restaurant_details:
            restaurant_id = self.app.restaurant_details.restaurant_id

        # Get reservation details from the database
        self.time = self.time_combo_box.get()
        self.date = self.date_combo_box.get()
        self.tableNo = self.table_combo_box.get()
        self.noPeople = self.people_combo_box.get()
        
        # Check if there's already a reservation with the same time and date
        if check_reservation(self.time, self.date, restaurant_id):
            messagebox.showerror("Reservation Failed", "Timeslot already exists")
            return
        
        else:
            self.app.res_purchasepage.purchase_info() #Opens the reservation purchase page


    #Displays reservation bill then returns user to homepage
    def purchase(self):

        if self.app.restaurant_details:
            restaurant_id = self.app.restaurant_details.restaurant_id
        if self.app.user_details:
            user_id = self.app.user_details.user_id

        # Add reservation to database
        add_reservation(self.time, self.date, self.tableNo, self.noPeople, user_id, restaurant_id)
        
        messagebox.showinfo("Reservation Confirmation",
        f'''Your reservation has been booked!
        Total cost: £{self.app.menupage.total_cost:.2f}
        Meals purchased: {self.app.menupage.total_items}
        Table number: {self.tableNo}
        Timeslot: {self.time} {self.date}''')
        
        self.app.show_page("homepage") 
    

        

class ReservationPurchasePage(Page):

    def create_widgets(self):

        # Title labels
        self.title_label = tk.Label(self,
              text="Reservation for restaurant:",
              font=('Arial',30,'bold'),
              bd = 5,
              padx=20)
        self.title_label.pack()

        # Frame to store labels displaying purchase info
        self.purchaseInfo_frame = tk.Frame(self)
        self.purchaseInfo_frame.pack() 
      
        # Create the bottom frame
        back_bar = tk.Frame(self, width=600)
        back_bar.pack(side=tk.BOTTOM, pady=20)

        backward_button = tk.Button(back_bar, text="Back", command=lambda: self.app.show_page("reservationpage"))
        backward_button.pack(side=tk.LEFT, padx=5)

        #Button to make final purchase
        purchase_button = tk.Button(back_bar, text="Purchase", command=self.app.reservationpage.purchase)
        purchase_button.pack(side=tk.LEFT, padx=5)


    # Creates the labels displaying the purchase info to the user
    def purchase_info(self):
        
        if self.app.restaurant_details:
            restaurantName = self.app.restaurant_details.restaurantName #Gets the restaurant's id from the restaurant details object
            
        # Changes the title label depending on the restaurant name 
        self.title_label.config(text=f"Reservation for restaurant: {restaurantName}")

        # Destroy the current frame 
        self.purchaseInfo_frame.destroy()

        # Create the new frame
        self.purchaseInfo_frame = tk.Frame(self)
        self.purchaseInfo_frame.pack()

        # Creates table number, timeslot, price and meal quantity labels to display the purchase information
        tableNo_label = tk.Label(self.purchaseInfo_frame,
              text=f"Table number: {self.app.reservationpage.tableNo}",
              font=('Arial',15),
              bd = 5,
              padx=20)
        tableNo_label.pack(pady=10)

        timeslot_label = tk.Label(self.purchaseInfo_frame,
              text=f"Timeslot: {self.app.reservationpage.time} {self.app.reservationpage.date}",
              font=('Arial',15),
              bd = 5,
              padx=20)
        timeslot_label.pack(pady=10)
        
        price_label = tk.Label(self.purchaseInfo_frame,
              text=f"Final Price: £{self.app.menupage.total_cost:.2f}",
              font=('Arial',15),
              bd = 5,
              padx=20)
        price_label.pack(pady=10)

        quantity_label = tk.Label(self.purchaseInfo_frame,
              text=f"Number of meals purchased: {self.app.menupage.total_items}",
              font=('Arial',15),
              bd = 5,
              padx=20)
        quantity_label.pack(pady=10)

        
        self.app.show_page("res_purchasepage")


 
              

###


 
        
###

# Create the main window
window = tk.Tk()

# Create the app object
app = App(window)
  

# Start the Tkinter event loop
window.mainloop()


