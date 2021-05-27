import jwt
from kivy import Logger
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp

from settings import HOST, PORT


class MainApp(MDApp):
    def build(self):
        Builder.load_file('kv/screens.kv')

        from screens import set_sm, screens, into_main_page

        sm = ScreenManager(transition=NoTransition())
        set_sm(sm)

        from utils import jwt_refresh

        store = JsonStore('hello.json')
        if store.exists('jwt'):
            tokens = store.get('jwt')
            user_id = jwt.decode(tokens['access'], options={"verify_signature": False})['user_id']

            url = f'http://{HOST}:{PORT}/api/accounting/info_employees/{user_id}/'
            Logger.debug('url = %s', url)
            Logger.debug('JWT access token = %s', store.get('jwt')['access'])
            UrlRequest(
                url,
                on_success=into_main_page,
                on_redirect=jwt_refresh,
                on_error=jwt_refresh,
                on_cancel=jwt_refresh,
                on_failure=jwt_refresh,
                req_headers={
                    'Authorization': 'Bearer ' + tokens['access']
                }
            )
            Logger.debug("Sent request")
        else:
            Logger.debug('Entering LoingScreen')
            sm.switch_to(screens['LoginScreen'])
        return sm


if __name__ == '__main__':
    MainApp().run()
