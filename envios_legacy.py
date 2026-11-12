from decimal import Decimal, ROUND_HALF_UP

# Código heredado transcrito del enunciado. CONFIG personalizado: A-F=3,1,0,0,5,7.
CONFIG = {
    "PMAX": 45,
    "L1": 3,
    "L2": 10,
    "RECARGO_RURAL": 0.15,
    "RECARGO_NACIONAL": 0.45,
    "DESC_VIP": 0.10,
    "RECARGO_FINDE": 2000,
}


def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > CONFIG["PMAX"]:
        raise ValueError("peso invalido")
    if z not in {"urbana", "rural", "nacional"}:
        raise ValueError("zona inválida")
    if not isinstance(d, int) or isinstance(d, bool) or not 1 <= d <= 7:
        raise ValueError("día inválido")
    if cup is not None and cup != "ENVIO10":
        raise ValueError("cupón inválido")
    if p <= CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "urbana":
        t = t
    elif z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    if c == "frecuente":
        t = t - t * 0.05
    if c == "vip":
        t = t - t * CONFIG["DESC_VIP"]
    if cup is not None:
        if cup == "ENVIO10":
            t = t - t * 0.10
    if d in (6, 7):
        t = t + CONFIG["RECARGO_FINDE"]
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    return int(Decimal(str(t)).quantize(Decimal("1E2"), rounding=ROUND_HALF_UP))

