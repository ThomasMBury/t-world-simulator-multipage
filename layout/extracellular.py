from dash import html, dcc


def make_extracellular_inputs(params_default):
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
                "Cao", "extracellular_cao_box", params_default["extracellular.cao"]
            ),
            param_input(
                "Clo", "extracellular_clo_box", params_default["extracellular.clo"]
            ),
            param_input(
                "Ko", "extracellular_ko_box", params_default["extracellular.ko"]
            ),
            param_input(
                "Nao", "extracellular_nao_box", params_default["extracellular.nao"]
            ),
        ]
    )
