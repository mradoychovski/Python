"""
    Calculate temperature, pressure, and density in accordance with ISA
    for given altitude using Hidrostatic equation
    International Standart Atmosphere (ISA):
        altitude = 0 (sea level)
        temperature = 288.15 K (15 C)
        pressure = 101325 Pa
        density = 1.225 kg/m^3
        R = 287.0 J/(kg*K)
"""

from math import e


def delta_altitude(h1, h2):
    """
    Calculate altitude difference in m
    """
    return abs(h2 - h1)


def temp_press_dens(a, h0, T0=288.15, P0=101325, rho0=1.225, g=9.80665, R=287.):
    """
    a -> Lapse rate (temperature change) in Kelvin per meter
    R -> real gas constant for air in J/(kg*K)
    g -> acceleration due to gravity in m/s^2
    h0 -> altitude difference in m
    T0 -> temperature in Kelvin
    P0 -> pressure in Pa
    rho0 -> density in kg/m^3
    """
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
    altitude = input("Enter altitude in m, please: ")

    assert altitude >= 0, "altitude is less then zero"
    assert altitude <= 84852, "altitude is greater then 84852m "

    # [Lapse rate in K/m, altitude in m]
    a_alt = [[-0.0065, 11000], [0, 20000], [0.001, 32000],
        [0.0028, 47000], [0, 51000], [-0.0028, 71000], [-0.002, 84852]]

    h0 = 0
    t0 = 288.15
    p0 = 101325
    rho0 = 1.225

    for i in a_alt:
        if altitude <= i[1]:
            alt = delta_altitude(h0, altitude)
            t0, p0, rho0 = \
                temp_press_dens(i[0], alt, t0, p0, rho0)
            break
        else:
            h1 = i[1]
            alt = delta_altitude(h0, h1)
            t0, p0, rho0 = \
                temp_press_dens(i[0], alt, t0, p0, rho0)
            h0 = i[1]

    print ((t0, p0, rho0))