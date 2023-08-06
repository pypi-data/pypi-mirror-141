## module order2

Outils pédagogiques pour l'étude des systèmes du 2ème ordre

### Installation du module python order2

From Pypi repository :  
[https://pypi.org/project/order2](https://pypi.org/project/order2)

```
pip install order2
```

### Réponse indicielle en régime transitoire

On s'intéresse aux systèmes du 2ème ordre régis par l'équation différentielle suivante :

```
(1/ω0²).d²y(t)/dt² + (2m/ω0).dy(t)/dt + y(t) = A.u(t)
```

avec :

- t : temps en s
- A : amplification statique (sans unité)
- m : coefficient d'amortissement (sans unité, m >= 0)
- ω0 : pulsation propre (en rad/s)
- u(t) : échelon unité (Heaviside)
    - u(t) = 0 pour t < 0
    - u(t) = 1 pour t >= 0

Conditions initiales (système au repos) :  
- y(t=0) = 0
- dy(t=0)/dt = 0

Exemple :  
```python
>>> import order2
>>> syst = order2.Ordre2(A=2, coeff_amortissement=0.05, w0=1000)
>>> syst.courbe_reponse_indicielle()
>>> syst.show()
``` 

![screenshot01](https://framagit.org/fsincere/order2/-/raw/master/images/image01.png)


```python
>>> syst = order2.Ordre2(A=1, coeff_amortissement=2.5, w0=1000)
>>> syst.courbe_reponse_indicielle()
>>> syst.show()
``` 

![screenshot01b](https://framagit.org/fsincere/order2/-/raw/master/images/image01b.png)


### Etude en régime harmonique (sinusoïdal)

La fonction de transfert (transmittance complexe) s'écrit alors :

```
                A
H(jω) = ----------------------
         1 + 2mjω/ω0 -(ω/ω0)²
```

avec :  
- ω : pulsation en rad/s
- A : amplification statique (sans unité)
- m : coefficient d'amortissement (sans unité, m >= 0)
- ω0 : pulsation propre (en rad/s)

Exemple :  
```python 
>>> import order2
>>> syst = order2.Ordre2(A=2, coeff_amortissement=0.05, w0=1000)
>>> syst.bode()
>>> syst.show()
```

![screenshot02](https://framagit.org/fsincere/order2/-/raw/master/images/image02.png)

### Cas particulier : circuit électrique RLC série

```
                        L
            ---[ R ]---^^^^-----
          ^                     |    ^
tension   |                    ---   |  tension
d'entrée  |                  C ---   |  de sortie
Vin       |                     |    |  Vout
            --------------------
```

- R résistance en Ω
- L inductance en henry
- C capacité en farad

Exemple :  
```python 
>>> import order2
>>> syst = order2.RLC(R=100, L=0.01, C=100e-9)
>>> print(syst.pulsation_propre)
31622.7766016
>>> print(syst.amortissement)
0.158113883008
>>> syst.courbe_reponse_indicielle()
>>> syst.bode()
>>> syst.show()
```

![screenshot03](https://framagit.org/fsincere/order2/-/raw/master/images/image03.png)

![screenshot04](https://framagit.org/fsincere/order2/-/raw/master/images/image04.png)

### Autre cas particulier : masse suspendue à un ressort

- M : masse en kg
- K : constante de raideur du ressort (en N/m)
- f : coefficient de frottement (en N.s/m)

Exemple :
```python
>>> import order2
>>> syst = order2.MKF(M=2, K=100, f=13)
>>> print(syst.pulsation_propre)
7.07106781186
>>> print(syst.amortissement)
0.45961940777
>>> syst.courbe_reponse_indicielle()
>>> syst.bode()
>>> syst.show()
```

### Autres fonctionnalités

#### Réponse indicielle

- détermination du type de régime
- temps de réponse
- pseudo-période
- fréquence propre
- dépassements en %

Exemple :  
```python
>>> import order2
>>> syst = order2.Ordre2(A=10, coeff_amortissement=0.5, w0=600)
>>> print(syst.regime())
pseudo-périodique
>>> print(syst.temps_de_reponse(5))  # à 5 %
0.0088151553719
>>> print(syst.temps_de_reponse(1))  # à 1 %
0.0146342745411
>>> print(syst.frequence_propre())
95.49296585
>>> print(syst.depassement(1))  # 1er dépassement en %
16.3033534821
```

#### Réponse harmonique

- fréquence propre
- fréquence de résonance
- facteur de résonance
- fréquence de coupure à -3 dB

Exemple :  
```python
>>> import order2
>>> syst = order2.Ordre2(A=10, coeff_amortissement=0.5, w0=600)
>>> print(syst.frequence_propre())
95.49296585
>>> print(syst.frequence_resonance_harmonique())
67.523723711
>>> print("{} ou {} dB".format(*syst.facteur_resonance_harmonique()))
1.15470053837 ou 1.24938736608 dB
>>> print(syst.frequence_coupure_harmonique())
121.468928958
```

- fonction de transfert complexe (transmittance)

Exemple :  
```python
>>> syst = order2.Ordre2(A=2, coeff_amortissement=0.05, w0=1000)
>>> H = syst.fonction_transfert
>>> # help(H)
>>> H.properties(150)  # transmittance à 150 Hz
Frequency (Hz) : 150
Angular frequency (rad/s) : 942.478
Complex value : 10.4585-8.82161j
Magnitude : 13.6821
Magnitude (dB) : 22.72306
Phase (degrees) : -40.1473
Phase (radians) : -0.700702
>>> print(H.db(150))  # gain en dB à 150 Hz
22.723064994
>>> print(H.phase_deg(150))  # déphasage en degrés à 150 Hz
-40.147271165
```

### Abaques

#### Réponse indicielle

- coefficient d'amortissement en fonction du premier dépassement en %

```python
>>> import order2
>>> print(order2.Ordre2.abaque_coeff_amortissement(depassement=60))
0.160493046664
```

- n-ième dépassement en % en fonction du coefficient d'amortissement

```python
>>> print(order2.Ordre2.abaque_depassement(coeff_amortissement=0.16))
60.0967132139
>>> print(order2.Ordre2.abaque_depassement(coeff_amortissement=0.16, n=2)) 
36.1161493911
```

- temps de réponse en fonction de m et de ω0

```python
>>> print(order2.Ordre2.abaque_temps_de_reponse(coeff_amortissement=0.16, w0=10000,
                                                pourcentage=5))
0.0016837960245
```

- pseudo-période en fonction de m et de ω0

```python
>>> print(order2.Ordre2.abaque_pseudo_periode(coeff_amortissement=0.16, w0=10000))
0.00063651879320
```
- ω0 en fonction de m et de la pseudo-période

```python
>>> print(order2.Ordre2.abaque_pulsation_propre(coeff_amortissement=0.16,
                                                pseudo_periode=0.0006365))
10000.295258
```

#### Réponse harmonique

- coefficient d'amortissement en fonction du facteur de résonance en dB

```python
>>> import order2
>>> print(order2.Ordre2.abaque_coeff_amortissement_harmonique(facteur_resonance_db=20))
0.0500627750598
```

- facteur de résonance (sans unité et en dB) en fonction du coefficient d'amortissement

```python
>>> result = order2.Ordre2.abaque_facteur_resonance_harmonique(coeff_amortissement=0.05)
>>> print("{} ou {} dB".format(*result))
10.0125234864 ou 20.010870956 dB
```

- fréquence de coupure à -3 dB en fonction de m et ω0

```python
>>> print(order2.Ordre2.abaque_frequence_coupure_harmonique(coeff_amortissement=0.16,
                                                            w0=10000))
2427.97905105
```

- fréquence de résonance en fonction de m et ω0

```python
>>> print(order2.Ordre2.abaque_frequence_resonance_harmonique(coeff_amortissement=0.16,
                                                              w0=10000))
1550.27045
```
- ω0 en fonction de m et de la fréquence de résonance

```python
>>> print(order2.Ordre2.abaque_pulsation_propre_resonance_harmonique(
        coeff_amortissement=0.16, frequence_resonance=1550.27))
9999.9970809
```

### Pôles de la fonction de transfert

```
                A                     A.ω0²
H(s) = ---------------------- = ----------------------
         1 + 2ms/ω0 +(s/ω0)²    (s - pole1)(s - pole2)
```

avec : s = jω (opérateur de Laplace)

- calcul des pôles à partir de m et ω0

```python
>>> print(order2.Ordre2.abaque_poles(coeff_amortissement=0.6, w0=1000))
((-600+800j), (-600-800j))
```
- calcul de m et ω0 à partir des pôles

```python
>>> print(order2.Ordre2.abaque_m_w0_depuis_poles(-600+800j, -600-800j))
(0.6, 1000.0)
```

#### Exemples : mise en cascade de deux systèmes du 1er ordre

L'ensemble donne un système du 2ème ordre :

```
            1         1                1
H(s) = ----------.---------- = ---------------------
        1 + s/ω1   1 + s/ω2     1 + 2ms/ω0 +(s/ω0)² 
```

```python
>>> w1, w2 = 1000, 100000
>>> m, w0 = order2.Ordre2.abaque_m_w0_depuis_poles(-w1, -w2)
>>> print(m ,w0)
5.05 10000.0
>>> syst = order2.Ordre2(A=1, coeff_amortissement=m, w0=w0)
>>> syst.bode()
>>> syst.show()
```

Si le coefficient d'amortissement est supérieur à 1, on peut décomposer
un système du 2ème ordre en deux systèmes du 1er ordre :


```python
>>> syst = order2.Ordre2(A=1, coeff_amortissement=2.5, w0=1000) 
>>> pole1, pole2 = syst.poles
>>> w1, w2 = -pole1, -pole2
>>> print(w1, w2)                                                          
208.71215252208003 4791.28784747792
>>> tau1, tau2 = 1/w1, 1/w2                                                
>>> print(tau1, tau2)  # constantes de temps
0.004791287847477919 0.00020871215252208
```

### Aide complète

```python
>>> import order2
>>> help(order2)
```

### Bonus

Vous trouverez [ici](https://framagit.org/fsincere/order2/-/tree/master/abaques) les scripts permettant de tracer les courbes suivantes :

- Abaque : premier dépassement en fonction du coefficient d'amortissement  

![screenshot05](https://framagit.org/fsincere/order2/-/raw/master/abaques/depassement_reponse_indicielle/abaque_depassement.png)

- Abaque : temps de réponse réduit en fonction du coefficient d'amortissement    

![screenshot06](https://framagit.org/fsincere/order2/-/raw/master/abaques/temps_de_reponse_reponse_indicielle/abaque_temps_de_reponse.png)

- Abaque : facteur de résonance en fonction du coefficient d'amortissement  

![screenshot07](https://framagit.org/fsincere/order2/-/raw/master/abaques/facteur_resonance_regime_harmonique/abaque_facteur_resonance.png)

### Documentation complète

[https://framagit.org/fsincere/order2](https://framagit.org/fsincere/order2)


### TO DO

English translation...

### A voir

[https://pypi.org/project/ac-electricity](https://pypi.org/project/ac-electricity)
