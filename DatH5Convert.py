#!/usr/bin/env python

from scipy import *
from tables import *
from pickle import load
from os import listdir

class PureCompound(IsDescription):
    name = StringCol(25)
    Method = Int32Col()
    Pc = Float64Col()
    Tc = Float64Col()
    Tmax = Float64Col()
    Tmin = Float64Col()
    VPa =  Float64Col()
    VPb =  Float64Col()
    VPc =  Float64Col()
    VPd =  Float64Col()

class UNIQUACParams(IsDescription):
    r1 =  Float64Col()
    r2 =  Float64Col()
    q1 =  Float64Col()
    q2 =  Float64Col()

MixtureDataDir = 'Data/Mixtures'
PureDataDir = 'Data/PureComps'
   
for PureComp in listdir(PureDataDir):
    Data = load(file(PureDataDir+'/'+PureComp))
    h5file = openFile(PureDataDir +'/'+ PureComp[0:-4] +".h5", "w", "Pure Compound Data")
    table = h5file.createTable("/", 'Properties', PureCompound, "Input Data")
    table.row['name'] = PureComp[0:-4]
    for field in Data.keys():
        table.row[field] = Data[field]
    table.row.append()
    table.flush()
    h5file.close()

for Mixture in listdir(MixtureDataDir):
    M = load(file(MixtureDataDir+'/'+ Mixture))
    h5file = openFile(MixtureDataDir + '/'+ Mixture[0:-4] +".h5", "w", "Mixture Data")
    h5file.createArray("/", 'Compounds', M['Compounds'], "Mixture Constituents")  
    ExpDataGroup = h5file.createGroup("/", "ExperimentalData", "Temperature and Compositions")
    h5file.createArray(ExpDataGroup, 'T', M['T'], "Experimental Temperature Points")
    h5file.createArray(ExpDataGroup, 'ExpComp', M['ExpComp'], "Experimental LLE Compositions")
    table = h5file.createTable("/", "UNIQUACParams", UNIQUACParams, "Does this need an explanation?")
    for field in table.colnames:
        table.row[field] = M[field]
    table.row.append()
    table.flush()
    h5file.close()


