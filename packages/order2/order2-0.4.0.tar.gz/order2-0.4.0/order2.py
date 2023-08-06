# -*- coding: utf8 -*-
# python >= 3.5
# python3 en supprimant import typing

""" Outils pédagogiques pour l'étude des systèmes du 2ème ordre

Outils pédagogiques pour l'étude des systèmes du 2ème ordre
1) Réponse indicielle en régime transitoire

Equation différentielle (forme canonique) :

(1/w0²).d²y(t)/dt² + (2m/w0).dy(t)/dt + y(t) = A.u(t)

avec :

t : temps en s
A : amplification statique (sans unité)
m : coefficient d'amortissement (sans unité, m >= 0)
w0 : pulsation propre (en rad/s)
u(t) : échelon unité (Heaviside)
u(t) = 0 pour t < 0
u(t) = 1 pour t >= 0

Conditions initiales (système au repos) :
y(t=0) = 0
dy(t=0)/dt = 0

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=2, coeff_amortissement=0.05, w0=1000)
>>> syst.courbe_reponse_indicielle()
>>> syst.show()

2) Etude en régime harmonique (sinusoïdal)

Fonction de transfert (transmittance complexe) :

                A
H(jw) = ----------------------
         1 + 2mjw/w0 -(w/w0)²

avec :
w : pulsation en rad/s
A : amplification statique (sans unité)
m : coefficient d'amortissement (sans unité, m >= 0)
w0 : pulsation propre (en rad/s)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=2, coeff_amortissement=0.05, w0=1000)
>>> syst.bode()
Plot figure ...
>>> syst.show()


Cas particulier : circuit électrique RLC série
----------------------------------------------

                        L
            ---[ R ]---^^^^-----
          ^                     |    ^
tension   |                    ---   |  tension
d'entrée  |                  C ---   |  de sortie
Vin       |                     |    |  Vout
            --------------------

Exemple :
>>> import order2
>>> syst = order2.RLC(R=100, L=0.01, C=100e-9)
>>> print(syst.pulsation_propre)
31622.7766016...
>>> print(syst.amortissement)
0.158113883008...
>>> syst.courbe_reponse_indicielle()
>>> syst.bode()
Plot figure ...
>>> syst.show()

Cas particulier : masse suspendue à un ressort
----------------------------------------------

M : masse en kg
K : constante de raideur du ressort (en N/m)
f : coefficient de frottement (en N.s/m)

Exemple :
>>> import order2
>>> syst = order2.MKF(M=2, K=100, f=13)
>>> print(syst.pulsation_propre)
7.07106781186...
>>> print(syst.amortissement)
0.45961940777...
>>> syst.courbe_reponse_indicielle()
>>> syst.bode()
Plot figure ...
>>> syst.show()
"""

import math
import cmath
import sys
import warnings

from typing import Callable  # python >= 3.5

try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError:
    print("Vous devez installer le module matplotlib pour tracer \
les chronogrammes")

try:
    import acelectricity
except ImportError:
    print("Vous devez installer le module ac-electricity pour tracer \
les diagrammes de Bode")

warnings.simplefilter('default', UserWarning)

""" historique des versions
0.4.0 : add poles
0.3.9 : pep8 style
0.3.8 : add warnings 2022-01
0.3.7 : 2022-01
0.0.1 : initial release 2021-11
"""

__version__ = (0, 4, 0)
__author__ = "Fabrice Sincère <fabrice.sincere@ac-grenoble.fr>"


if sys.version_info[0] < 3:
    print('You need to run this with Python >= 3')
    exit(1)


class Order2:
    """english version
TODO"""
    pass


class Ordre2:
    """ Outils pédagogiques pour l'étude des systèmes du 2ème ordre """
    # constructeur
    def __init__(self, A: float, coeff_amortissement: float, w0: float):
        """ A : amplification statique (sans unité)
m : coefficient d'amortissement (sans unité, m >= 0)
w0 : pulsation propre (en rad/s)
"""
        if w0 <= 0:
            raise ValueError("La pulsation propre doit être positive")
        if coeff_amortissement < 0:
            raise ValueError("Le coefficient d'amortissement doit être positif")
        if A == 0:
            raise ValueError("L'amplification statique ne doit pas être nulle")
        # coefficient d'amortissement
        self.__coeff_amortissement = coeff_amortissement
        # pulsation propre
        self.__w0 = w0
        # pôles
        self.__poles = self.abaque_poles(self.__coeff_amortissement, self.__w0)
        # amplification statique
        self.__A = A
        # fonction de transfert complexe (module acelectricity)
        self.__fonction_transfert = acelectricity.Ratio(
            fw=lambda w: A/(1+2*coeff_amortissement*1j*w/w0-(w/w0)**2))

    @property
    def pulsation_propre(self) -> float:
        """ Retourne la pulsation propre (en rad/s)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.pulsation_propre)
10000
"""
        # getter (lecture seule)
        return self.__w0

    @property
    def amortissement(self) -> float:
        """ Retourne le coefficient d'amortissement (sans unité)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.amortissement)
0.16
"""
        # getter
        return self.__coeff_amortissement

    @property
    def poles(self) -> tuple:
        """ Retourne les 2 pôles de la fonction de transfert :

                A                     A.w0²
H(s) = ---------------------- = ----------------------
         1 + 2ms/w0 +(s/w0)²    (s - pole1)(s - pole2)

avec : s = jw (opérateur de Laplace)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=10, coeff_amortissement=0.6, w0=1000)
>>> print(syst.poles)
((-600+800j), (-600-800j))
>>> syst = order2.Ordre2(A=10, coeff_amortissement=2, w0=1000)
>>> print(syst.poles)
(-267.94919..., -3732.05080...)
"""
        # getter
        return self.__poles

    @property
    def amplification_statique(self) -> float:
        """ Retourne l'amplification statique (sans unité)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.amplification_statique)
1
"""
        # getter
        return self.__A

    @property
    def fonction_transfert(self):
        """ Retourne la fonction de transfert complexe (il s'agit d'un \
objet du module acelectricity)

                A
H(jw) = ----------------------
         1 + 2mjw/w0 -(w/w0)²

avec :
w : pulsation en rad/s
A : amplification statique (sans unité)
m : coefficient d'amortissement (sans unité, m >= 0)
w0 : pulsation propre (en rad/s)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=2, coeff_amortissement=0.05, w0=1000)
>>> H = syst.fonction_transfert
>>> # help(H)
>>> H.properties(150)
Frequency (Hz) : 150
Angular frequency (rad/s) : 942.478
Complex value : 10.4585-8.82161j
Magnitude : 13.6821
Magnitude (dB) : 22.723064994...
Phase (degrees) : -40.1473
Phase (radians) : -0.700702
>>> print(H.db(150))
22.723064994...
>>> print(H.phase_deg(150))
-40.147271165...
"""
        # getter
        return self.__fonction_transfert

    def gain_statique(self) -> float:
        """ Retourne le gain statique (en dB)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=10, coeff_amortissement=0.16, w0=10000)
>>> print(syst.gain_statique())
20.0
"""
        return 20*math.log10(abs(self.__A))

    def frequence_propre(self) -> float:
        """ Retourne la fréquence propre (en hertz)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.frequence_propre())
1591.54943091...
"""
        return self.__w0/(2*math.pi)

    def pseudo_periode(self) -> float:
        """ Retourne la pseudo-période (en seconde)
(dans le cas d'un régime pseudo-périodique)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.pseudo_periode())
0.00063651879320...
"""
        return self.abaque_pseudo_periode(self.__coeff_amortissement,
                                          self.__w0)

    def depassement(self, n: int = 1) -> float:
        """ Retourne le n-ième dépassement en %
(dans le cas d'un régime pseudo-périodique)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.depassement())
60.0967132139...
>>> print(syst.depassement(2))
36.116149391...
"""
        return self.abaque_depassement(self.__coeff_amortissement, n)

    def regime(self) -> str:
        """ Retourne le type de régime :
'apériodique', 'critique'', 'pseudo-périodique' ou 'oscillant'

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.regime())
pseudo-périodique
"""
        # coefficient d'amortissement
        m = self.__coeff_amortissement
        if m == 0:
            return 'oscillant'
        elif 0 < m < 1:
            return 'pseudo-périodique'
        elif m == 1:
            return 'critique'
        elif m > 1:
            return 'apériodique'

    def temps_de_reponse(self, pourcentage: float = 5) -> float:
        """ Retourne le temps de réponse à p % (en seconde)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.temps_de_reponse(5))
0.0016837960245...
>>> print(syst.temps_de_reponse(1))
0.0028855831636...
"""
        return self.abaque_temps_de_reponse(self.__coeff_amortissement,
                                            self.__w0, pourcentage)

    def reponse_indicielle(self, t: float) -> float:
        """ Retourne la réponse indicielle unitaire à l'instant t \
(en seconde)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.reponse_indicielle(0))
0
>>> print(syst.reponse_indicielle(0.00168))
1.05203332613...
>>> print(syst.reponse_indicielle(100))
1.0
"""
        m = self.__coeff_amortissement
        w0 = self.__w0
        A = self.__A

        if t <= 0:
            return 0

        if 0 < m < 1:
            # régime pseudo-périodique
            m0 = math.sqrt(1-m*m)
            phi = math.atan(m0/m)
            # réponse indicielle unitaire
            return A*(1-math.exp(-m*w0*t)*math.sin(w0*m0*t+phi)/m0)
        elif m == 0:
            return A*(1-math.sin(w0*t+math.pi/2))
        elif m == 1:
            return A*(1-(1+t*w0)*math.exp(-w0*t))
        else:
            # régime apériodique
            m0 = math.sqrt(m*m-1)
            # réponse indicielle unitaire
            return (A*(1-(0.5/m0)*(math.exp(-w0*(m-m0)*t)/(m-m0)
                    - math.exp(-w0*(m+m0)*t)/(m+m0))))

    def courbe_reponse_indicielle(self, tmin=None, tmax=None):
        """ Dessine la courbe de la réponse indicielle unitaire \
dans l'intervalle de temps tmin à tmax

tmin : en seconde (None pour une échelle automatique)
tmax : en seconde (None pour une échelle automatique)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=2, coeff_amortissement=0.05, w0=1000)
>>> syst.courbe_reponse_indicielle()
>>> syst.show()
"""
        if self.__coeff_amortissement >= 1:
            if tmin is None:
                tmin = -0.3*self.temps_de_reponse()
            if tmax is None:
                tmax = 3*self.temps_de_reponse()
        else:
            if tmin is None:
                tmin = -1/self.frequence_propre()
            if tmax is None:
                tmax = 10/self.frequence_propre()

        fig, axe = plt.subplots(1, 1)

        axe.grid(True, which="both")

        axe.set_title("Réponse indicielle unitaire", fontsize=14)
        axe.set_xlabel("Temps (s)")

        temps = np.linspace(tmin, tmax, 2000)

        u = []
        for t in temps:
            u.append(self.reponse_indicielle(t))

        axe.plot(temps, u, 'b-', linewidth=2.0)
        fig.tight_layout()

    def show(self):
        """ Affiche les courbes """
        plt.show()

    # <-- régime harmonique
    def frequence_resonance_harmonique(self) -> float:
        """ En régime harmonique, retourne la fréquence de résonance \
(en hertz)
Retourne 0 si le coefficient d'amortissement est >= 1/√2 \
(pas de résonance)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.frequence_resonance_harmonique())
1550.27045...
"""
        return self.abaque_frequence_resonance_harmonique(
            self.__coeff_amortissement, self.__w0)

    def facteur_resonance_harmonique(self) -> tuple:
        """ En régime harmonique, retourne le facteur de résonance \
sans unité et en dB (tuple)
Retourne 1 et 0 dB si le coefficient d'amortissement est >= 1/√2 \
(pas de résonance)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=2, coeff_amortissement=0.05, w0=1000)
>>> print("facteur de résonance : {} ou {} dB".format\
(*syst.facteur_resonance_harmonique()))
facteur de résonance : 10.0125234864... ou 20.010870956... dB
"""
        return self.abaque_facteur_resonance_harmonique(
            self.__coeff_amortissement)

    def fonction_transfert_complexe(self, valeur: float,
                                    unite: str = 'Hz') -> float:
        """ Retourne la fonction de transfert complexe pour une \
fréquence (ou une pulsation) donnée.
valeur : nombre positif
unite : 'Hz' ou 'rad/s'

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=2, coeff_amortissement=0.05, w0=1000)
>>> print(syst.fonction_transfert_complexe(150))
(10.4584682990...-8.8216054763...j)
"""
        return self.__fonction_transfert(valeur, unite)

    def bode(self, xmin=None, xmax=None, xunit='Hz', n=1000,
             xscale='log', yscale='linear',
             magnitude_label='Magnitude', magnitude_unit='db',
             phase_unit='degrees', title='Diagramme de Bode',
             filename=None, draw_phase=True):

        """ En régime harmonique, dessine la réponse en fréquence \
(diagramme de Bode du gain et du déphasage) dans l'intervalle de \
fréquence (ou de pulsation) xmin à xmax

xunit = 'Hz' ou 'rad/s'
xmin : None pour une échelle automatique
xmax : None pour une échelle automatique

n = nombre de points (int)
xscale = 'log' ou 'linear'
yscale = 'log' ou 'linear'
magnitude_unit = 'db' ou 'default'
phase_unit= 'degrees' ou 'radians'
filename (str) : sauvegarde des données dans un fichier au format csv
draw_phase : bool

retourne fig, ax1, ax2, l1, l2
(matplotlib Figure, AxesSubplot (magnitude/dB), AxesSubplot(phase),
Line2D (ax1 plot datas), Line2D (ax2 plot datas))

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=10, coeff_amortissement=10, w0=10000)
>>> syst.bode()
Plot figure ...
>>> syst.show()
"""
        if xunit not in ['Hz', 'rad/s']:
            raise ValueError("xunit ne peut prendre que les valeurs 'Hz' ou \
'rad/s'")

        m = self.__coeff_amortissement
        w0 = self.__w0
        if xmin is None:
            # échelle automatique (en rad/s)
            if m < 1:
                xmin = w0/200  # 2 décades
            else:
                xmin = w0/(2*m*100)  # 2 décades
            if xunit == 'Hz':
                xmin /= 2*math.pi

        if xmax is None:
            # échelle automatique (en rad/s)
            if m < 1:
                xmax = 200*w0  # 2 décades
            else:
                xmax = 2*m*100*w0  # 2 décades
            if xunit == 'Hz':
                xmax /= 2*math.pi

        return self.__fonction_transfert.bode(xmin=xmin, xmax=xmax, xunit=xunit,
                                              n=n, xscale=xscale, yscale=yscale,
                                              magnitude_label=magnitude_label,
                                              magnitude_unit=magnitude_unit,
                                              phase_unit=phase_unit,
                                              title=title, filename=filename,
                                              draw_phase=draw_phase)

    def frequence_coupure_harmonique(self) -> float:
        """ En régime harmonique, retourne la fréquence de coupure à \
-3 dB (en Hz)

Exemple :
>>> import order2
>>> syst = order2.Ordre2(A=1, coeff_amortissement=0.16, w0=10000)
>>> print(syst.frequence_coupure_harmonique())
2427.97905105...
"""
        return self.abaque_frequence_coupure_harmonique(
            self.__coeff_amortissement, self.__w0)

    @staticmethod
    def abaque_frequence_coupure_harmonique(coeff_amortissement: float,
                                            w0: float) -> float:
        """ En régime harmonique, retourne la fréquence de coupure à \
-3 dB (en Hz)

Exemple :
>>> import order2
>>> print(order2.Ordre2.abaque_frequence_coupure_harmonique(\
coeff_amortissement=0.16, w0=10000))
2427.97905105...
"""
        m = coeff_amortissement
        if m < 0:
            raise ValueError("Le coefficient d'amortissement doit être positif")
        if w0 <= 0:
            raise ValueError("La pulsation propre doit être positive")
        if m <= 100:
            # formule théorique
            return w0/(2*math.pi)*math.sqrt(1-2*m*m+math.sqrt((2*m*m-1)**2+1))
        else:
            # approximation (car la précision de la formule
            # théorique se dégrade quand m augmente)
            warnings.warn('Valeur approchée avec une bonne approximation')
            return w0/(2*math.pi)/math.sqrt(2*(2*m*m-1))

    @staticmethod
    def abaque_poles(coeff_amortissement: float, w0: float) -> tuple:
        """Retourne les 2 pôles de la fonction de transfert
calculés à partir du coefficient d'amortissement et de la pulsation propre :

                A                     A.w0²
H(s) = ---------------------- = ----------------------
         1 + 2ms/w0 +(s/w0)²    (s - pole1)(s - pole2)

avec : s = jw (opérateur de Laplace)

>>> import order2
>>> print(order2.Ordre2.abaque_poles(coeff_amortissement=0, w0=1000))
(1000j, -1000j)
>>> print(order2.Ordre2.abaque_poles(0.6, 1000))
((-600+800j), (-600-800j))
>>> print(order2.Ordre2.abaque_poles(1, 1000))
(-1000, -1000)
>>> print(order2.Ordre2.abaque_poles(2, 1000))
(-267.94919..., -3732.05080...)
"""
        m = coeff_amortissement
        if m < 0:
            raise ValueError("Le coefficient d'amortissement doit être positif")
        if w0 <= 0:
            raise ValueError("La pulsation propre doit être positive")
        if m == 0.0:
            return 1j*w0, -1j*w0
        elif m == 1.0:
            return -w0, -w0
        elif 0.0 < m < 1.0:
            # 2 pôles complexes conjugués
            p1 = -m*w0 + 1j*w0*math.sqrt(1-m*m)
            p2 = -m*w0 - 1j*w0*math.sqrt(1-m*m)
            return p1, p2
        else:
            # m > 1
            # 2 pôles réels négatifs
            if m > 1e6:
                # approximation (car la précision de la formule
                # théorique se dégrade quand m augmente)
                warnings.warn('Valeur approchée avec une bonne approximation')
                p1 = -w0/(2*m)
                p2 = -2*m*w0
                return p1, p2
            else:
                p1 = -m*w0 + w0*math.sqrt(m*m-1)
                p2 = -m*w0 - w0*math.sqrt(m*m-1)
                return p1, p2

    @staticmethod
    def abaque_m_w0_depuis_poles(pole1: complex, pole2: complex) -> tuple:
        """Retourne le tuple (coefficient d'amortissement, pulsation propre)
calculé à partir des 2 pôles de la fonction de transfert :

                A                     A.w0²
H(s) = ---------------------- = ----------------------
         1 + 2ms/w0 +(s/w0)²    (s - pole1)(s - pole2)

avec : s = jw (opérateur de Laplace)

>>> import order2
>>> print(order2.Ordre2.abaque_m_w0_depuis_poles(-268, -3732))
(1.99982..., 1000.087...)
>>> print(order2.Ordre2.abaque_m_w0_depuis_poles(-1000, -1000))
(1.0, 1000.0)
>>> print(order2.Ordre2.abaque_m_w0_depuis_poles(-600+800j, -600-800j))
(0.6, 1000.0)
>>> print(order2.Ordre2.abaque_m_w0_depuis_poles(-1000j, 1000j))
(0.0, 1000.0)
"""
        pole1 = complex(pole1)
        pole2 = complex(pole2)
        if pole1.imag == 0.0 and pole2.imag == 0.0:
            # les deux pôles sont réels
            # m >= 1
            if pole1.real >= 0.0 or pole2.real >= 0.0:
                raise ValueError("Partie réelle négative attendue")
            tau1 = -1/pole1.real  # constante de temps (en seconde)
            tau2 = -1/pole2.real
            w0 = 1/math.sqrt(tau1*tau2)
            m = (tau1+tau2)/(2*math.sqrt(tau1*tau2))
            return m, w0
        else:
            # les deux pôles sont complexes
            # 0 <= m < 1
            if cmath.isclose(pole1, pole2.conjugate()) is False:
                raise ValueError("Pôles complexes conjugués attendus")
            if pole1.real > 0.0:
                raise ValueError("Partie réelle négative attendue")
            w0 = abs(pole1)
            m = -pole1.real/w0
            return m, w0

    @staticmethod
    def abaque_coeff_amortissement_harmonique(
            facteur_resonance_db: float) -> float:
        """ En régime harmonique, retourne le coefficient \
d'amortissement à partir du facteur de résonance en dB

Exemple :
>>> import order2
>>> print(order2.Ordre2.abaque_coeff_amortissement_harmonique(\
facteur_resonance_db=20))
0.0500627750598...
"""
        if facteur_resonance_db <= 0:
            raise ValueError("Valeur positive attendue")

        if facteur_resonance_db > 100:
            # approximation
            try:
                f = 10**(facteur_resonance_db/20)
            except OverflowError:
                warnings.warn('Valeur attendue très proche de 0')
                return 0.0
            warnings.warn('Valeur approchée avec une bonne approximation')
            return 1/(2*f)

        # formule théorique
        f = 10**(facteur_resonance_db/20)
        return math.sqrt((1-math.sqrt(1-1/f**2))/2)

    @staticmethod
    def abaque_facteur_resonance_harmonique(
            coeff_amortissement: float) -> tuple:
        """ En régime harmonique, retourne le facteur de résonance \
sans unité et en dB (tuple)
Retourne 1 et 0 dB si le coefficient d'amortissement est >= 1/√2 \
(pas de résonance)

Exemple :
>>> import order2
>>> result = order2.Ordre2.abaque_facteur_resonance_harmonique(\
coeff_amortissement=0.05)
>>> print("facteur de résonance : {} ou {} dB".format(*result))
facteur de résonance : 10.0125234864... ou 20.010870956... dB
"""
        m = coeff_amortissement
        if m < 0:
            raise ValueError("Le coefficient d'amortissement doit être positif")
        if m == 0:
            warnings.warn('Résonance infinie')
            return float('inf'), float('inf')
        elif m >= 1/math.sqrt(2):
            # pas de résonance harmonique
            warnings.warn('Pas de résonance')
            return 1, 0
        else:
            f = 1/(2*m*math.sqrt(1-m*m))
            return f, 20*math.log10(f)

    @staticmethod
    def abaque_pulsation_propre_resonance_harmonique(
            coeff_amortissement: float, frequence_resonance: float) -> float:
        """ En régime harmonique, retourne la pulsation propre \
(en rad/s)
Retourne 0 si le coefficient d'amortissement est >= 1/√2 \
(pas de résonance)

Exemple :
>>> import order2
>>> print(order2.Ordre2.abaque_pulsation_propre_resonance_harmonique(\
coeff_amortissement=0.16, frequence_resonance=1550.27))
9999.9970809...
"""
        m = coeff_amortissement
        if m < 0:
            raise ValueError("Le coefficient d'amortissement doit être positif")
        fr = frequence_resonance
        if fr <= 0:
            raise ValueError("La fréquence de résonance doit être positive")

        if m >= 1/math.sqrt(2):
            # pas de résonance harmonique
            warnings.warn('Pas de résonance')
            return 0
        else:
            return fr*(2*math.pi)/math.sqrt(1-2*m*m)

    @staticmethod
    def abaque_frequence_resonance_harmonique(
            coeff_amortissement: float, w0: float) -> float:
        """ En régime harmonique, retourne la fréquence de résonance \
(en hertz)
Retourne 0 si le coefficient d'amortissement est >= 1/√2 \
(pas de résonance)

Exemple :
>>> import order2
>>> print(order2.Ordre2.abaque_frequence_resonance_harmonique(\
coeff_amortissement=0.16, w0=10000))
1550.27045...
"""
        m = coeff_amortissement
        if m < 0:
            raise ValueError("Le coefficient d'amortissement doit être positif")
        if w0 <= 0:
            raise ValueError("La pulsation propre doit être positive")

        if m >= 1/math.sqrt(2):
            # pas de résonance harmonique
            warnings.warn('Pas de résonance')
            return 0
        else:
            return w0*math.sqrt(1-2*m*m)/(2*math.pi)

    @staticmethod
    def abaque_temps_de_reponse(coeff_amortissement: float, w0: float,
                                pourcentage: float = 5) -> float:
        """ Retourne le temps de réponse à p % (en seconde)
coeff_amortissement : coefficient d'amortissement (sans unité)
w0 : pulsation propre (en rad/s)

Exemple :
>>> import order2
>>> print(order2.Ordre2.abaque_temps_de_reponse(\
coeff_amortissement=0.16, w0=10000))
0.0016837960245...
"""
        m = coeff_amortissement
        if m < 0:
            raise ValueError("Le coefficient d'amortissement doit être \
positif")
        if w0 <= 0:
            raise ValueError("La pulsation propre doit être positive")
        # pourcentage
        p = pourcentage*0.01

        if not(0.000001 <= p <= 1):
            raise ValueError("Le pourcentage doit être compris \
entre 0.0001 % et 100 %")
        if p == 1:  # 100 %
            return 0

        if m == 0:
            # régime oscillant
            warnings.warn('Temps de réponse infini')
            return float('inf')
        elif 0 < m < 1:
            # régime pseudo-périodique
            m0 = math.sqrt(1-m*m)
            phi = math.atan(m0/m)

            def u(t):
                # réponse indicielle unitaire
                return 1-math.exp(-m*w0*t)*math.sin(w0*m0*t+phi)/m0

            # recherche des deux dépassements successifs qui encadrent
            # la solution [D(n-1), D(n)]
            n = 1
            while not 1-p < u(n*math.pi/(w0*m0)) < 1+p:
                n += 1
                if n > 10000:
                    raise ValueError("Problème de convergence")

            # n impaire dépassement positif
            # n paire dépassement négatif
            if n % 2 == 0:
                y = 1+p
            else:
                y = 1-p
            # recherche solution
            # solution tr 5 % # 4.74/w0 pour m=1
            # solution tr 1 % # 6.64/w0 pour m=1
            # solution tr 5 % # 2.86/w0 pour m=0.691 (minimum)
            # solution tr 5 % # 29/w0   pour m=0.1
            # solution tr 5 % # 299/w0  pour m=0.01
            # solution tr 5 % # 2994/w0 pour m=0.001
            # m << 1 : tr 5 % # 3/(m*w0)
            # m << 1 : tr 1 % # 4.6/(m*w0)
            return _rechercheSolution((n-1)*math.pi/(w0*m0),
                                      n*math.pi/(w0*m0), y, 1e-9, u)

        elif m == 1:
            # régime apériodique critique
            def u(t):
                # réponse indicielle unitaire
                return 1-(1+t*w0)*math.exp(-w0*t)
            # recherche solution
            # solution tr 5 % # 4.74/w0
            # solution tr 1 % # 6.64/w0

            # intervalle de recherche
            intervalle = 10/w0  # OK pour 5 % et 1 %
            if p < 0.01:
                # on élargie l'intervalle
                compteur = 0
                while u(intervalle) < 1-p:
                    intervalle *= 2
                    compteur += 1
                    if compteur > 10000:
                        raise ValueError("Problème de convergence")
            return _rechercheSolution(0, intervalle, 1-p, 1e-9, u)

        elif m > 1:
            # régime apériodique
            m0 = math.sqrt(m*m-1)

            def u(t):
                # réponse indicielle unitaire
                return (1-(0.5/m0)*(math.exp(-w0*(m-m0)*t)/(m-m0)
                        - math.exp(-w0*(m+m0)*t)/(m+m0)))
            # recherche solution
            # solution tr 5 % # 4.74/w0 pour m=1
            # solution tr 1 % # 6.64/w0 pour m=1
            # solution tr 5 % # 11.5/w0 pour m=2
            # solution tr 5 % # 59.8/w0 pour m=10
            # solution tr 5 % # 599/w0  pour m=100
            # solution tr 5 % # 5991/w0 pour m=1000
            # m >> 1 : tr 5 % # 6*m/w0
            # m >> 1 : tr 1 % # 9.2*m/w0

            # intervalle de recherche
            intervalle = m*10/w0  # OK pour 5 % et 1 %
            if p < 0.01:
                # on élargie l'intervalle
                compteur = 0
                while u(intervalle) < 1-p:
                    intervalle *= 2
                    compteur += 1
                    if compteur > 10000:
                        raise ValueError("Problème de convergence")
            return _rechercheSolution(0, intervalle, 1-p, 1e-9, u)

    @staticmethod
    def abaque_coeff_amortissement(depassement: float) -> float:
        """ Retourne le coefficient d'amortissement en fonction du \
premier dépassement en % (dans le cas d'un régime pseudo-périodique)

Exemple :
>>> import order2
>>> print(order2.Ordre2.abaque_coeff_amortissement(depassement=60))
0.160493046664...
"""
        if 0 <= depassement <= 100:
            if depassement == 0:
                return 1
            elif depassement == 100:
                return 0
            else:
                # formule théorique
                return (-math.log(depassement/100)/math.sqrt(math.pi**2
                        + math.log(depassement/100)**2))
        raise ValueError("Le premier dépassement doit être compris \
entre 0 et 100 %")

    @staticmethod
    def abaque_depassement(coeff_amortissement: float, n: int = 1) -> float:
        """ Retourne le n-ième dépassement en % en fonction du \
coefficient d'amortissement (dans le cas d'un régime pseudo-périodique)

Exemple :
>>> import order2
>>> print(order2.Ordre2.abaque_depassement(coeff_amortissement=0.16))
60.0967132139...
"""
        if 0 <= coeff_amortissement <= 1:
            if coeff_amortissement == 1:
                return 0
            # formule théorique
            D = math.exp(-n*coeff_amortissement*math.pi /
                         (math.sqrt(1-coeff_amortissement**2)))*100
            return D
        raise ValueError("Le régime doit être pseudo-périodique")

    @staticmethod
    def abaque_pulsation_propre(coeff_amortissement: float,
                                pseudo_periode: float) -> float:
        """ Retourne la pulsation propre (en rad/s) en fonction du \
coefficient d'amortissement et de la pseudo-période (en seconde)
(dans le cas d'un régime pseudo-périodique)

Exemple :
>>> import order2
>>> print(order2.Ordre2.abaque_pulsation_propre(\
coeff_amortissement=0.16, pseudo_periode=0.0006365))
10000.295258...
"""
        # régime pseudo-périodique ou oscillant
        if 0 <= coeff_amortissement < 1:
            Tp = 2*math.pi/(math.sqrt(1-coeff_amortissement**2)*pseudo_periode)
            return Tp
        raise ValueError("Le régime n'est pas pseudo-périodique")

    @staticmethod
    def abaque_pseudo_periode(coeff_amortissement: float, w0: float) -> float:
        """ Retourne la pseudo-période (en seconde) en fonction du \
coefficient d'amortissement et de la pulsation propre (en rad/s)
(dans le cas d'un régime pseudo-périodique)

Exemple :
>>> import order2
>>> print(order2.Ordre2.abaque_pseudo_periode(\
coeff_amortissement=0.16, w0=10000))
0.00063651879320...
"""
        # régime pseudo-périodique ou oscillant
        if 0 <= coeff_amortissement < 1:
            Tp = 2*math.pi/(math.sqrt(1-coeff_amortissement**2)*w0)
            return Tp
        raise ValueError("Le régime n'est pas pseudo-périodique")


class RLC(Ordre2):
    """ Outils pour l'étude des circuits électriques RLC série

                        L
            ---[ R ]---^^^^-----
          ^                     |    ^
tension   |                    ---   |  tension
d'entrée  |                  C ---   |  de sortie
Vin       |                     |    |  Vout
            --------------------

Exemple :
>>> import order2
>>> syst = order2.RLC(R=100, L=0.01, C=100e-9)
>>> print(syst.pulsation_propre)
31622.7766016...
>>> print(syst.amortissement)
0.158113883008...
>>> syst.courbe_reponse_indicielle()
>>> syst.bode()
Plot figure ...
>>> syst.show()
"""

    # constructeur
    def __init__(self, R: float, L: float, C: float):
        """ R résistance en Ω
L inductance en henry
C capacité en farad
"""
        # attributs d'instance
        self.__R = R  # Ω
        if self.__R < 0:
            raise ValueError("R doit être positif")
        self.__L = L  # henry
        if self.__L <= 0:
            raise ValueError("L doit être strictement positif")
        self.__C = C  # farad
        if self.__C <= 0:
            raise ValueError("C doit être strictement positif")

        # coefficient d'amortissement
        coeff_amortissement = (self.__R/2)*math.sqrt(self.__C/self.__L)
        # pulsation propre
        w0 = 1/math.sqrt(self.__L*self.__C)
        # amplification statique
        A = 1

        # héritage
        Ordre2.__init__(self, A, coeff_amortissement, w0)

    @property
    def R(self) -> float:
        """ Retourne la résistance (en Ω) """
        # getter
        return self.__R

    @property
    def L(self) -> float:
        """ Retourne l'inductance (en H)"""
        # getter
        return self.__L

    @property
    def C(self) -> float:
        """ Retourne la capacité (en F)"""
        # getter
        return self.__C

    def resistance_critique(self) -> float:
        """ Retourne la résistance critique en Ω """
        return 2*math.sqrt(self.__L/self.__C)

    def inductance_critique(self) -> float:
        """ Retourne l'inductance critique en H """
        if self.__R == 0:
            return None
        else:
            return self.__C*self.__R**2/4

    def capacite_critique(self) -> float:
        """ Retourne la capacité critique en F """
        if self.__R == 0:
            return None
        else:
            return 4*self.__L/self.__R**2


class MKF(Ordre2):
    """ Un exemple de système du 2ème ordre dans le domaine mécanique :
masse suspendue à un ressort

M : masse en kg
K : constante de raideur du ressort (en N/m)
f : coefficient de frottement (en N.s/m)

Exemple :
>>> import order2
>>> syst = order2.MKF(M=2, K=100, f=13)
>>> print(syst.pulsation_propre)
7.07106781186...
>>> print(syst.amortissement)
0.45961940777...
>>> syst.courbe_reponse_indicielle()
>>> syst.bode()
Plot figure ...
>>> syst.show()
"""
    # constructeur
    def __init__(self, M: float, K: float, f: float):
        """ M : masse en kg
K : constante de raideur du ressort (en N/m)
f : coefficient de frottement (en N.s/m)
"""
        # attributs d'instance
        self.__M = M
        if self.__M <= 0:
            raise ValueError("M doit être strictement positive")
        self.__K = K
        if self.__K <= 0:
            raise ValueError("K doit être strictement positive")
        self.__f = f  # farad
        if self.__f <= 0:
            raise ValueError("f doit être strictement positif")

        # coefficient d'amortissement
        coeff_amortissement = self.__f/(2*math.sqrt(self.__K*self.__M))
        # pulsation propre
        w0 = math.sqrt(self.__K/self.__M)
        # amplification statique
        A = 1

        # héritage
        Ordre2.__init__(self, A, coeff_amortissement, w0)

    @property
    def M(self) -> float:
        """ Retourne la masse (en kg) """
        # getter
        return self.__M

    @property
    def f(self) -> float:
        """ Retourne le coefficient de frottement (en N.s/m) """
        # getter
        return self.__f

    @property
    def K(self) -> float:
        """ Retourne la constante de raideur du ressort (en N/m) """
        # getter
        return self.__K


def show():
    """ Affiche les courbes """
    plt.show()

# python 3.4
# def _rechercheSolution(a: float, b: float, y0: float, eps: float,
#                        f: [[float], float]) -> float:
# python >= 3.5


def _rechercheSolution(a: float, b: float, y0: float, eps: float,
                       f: Callable[[float], float]) -> float:
    """Recherche par dichotomie de la solution x de l'équation f(x) = y0
f est une fonction à une variable réelle
intervalle de recherche [a, b]
eps précision relative sur x

Exemple :

>>> def g(x):
...     return x*x
>>> solution = _rechercheSolution(1, 200, 20000, 1e-9, g)
>>> print(solution)
141.42135620...
"""
    # autre solution : module Scipy...
    if (f(a)-y0)*(f(b)-y0) > 0:
        raise ValueError("Mauvais intervalle de recherche")
    compteur = 0
    while ((abs(a-b) if a == 0 else abs((a-b)/a))) > abs(eps):
        c = (a+b)/2
        if (f(a)-y0)*(f(c)-y0) < 0:
            b = c
        else:
            a = c
        compteur += 1
        if compteur > 10000:
            raise ValueError("Problème de convergence")
    return c


if __name__ == '__main__':
    # aide sur le module
    help(__name__)
    # doctest
    import doctest
    doctest.testmod(verbose=True,
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
