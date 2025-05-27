import dash
from dash import Dash, html, dcc
from components.navbar import navbar
import dash_bootstrap_components as dbc


app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # suppress_callback_exceptions=True,
)

app.layout = html.Div(
    [
        navbar,
        dash.page_container,
    ]
)

# For gunicorn compatibility
server = app.server

if __name__ == "__main__":
    app.run(debug=True)
