import json

from kivy import Logger
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

from settings import HOST, PORT
from screens import screens, sm

store = JsonStore('hello.json')


def jwt_refresh(old_request: UrlRequest, _):
    print('jwt expired')
    refresh_token = store.get('jwt')['refresh']
    url = f'http://{HOST}:{PORT}/api/auth/refresh/'
    Logger.debug('url = %s', url)

    def callback(_, result):
        Logger.debug('Recreate old request')
        Logger.debug('JWT access token = %s', result['access'])
        store.put('jwt', access=result['access'], refresh=result['refresh'])
        UrlRequest(
            url=old_request.url,
            req_headers={
                'Authorization': 'Bearer ' + result['access']
            },
            on_success=old_request.on_success.method,
            on_redirect=bad_credantials,
            method=old_request._method,
        )

    def bad_credantials(_, __):
        Logger.debug('Bad credantials')
        sm.switch_to(screens['LoginScreen'])

    UrlRequest(
        url=url,
        req_headers={'Content-type': 'application/json'},
        req_body=json.dumps({
            "refresh": refresh_token
        }),
        on_success=callback,
        on_redirect=bad_credantials,
        on_error=bad_credantials,
        on_failure=bad_credantials,
    )


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    content_text = StringProperty("")
