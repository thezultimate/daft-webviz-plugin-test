from uuid import uuid4

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from webviz_config import WebvizPluginABC

from ._auth import Auth

from flask import request

CLIENT_ID = "f9d8dfc9-9bd5-4df3-a53a-f09d211e1e97"
RESOURCE_ID = "1025aa65-09e1-41a8-8c59-68ede2e41340"

class SomeRadixDaftPlugin(WebvizPluginABC):
    def __init__(self, app):
        super().__init__()
        self.auth_button_id = f"auth-button-{uuid4()}"
        self.auth_div_id = f"auth-state-{uuid4()}"
        self.message_div_id = f"message-state-{uuid4()}"
        self.set_callbacks(app)

        self.is_authenticated = False
        self.is_waiting_auth = False
        self.auth = Auth(CLIENT_ID, RESOURCE_ID)
        
    @property
    def layout(self):
        return html.Div(
            [
                html.H1("Testing Radix API via Webviz"),
                html.Div([
                    dcc.Input(id="is_authenticated", type="hidden", value=self.is_authenticated),
                    dcc.Input(id="is_waiting_auth", type="hidden", value=self.is_waiting_auth),
                    html.H3("Authentication with Azure"),
                    html.Button("Authenticate", id=self.auth_button_id),
                    html.Div(id=self.auth_div_id),
                    html.Div(id=self.message_div_id),
                    html.Div(id="test_url")
                ])
            ]
        )

    def set_callbacks(self, app):
        @app.callback(
            [Output("is_waiting_auth", "value"),
             Output(self.message_div_id, "children")],
            [Input(self.auth_button_id, "n_clicks")],
            prevent_initial_call=True
        )
        def button_clicked(n_clicks):
            print("button_clicked: self.is_waiting_auth:", self.is_waiting_auth)
            print("button_clicked: self.is_authenticated", self.is_authenticated)

            if not self.is_authenticated:
                self.flow = self.auth.initiate_device_code()
                print("button_clicked: self.flow:", self.flow)
                self.is_waiting_auth = True
                message = self.flow['message']
                return self.is_waiting_auth, message
            
            return self.is_waiting_auth, ""

        @app.callback(
            Output(self.auth_div_id, "children"),
            [Input("is_waiting_auth", "value")]
        )
        def auth_info(is_waiting_auth):
            print("auth_info: is_waiting_auth:", is_waiting_auth)

            if is_waiting_auth:
                print("auth_info: Waiting for auth....")
                self.auth_result = self.auth.app.acquire_token_by_device_flow(self.flow)
                print("auth_info: self.auth_result", self.auth_result)
                print("auth_info: authenticated")
                self.is_waiting_auth = False
                self.is_authenticated = True
                return "Authenticated"
            
            if self.is_authenticated:
                print("auth_info: self.is_authenticated:", self.is_authenticated)
                return "Authenticated"

            return "Not authenticated"

        @app.callback(
            Output("test_url", "children"),
            [Input("url", "href")]
        )
        def url_info(url_href):
            print("url_info: ", url_href)
            print("url_info: ", app.server)
            print("url_info: ", request)
            return f"The URL is: {url_href}"