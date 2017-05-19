#!/usr/bin/python
"""
    seawater_state.py
Lives: /Users/pgierz/Code/MyPythonModules/analysis/seawater_state.py

Calculates the state equation is seawater and returns alpha, beta, and rho

Paul J. Gierz Fri May 29 14:21:36 2015
"""


def state(t, s, p):
    #-------------------------------------------------------------------------
    #
    #   Calculate the state equation
    #
    #-------------------------------------------------------------------------
    #     Refer to J.C Williams and G. Danabasoglu, JPO 2002,2054-2071
    #     Modifed form ccsm3_0_1_beta32_pop/source/hmix_gm by Wei Liu 2010/11/01
    #-------------------------------------------------------------------------

    #*** these constants will be used to construct the numerator
    #*** factor unit change (kg/m^3 -> g/cm^3) into numerator terms
    mwjfnp0s0t0 = 9.99843699e+2 * 0.001
    mwjfnp0s0t1 = 7.35212840e+0 * 0.001
    mwjfnp0s0t2 = -5.45928211e-2 * 0.001
    mwjfnp0s0t3 = 3.98476704e-4 * 0.001
    mwjfnp0s1t0 = 2.96938239e+0 * 0.001
    mwjfnp0s1t1 = -7.23268813e-3 * 0.001
    mwjfnp0s2t0 = 2.12382341e-3 * 0.001
    mwjfnp1s0t0 = 1.04004591e-2 * 0.001
    mwjfnp1s0t2 = 1.03970529e-7 * 0.001
    mwjfnp1s1t0 = 5.18761880e-6 * 0.001
    mwjfnp2s0t0 = -3.24041825e-8 * 0.001
    mwjfnp2s0t2 = -1.23869360e-11 * 0.001
    #*** these constants will be used to construct the denominator
    mwjfdp0s0t0 = 1.0e+0
    mwjfdp0s0t1 = 7.28606739e-3
    mwjfdp0s0t2 = -4.60835542e-5
    mwjfdp0s0t3 = 3.68390573e-7
    mwjfdp0s0t4 = 1.80809186e-10
    mwjfdp0s1t0 = 2.14691708e-3
    mwjfdp0s1t1 = -9.27062484e-6
    mwjfdp0s1t3 = -1.78343643e-10
    mwjfdp0sqt0 = 4.76534122e-6
    mwjfdp0sqt2 = 1.63410736e-9
    mwjfdp1s0t0 = 5.30848875e-6
    mwjfdp2s0t3 = -3.03175128e-16
    mwjfdp3s0t1 = -1.27934137e-17

    #  get thermal and samlity coefficient for current level from state subroutine

    SQR = s ** 0.500

    #*************************************************************************
    #      Below is the calculation of the isppycal slope DRDT and DRDS
    #                   from the state equation
    #*************************************************************************
    tmin = -2.0    # limited on the low end
    tmax = 999.0   # unlimited on the high end
    smin = 0.0    # limited on the low end
    smax = 999     # unlimited on the high end
    t = min(t, tmax)
    t = max(t, tmin)
    s = min(s, smax)
    s = max(s, smin)
    #p = 10.*0.059808*(exp(-0.025*depth)-1.)+0.100766*depth+2.28405e-7*depth^2;
    p = 10 * p
    #***
    #*** first calculate numerator of MWJF density [P_1(S,T,p)]
    #***
    mwjfnums0t0 = mwjfnp0s0t0 + p * (mwjfnp1s0t0 + p * mwjfnp2s0t0)
    mwjfnums0t1 = mwjfnp0s0t1
    mwjfnums0t2 = mwjfnp0s0t2 + p * (mwjfnp1s0t2 + p * mwjfnp2s0t2)
    mwjfnums0t3 = mwjfnp0s0t3
    mwjfnums1t0 = mwjfnp0s1t0 + p * mwjfnp1s1t0
    mwjfnums1t1 = mwjfnp0s1t1
    mwjfnums2t0 = mwjfnp0s2t0
    WORK1 = mwjfnums0t0 + t*(mwjfnums0t1 + t*(mwjfnums0t2 + mwjfnums0t3 * t)) + s*(mwjfnums1t0 + mwjfnums1t1 * t + mwjfnums2t0 * s)
    #***
    #*** now calculate denominator of MWJF density [P_2(S,T,p)]
    #***
    mwjfdens0t0 = mwjfdp0s0t0 + p * mwjfdp1s0t0
    mwjfdens0t1 = mwjfdp0s0t1 + p ** 3 * mwjfdp3s0t1
    mwjfdens0t2 = mwjfdp0s0t2
    mwjfdens0t3 = mwjfdp0s0t3 + p ** 2 * mwjfdp2s0t3
    mwjfdens0t4 = mwjfdp0s0t4
    mwjfdens1t0 = mwjfdp0s1t0
    mwjfdens1t1 = mwjfdp0s1t1
    mwjfdens1t3 = mwjfdp0s1t3
    mwjfdensqt0 = mwjfdp0sqt0
    mwjfdensqt2 = mwjfdp0sqt2

    WORK2 = mwjfdens0t0 + t*(mwjfdens0t1 + t*(mwjfdens0t2 + t*(mwjfdens0t3 + mwjfdens0t4*t))) + s*(mwjfdens1t0 + t*(mwjfdens1t1 + t*t*mwjfdens1t3) + SQR*(mwjfdensqt0 + t*t * mwjfdensqt2))

    DENOMK = 1. / WORK2

    WORK3 = mwjfnums0t1 + t*(2 * mwjfnums0t2 + 3 * mwjfnums0t3 * t) + mwjfnums1t1 * s
    WORK4 = mwjfdens0t1 + s*mwjfdens1t1 + t* (2 * (mwjfdens0t2 + s*SQR*mwjfdensqt2) + t*(3 * (mwjfdens0t3 + s * mwjfdens1t3) + t*4 * mwjfdens0t4))
    drdt = (WORK3 - WORK1*DENOMK*WORK4)*DENOMK

    WORK3 = mwjfnums1t0 + mwjfnums1t1 * t + 2 * mwjfnums2t0 * s
    WORK4 = mwjfdens1t0 + t*(mwjfdens1t1 + t*t*mwjfdens1t3) + 1.5 * SQR*(mwjfdensqt0 + t*t * mwjfdensqt2)
    drds = (WORK3 - WORK1*DENOMK*WORK4)*DENOMK

    # alpha is thermal expansion coefficient : alpha = -(1/rho)*drdt
    # beta is haline contraction coefficient : beta  = (1/rho)*drds
    rho = WORK1*DENOMK
    alpha = -1. / rho*drdt
    beta = 1. / rho*drds
    return alpha, beta, rho
