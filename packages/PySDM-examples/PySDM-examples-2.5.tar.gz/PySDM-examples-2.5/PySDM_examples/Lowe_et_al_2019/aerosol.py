from pystrict import strict
from chempy import Substance
from PySDM.initialisation import spectra
from PySDM.physics import si
from PySDM.physics.constants_defaults import rho_w, Mv

compounds = ('palmitic', 'SOA1', 'SOA2', '(NH4)2SO4', 'NH4NO3', 'NaCl')

molar_masses = {
    "(NH4)2SO4": Substance.from_formula("(NH4)2SO4").mass * si.gram / si.mole,
    "NH4NO3": Substance.from_formula("NH4NO3").mass * si.gram / si.mole,
    'SOA1': 190 * si.g / si.mole,
    'SOA2': 368.4 * si.g / si.mole,
    "NaCl": Substance.from_formula("NaCl").mass * si.gram / si.mole,
    "palmitic": 256.4 * si.g / si.mole
}

densities = {
    'palmitic': 0.852 * si.g / si.cm**3,
    'SOA1': 1.24 * si.g / si.cm**3,
    'SOA2': 1.2 * si.g / si.cm**3,
    '(NH4)2SO4': 1.77 * si.g / si.cm**3,
    'NH4NO3': 1.72 * si.g / si.cm**3,
    'NaCl': 2.16 * si.g / si.cm**3
}

is_organic = {
    'palmitic': True,
    'SOA1': True,
    'SOA2': True,
    '(NH4)2SO4': False,
    'NH4NO3': False,
    'NaCl': False
}

ionic_dissociation_phi = {
    'palmitic': 1,
    'SOA1': 1,
    'SOA2': 1,
    '(NH4)2SO4': 3,
    'NH4NO3': 2,
    'NaCl': 2
}


def volume_fractions(mass_fractions: dict):
    return {
        k: (mass_fractions[k] / densities[k]) / sum(
            mass_fractions[i] / densities[i] for i in compounds
        ) for k in compounds
    }


def f_org_volume(mass_fractions: dict):
    volfrac = volume_fractions(mass_fractions)
    return sum(is_organic[k] * volfrac[k] for k in compounds)


def volfrac_just_xxx(volfrac: dict, just_org=True):
    if just_org:
        _masked = {k: (is_organic[k]) * volfrac[k] for k in compounds}
    else:
        _masked = {k: (not is_organic[k]) * volfrac[k] for k in compounds}

    _denom = sum(list(_masked.values()))
    if _denom == 0.0:
        x = {k:0.0 for k in compounds}
    else:
        x = {k:_masked[k] / _denom for k in compounds}
    return x


def kappa(mass_fractions: dict):
    result = {}
    for model in ('bulk', 'film'):
        volfrac = volume_fractions(mass_fractions)
        molar_volumes = {i: molar_masses[i] / densities[i] for i in compounds}

        if model == 'film':
            volume_fractions_of_just_inorg = volfrac_just_xxx(volfrac, just_org=False)
            ns_per_vol = (1 - f_org_volume(mass_fractions)) * sum(
                ionic_dissociation_phi[i] * volume_fractions_of_just_inorg[i] / molar_volumes[i]
                for i in compounds
            )
        elif model == 'bulk':
            ns_per_vol = sum(ionic_dissociation_phi[i] * volfrac[i] / molar_volumes[i]
                             for i in compounds)
        else:
            raise AssertionError()
        result[model] = ns_per_vol * Mv / rho_w

    return result

def nu_org(mass_fractions: dict):
    volfrac = volume_fractions(mass_fractions)
    molar_volumes = {i: molar_masses[i] / densities[i] for i in compounds}
    volume_fractions_of_just_org = volfrac_just_xxx(volfrac, just_org=True)
    _nu = sum(volume_fractions_of_just_org[i] * molar_volumes[i] for i in compounds)
    return _nu

class Aerosol:
    pass


@strict
class AerosolMarine(Aerosol):
    def __init__(self, Acc_Forg: float = 0.2, Acc_N2: float = 134):
        Aitken = {
            'palmitic': .2,
            'SOA1': 0,
            'SOA2': 0,
            '(NH4)2SO4': .8,
            'NH4NO3': 0,
            'NaCl': 0
        }
        Accumulation = {
            'palmitic': Acc_Forg,
            'SOA1': 0,
            'SOA2': 0,
            '(NH4)2SO4': 0,
            'NH4NO3': 0,
            'NaCl': (1-Acc_Forg)
        }

        self.aerosol_modes = (
        {
            'f_org': f_org_volume(Aitken),
            'kappa': kappa(Aitken),
            'nu_org': nu_org(Aitken),
            'spectrum': spectra.Lognormal(
                norm_factor=226 / si.cm ** 3,
                m_mode=19.6 * si.nm,
                s_geom=1.71
            )
        },
        {
            'f_org': f_org_volume(Accumulation),
            'kappa': kappa(Accumulation),
            'nu_org': nu_org(Accumulation),
            'spectrum': spectra.Lognormal(
                norm_factor=Acc_N2 / si.cm ** 3,
                m_mode=69.5 * si.nm,
                s_geom=1.7
            ),
        }
    )
    color = 'dodgerblue'


@strict
class AerosolBoreal(Aerosol):
    def __init__(self, Acc_Forg: float = 0.668, Acc_N2: float = 540):
        # note: SOA1 or SOA2 unclear from the paper
        Aitken = {
            'palmitic': 0,
            'SOA1': 0.668,
            'SOA2': 0,
            '(NH4)2SO4': 0.166,
            'NH4NO3': 0.166,
            'NaCl': 0
        }
        Accumulation = {
            'palmitic': 0,
            'SOA1': 0,
            'SOA2': Acc_Forg,
            '(NH4)2SO4': (1-Acc_Forg)/2,
            'NH4NO3': (1-Acc_Forg)/2,
            'NaCl': 0
        }

        self.aerosol_modes = (
        {
            'f_org': f_org_volume(Aitken),
            'kappa': kappa(Aitken),
            'nu_org': nu_org(Aitken),
            'spectrum': spectra.Lognormal(
                norm_factor=1100 / si.cm ** 3,
                m_mode=22.7 * si.nm,
                s_geom=1.75
            )
        },
        {
            'f_org': f_org_volume(Accumulation),
            'kappa': kappa(Accumulation),
            'nu_org': nu_org(Accumulation),
            'spectrum': spectra.Lognormal(
                norm_factor=Acc_N2 / si.cm ** 3,
                m_mode=82.2 * si.nm,
                s_geom=1.62
            )
        },
    )
    color = 'yellowgreen'


@strict
class AerosolNascent(Aerosol):
    def __init__(self, Acc_Forg: float = 0.3, Acc_N2: float = 30):
        Ultrafine = {
            'palmitic': 0,
            'SOA1': .52,
            'SOA2': 0,
            '(NH4)2SO4': .48,
            'NH4NO3': 0,
            'NaCl': 0
        }
        Accumulation = {
            'palmitic': 0,
            'SOA1': 0,
            'SOA2': Acc_Forg,
            '(NH4)2SO4': (1-Acc_Forg),
            'NH4NO3': 0,
            'NaCl': 0
        }
        self.aerosol_modes = (
            {
                'f_org': f_org_volume(Ultrafine),
                'kappa': kappa(Ultrafine),
                'nu_org': nu_org(Ultrafine),
                'spectrum': spectra.Lognormal(
                    norm_factor=2000 / si.cm ** 3,
                    m_mode=11.5 * si.nm,
                    s_geom=1.71
                )
            },
            {
                'f_org': f_org_volume(Accumulation),
                'kappa': kappa(Accumulation),
                'nu_org': nu_org(Accumulation),
                'spectrum': spectra.Lognormal(
                    norm_factor=Acc_N2 / si.cm ** 3,
                    m_mode=100 * si.nm,
                    s_geom=1.70
                ),
            }
        )
    color = 'orangered'
