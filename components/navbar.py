import dash_bootstrap_components as dbc

# Top navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(
                    "Regular stimulation",
                    href="/app-reg-stim",
                ),
                dbc.DropdownMenuItem(
                    "S1-S2 restitution",
                    href="/app-s1-s2",
                ),
                dbc.DropdownMenuItem(
                    "Rate dependence and alternans",
                    href="/app-rate-dep",
                ),
                dbc.DropdownMenuItem(
                    "Delayed afterdepolariztions",
                    href="/app-dad",
                ),
            ],
            label="Protocol",
            nav=True,
        ),
        dbc.NavItem(
            dbc.NavLink(
                "User Guide",
                href="/user-guide",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Article",
                href="https://www.biorxiv.org/content/10.1101/2025.03.24.645031v2.abstract",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Source Code",
                href="https://github.com/ThomasMBury/ap_simulation_app",
            )
        ),
    ],
    brand="Simulator for T-World: A computational model of the human ventricular cardiomyocyte",
    brand_href="/",
    color="dark",
    dark=True,
)
