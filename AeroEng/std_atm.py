from math import e


def height(h1, h2):
    return h2 - h1


def temp_press_dens(a, h0, T0=288.15, P0=101325, rho0=1.225, g=9.80665, R=287.):
    if a == 0:
        P1 = P0 * e ** (-g / (R * T0) * h0)
        rho1 = rho0 * e ** (-g / (R * T0) * h0)
        return T0, P1, rho1
    else:
        T1 = T0 + a * h0
        P1 = P0 * (T1 / T0) ** (-g / (a * R))
        rho1 = rho0 * (T1 / T0) ** (-g / (a * R) - 1)
    return T1, P1, rho1


if __name__ == "__main__":
    h = input("Enter height h in m: ")

    assert h >= 0, "h is less then zero"
    assert h <= 84852, "h is greater then 84852m "

    a_h = [[-0.0065, 11000], [0, 20000], [0.001, 32000],
        [0.0028, 47000], [0, 51000], [-0.0028, 71000], [-0.002, 84852]]

    h0 = 0
    t0 = 288.15
    p0 = 101325
    rho0 = 1.225

    for i in a_h:
        if h <= i[1]:
            hght = height(h0, h)
            t0, p0, rho0 = \
                temp_press_dens(i[0], hght, t0, p0, rho0)
            break
        else:
            h1 = i[1]
            hght = height(h0, h1)
            t0, p0, rho0 = \
                temp_press_dens(i[0], hght, t0, p0, rho0)
            h0 = i[1]

    print ((t0, p0, rho0))