from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import os
import shutil

# Load all KV files manually
kv_dir = os.path.join(os.path.dirname(__file__), 'kivy')
Builder.load_file(os.path.join(kv_dir, "login.kv"))
Builder.load_file(os.path.join(kv_dir, "shop_selection.kv"))
Builder.load_file(os.path.join(kv_dir, "item_selection.kv"))
Builder.load_file(os.path.join(kv_dir, "cart.kv"))
Builder.load_file(os.path.join(kv_dir, "orders.kv"))

# Define screens
class LoginScreen(Screen):
    def do_login(self, username, password):
        if username == "admin":
            self.manager.current = "orders"
        else:
            self.manager.get_screen('shop_selection').username = username
            self.manager.current = "shop_selection"

class ShopSelectionScreen(Screen):
    def select_shop(self, shop_name):
        self.manager.get_screen('item_selection').selected_shop = shop_name
        self.manager.current = "item_selection"

class ItemSelectionScreen(Screen):
    selected_shop = ""
    cart_items = []

    def add_to_cart(self, item):
        self.cart_items.append(item)

    def view_cart(self):
        cart_screen = self.manager.get_screen('cart')
        cart_screen.selected_shop = self.selected_shop
        cart_screen.cart_items = self.cart_items
        self.manager.current = "cart"

class CartScreen(Screen):
    selected_shop = ""
    cart_items = []

    def place_order(self):
        print(f"Order placed for {self.selected_shop}: {', '.join(self.cart_items)}")
        self.manager.current = "login"

class OrdersScreen(Screen):
    orders = [(1, "admin", "Fresh Mart", "Rice, Eggs"),
              (2, "admin", "Daily Needs", "Milk")]

    def update_status(self, order_id, status):
        print(f"Order {order_id} marked as {status}")

class GroceryApp(App):
    def build(self):
        self.ensure_db_exists()

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ShopSelectionScreen(name='shop_selection'))
        sm.add_widget(ItemSelectionScreen(name='item_selection'))
        sm.add_widget(CartScreen(name='cart'))
        sm.add_widget(OrdersScreen(name='orders'))
        return sm

    def ensure_db_exists(self):
        # Ensure the DB file is accessible in Android user directory
        source_db = os.path.join(self.directory, 'db', 'app.db')
        target_db = os.path.join(self.user_data_dir, 'app.db')
        if not os.path.exists(target_db):
            os.makedirs(os.path.dirname(target_db), exist_ok=True)
            if os.path.exists(source_db):
                shutil.copy(source_db, target_db)

if __name__ == '__main__':
    GroceryApp().run()
