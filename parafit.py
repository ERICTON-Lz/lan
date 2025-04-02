#!/usr/bin/env python3


import os
import numpy as np
import scipy.optimize as opt
import define

# Define folders
d_main = os.popen('pwd').readlines()[0].replace('\n', '')
d_code = '%s/../../../00-Code' % d_main
d_fit = '%s/../SLY4' % d_main
d_leastsq = '%s/leastsq' % d_main

print()
print('*********************************************************************')
print('                          Start Fitting                              ')
print('*********************************************************************')

# Define parameters for parafit
init   = 1          # 0: read from para_init.dat; 1: read from para_final.dat
tol    = 1.0e-6     # lm fitting: 
epsfcn = 5.0e-5     # lm fitting: step to calculate derivative
maxfev = 5000       # lm fitting: maximum iteration for lm fitting
print()
print('Parameters for parafit: init = %d, tol = %f, epsfcn = %f, maxfev = %d' % (init, tol, epsfcn, maxfev))

# Set a dictionary for parameters: read initial parameter from para_init.dat or para_final.dat
if init == 0:
    param, ipara = define.read_input('para_init.dat')
else:
    param, ipara = define.read_input('para_final.dat')

# Choose the parameters to be fitted
list_para = []
for i in ipara.keys():
    if ipara[i] == 1:
        list_para.append(i)

print()
print('Parameters to be fitted: ', " ".join(['{}'.format(i) for i in list_para]))

print()
print('The initial parameters:')
define.print_para(param)

# Set information for observables
# name = define.Observable(ele.name, mass number, neutron number, proton number, [exp. data], [theo. data], [error bar], [quantity to be fitted])
#matter = define.Observable(
#    'Matter', 0, 0, 0, [0.160, -16.00, 32.0, 230.0, 60.0, -600, 0.58, 0.7], [0.0, 0.0], [0.0001, 0.1, 0.1, 2.0, 60, 50, 5, 5], ['rvs','EA','J','K','L','Q','Ms','Mnr'])
#matter = define.Observable(
#    'Matter', 0, 0, 0, [0.166, -16.00, 31.7, 240.0, 58.7, -600, 0.58, 0.7], [0.0, 0.0], [0.0001, 0.01, 0.01, 0.2, 0.2, 50, 5, 5], ['rvs','EA','J','K','L'])
matter = define.Observable(
    'Matter', 0, 0, 0, [0.166, -16.00, 31.7, 240.0, 58.7, -600, 0.58, 0.7], [0.0, 0.0], [1000, 1000, 0.01, 1000, 0.05, 50, 5, 5], ['rvs','EA','J','K','L'])
c14   = define.Observable('C ',  14,   8,  6, [ 0.0000, 3.5242625, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
o14   = define.Observable('O ',  14,   6,  8, [ 3.582256,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
o16   = define.Observable('O ',  16,   8,  8, [ -127.6193, 2.6991, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
o16   = define.Observable('O ',  16,   8,  8, [ 0.0000,    0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
o18   = define.Observable('O ',  18,  10,  8, [ 1.9668035, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
o20   = define.Observable('O ',  20,  12,  8, [ 1.7876382, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
o22   = define.Observable('O ',  22,  14,  8, [ 1.592355,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
o24   = define.Observable('O ',  24,  16,  8, [ -168.9600, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
ne18  = define.Observable('Ne',  18,  8,  10, [ 0.0000, 1.8595935, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ne22  = define.Observable('Ne',  22,  12, 10, [2.199817, 2.497001, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
mg20  = define.Observable('Mg',  20,  8,  12, [ 0.0000, 2.0165782, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
mg22  = define.Observable('Mg',  22,  10, 12, [2.572032, 2.118652, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
# Z.Z. used begin
#mg28  = define.Observable('Mg',  28,  16, 12, [1.765500, 2.44575, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapp'])
mg28  = define.Observable('Mg',  28,  16, 12, [ 2.44575, 0.00000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapp'])
#si28  = define.Observable('Si',  28,  14, 14, [ 2.81875, 2.92000, 3.5, 0.0], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp']) 
#si28  = define.Observable('Si',  28,  14, 14, [ 2.81875, 0.00000, 3.5, 0.0], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn'])#for 30Si
si28  = define.Observable('Si',  28,  14, 14, [ 2.92000, 0.00000, 3.5, 0.0], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapp']) #for 30S
si30  = define.Observable('Si',  30,  16, 14, [ 1.50050, 2.22100, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#si32  = define.Observable('Si',  32,  18, 14, [ 1.80525, 2.16675, 3.5, 0.0], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
si32  = define.Observable('Si',  32,  18, 14, [ 1.80525, 0.00000, 3.5, 0.0], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn'])
#s28   = define.Observable('S ',  28,  12, 16, [ 2.40075, 1.80775, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
s28   = define.Observable('S ',  28,  12, 16, [ 2.40075, 0.00000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn'])
s30   = define.Observable('S ',  30,  14, 16, [ 2.12250, 1.59350, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#s32   = define.Observable('S ',  32,  16, 16, [ 2.14775, 2.21125, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#s32   = define.Observable('S ',  32,  16, 16, [ 2.21125, 0.00000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapp']) #for 30Si
s32   = define.Observable('S ',  32,  16, 16, [ 2.14775, 0.00000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn']) #for 30S
#ar32  = define.Observable('Ar',  32,  14, 18, [ 2.27225, 1.87075, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ar32  = define.Observable('Ar',  32,  14, 18, [ 1.87075, 0.00000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0],  [1.0, 1.0, 0.050, 0.050], ['pgapp'])
# Z.Z. used end
#si30  = define.Observable('Si',  30,  16, 14, [ 2.01090,  3.10881, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
si34  = define.Observable('Si',  34,  20, 14, [ -283.4274, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
si34  = define.Observable('Si',  34,  20, 14, [ 0.0000,  3.277795, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#s30   = define.Observable('S ',  30,  14, 16, [ 2.99078,  2.06555, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
s34   = define.Observable('S ',  34,  18, 16, [ 1.817712,1.561948, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
s36   = define.Observable('S ',  36,  20, 16, [ -308.7140, 3.2985, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
s36   = define.Observable('S ',  36,  20, 16, [ 0.0000,   1.52674, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ar34  = define.Observable('Ar',  34,  16, 18, [ 1.621912,1.754014, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ar38  = define.Observable('Ar',  38,  20, 18, [ -327.3426, 3.4028, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
ar38  = define.Observable('Ar',  38,  20, 18, [ 0.0000, 1.4405595, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ca34  = define.Observable('Ca',  34,  14, 20, [ 4.07300,   0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ca36  = define.Observable('Ca',  36,  16, 20, [ -281.3724, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
ca36  = define.Observable('Ca',  36,  16, 20, [ 1.760264,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ca38  = define.Observable('Ca',  38,  18, 20, [ 1.4967895, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#ca40  = define.Observable('Ca',  40,  20, 20, [ -342.0521, 3.4776, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
#ca40  = define.Observable('Ca',  40,  20, 20, [ -342.0521, 3.4776, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
ca40  = define.Observable('Ca',  40,  20, 20, [ 2.500212,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#ca40  = define.Observable('Ca',  40,  20, 20, [ -342.0521, 3.4776, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.05, 0.910, 0.050, 0.050], ['EB'])
ca42  = define.Observable('Ca',  42,  22, 20, [ 1.6764845, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ca44  = define.Observable('Ca',  44,  24, 20, [ 1.7018487, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ca46  = define.Observable('Ca',  46,  26, 20, [ 1.487901,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ca48  = define.Observable('Ca',  48,  28, 20, [ 1.687428,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#ca48  = define.Observable('Ca',  48,  28, 20, [ -416.0009, 3.4771, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
ca50  = define.Observable('Ca',  50,  30, 20, [ -427.5080, 3.5168, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
ca52  = define.Observable('Ca',  52,  32, 20, [ -438.3278, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
ca54  = define.Observable('Ca',  54,  34, 20, [ -445.3650, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
ti42  = define.Observable('Ti',  42,  20, 22, [ 0.0000, 1.5739865, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ti50  = define.Observable('Ti',  50,  28, 22, [ 0.0000,  1.646575, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
cr44  = define.Observable('Cr',  44,  20, 24, [ 0.0000, 1.4600467, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
cr52  = define.Observable('Cr',  52,  28, 24, [ 0.0000,  1.578225, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
fe46  = define.Observable('Fe',  46,  20, 26, [ 0.0000,  1.4485  , 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
fe54  = define.Observable('Fe',  54,  28, 26, [ 0.0000,  1.49672 , 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ni50  = define.Observable('Ni',  50,  22, 28, [ 1.9445  ,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ni52  = define.Observable('Ni',  52,  24, 28, [ 1.395688,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ni54  = define.Observable('Ni',  54,  26, 28, [ 1.501218,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#ni56  = define.Observable('Ni',  56,  28, 28, [ -483.9956, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
ni56  = define.Observable('Ni',  56,  28, 28, [ -483.9956, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.05, 0.910, 0.050, 0.050], ['EB'])
ni58  = define.Observable('Ni',  58,  30, 28, [ 1.348888,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ni60  = define.Observable('Ni',  60,  32, 28, [ 1.489035,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ni62  = define.Observable('Ni',  62,  34, 28, [ 1.6389155, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ni64  = define.Observable('Ni',  64,  36, 28, [ 1.59902525,0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ni72  = define.Observable('Ni',  72,  44, 28, [ -613.4551, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
ni72  = define.Observable('Ni',  72,  44, 28, [ 1.413250,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
zn58  = define.Observable('Zn',  58,  28, 30, [ 0.0000,  1.329136, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
ge60  = define.Observable('Ge',  60,  28, 32, [ 0.0000,   1.62705, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
se84  = define.Observable('Se',  84,  50, 34, [ -727.3386, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
kr72  = define.Observable('Kr',  72,  36, 36, [ 1.937750, 2.04225, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
kr86  = define.Observable('Kr',  86,  50, 36, [ -749.2345, 4.1835, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
sr88  = define.Observable('Sr',  88,  50, 38, [ -768.4684, 4.2240, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
zr90  = define.Observable('Zr',  90,  50, 40, [ -783.8972, 4.2694, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
zr92  = define.Observable('Zr',  92,  52, 40, [ -799.7264, 4.3057, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
zr94  = define.Observable('Zr',  94,  54, 40, [ -814.6793, 4.3320, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
zr96  = define.Observable('Zr',  96,  56, 40, [ -828.9914, 4.3512, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
mo92  = define.Observable('Mo',  92,  50, 42, [ -796.5112, 4.3151, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
ru94  = define.Observable('Ru',  94,  50, 44, [ -806.8640, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
cd98  = define.Observable('Cd',  98,  50, 48, [ -821.0734, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
cd106 = define.Observable('Cd', 106,  58, 48, [ 1.39100,  1.47000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
cd108 = define.Observable('Cd', 108,  60, 48, [ 1.43149,  1.49774, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
cd110 = define.Observable('Cd', 110,  62, 48, [ 1.37399,  1.51149, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
cd112 = define.Observable('Cd', 112,  64, 48, [ 1.31650,  1.52575, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
cd114 = define.Observable('Cd', 114,  66, 48, [ 1.39650,  1.43999, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
cd116 = define.Observable('Cd', 116,  68, 48, [ 1.42100,  1.50850, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
sn100 = define.Observable('Sn', 100,  50, 50, [ -825.3000, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
sn112 = define.Observable('Sn', 112,  62, 50, [ 1.4081785, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
sn114 = define.Observable('Sn', 114,  64, 50, [ 1.261438,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#sn114 = define.Observable('Sn', 114,  64, 50, [ -971.5725, 4.6099, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
sn116 = define.Observable('Sn', 116,  66, 50, [ 1.2053082, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#sn116 = define.Observable('Sn', 116,  66, 50, [ 1.20530825, 4.6250, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 0.910, 0.050, 0.050], ['pgapn'])
sn118 = define.Observable('Sn', 118,  68, 50, [ 1.3362735,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#sn118 = define.Observable('Sn', 118,  68, 50, [ 1.33627350, 4.6393, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 0.910, 0.050, 0.050], ['pgapn'])
sn120 = define.Observable('Sn', 120,  70, 50, [ 1.3918475,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#sn120 = define.Observable('Sn', 120,  70, 50, [ 1.39184750, 4.6519, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 0.910, 0.050, 0.050], ['pgapn'])
sn122 = define.Observable('Sn', 122,  72, 50, [ 1.365791,   0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#sn122 = define.Observable('Sn', 122,  72, 50, [ 1.36579100, 4.6634, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 0.910, 0.050, 0.050], ['pgapn'])
sn124 = define.Observable('Sn', 124,  74, 50, [ 1.3138553,  0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#sn124 = define.Observable('Sn', 124,  74, 50, [ 1.31390250, 4.6735, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 0.910, 0.050, 0.050], ['pgapn'])
sn126 = define.Observable('Sn', 126,  76, 50, [ 1.27736850, 4.6735, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 0.910, 0.050, 0.050], ['pgapn'])
sn128 = define.Observable('Sn', 128,  78, 50, [ 1.25910075, 4.6921, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 0.910, 0.050, 0.050], ['pgapn'])
sn130 = define.Observable('Sn', 130,  80, 50, [ 1.15998750, 4.6921, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 0.910, 0.050, 0.050], ['pgapn'])
sn132 = define.Observable('Sn', 132,  82, 50, [-1102.8431, 4.7093, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
te122 = define.Observable('Te', 122,  70, 52, [ 1.41800,  1.29600, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
te124 = define.Observable('Te', 124,  72, 52, [ 1.34825,  1.24000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
te126 = define.Observable('Te', 126,  74, 52, [ 1.30700,  1.19749, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
te128 = define.Observable('Te', 128,  76, 52, [ 1.23175,  1.15250, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
te130 = define.Observable('Te', 130,  78, 52, [ 1.16950,  1.02450, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
te134 = define.Observable('Te', 134,  82, 52, [-1123.4082, 4.7569, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
xe136 = define.Observable('Xe', 136,  82, 54, [-1141.8816, 4.7964, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
ba138 = define.Observable('Ba', 138,  82, 56, [-1158.2920, 4.8378, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
ce140 = define.Observable('Ce', 140,  82, 58, [-1172.6844, 4.8771, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
nd142 = define.Observable('Nd', 142,  82, 60, [-1185.1363, 4.9123, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
sm144 = define.Observable('Sm', 144,  82, 62, [-1195.7298, 4.9524, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
gd146 = define.Observable('Gd', 146,  82, 64, [-1204.4279, 4.9801, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc','split1','split2'])
gd148 = define.Observable('Gd', 148,  84, 64, [-1220.7540, 5.0080, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
dy148 = define.Observable('Dy', 148,  82, 66, [-1210.7791, 5.0455, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
dy152 = define.Observable('Dy', 152,  86, 66, [-1245.3238, 5.0950, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
er150 = define.Observable('Er', 150,  82, 68, [-1215.3300, 5.0548, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
hg204 = define.Observable('Hg', 204, 124, 80, [-1608.6512, 5.4744, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
hg206 = define.Observable('Hg', 206, 126, 80, [-1621.0490, 5.4837, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
pb182 = define.Observable('Pb', 182, 100, 82, [-1411.6521, 5.3788, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
pb194 = define.Observable('Pb', 194, 112, 82, [-1525.8915, 5.4372, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
pb200 = define.Observable('Pb', 200, 118, 82, [-1576.3620, 5.4611, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
pb204 = define.Observable('Pb', 204, 122, 82, [ 0.7694275, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#pb204 = define.Observable('Pb', 204, 122, 82, [-1607.5061, 5.4803, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
pb206 = define.Observable('Pb', 206, 124, 82, [ 0.5854145, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#pb206 = define.Observable('Pb', 206, 124, 82, [-1622.3246, 5.4902, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
#pb208 = define.Observable('Pb', 208, 126, 82, [-1636.4302, 5.5012, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
pb208 = define.Observable('Pb', 208, 126, 82, [ 1.09247375,0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn', 'pgapp'])
#pb208 = define.Observable('Pb', 208, 126, 82, [-1636.4302, 5.5012, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.01, 0.910, 0.050, 0.050], ['EB'])
pb210 = define.Observable('Pb', 210, 128, 82, [-1645.5527, 5.5208, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
pb214 = define.Observable('Pb', 214, 132, 82, [-1663.2923, 5.5577, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
po210 = define.Observable('Po', 210, 126, 84, [-1645.2127, 5.5704, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
rn212 = define.Observable('Rn', 212, 126, 86, [-1652.4970, 5.5915, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
ra214 = define.Observable('Ra', 214, 126, 88, [-1658.3226, 5.6079, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB','rc'])
th216 = define.Observable('Th', 216, 126, 90, [-1662.6946, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
u218  = define.Observable('U ', 218, 126, 92, [-1665.6770, 0.0000, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [0.20, 0.910, 0.050, 0.050], ['EB'])
cf248 = define.Observable('Cf', 248, 150, 98, [0.57734325, 0.86995375, 3.5, 0.5], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.050, 0.050], ['pgapn','pgapp'])
# Choose the observables used for fitting
#list_obs = [matter, o16, o24, s36, ca40, ca48, ca52, ca54, ni56, ni68, ni72, kr86, zr90, ru94, sn100, sn116, sn124, sn132,
#            xe136, ce140, gd146, pb182, pb194, pb200, pb204, pb208, pb214, po210, ra214, u218]
#list_obs = [sn116, sn118, sn120, sn122, sn124, sn126, sn128, sn130]
#list_obs=[ni72]
#list_obs = [si28,si30,si32,mg28,s32]
#list_obs=[s28,s30,s32,si28,ar32]
#list_obs=[te122,te124,te126,te128,te130]
#list_obs=[cd106,cd108,cd110,cd112,cd114,cd116]
list_obs=[ca50]
# list_obs = [matter]
print()
print('Chosen observables:')
for i in list_obs:
    print(i.ele, i.A, i.key, i.exp, i.err)

# Create folder to run leastsq
os.system('mkdir -p %s' % d_leastsq)
os.chdir(d_leastsq)
os.system('rm -rf *')

# Define filename for inout
filename = 'cal'
with open('inm-%s' % filename,'w') as f:
    f.write('%s\n' % filename)

# Copy the executable file of SHFB 
#os.system('cd %s/ || make' % d_code)
#os.system('cd %s/' % d_fit)
os.system('cp -r %s/run %s/' % (d_code, d_leastsq))

x0 = []
for i in list_para:
    x0.append(param[i])
print()
print('Initial input for leastsq')
print('Para0:'," ".join(['{0:12.6f}'.format(p) for p in x0]))

chi_square = 0.0
Delta_be   = 0
Delta_rch  = 0

# Define function to calculate chi^2
def func(x):
    print()
    print('Parameters: ', " ".join(['{0:12.6f}'.format(p) for p in x]))
    chi = []
    lpr = False

    global param, list_para, list_obs, ipara, chi_square, Delta_be, Delta_rch, filename
    for i in range(len(list_para)):
        param[list_para[i]] = x[i]

    # Modify the parameter input files
    define.write_para(param, 'paralist.in')

    count_be  = 0
    count_rch = 0
    Delta_be  = 0
    Delta_rch = 0
    # Calculate the observables with hfb code
    for i in list_obs:
        if i.ele != 'Matter':
            if lpr:
                chi.append(1000.0/i.err[0])
                if(len(i.key) == 2):
                    chi.append(10.0/i.err[1])
            else:
                i.rhf_cal(filename)
                print('Nuclei  %2s%3d:' % (i.ele,i.A), "    ".join(['{0:12.4f} ({1:12.4f})'.format(i.theo[k], i.exp[k]) for k in range(len(i.key))]))
                if(i.theo[0] == -526.00):
                    # lpr = True
                    chi.append(1000.0/i.err[0])
                    if(len(i.key) == 2):
                        chi.append(10.0/i.err[1])
                else:
                    for j in range(len(i.key)):
                        chi.append((i.exp[j] - i.theo[j]) / i.err[j])
                        if(i.key[j]=='EB'):
                            count_be  = count_be  + 1
                            Delta_be  = Delta_be  + (i.exp[j] - i.theo[j])**2
                        elif(i.key[j]=='rc'):
                            count_rch = count_rch + 1
                            Delta_rch = Delta_rch + (i.exp[j] - i.theo[j])**2
        else:
            i.rhf_cal(filename)
            param['rvs'] = i.theo[0]
            define.write_para(param, 'parameter-%s.in' % filename)
            print('Nuclear Matter:', " ".join(['{0:12.4f}'.format(theo) for theo in i.theo]))
            if i.theo[0] == 0.3:
                lpr = True
                for j in range(len(i.key)):
                    chi.append(1000.0/i.err[j])
            else:
                for j in range(len(i.key)):
                    chi.append((i.exp[j] - i.theo[j]) / i.err[j])
    
    chi_square = 0.0
    for i in chi:
        chi_square = chi_square + i**2
    print('chi_square = %f' % chi_square)

    if(count_be  != 0):
        Delta_be  = (Delta_be /count_be )**0.5
    if(count_rch != 0):
        Delta_rch = (Delta_rch/count_rch)**0.5
    print('Delta_BE   = %f' % Delta_be)
    print('Delta_Rch  = %f' % Delta_rch)

    return chi

# Non-linear fitting method
# method = trf, lm, dogbox
bound = (-np.inf, np.inf)
# bound = ([1,0,1,0,0,0,0,0], [1.5,4,1.5,4,2,2,2,2])
res = opt.least_squares(func, x0, jac='2-point', bounds=bound, method='lm',
                        ftol=tol, xtol=tol, gtol=tol, x_scale='jac',
                        loss='linear', diff_step=epsfcn, max_nfev=maxfev)
print()
print(res.message)
x0 = res.x

for i in range(len(list_para)):
    param[list_para[i]] = x0[i]
print()
print('The final parameters:')
define.print_para(param)
define.write_output(param, ipara, '%s/%s' % (d_main, 'para_final.dat'))
chi2 = func(x0)
with open('%s/obserable.dat' % d_main, 'w') as f:
    f.write('Nuclear Matter:'+" ".join(['{0:12.4f}'.format(theo) for theo in matter.theo])+'\n')
    for i in list_obs[1:]:
        f.write('Nuclei  %2s%3d:' % (i.ele,i.A)+"    ".join(['{0:12.4f} ({1:12.4f})'.format(i.theo[k], i.exp[k]) for k in range(len(i.key))])+'\n')
    f.write('Chi_Square = {} \n'.format(chi_square))
    f.write('Delta_be   = {} \n'.format(Delta_be))
    f.write('Delta_rch  = {}   '.format(Delta_rch))

print()
print('*********************************************************************')
print('                           The END                                   ')
print('*********************************************************************')
print()

exit()
