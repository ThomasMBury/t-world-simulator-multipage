from dash import html, dcc
from utils.model import MODEL_PARAMS_DEFAULT


def make_extracellular_inputs(page_id):
    def param_input(label, id_, value):
        return html.Div(
            [
                html.Label(f"{label} =", style={"fontSize": 14}),
                dcc.Input(
                    id=id_,
                    value=value,
                    type="number",
                    style={"width": 80, "display": "inline-block"},
                    min=0,
                    max=1000,
                    step=0.1,
                ),
            ]
        )

    return html.Div(
        [
            dcc.Markdown("-----\n**Extracellular concentrations**:"),
            param_input(
                "Cao",
                f"page-{page_id}-extracellular_cao-box",
                MODEL_PARAMS_DEFAULT["extracellular.cao"],
            ),
            param_input(
                "Clo",
                f"page-{page_id}-extracellular_clo-box",
                MODEL_PARAMS_DEFAULT["extracellular.clo"],
            ),
            param_input(
                "Ko",
                f"page-{page_id}-extracellular_ko-box",
                MODEL_PARAMS_DEFAULT["extracellular.ko"],
            ),
            param_input(
                "Nao",
                f"page-{page_id}-extracellular_nao-box",
                MODEL_PARAMS_DEFAULT["extracellular.nao"],
            ),
        ]
    )
