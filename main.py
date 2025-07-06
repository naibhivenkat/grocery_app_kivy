from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import StringProperty, ListProperty


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.logo = Image(source="kivy/icons/app_icon.png", size_hint_y=0.4)
        self.username = TextInput(hint_text="123")
        self.password = TextInput(hint_text="123", password=True)
        self.login_status = Label(color=(1, 0, 0, 1))

        login_btn = Button(text="Login")
        login_btn.bind(on_release=self.do_login)

        layout.add_widget(self.logo)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        layout.add_widget(self.login_status)

        self.add_widget(layout)

    def do_login(self, *args):
        if self.username.text and self.password.text:
            self.manager.current = "shop_selection"
        else:
            self.login_status.text = "Enter username and password"


class ShopSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Select Shop", font_size=24))

        shop_layout = GridLayout(cols=1, size_hint_y=None)
        shop_layout.bind(minimum_height=shop_layout.setter('height'))

        for shop_name in ["Fresh Mart", "Green Grocers", "Daily Needs"]:
            btn = Button(text=shop_name)
            btn.bind(on_release=lambda btn: self.select_shop(btn.text))
            shop_layout.add_widget(btn)

        layout.add_widget(shop_layout)
        self.add_widget(layout)

    def select_shop(self, shop_name):
        app = App.get_running_app()
        app.selected_shop = shop_name
        self.manager.get_screen("item_selection").selected_shop = shop_name
        self.manager.current = "item_selection"


class ItemSelectionScreen(Screen):
    selected_shop = StringProperty("")
    cart_items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.shop_label = Label(text="")
        self.layout.add_widget(self.shop_label)

        self.items_grid = GridLayout(cols=2)

        for item in ["Rice", "Milk", "Eggs", "Tomatoes"]:
            btn = Button(text=item)
            btn.bind(on_release=lambda btn: self.add_to_cart(btn.text))
            self.items_grid.add_widget(btn)

        self.layout.add_widget(self.items_grid)

        view_cart_btn = Button(text="View Cart")
        view_cart_btn.bind(on_release=self.view_cart)
        self.layout.add_widget(view_cart_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.shop_label.text = f"Select Items from {self.selected_shop}"

    def add_to_cart(self, item):
        self.cart_items.append(item)

    def view_cart(self, *args):
        cart_screen = self.manager.get_screen("cart")
        cart_screen.selected_shop = self.selected_shop
        cart_screen.cart_items = self.cart_items.copy()
        self.manager.current = "cart"


class CartScreen(Screen):
    selected_shop = StringProperty("")
    cart_items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.shop_label = Label()
        self.items_label = Label()
        self.layout.add_widget(self.shop_label)
        self.layout.add_widget(self.items_label)

        place_order_btn = Button(text="Place Order")
        place_order_btn.bind(on_release=self.place_order)
        self.layout.add_widget(place_order_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.shop_label.text = f"Cart for {self.selected_shop}"
        self.items_label.text = ", ".join(self.cart_items)

    def place_order(self, *args):
        print(f"Placing order for {self.selected_shop}: {self.cart_items}")
        self.manager.current = "orders"


class OrdersScreen(Screen):
    orders = ListProperty([(1, 'Fresh Mart', 'Rice, Milk', 'Pending')])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Label(text="Shopkeeper Orders", font_size=24))
        self.orders_grid = GridLayout(cols=1, size_hint_y=None)
        self.orders_grid.bind(minimum_height=self.orders_grid.setter('height'))

        self.refresh_orders()

        refresh_btn = Button(text="Refresh")
        refresh_btn.bind(on_release=lambda *args: self.refresh_orders())
        layout.add_widget(self.orders_grid)
        layout.add_widget(refresh_btn)

        back_btn = Button(text="Back to Login")
        back_btn.bind(on_release=self.back_to_login)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def refresh_orders(self):
        self.orders_grid.clear_widgets()
        for o in self.orders:
            order_btn = Button(text=f"Order {o[0]}: {o[2]} - {o[3]}")
            order_btn.bind(on_release=lambda btn, oid=o[0]: self.update_status(oid, "Completed"))
            self.orders_grid.add_widget(order_btn)

    def update_status(self, order_id, status):
        print(f"Order {order_id} status updated to {status}")

    def back_to_login(self, *args):
        self.manager.current = "login"


class GroceryApp(App):
    selected_shop = StringProperty("")

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ShopSelectionScreen(name="shop_selection"))
        sm.add_widget(ItemSelectionScreen(name="item_selection"))
        sm.add_widget(CartScreen(name="cart"))
        sm.add_widget(OrdersScreen(name="orders"))
        return sm


if __name__ == '__main__':
    GroceryApp().run()
