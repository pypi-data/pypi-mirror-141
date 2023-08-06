#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
def PLANCK():

    """
    ========== DESCRIPTION ==========

    This function return the Planck constant

    ========== VALIDITY ==========

    Always

    ========== FROM ==========

    Wikipedia : https://en.wikipedia.org/wiki/Planck_constant

    ========== INPUT ==========

    ========== OUTPUT ==========

    <PLANCK>
        -- float --
    	The Planck constant
        [kg].[m]**(2).[s]**(-1)

    ========== STATUS ==========

    Status : Checked

    """

    ################## RETURN #################################################

    return  6.626070040e-34

#%%
def REDUCED_PLANCK():

    """
    ========== DESCRIPTION ==========

    This function return the reduced Planc constant

    ========== VALIDITY ==========

    Always

    ========== FROM ==========

    Wikipedia : https://en.wikipedia.org/wiki/Planck_constant

    ========== INPUT ==========

    ========== OUTPUT ==========

    <REDUCES_PLANCK>
        -- float --
    	The reduced Planck constant
        [kg].[m]**(2).[s]**(-1)

    ========== STATUS ==========

    Status : Checked

    """

    ################## MODULES ################################################

    import numpy as np
    from cryopy import Constant

    ################## RETURN #################################################

    return  Constant.PLANCK/2/np.pi

#%%
def GAS():

    """
    ========== DESCRIPTION ==========

    This function return the molar gas constant

    ========== VALIDITY ==========

    Always

    ========== FROM ==========

    Wikipedia : https://en.wikipedia.org/wiki/Gas_constant

    ========== INPUT ==========

    ========== OUTPUT ==========

    [GAS]
        -- float --
        [J].[K]**(-1).[mol]**(-1)
    	The molar gas constant

    ========== STATUS ==========

    Status : Checked

    """

    ################## RETURN #################################################

    return  8.31446261815324

#%%
def BOLTZMANN():

    """
    ========== DESCRIPTION ==========

    This function return the Boltzmann constant

    ========== VALIDITY ==========

    Always

    ========== FROM ==========

    Wikipedia : https://en.wikipedia.org/wiki/Boltzmann_constant

    ========== INPUT ==========

    ========== OUTPUT ==========

    <BOLTZMANN>
        -- float --
    	The Boltzmann constant
        [J].[K]**(-1)

    ========== STATUS ==========

    Status : Checked

    """

    ################## RETURN #################################################

    return  1.38064852e-23

#%%
def AVOGADRO():

    """
    ========== DESCRIPTION ==========

    This function return the Avogadro constant

    ========== VALIDITY ==========

    Always

    ========== SOURCE ==========

    Wikipedia : https://en.wikipedia.org/wiki/Avogadro_constant

    ========== INPUT ==========

    ========== OUTPUT ==========

    <AVOGADRO>
        -- float --
    	The Avogadro constant
        [mol]**(-1)

    ========== STATUS ==========

    Status : Checked

    """

    ################## RETURN #################################################

    return  6.0221367e23

#%%
def SPEED_OF_LIGHT():

    """
    ========== DESCRIPTION ==========

    This function return the speed of light in vacuum

    ========== VALIDITY ==========

    Only in Vacuum

    ========== FROM ==========

    Wikipedia : https://en.wikipedia.org/wiki/Speed_of_light

    ========== INPUT ==========

    ========== OUTPUT ==========

    <SPEED_OF_LIGHT>
        -- int --
    	The speed of light
        [m].[s]**(-1)

    ========== STATUS ==========

    Status : Checked

    """

    ################## RETURN #################################################

    return  299792458


#%%
def STEFAN_BOLTMANN():

    """
    ========== DESCRIPTION ==========

    This function return the Stefan-Boltzmann constant

    ========== VALIDITY ==========

    Always

    ========== FROM ==========

    Wikipedia : https://en.wikipedia.org/wiki/Stefan–Boltzmann_law

    ========== INPUT ==========

    ========== OUTPUT ==========

    <STEFAN_BOLTMANN>
        -- float --
    	The Stefan-Boltzmann constant
        [W].[m]**(-2).[K]**(-4)

    ========== STATUS ==========

    Status : Checked

    """

    ################## MODULES ################################################

    import numpy as np
    from cryopy import Constant

    ################## RETURN #################################################

    return 2*np.pi**5*Constant.BOLTZMANN**4/(15*Constant.SPEED_OF_LIGHT**2*Constant.PLANCK**3)
