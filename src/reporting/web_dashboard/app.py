import dash
from dash import dcc, html, Input, Output
import plotly.express as px

class SecurityDashboard:
    def __init__(self, findings):
        self.app = dash.Dash(__name__)
        self.findings = findings
        self._setup_layout()
        self._register_callbacks()

    def _setup_layout(self):
        self.app.layout = html.Div([
            dcc.Graph(id='severity-heatmap'),
            dcc.Interval(id='refresh-interval', interval=60*1000),
            html.Div(id='live-update-text'),
            dcc.Store(id='findings-store', data=self.findings)
        ])

    def _register_callbacks(self):
        @self.app.callback(
            Output('severity-heatmap', 'figure'),
            Input('findings-store', 'data')
        )
        def update_heatmap(data):
            df = pd.DataFrame(data)
            return px.density_heatmap(
                df, x='file_type', y='severity', 
                histfunc="sum", title="Risk Distribution"
            )

    def run_server(self, port=8050):
        self.app.run_server(port=port)
