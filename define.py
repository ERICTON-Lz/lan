#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'a module for parafit'

__author__ = 'ZZLi, based on RHF code of Q.Zhao'
import os
import numpy as np

# Define a new class for obserbables


class Observable(object):

    def __init__(self, ele, A, N, Z, exp, theo, err, key):
        self.ele = ele
        self.A = A
        self.N = N
        self.Z = Z
        self.exp = exp
        self.theo = theo
        self.err = err
        self.key = key

    # Define function to calculate saturation property of symmetry nuclear matter
    def rhf_cal(self, filename):
        obs = {}
        if self.ele != 'Matter':
            # Modify hfb.in to write in the nucleus information
            os.system('rm hfb.in')
            with open('hfb.in', 'w') as f:
                f.write('&input\n')
                f.write('force = "SLY4",              mesh_points = 200,\n')
                f.write('integ_step = 0.1,         it_max = 1000,\n')
                f.write('eps_energy = 1.e-9,       max_delta = 1.e-7,\n')
                f.write('boundary_condition = 0,   xmu = 0.93333,\n')
                f.write('bogolyubov = T, T,        pairing_force = 2,\n')
                f.write('E_cutoff = 90.0,          regularization = F,\n')
                f.write('if_nm = .false.,           zda = 0.5, \n')
                f.write('if_reset_force = .true. /    \n')
                f.write('\n')
                f.write('&nucleus  neutron = %d, proton = %d, j_max = 21, 21 /' % (
                    self.N, self.Z))
            # Run the code to calculate finite nuclei properties
            os.system('./run')
            data = np.loadtxt('nucleus-%s.out' % filename)
            os.system('rm -rf nucleus-%s.out' % filename)
            obs['EB'] = data[0]
            obs['rc'] = data[1]
            obs['pgapn'] = data[2]
            obs['pgapp'] = data[3] 
            #obs['split1'] = data[2]
            #obs['split2'] = data[3]
            self.theo = [obs[i] for i in self.key]
        else:
            # Modify the input file for nuclear matter
            os.system('rm hfb.in')
            with open('hfb.in', 'w') as f:
                f.write('&input\n')
                f.write('force = "LNS",              mesh_points = 200,\n')
                f.write('integ_step = 0.1,         it_max = 300,\n')
                f.write('eps_energy = 1.e-9,       max_delta = 1.e-7,\n')
                f.write('boundary_condition = 0,   xmu = 0.65,\n')
                f.write('bogolyubov = T, T,        pairing_force = 2,\n')
                f.write('E_cutoff = 90.0,          regularization = F,\n')
                f.write('if_nm = .ture.,           zda = 0.5, \n')
                f.write('if_reset_force = .true. /    \n')
            # Run the program to calculate the saturation property
            os.system('./run')
            data = np.loadtxt('matter-%s.out' % filename, skiprows=0)
            os.system('rm -rf matter-%s.out' % filename)
            obs['rvs'] = data[0]
            obs['EA']  = data[1]
            obs['J']   = data[2]
            obs['K']   = data[3]
            obs['L']   = data[4]
            #print(data)
            
            #obs['Q']   = data[6]
            #obs['Ms']  = data[7]
            #obs['Mr']  = data[8]
            #obs['Mnr'] = data[9]
            #obs['P']   = data[11]
            self.theo = [obs[i] for i in self.key]




def read_input(filename):
    para = {}
    ipar = {}
    with open(filename, 'r') as f:
        para['name'] = f.readline().replace('\n','').replace('\r','').replace(' ','')
        para['icom'], para['j2terms'], para['ixtls'], para['ixttensor'], para['isp'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        para['dmshb01'], para['dmshb02'] = np.fromstring(
            f.readline(), dtype=np.dtype('float64'), sep=' ')
        ipar['tten'], ipar['uten'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        ipar['t0'], ipar['x0'], ipar['w'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        ipar['t3'], ipar['x3'], ipar['gamma'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        ipar['t4'], ipar['x4'], ipar['gamma2'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        ipar['t1'], ipar['x1'], ipar['t2'], ipar['x2'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        ipar['t0p1'], ipar['t0p2'], ipar['x0p'], ipar['wp'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        ipar['t3p1'], ipar['t3p2'], ipar['x3p'], ipar['gammap'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        ipar['vsp1'], ipar['vsp2'], ipar['rhoc'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        ipar['t3ps1'], ipar['t3ps2'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        ipar['t1p'], ipar['x1p'], ipar['t2p'], ipar['x2p'] = np.fromstring(
            f.readline(), dtype=int, sep=' ')
        para['tten'], para['uten'] =  np.fromstring(
            f.readline(), dtype=float, sep=' ')
        para['t0'], para['x0'], para['w'] = np.fromstring(
            f.readline(), dtype=float, sep=' ')
        para['t3'], para['x3'], para['gamma'] =  np.fromstring(
            f.readline(), dtype=float, sep=' ')
        para['t4'], para['x4'], para['gamma2'] =  np.fromstring(
            f.readline(), dtype=float, sep=' ')
        para['t1'], para['x1'], para['t2'], para['x2'] =  np.fromstring(
            f.readline(), dtype=float, sep=' ')
        para['t0p1'], para['t0p2'], para['x0p'], para['wp'] = np.fromstring(
            f.readline(), dtype=float, sep=' ')
        para['t3p1'], para['t3p2'], para['x3p'], para['gammap'] = np.fromstring(
            f.readline(), dtype=float, sep=' ')
        para['vsp1'], para['vsp2'], para['rhoc'] =  np.fromstring(
            f.readline(), dtype=float, sep=' ')
        para['t3ps1'], para['t3ps2'] =  np.fromstring(
            f.readline(), dtype=float, sep=' ')
        para['t1p'], para['x1p'], para['t2p'], para['x2p'] = np.fromstring(
            f.readline(), dtype=float, sep=' ')
    return para, ipar

def write_output(para, ipar, filename):
    with open(filename, 'w') as f:
        f.write('%s\n' % para['name'])
        f.write('%d %d %d %d %d\n' % (para['icom'], para['j2terms'], para['ixtls'],
            para['ixttensor'], para['isp']))
        f.write('%.15f %.15f\n' % (para['dmshb01'], para['dmshb02']))
        f.write('%d %d\n' % (ipar['tten'], ipar['uten']))
        f.write('%d %d %d\n' % (ipar['t0'], ipar['x0'], ipar['w']))
        f.write('%d %d %d\n' % (ipar['t3'], ipar['x3'], ipar['gamma']))
        f.write('%d %d %d\n' % (ipar['t4'], ipar['x4'], ipar['gamma2']))
        f.write('%d %d %d %d\n' % (ipar['t1'], ipar['x1'], ipar['t2'], ipar['x2']))
        f.write('%d %d %d %d\n' % (ipar['t0p1'], ipar['t0p2'], ipar['x0p'], ipar['wp']))
        f.write('%d %d %d %d\n' % (ipar['t3p1'], ipar['t3p2'], ipar['x3p'], ipar['gammap']))
        f.write('%d %d %d\n' % (ipar['vsp1'], ipar['vsp2'], ipar['rhoc']))
        f.write('%d %d\n' % (ipar['t3ps1'], ipar['t3ps2']))
        f.write('%d %d %d %d\n' % (ipar['t1p'], ipar['x1p'], ipar['t2p'], ipar['x2p']))
        f.write('%f %f\n' % (para['tten'], para['uten']))
        f.write('%f %f %f\n' % (para['t0'], para['x0'], para['w']))
        f.write('%f %f %f\n' % (para['t3'], para['x3'], para['gamma']))
        f.write('%f %f %f\n' % (para['t4'], para['x4'], para['gamma2']))
        f.write('%f %f %f %f\n' % (para['t1'], para['x1'], para['t2'], para['x2']))
        f.write('%f %f %f %f\n' % (para['t0p1'], para['t0p2'], para['x0p'], para['wp']))
        f.write('%f %f %f %f\n' % (para['t3p1'], para['t3p2'], para['x3p'], para['gammap']))
        f.write('%f %f %f\n' % (para['vsp1'], para['vsp2'], para['rhoc']))
        f.write('%f %f\n' % (para['t3ps1'], para['t3ps2']))
        f.write('%f %f %f %f\n' % (para['t1p'], para['x1p'], para['t2p'], para['x2p']))  



def write_para(para, filename):
    with open(filename, 'w') as f:
        f.write('&paralist')
        f.write('\n\n')
        f.write('t0p(1)=%f, t0p(2)=%f /' % (para['t0p1'], para['t0p2']))
        f.write('\n\n')
        f.write('force = %s,' % para['name'])
        f.write('\n\n')
        f.write('icom=%d,  j2terms=%d,  ixtls=%d,  ixttensor=%d,  isp=%d,\n' % ( 
            para['icom'], para['j2terms'], para['ixtls'], para['ixttensor'], para['isp']))
        f.write('dmshb0(1)=%.15f, dmshb0(2)=%.15f,\n' % (para['dmshb01'], para['dmshb02']))
        f.write('tten=%f,  uten=%f,\n' % (para['tten'], para['uten']))
        f.write('\n')
        f.write('t0=%f, x0=%f, w=%f,\n' % (para['t0'], para['x0'], para['w']))
        f.write('t3=%f, x3=%f, gamma=%f,\n' % (para['t3'], para['x3'], para['gamma']))
        f.write('t4=%f, x4=%f, gamma2=%f,\n' % (para['t4'], para['x4'], para['gamma2']))
        f.write('t1=%f, x1=%f, t2=%f, x2=%f,\n' % (para['t1'], para['x1'], para['t2'], para['x2']))
        f.write('\n')
        f.write('t0p(1)=%f, t0p(2)=%f, x0p=%f, wp=%f,\n' % (para['t0p1'], para['t0p2'],
            para['x0p'], para['wp']))
        f.write('t3p(1)=%f, t3p(2)=%f, x3p=%f, gammap=%f,\n' % (para['t3p1'], para['t3p2'],
            para['x3p'], para['gammap']))
        f.write('vsp(1)=%f, vsp(2)=%f, rhoc=%f,\n' % (para['vsp1'], para['vsp2'], para['rhoc']))
        f.write('t3ps(1)=%f, t3ps(2)=%f,\n' % (para['t3ps1'], para['t3ps2']))
        f.write('t1p=%f, x1p=%f, t2p=%f, x2p=%f /' % (para['t1p'], para['x1p'], 
            para['t2p'], para['x2p']))

def print_para(para):
    print('Parameter   : %s' % para['name'])
    print('default sets:')
    print('com,j2,ls   : %d %d %d' % (para['icom'], para['j2terms'], para['ixtls']))
    print('tensor,isp  : %d %d' % (para['ixttensor'], para['isp']))
    print('2m/hbar2    : %.15f %.15f' % (para['dmshb01'], para['dmshb02']))
    print('Mean Field  :')
    print('t0,x0,w0    : %f %f %f' % (para['t0'], para['x0'], para['w']))
    print('t3,x3,alp   : %f %f %f' % (para['t3'], para['x3'], para['gamma']))
    print('t4,x4,alp2  : %f %f %f' % (para['t4'], para['x4'], para['gamma2']))
    print('t1,x1,t2,x2 : %f %f %f %f' % (para['t1'], para['x1'], para['t2'], para['x2']))
    print('Tensor T, U : %f %f' % (para['tten'], para['uten']))
    print('PairingField:')
    print('t0p,x0p,w0p : %f %f %f %f' % (para['t0p1'], para['t0p2'], para['x0p'], para['wp']))
    print('t3p,x3p,alpp: %f %f %f %f' % (para['t3p1'], para['t3p2'], para['x3p'], para['gammap']))
    print('vsp,rhoc    : %f %f %f' % (para['vsp1'], para['vsp2'], para['rhoc']))
    print('t3ps        : %f %f' % (para['t3ps1'], para['t3ps2']))
    print('t1x1p,t2x2p : %f %f %f %f' % (para['t1p'], para['x1p'], para['t2p'], para['x2p']))


