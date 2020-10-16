import dash_html_components as html
from webviz_config import WebvizPluginABC


class SomeCustomPlugin(WebvizPluginABC):
    @property
    def layout(self):
        return html.Div(
            [html.H1("Custom plugin"), "This is a custom plugin."]
        )
