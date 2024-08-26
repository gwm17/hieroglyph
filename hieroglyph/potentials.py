import math
from typing import Callable

AN_CAI = "an-cai"
DAEHNICK = "daehnick"
BOJOWALD = "bojowald"
KONING_DELAROCHE_PROTON = "koning-delaroche-proton"


def an_cai_potential(E: float, zt: int, at: int, params: dict[str, float]):
    a3 = at ** (0.333)

    params["V"] = 91.85 - 0.249 * E + 1.116e-4 * E**2.0 + 0.642 * zt / a3
    params["Vi"] = 1.104 + 0.0622 * E
    params["Vsi"] = 10.83 - 0.0306 * E
    params["Vso"] = 3.557
    params["Vsoi"] = 0.0
    params["r0"] = 1.152 - 0.00776 / a3
    params["ri0"] = 1.305 + 0.0997 / a3
    params["rsi0"] = 1.334 + 0.152 / a3
    params["rso0"] = 0.972
    params["rsoi0"] = 0.0
    params["rc0"] = 1.303
    params["a"] = 0.719 + 0.0126 * a3
    params["ai"] = 0.855 - 0.1 * a3
    params["asi"] = 0.531 + 0.062 * a3
    params["aso"] = 1.011
    params["asoi"] = 0.0


def daehnick_potential(E: float, zt: int, at: int, params: dict[str, float]):
    nt = at - zt
    a3 = at ** (0.333)
    beta = -1.0 * (E * 0.01) ** 2.0
    mu1 = math.exp(-1.0 * ((8.0 - nt) * 0.5) ** 2.0)
    mu2 = math.exp(-1.0 * ((20.0 - nt) * 0.5) ** 2.0)
    mu3 = math.exp(-1.0 * ((28.0 - nt) * 0.5) ** 2.0)
    mu4 = math.exp(-1.0 * ((50.0 - nt) * 0.5) ** 2.0)
    mu5 = math.exp(-1.0 * ((82.0 - nt) * 0.5) ** 2.0)
    mu6 = math.exp(-1.0 * ((126.0 - nt) * 0.5) ** 2.0)

    mu = mu1 + mu2 + mu3 + mu4 + mu5 + mu6

    params["V"] = 88.0 - 0.283 * E + 0.88 * zt / a3
    params["Vi"] = (12.0 + 0.031 * E) * (1.0 - math.exp(beta))
    params["Vsi"] = (12.0 + 0.031 * E) * (math.exp(beta))
    params["Vso"] = 7.2 - 0.032 * E
    params["Vsoi"] = 0.0
    params["r0"] = 1.17
    params["ri0"] = 1.376 - 0.01 * math.sqrt(E)
    params["rsi0"] = 1.376 - 0.01 * math.sqrt(E)
    params["rso0"] = 1.07
    params["rsoi0"] = 0.0
    params["rc0"] = 1.3
    params["a"] = 0.717 + 0.0012 * E
    params["ai"] = 0.52 + 0.07 * a3 - 0.04 * mu
    params["asi"] = 0.52 + 0.07 * a3 - 0.04 * mu
    params["aso"] = 0.66
    params["asoi"] = 0.0


def bojowald_potential(E: float, zt: int, at: int, params: dict[str, float]):
    # nt = at - zt
    a3 = at ** (0.333)

    params["V"] = 81.33 - 0.24 * E + 1.43 * zt / a3
    params["Vi"] = 0.132 * (E - 45.0) if E > 45.0 else 0.0
    params["Vsi"] = 7.8 + 1.04 * a3 - 0.712 * params["Vi"]
    params["Vso"] = 6.0
    params["Vsoi"] = 0.0
    params["r0"] = 1.18
    params["ri0"] = 1.27
    params["rsi0"] = 1.27
    params["rso0"] = 0.78 + 0.038 * a3
    params["rsoi0"] = 0.0
    params["rc0"] = 1.3
    params["a"] = 0.636 + 0.035 * a3
    params["ai"] = 0.768 + 0.021 * a3
    params["asi"] = 0.768 + 0.021 * a3
    params["aso"] = 0.78 + 0.038 * a3
    params["asoi"] = 0.0


def koning_delaroche_proton_potential(
    E: float, zt: int, at: int, params: dict[str, float]
):
    nt = at - zt
    a3 = at ** (0.333)

    v1 = 59.30 + 21.0 * (nt - zt) / at - 0.024 * at
    v2 = 0.007067 + 4.23e-6 * at
    v3 = 1.729e-5 + 1.136e-8 * at
    v4 = 7.0e-9

    w1 = 14.667 + 0.009629 * at
    w2 = 73.55 + 0.0795 * at

    d1 = 16.0 + 16.0 * (nt - zt) / at
    d2 = 0.0180 + 0.003802 / (1.0 + math.exp((at - 156.0) / 8.0))
    d3 = 11.5

    vso1 = 5.922 + 0.0030 * at
    vso2 = 0.0040

    wso1 = -3.1
    wso2 = 160

    ef = -8.4075 + 0.01378 * at
    rc = 1.198 + 0.697 * at ** (-0.666) + 12.994 * at ** (-1.666)
    vc = 1.73 / rc * zt * a3

    delta_e = E - ef
    params["V"] = v1 * (
        1.0 - v2 * delta_e + v3 * delta_e**2.0 - v4 * delta_e**3.0
    ) + vc * v1 * (v2 - 2.0 * v3 * delta_e + 3.0 * v4 * delta_e**2.0)
    params["Vi"] = w1 * delta_e**2.0 / (delta_e**2.0 + w2**2.0)
    params["Vsi"] = (
        d1 * delta_e**2.0 / (delta_e**2.0 + d3**2.0) * math.exp(-1.0 * d2 * delta_e)
    )
    params["Vso"] = vso1 * math.exp(-1.0 * vso2 * delta_e)
    params["Vsoi"] = wso1 * delta_e**2.0 / (delta_e**2.0 + wso2**2.0)
    params["r0"] = 1.3039 - 0.4054 / a3
    params["ri0"] = params["r0"]
    params["rsi0"] = 1.3424 - 0.01585 * a3
    params["rso0"] = 1.1854 - 0.647 / a3
    params["rsoi0"] = params["rso0"]
    params["rc0"] = rc
    params["a"] = 0.6778 - 1.487e-4 * at
    params["ai"] = 0.6778 - 1.487e-4 * at
    params["asi"] = 0.5187 + 5.205e-4 * at
    params["aso"] = 0.59
    params["asoi"] = 0.59


POTENTIALS: dict[str, Callable[[float, int, int, dict[str, float]], None]] = {
    AN_CAI: an_cai_potential,
    DAEHNICK: daehnick_potential,
    BOJOWALD: bojowald_potential,
    KONING_DELAROCHE_PROTON: koning_delaroche_proton_potential,
}


def create_parameters(E: float, zt: int, at: int, potential: str) -> dict[str, float]:
    if potential not in POTENTIALS.keys():
        raise Exception(
            f"Potential {potential} is not in the set of allowed Potentials {POTENTIALS}!"
        )

    params = {
        "V": 0.0,
        "Vi": 0.0,
        "Vsi": 0.0,
        "Vso": 0.0,
        "Vsoi": 0.0,
        "r0": 0.0,
        "ri0": 0.0,
        "rsi0": 0.0,
        "rso0": 0.0,
        "rsoi0": 0.0,
        "rc0": 0.0,
        "a": 0.0,
        "ai": 0.0,
        "asi": 0.0,
        "aso": 0.0,
        "asoi": 0.0,
    }

    POTENTIALS[potential](E, zt, at, params)

    return params
