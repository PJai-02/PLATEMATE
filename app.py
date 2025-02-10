
import streamlit as st
import pandas as pd
import pydeck as pdk

# Optional: Inject custom CSS if you have one
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Uncomment to load custom CSS:
# local_css("assets/styles.css")

# Optional: Display the logo from the assets folder
try:
    st.image("assets/platematelogo.png", width=150)
except Exception as e:
    st.warning("Logo image not found in assets/logo.png.")

# Set the title of the app
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
# Extended Sample Menus for Each Restaurant with Local Images
# ------------------------------------
restaurant_menus = {
    "Restaurant A": [
        {"item": "Pizza", "price": 250, "image": "assets/pizza.png"},
        {"item": "Burger", "price": 150, "image": "assets/burger.png"},
        {"item": "Fries", "price": 100, "image": "assets/fries.png"},
        {"item": "Pasta", "price": 300, "image": "assets/pasta.png"},
        {"item": "Salad", "price": 150, "image": "assets/salad.png"}
    ],
    "Restaurant B": [
        {"item": "Biryani", "price": 350, "image": "assets/biryani.png"},
        {"item": "Tandoori roti", "price": 200, "image": "assets/tandooriroti.png"},
        {"item": "Shawarma", "price": 150, "image": "assets/shawarma.png"},
        {"item": "Paneer Curry", "price": 180, "image": "assets/paneercurry.png"}
    ],
    "Restaurant C": [
        {"item": "Idly", "price": 100, "image": "assets/idly.png"},
        {"item": "Dosa", "price": 110, "image": "assets/dosa.png"},
        {"item": "Vada", "price": 80, "image": "assets/vada.png"},
        {"item": "Puri", "price": 90, "image": "assets/puri.png"},
        {"item": "Mysore Bajji", "price": 90, "image": "assets/mysorebajji.jpeg"}
    ]
}

# Function to add a single item to the cart and trigger animation
def add_to_cart(item, restaurant):
    st.session_state.cart.append({"restaurant": restaurant, "item": f"{item['item']} (₹{item['price']})"})
    st.success(f"Added {item['item']} to cart!")
    st.balloons()  # Show animation

# ------------------------------------
# Feature: Browse Restaurants (with Cart and Remove feature)
# ------------------------------------
if feature == "Browse Restaurants":
    st.header("Browse Restaurants")
    
    # Use PyDeck to show a map of India
    view_state = pdk.ViewState(
        latitude=20.5937,   # Center of India
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
        # Display each menu item with its image and an Add button
        for item in menu:
            col1, col2 = st.columns([1, 3])
            with col1:
                try:
                    st.image(item["image"], width=100)
                except Exception as e:
                    st.error(f"Error loading image for {item['item']}: {e}")
            with col2:
                st.markdown(f"**{item['item']}**")
                st.write(f"Price: ₹{item['price']}")
                if st.button(f"Add {item['item']} to Cart", key=f"{restaurant_choice}_{item['item']}"):
                    add_to_cart(item, restaurant_choice)
    else:
        st.write("No menu available for this restaurant.")
    
    # Display current cart contents and allow removal
    if st.session_state.cart:
        st.subheader("Cart")
        cart_items_display = []
        total_cost = 0
        for cart_item in st.session_state.cart:
            display_str = f"{cart_item['restaurant']} - {cart_item['item']}"
            cart_items_display.append(display_str)
            try:
                price_str = cart_item["item"].split("₹")[1].rstrip(")")
                price = float(price_str)
                total_cost += price
            except Exception as e:
                st.error(f"Error calculating price for {cart_item['item']}: {e}")
        st.table(pd.DataFrame(st.session_state.cart))
        st.write(f"Total Cost: ₹{total_cost}")
        
        remove_items = st.multiselect("Select items to remove from cart", cart_items_display)
        if st.button("Remove Selected Items"):
            new_cart = [cart_item for cart_item in st.session_state.cart
                        if f"{cart_item['restaurant']} - {cart_item['item']}" not in remove_items]
            st.session_state.cart = new_cart
            st.success("Selected items removed from cart!")

# ------------------------------------
# Feature: Food Minimisation (Discounted Leftover Food)
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
        st.balloons()

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
            st.balloons()
    else:
        st.write("No items selected for collaborative ordering.")
