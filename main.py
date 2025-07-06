import sys
import os
from kivy.app import App
from kivy.config import Config
from kivy.resources import resource_find
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty

# Force debug logging
Config.set('kivy', 'log_level', 'debug')


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("LoginScreen init")  # startup log
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # load icon via resource_find
        icon_path = resource_find("kivy/icons/app_icon.png")
        if icon_path:
            layout.add_widget(Image(source=icon_path, size_hint=(1, .4)))
        else:
            print("Icon not found at kivy/icons/app_icon.png")

        self.username = TextInput(hint_text="Username", size_hint=(1, None), height=40)
        self.password = TextInput(hint_text="Password", password=True, size_hint=(1, None), height=40)
        self.login_status = Label(text="", color=(1, 0, 0, 1), size_hint=(1, None), height=30)

        login_btn = Button(text="Login", size_hint=(1, None), height=50)
        login_btn.bind(on_release=self.do_login)

        for w in (self.username, self.password, login_btn, self.login_status):
            layout.add_widget(w)
        self.add_widget(layout)

    def do_login(self, *args):
        print(f"Attempt login: {self.username.text}/{self.password.text}")
        if self.username.text and self.password.text:
            self.manager.current = "shop_selection"
        else:
            self.login_status.text = "Enter username and password"


class ShopSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ShopSelectionScreen init")
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Select Shop", font_size=24, size_hint=(1, None), height=40))

        shop_layout = GridLayout(cols=1, spacing=10, size_hint=(1, None))
        shop_layout.bind(minimum_height=shop_layout.setter('height'))
        for shop_name in ["Fresh Mart", "Green Grocers", "Daily Needs"]:
            btn = Button(text=shop_name, size_hint=(1, None), height=50)
            btn.bind(on_release=lambda btn: self.select_shop(btn.text))
            shop_layout.add_widget(btn)

        layout.add_widget(shop_layout)
        self.add_widget(layout)

    def select_shop(self, shop_name):
        print(f"Selected shop: {shop_name}")
        app = App.get_running_app()
        app.selected_shop = shop_name
        self.manager.get_screen("item_selection").selected_shop = shop_name
        self.manager.current = "item_selection"


class ItemSelectionScreen(Screen):
    selected_shop = StringProperty("")
    cart_items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ItemSelectionScreen init")
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.shop_label = Label(text="", size_hint=(1, None), height=30)
        self.layout.add_widget(self.shop_label)

        grid = GridLayout(cols=2, spacing=10, size_hint=(1, None))
        grid.bind(minimum_height=grid.setter('height'))
        for item in ["Rice", "Milk", "Eggs", "Tomatoes"]:
            btn = Button(text=item, size_hint=(1, None), height=40)
            btn.bind(on_release=lambda btn: self.add_to_cart(btn.text))
            grid.add_widget(btn)
        self.layout.add_widget(grid)

        view_cart_btn = Button(text="View Cart", size_hint=(1, None), height=50)
        view_cart_btn.bind(on_release=self.view_cart)
        self.layout.add_widget(view_cart_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.shop_label.text = f"Select Items from {self.selected_shop}"
        print("Now in ItemSelectionScreen for", self.selected_shop)

    def add_to_cart(self, item):
        print("Add to cart:", item)
        self.cart_items.append(item)

    def view_cart(self, *args):
        cart = self.manager.get_screen("cart")
        cart.selected_shop = self.selected_shop
        cart.cart_items = self.cart_items.copy()
        self.manager.current = "cart"


class CartScreen(Screen):
    selected_shop = StringProperty("")
    cart_items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("CartScreen init")
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.shop_label = Label(text="", size_hint=(1, None), height=30)
        self.items_label = Label(text="", size_hint=(1, None), height=30)
        self.layout.add_widget(self.shop_label)
        self.layout.add_widget(self.items_label)

        place_btn = Button(text="Place Order", size_hint=(1, None), height=50)
        place_btn.bind(on_release=self.place_order)
        self.layout.add_widget(place_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.shop_label.text = f"Cart for {self.selected_shop}"
        self.items_label.text = ", ".join(self.cart_items)
        print("CartScreen showing", self.cart_items)

    def place_order(self, *args):
        print(f"Placing order for {self.selected_shop}: {self.cart_items}")
        self.manager.current = "orders"


class OrdersScreen(Screen):
    orders = ListProperty([(1, 'Fresh Mart', 'Rice, Milk', 'Pending')])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("OrdersScreen init")
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Shopkeeper Orders", font_size=24, size_hint=(1, None), height=40))

        self.orders_grid = GridLayout(cols=1, spacing=10, size_hint=(1, None))
        self.orders_grid.bind(minimum_height=self.orders_grid.setter('height'))
        layout.add_widget(self.orders_grid)

        self.refresh_btn = Button(text="Refresh", size_hint=(1, None), height=50)
        self.refresh_btn.bind(on_release=lambda *a: self.refresh_orders())
        layout.add_widget(self.refresh_btn)

        self.back_btn = Button(text="Back to Login", size_hint=(1, None), height=50)
        self.back_btn.bind(on_release=self.back_to_login)
        layout.add_widget(self.back_btn)

        self.add_widget(layout)
        self.refresh_orders()

    def refresh_orders(self):
        print("Refreshing orders")
        self.orders_grid.clear_widgets()
        for order in self.orders:
            btn = Button(text=f"Order {order[0]}: {order[2]} - {order[3]}", size_hint=(1, None), height=40)
            btn.bind(on_release=lambda btn, oid=order[0]: self.update_status(oid, "Completed"))
            self.orders_grid.add_widget(btn)

    def update_status(self, order_id, status):
        print(f"Order {order_id} marked {status}")

    def back_to_login(self, *args):
        print("Back to login")
        self.manager.current = "login"


class GroceryApp(App):
    selected_shop = StringProperty("")

    def build(self):
        print("=== GroceryApp.build() ===")
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ShopSelectionScreen(name="shop_selection"))
        sm.add_widget(ItemSelectionScreen(name="item_selection"))
        sm.add_widget(CartScreen(name="cart"))
        sm.add_widget(OrdersScreen(name="orders"))
        return sm


if __name__ == "__main__":
    try:
        GroceryApp().run()
    except Exception as e:
        import traceback
        with open("crash.log", "w") as f:
            f.write(traceback.format_exc())
        print("APP CRASHED:", e)
        sys.exit(1)
