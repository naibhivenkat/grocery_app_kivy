from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
import sqlite3
import os

DB_PATH = "db/app.db"

# Initialize DB if not exists
if not os.path.exists("db"):
    os.makedirs("db")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT,
    shop TEXT,
    items TEXT,
    status TEXT
)
''')
conn.commit()
conn.close()

class LoginScreen(Screen):
    def do_login(self, username, password):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        res = c.fetchone()
        conn.close()
        if res:
            role = res[0]
            if role == "customer":
                self.manager.current = "shop_selection"
            else:
                self.manager.current = "orders"
        else:
            self.ids.login_status.text = "Invalid credentials"

class ShopSelectionScreen(Screen):
    shops = ListProperty(["Fresh Mart", "Green Grocers", "Daily Needs"])
    def select_shop(self, shop):
        self.manager.get_screen("item_selection").selected_shop = shop
        self.manager.current = "item_selection"

class ItemSelectionScreen(Screen):
    selected_shop = StringProperty("")
    cart = ListProperty([])

    items = ListProperty([
        "Rice", "Wheat", "Milk", "Eggs", "Tomatoes", "Potatoes"
    ])

    def add_to_cart(self, item):
        self.cart.append(item)

    def view_cart(self):
        self.manager.get_screen("cart").cart_items = self.cart
        self.manager.get_screen("cart").selected_shop = self.selected_shop
        self.manager.current = "cart"

class CartScreen(Screen):
    cart_items = ListProperty([])
    selected_shop = StringProperty("")

    def place_order(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO orders (customer, shop, items, status) VALUES (?, ?, ?, ?)", (
            "customer1", self.selected_shop, ",".join(self.cart_items), "Pending"
        ))
        conn.commit()
        conn.close()
        self.manager.current = "shop_selection"

class OrdersScreen(Screen):
    orders = ListProperty([])

    def on_pre_enter(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, customer, items, status FROM orders")
        self.orders = c.fetchall()
        conn.close()

    def update_status(self, order_id, new_status):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
        conn.commit()
        conn.close()
        self.on_pre_enter()

class GroceryApp(App):
    def build(self):
        Builder.load_file("kivy/login.kv")
        Builder.load_file("kivy/shop_selection.kv")
        Builder.load_file("kivy/item_selection.kv")
        Builder.load_file("kivy/cart.kv")
        Builder.load_file("kivy/orders.kv")
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ShopSelectionScreen(name="shop_selection"))
        sm.add_widget(ItemSelectionScreen(name="item_selection"))
        sm.add_widget(CartScreen(name="cart"))
        sm.add_widget(OrdersScreen(name="orders"))
        return sm

if __name__ == "__main__":
    GroceryApp().run()
