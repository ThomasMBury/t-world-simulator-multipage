PARAM_NAMES_CURRENT_MULTIPLIERS = [
    "multipliers.ICaLPCa_multiplier",
    "multipliers.ICab_multiplier",
    "multipliers.IClCa_multiplier",
    "multipliers.IClb_multiplier",
    "multipliers.IK1_multiplier",
    "multipliers.IKb_multiplier",
    "multipliers.IKr_multiplier",
    "multipliers.IKs_multiplier",
    "multipliers.INaCa_multiplier",
    "multipliers.INaK_multiplier",
    "multipliers.INaL_multiplier",
    "multipliers.INa_multiplier",
    "multipliers.INab_multiplier",
    "multipliers.IpCa_multiplier",
    "multipliers.Itof_multiplier",
    "multipliers.Itos_multiplier",
    "multipliers.Jrel_multiplier",
    "multipliers.Jup_multiplier",
]

PARAM_NAMES_EXTRACELLULAR = [
    "extracellular.cao",
    "extracellular.clo",
    "extracellular.nao",
    "extracellular.ko",
]


PARAM_NAMES_CELLTYPE = ["environment.celltype"]

PARAM_NAMES_PKA = [
    "PKA.fICaL_PKA",
    "PKA.fIKs_PKA",
    "PKA.fINaK_PKA",
    "PKA.fINa_PKA",
    "PKA.fMyBPC_PKA",
    "PKA.fPLB_PKA",
    "PKA.fTnI_PKA",
]

# The following variables are plotted by default
PLOT_VARIABLES_DEFAULT = [
    "membrane.v",
    "INa.INa",
    "INaCa.INaCa_i",
    "ICaL.ICaL",
    "IKr.IKr",
    "IKs.IKs",
]

CELL_TYPE_DICT = {"endo": 0, "epi": 1, "mid": 2}


BCL_DEFAULT = 1000
TOTAL_BEATS_DEFAULT = 10
SHOW_LAST_BEATS_DEFAULT = 1
