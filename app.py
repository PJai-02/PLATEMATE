
# import streamlit as st
# import pandas as pd
# import pydeck as pdk

# # Optional: Inject custom CSS from assets/styles.css
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# # Uncomment the next line if you have custom CSS in assets/styles.css
# # local_css("assets/styles.css")

# # Optional: Display logo from assets/logo.png
# try:
#     st.image("assets/PROMPTGENQR.png", width=150)
# except Exception as e:
#     st.warning("Logo image not found in assets/logo.png.")

# # Set the title of the app
# st.title("PlateMate: Online Food Ordering System")

# # Initialize session state for cart if not already present
# if 'cart' not in st.session_state:
#     st.session_state.cart = []

# # Sidebar: Choose a feature to explore
# feature = st.sidebar.selectbox("Select Feature", 
#                                ["Browse Restaurants", "Food Minimisation", "Collaborative Ordering"])

# # ------------------------------------
# # Sample Data for Restaurants
# # (Using coordinates from major Indian cities)
# # ------------------------------------
# restaurant_data = {
#     "name": ["Restaurant A", "Restaurant B", "Restaurant C"],
#     "lat": [28.7041, 19.0760, 12.9716],   # Delhi, Mumbai, Bangalore
#     "lon": [77.1025, 72.8777, 77.5946],
#     "is_local": [True, False, True],
#     "daily_deal": [True, False, True]
# }
# restaurants_df = pd.DataFrame(restaurant_data)

# # ------------------------------------
# # Extended Sample Menus for Each Restaurant
# # ------------------------------------
# restaurant_menus = {
#     "Restaurant A": [
#         {"item": "Pizza", "price": 250},
#         {"item": "Burger", "price": 150},
#         {"item": "Fries", "price": 50},
#         {"item": "Pasta", "price": 200},
#         {"item": "Salad", "price": 120}
#     ],
#     "Restaurant B": [
#         {"item": "Sushi", "price": 300},
#         {"item": "Ramen", "price": 220},
#         {"item": "Tempura", "price": 180},
#         {"item": "Miso Soup", "price": 80}
#     ],
#     "Restaurant C": [
#         {"item": "Tacos", "price": 100},
#         {"item": "Burrito", "price": 180},
#         {"item": "Nachos", "price": 120},
#         {"item": "Quesadilla", "price": 150},
#         {"item": "Guacamole", "price": 90}
#     ]
# }

# # Function to add selected items to the cart
# def add_to_cart(selected_items, restaurant):
#     for item in selected_items:
#         st.session_state.cart.append({"restaurant": restaurant, "item": item})
#     st.success("Items added to cart!")

# # ------------------------------------
# # Feature: Browse Restaurants
# # ------------------------------------
# if feature == "Browse Restaurants":
#     st.header("Browse Restaurants")
    
#     # Use PyDeck to show a map of India
#     view_state = pdk.ViewState(
#         latitude=20.5937,   # approximate center latitude for India
#         longitude=78.9629,  # approximate center longitude for India
#         zoom=4,
#         pitch=0
#     )
    
#     # Create a ScatterplotLayer with restaurant markers
#     layer = pdk.Layer(
#         "ScatterplotLayer",
#         data=restaurants_df,
#         get_position=["lon", "lat"],
#         get_radius=50000,
#         get_fill_color=[0, 128, 255, 160],
#         pickable=True
#     )
    
#     # Create and display the deck instance
#     deck = pdk.Deck(
#         initial_view_state=view_state,
#         layers=[layer],
#         map_style="mapbox://styles/mapbox/streets-v11"
#     )
    
#     st.subheader("Map of Restaurants in India")
#     st.pydeck_chart(deck)
    
#     # Let the user select a restaurant
#     restaurant_choice = st.selectbox("Select a Restaurant", restaurants_df["name"].tolist())
    
#     st.subheader(f"Menu for {restaurant_choice}")
#     menu = restaurant_menus.get(restaurant_choice, [])
#     if menu:
#         menu_df = pd.DataFrame(menu)
#         st.table(menu_df)
        
#         # Create a list of menu items with their prices as strings
#         menu_items = [f"{item['item']} (₹{item['price']})" for item in menu]
#         selected_menu_items = st.multiselect("Select items to add to cart", menu_items)
        
#         if st.button("Add Selected Items to Cart"):
#             add_to_cart(selected_menu_items, restaurant_choice)
#     else:
#         st.write("No menu available for this restaurant.")
    
#     # Display the current cart contents
#     if st.session_state.cart:
#         st.subheader("Cart")
#         cart_df = pd.DataFrame(st.session_state.cart)
#         st.table(cart_df)
#         total_cost = 0
#         for cart_item in st.session_state.cart:
#             item_str = cart_item["item"]
#             try:
#                 price_str = item_str.split("₹")[1].rstrip(")")
#                 price = float(price_str)
#                 total_cost += price
#             except Exception as e:
#                 st.error(f"Error calculating price for {item_str}: {e}")
#         st.write(f"Total Cost: ₹{total_cost}")

# # ------------------------------------
# # Feature: Food Minimisation
# # ------------------------------------
# elif feature == "Food Minimisation":
#     st.header("Food Minimisation - Discounted Leftover Food")
    
#     discount_data = {
#         "Restaurant": ["Restaurant A", "Restaurant C"],
#         "Item": ["Burger", "Burrito"],
#         "Original Price": [150, 180],
#         "Discount Price": [100, 120]
#     }
#     discount_df = pd.DataFrame(discount_data)
#     st.table(discount_df)
    
#     st.write("Order discounted leftover food items at a discount price!")
#     selected_item = st.selectbox("Select an Item", discount_df["Item"].tolist())
#     if st.button("Order Discounted Item"):
#         st.success(f"Your order for {selected_item} has been placed at a discounted price!")

# # ------------------------------------
# # Feature: Collaborative Ordering
# # ------------------------------------
# elif feature == "Collaborative Ordering":
#     st.header("Collaborative Ordering - Share the Bill")
    
#     st.write("Select items to add to your collaborative order:")
#     all_items = []
#     for restaurant, items in restaurant_menus.items():
#         for item in items:
#             all_items.append(f"{restaurant} - {item['item']} (₹{item['price']})")
    
#     selected_items = st.multiselect("Select Items", all_items)
    
#     if selected_items:
#         total_cost = 0
#         for selected in selected_items:
#             try:
#                 price_str = selected.split("₹")[1].rstrip(")")
#                 price = float(price_str)
#                 total_cost += price
#             except Exception as e:
#                 st.error(f"Error parsing price: {e}")
#         st.write(f"Total Order Cost: ₹{total_cost}")
        
#         num_people = st.number_input("Enter number of people sharing the bill", min_value=1, value=1)
#         if num_people > 0:
#             share = total_cost / num_people
#             st.write(f"Each person pays: ₹{share:.2f}")
        
#         if st.button("Place Collaborative Order"):
#             st.success("Collaborative order placed successfully!")
#     else:
#         st.write("No items selected for collaborative ordering.")

import streamlit as st
import pandas as pd
import pydeck as pdk

# Optional: Function to load custom CSS from assets/styles.css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Uncomment if you want to load custom CSS:
# local_css("assets/styles.css")

# Optional: Display logo (ensure assets/logo.png exists)
try:
    st.image("assets/PROMPTGENQR.png", width=150)
except Exception as e:
    st.warning("Logo image not found in assets/logo.png.")

# App Title
st.title("PlateMate: Online Food Ordering System")

# Initialize session state for cart if not already present
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Sidebar: Choose a feature to explore
feature = st.sidebar.selectbox("Select Feature", 
                               ["Browse Restaurants", "Food Minimisation", "Collaborative Ordering"])

# ------------------------------------
# Sample Data for Restaurants (Coordinates in India)
# ------------------------------------
restaurant_data = {
    "name": ["Restaurant A", "Restaurant B", "Restaurant C"],
    "lat": [28.7041, 19.0760, 12.9716],   # Delhi, Mumbai, Bangalore
    "lon": [77.1025, 72.8777, 77.5946],
    "is_local": [True, False, True],
    "daily_deal": [True, False, True]
}
restaurants_df = pd.DataFrame(restaurant_data)

# ------------------------------------
# Extended Sample Menus for Each Restaurant
# ------------------------------------
restaurant_menus = {
    "Restaurant A": [
        {"item": "Pizza", "price": 250},
        {"item": "Burger", "price": 150},
        {"item": "Fries", "price": 50},
        {"item": "Pasta", "price": 200},
        {"item": "Salad", "price": 120}
    ],
    "Restaurant B": [
        {"item": "Sushi", "price": 300},
        {"item": "Ramen", "price": 220},
        {"item": "Tempura", "price": 180},
        {"item": "Miso Soup", "price": 80}
    ],
    "Restaurant C": [
        {"item": "Tacos", "price": 100},
        {"item": "Burrito", "price": 180},
        {"item": "Nachos", "price": 120},
        {"item": "Quesadilla", "price": 150},
        {"item": "Guacamole", "price": 90}
    ]
}

# Function to add selected items to the cart
def add_to_cart(selected_items, restaurant):
    for item in selected_items:
        st.session_state.cart.append({"restaurant": restaurant, "item": item})
    st.success("Items added to cart!")

# ------------------------------------
# Feature: Browse Restaurants (with Cart and Remove feature)
# ------------------------------------
if feature == "Browse Restaurants":
    st.header("Browse Restaurants")
    
    # Use PyDeck to show a map of India
    view_state = pdk.ViewState(
        latitude=20.5937,   # approximate center of India
        longitude=78.9629,
        zoom=4,
        pitch=0
    )
    
    # Create a ScatterplotLayer with restaurant markers
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=restaurants_df,
        get_position=["lon", "lat"],
        get_radius=50000,
        get_fill_color=[0, 128, 255, 160],
        pickable=True
    )
    
    deck = pdk.Deck(
        initial_view_state=view_state,
        layers=[layer],
        map_style="mapbox://styles/mapbox/streets-v11"
    )
    
    st.subheader("Map of Restaurants in India")
    st.pydeck_chart(deck)
    
    # Let the user select a restaurant
    restaurant_choice = st.selectbox("Select a Restaurant", restaurants_df["name"].tolist())
    
    st.subheader(f"Menu for {restaurant_choice}")
    menu = restaurant_menus.get(restaurant_choice, [])
    if menu:
        menu_df = pd.DataFrame(menu)
        st.table(menu_df)
        
        # Create list of menu items with prices as strings
        menu_items = [f"{item['item']} (₹{item['price']})" for item in menu]
        selected_menu_items = st.multiselect("Select items to add to cart", menu_items)
        
        if st.button("Add Selected Items to Cart"):
            add_to_cart(selected_menu_items, restaurant_choice)
    else:
        st.write("No menu available for this restaurant.")
    
    # Display current cart contents and allow removal
    if st.session_state.cart:
        st.subheader("Cart")
        # Create a list for display and calculation
        cart_items_display = []
        total_cost = 0
        
        for cart_item in st.session_state.cart:
            item_str = cart_item["item"]
            display_str = f"{cart_item['restaurant']} - {item_str}"
            cart_items_display.append(display_str)
            try:
                price_str = item_str.split("₹")[1].rstrip(")")
                price = float(price_str)
                total_cost += price
            except Exception as e:
                st.error(f"Error calculating price for {item_str}: {e}")
                
        st.table(pd.DataFrame(st.session_state.cart))
        st.write(f"Total Cost: ₹{total_cost}")
        
        # Multi-select to remove items from the cart
        remove_items = st.multiselect("Select items to remove from cart", cart_items_display)
        if st.button("Remove Selected Items"):
            new_cart = []
            for cart_item in st.session_state.cart:
                display_str = f"{cart_item['restaurant']} - {cart_item['item']}"
                if display_str not in remove_items:
                    new_cart.append(cart_item)
            st.session_state.cart = new_cart
            st.success("Selected items removed from cart!")

# ------------------------------------
# Feature: Food Minimisation
# ------------------------------------
elif feature == "Food Minimisation":
    st.header("Food Minimisation - Discounted Leftover Food")
    
    discount_data = {
        "Restaurant": ["Restaurant A", "Restaurant C"],
        "Item": ["Burger", "Burrito"],
        "Original Price": [150, 180],
        "Discount Price": [100, 120]
    }
    discount_df = pd.DataFrame(discount_data)
    st.table(discount_df)
    
    st.write("Order discounted leftover food items at a discount price!")
    selected_item = st.selectbox("Select an Item", discount_df["Item"].tolist())
    if st.button("Order Discounted Item"):
        st.success(f"Your order for {selected_item} has been placed at a discounted price!")

# ------------------------------------
# Feature: Collaborative Ordering (Share the Bill)
# ------------------------------------
elif feature == "Collaborative Ordering":
    st.header("Collaborative Ordering - Share the Bill")
    
    st.write("Select items to add to your collaborative order:")
    all_items = []
    for restaurant, items in restaurant_menus.items():
        for item in items:
            all_items.append(f"{restaurant} - {item['item']} (₹{item['price']})")
    
    selected_items = st.multiselect("Select Items", all_items)
    
    if selected_items:
        total_cost = 0
        for selected in selected_items:
            try:
                price_str = selected.split("₹")[1].rstrip(")")
                price = float(price_str)
                total_cost += price
            except Exception as e:
                st.error(f"Error parsing price: {e}")
        st.write(f"Total Order Cost: ₹{total_cost}")
        
        num_people = st.number_input("Enter number of people sharing the bill", min_value=1, value=1)
        if num_people > 0:
            share = total_cost / num_people
            st.write(f"Each person pays: ₹{share:.2f}")
        
        if st.button("Place Collaborative Order"):
            st.success("Collaborative order placed successfully!")
    else:
        st.write("No items selected for collaborative ordering.")
