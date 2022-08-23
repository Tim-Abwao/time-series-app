# from dash import dcc, html
# from dash.dependencies import Input, Output

# from ts_app.dash_app import app

# server = app.server

# import dash
# from dash import Dash, dcc, html

# app = Dash(__name__, use_pages=True)



# app.layout = html.Div(
#     [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
# )


# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def render_page(pathname: str) -> html.Div:
#     """Display the page at the given `pathname`.

#     Args:
#         pathname (str): The url to a page.

#     Returns:
#         dash.html.Div.Div: Page content.
#     """
#     if pathname == "/glossary":
#         return glossary.layout
#     elif pathname == "/sample":
#         return generate_dashboard(data_source=sample.input_layout)
#     elif pathname == "/upload":
#         return generate_dashboard(data_source=upload.input_layout)
#     else:
#         return home_page.layout


