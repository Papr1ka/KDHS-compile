from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivy.properties import ListProperty, ColorProperty, StringProperty, OptionProperty, DictProperty
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.widget import MDAdaptiveWidget
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp
from kivymd.uix.toolbar import MDTopAppBar

from libs.components.profile_popup import ProfilePopup
from libs.components.text_input_round import TextInputRound, TextInputString
from libs.components.chat_bubble import ChatBubble
from libs.components.listitem import ChatListItem
from libs.exceptions import ServerError
from libs.utils.behaviors import GetApp
from libs.models import *
from threading import Thread

from settings import Logger

name = __name__

class Bar(MDTopAppBar, GetApp):
    pass


class ChatItem(ChatListItem):
    
    def on_touch_down(self, touch):
        if self.app and self.collide_point(touch.x, touch.y):
            self.open_messages()
    
    def open_messages(self):
        self.app.screen_manager.adaptive_switch_screen('messages_screen', self.app.root)
        try:
            self.app.on_chat_switch(self.chat_id)
        except AttributeError as E:
            self.app.create_chat(self.id)
            
            Logger.debug(f"{name}: on_open_messages")


class ContentNavigationDrawer(MDBoxLayout):
    pass


class MainContactEventBehavior(GetApp):
    
    def __init__(self) -> None:
        super().__init__()
        Clock.schedule_once(self.bind_components, 1)
    
    def bind_components(self, tm):
        if self.ids.get("search"):
            self.ids.search.textinput.bind(
                on_text_validate=self.search
            )
    
    def search(self, textinput):
        query = textinput.text
        if query != '':
            self.app.search_contacts(query)
        else:
            self.app.show_contacts()

class SidebarNavigation(MDNavigationDrawer, MainContactEventBehavior):
    back_color = ColorProperty((0, 0, 0, 1))
    header_head = StringProperty("")
    icon_source = StringProperty("")
    
    def sign_out(self):
        self.app.screen_manager.switch_screen("login_screen")
        self.app.on_sign_out()
    
    
    def show_profile_dialog(self, *args):
        
        popup = ProfilePopup(
            avatar_url=self.app.current_avatar_url,
            display_name=self.app.current_display_name,
            username=self.app.current_username,
            status=self.app.current_status
        )
        
        dialog = MDDialog(
            md_bg_color=self.app.colors["SearchColor"],
            title="????????????????????",
            type="custom",
            content_cls=popup,
            width_offset=0,
        )
        dialog.open()

class MainMobileView(MDScreen, MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MainTabletView(MDScreen, MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MainDesktopView(MDScreen, MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MessagesBehavior(GetApp):
    messages: list = []
    dialog = None
    refreshing = False
    
    def send_from_button(self, button):
        self.send_message(button.parent.textinput)
    
    def send_message(self, instance_textfield):
        text = instance_textfield.text
        if text != '':
            self.app.send_message(text)
            instance_textfield.text = ''
    
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.bind_components, 1)
    
    def bind_components(self, x):
        self.messages = self.app.messages
        self.ids.text_input.textinput.bind(
            on_text_validate=self.send_message
        )
        self.ids.text_input.button.bind(
            on_press=self.send_from_button
        )
        self.ids.messages_rv.data = self.messages
        self.ids.messages_rv.bind(
            on_scroll_stop=self.check_pull_refresh
        )
    
    def check_pull_refresh(self, rv, event):
        if rv.collide_point(event.x, event.y):
            view = self.ids.messages_rv
            box = self.ids.rm_box
            max_pixel = 120
            to_relative = max_pixel / (box.height - view.height)
            if view.scroll_y < 1.0 + to_relative or self.refreshing:
                return
            
            self.refresh()
    
    def refresh(self):
        self.refreshing = True
        Clock.schedule_once(self._refresh, 0)
    
    def _refresh(self, interval):
        Logger.debug(f"{name}: on_messages_refresh")
        self.app.get_messages(self.app.selected_chat_id, mode=True)
        self.refreshing = False
    
    def show_user_profile(self):
        chat = self.app.find_contact_by_chat_id(self.app.selected_chat_id)
        user: Union[UserModel, None] = self.app.get_user(chat.users[-1])
        if user:
            popup = ProfilePopup(
                avatar_url=user.avatar_image,
                display_name=user.display_name,
                username=user.username,
                status=user.status if user.status != "" else "???????? ????????????, ?? ?????????????????? WhatsApp!",
            )
            
            dialog = MDDialog(
                    md_bg_color=self.app.colors["SearchColor"],
                    title="????????????????????",
                    type="custom",
                    content_cls=popup,
                    width_offset=0,
                )
            dialog.open()
        


class MessagesLayout(RelativeLayout, MDAdaptiveWidget, MessagesBehavior):
    pass

class MessagesScreen(MDScreen, MessagesBehavior):
    pass


class MainScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MainMobileView()
        self.tablet_view = MainTabletView()
        self.desktop_view = MainDesktopView()
