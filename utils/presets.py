PARAMETER_PRESETS = {
    "default": {},
    "EAD prone": {
        "extracellular.cao": 2,
        "extracellular.clo": 148,
        "extracellular.nao": 137,
        "multipliers.IKr_multiplier": 0.15,
        "bcl": 4000,
    },
    "alternans with low SERCA": {
        "bcl": 300,
        # "show_last_beats": 4,
        "total_beats": 250,
        "multipliers.Jup_multiplier": 0.65,
    },
    "DAD prone": {
        "extracellular.cao": 4.0,
        "bcl": 400,
        "total_beats": 200,
        "PKA.fICaL_PKA": 1,
        "PKA.fIKs_PKA": 1,
        "PKA.fINaK_PKA": 1,
        "PKA.fINa_PKA": 1,
        "PKA.fMyBPC_PKA": 1,
        "PKA.fPLB_PKA": 1,
        "PKA.fTnI_PKA": 1,
    },
}
