import json
from typing import Optional

import jwt
from kivy.logger import Logger, LOG_LEVELS
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.material_resources import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen

from settings import HOST, PORT

Logger.setLevel(LOG_LEVELS["debug"])
store = JsonStore('hello.json')

sm: Optional[ScreenManager] = None


def set_sm(screen_manager):
    global sm
    sm = screen_manager


def into_main_page(request, result):
    print(result)
    if result.get('detail'):
        store.delete('jwt')
        sm.switch_to(screens['LoginScreen'])
        return

    screens.update({
        'MainPage': MainPage(
            first_name=result['first_name'],
            second_name=result['second_name'],
            profession=result['profession'],
            equipment=result['equipment'],
            created_at=result['created_at'],
        ),
    })
    sm.switch_to(screens['MainPage'])


class LoginScreen(MDScreen):
    def login(self):
        login = self.ids.login.text
        password = self.ids.password.text
        url = f'http://{HOST}:{PORT}/api/auth/login/'

        Logger.debug('login = %s password = %s', login, password)
        Logger.debug('url = %s', url)

        UrlRequest(
            url,
            on_success=self.parce_responce,
            on_error=self.parce_responce,
            on_cancel=self.parce_responce,
            on_failure=self.parce_responce,
            method='POST',
            req_headers={'Content-type': 'application/json'},
            req_body=json.dumps({
                "username": login,
                "password": password,
            })
        )

    def parce_responce(self, _, result):
        Logger.debug('Result: %s', result)

        try:
            store.put('jwt', access=result['access'], refresh=result['refresh'])
            self.ids.login.text = ''
            self.ids.password.text = ''
            user_id = jwt.decode(result['access'], options={"verify_signature": False})['user_id']

            url = f'http://{HOST}:{PORT}/api/accounting/info_employees/{user_id}/'
            Logger.debug('url = %s', url)
            Logger.debug('JWT access = %s', result['access'])
            UrlRequest(
                url,
                req_headers={
                    'Authorization': 'Bearer ' + result['access']
                },
                on_success=into_main_page,
                on_redirect=into_main_page,
            )

        except Exception:
            if login_error := result.get('username'):
                self.ids.login.helper_text = '\n'.join(login_error)
                self.ids.login.helper_text_mode = 'on_error'
                self.ids.login.error = True
                self.ids.login.on_focus()

            if password_error := result.get('password'):
                self.ids.password.helper_text = '\n'.join(password_error)
                self.ids.password.helper_text_mode = 'on_error'
                self.ids.password.error = True
                self.ids.password.on_focus()

            if detail_error := result.get('detail'):
                self.ids.login.helper_text = detail_error
                self.ids.login.error = True
                self.ids.login.on_focus()

                self.ids.password.helper_text = detail_error
                self.ids.password.error = True
                self.ids.password.on_focus()

    @staticmethod
    def focus(text_field):
        text_field.error = False
        text_field.on_focus()


class MainPage(MDScreen):
    first_name = StringProperty()
    second_name = StringProperty()
    profession = StringProperty('неуказанно')
    created_at = StringProperty()
    equipment = ListProperty()

    def __init__(self, first_name, second_name, profession, created_at, equipment, **kw):
        super().__init__(**kw)
        self.first_name = first_name
        self.second_name = second_name
        self.equipment = equipment

        if profession:
            self.profession = profession['name']
        self.created_at = created_at

        data_tables = MDDataTable(
            size_hint=(.8, .9),
            pos_hint={'center_x': .5, 'center_y': .5},
            use_pagination=False,
            column_data=[
                ('name', dp(30)),
                ('type', dp(30)),
                ('price', dp(30)),
                ('period', dp(30)),
            ],
            row_data=[
                (eq['name'], eq['type'], eq['price'], eq['period']) for eq in self.equipment
            ],
            elevation=2,
        )
        self.ids.tab1.add_widget(data_tables)

    def logout(self):
        self.ids.nav_drawer.set_state("close")
        store.delete('jwt')
        sm.switch_to(screens['LoginScreen'])

    # def load_data(self):
    #     data_tables = MDDataTable(
    #         use_pagination=True,
    #         check=True,
    #         column_data=[
    #             ('name', dp(30)),
    #             ('type', dp(30)),
    #             ('price', dp(30)),
    #             ('period', dp(30)),
    #         ],
    #         row_data=[],
    #         orientation="lr-tb",
    #     )
    #     self.ids.tab1.add_widget(data_tables)


screens = {
    'LoginScreen': LoginScreen(name='LoginScreen'),
}
