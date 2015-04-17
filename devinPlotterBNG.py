# -*- coding: utf-8 -*-
"""
Created on Thurs Dec 4 2014

@author: Devin P Sullivan
"""
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as pyplot
import os
import numpy
import fnmatch
import re
from collections import defaultdict

def get_immediate_subdirectories(a_dir,substr):
    namelist = []
    for name in os.listdir(a_dir):
        #print(name)
        if substr not in name: continue
        fullpath = os.path.join(a_dir,name)
        #print(fullpath)
        if os.path.isdir(fullpath):
            namelist.append(fullpath)
        else:
            print("could not find directory")
    #return [name for name in os.listdir(a_dir)
    #if os.path.isdir(os.path.join(a_dir, name))]
    return namelist


def getMCellResults(directory):
    matches = []
    mynames = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.dat'):
            matches.append(os.path.join(root, filename))
            mynames.append(filename)
    return matches,mynames

def getResultsFiles(directory,substr):
    matches = []
    mynames = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, substr+'*.gdat'):
            #print(filename)
            matches.append(os.path.join(root, filename))
            mynames.append(filename)
    return matches,mynames

def getObservables(reactdir):
    seeds = get_immediate_subdirectories(reactdir)
    allseeds = [reactdir+x for x in seeds]
    datapath,filenames = getResultsFiles(allseeds[0])
    return filenames

def parse_gdat(filename):
    print('reading file')
    print(filename)
    #create a dictionary of obserables
    observableDict = defaultdict(list)
    data = []
    sind = 0
    #loop through all the seeds performed
    arraysize = []
    datatmp = pylab.loadtxt(filename)
    arraysize.append(numpy.size(datatmp,axis=0))
    observableDict[filename].append(datatmp)
    print(observableDict[filename])
    with open(filename, 'r') as f:
        observableNames = f.readline()
    observableNames = observableNames.split()
    #print(numpy.size(observableDict[f],axis=0))
    #print(numpy.size(observableDict[f],axis=1))
    #print(numpy.size(observableDict[f],axis=2))
    #now average the data for each seed
    #convert to a numpy array
    #print(data)
    #get the minimum size for data

    return observableDict,observableNames

if __name__ == "__main__":
    #BNGrootpath ='/Users/admin/Dropbox/HighThroughputModeling/BNGLFilesforSim/'
    #BNGrootpath ='/Users/admin/MurphyLab/HTM/xmlfiles_t400/'
    BNGrootpath ='/Users/admin/MurphyLab/HTM/BNGmanualmatch/'
    MCellrootpath = '/Users/admin/MurphyLab/HTM/resultCount_every1000/seed3/'
    #rootpath = '/helix/home/usr/ue/6/dpsulliv/NewRuns/MoreCells/FilesToExport/'
    #rootpath = '/helix/home/usr/ue/6/dpsulliv/NewRuns/MoreCells/BNGResults/'
    substr = "meanEN0_5std_cell_10seed3"
    #First lets get the different run directories
    MCellrunDirs = get_immediate_subdirectories(MCellrootpath,substr)
    print(MCellrunDirs)
    #print('oh hey')
    savedir = './resultPlotsBNG_mcell_manualmatchWTF/'
    try:
        os.stat(savedir)
    except:
        os.mkdir(savedir)
    
    #MCellfullDirs = [x+'/mcell/react_data/' for x in MCellrunDirs]
    #print(MCellfullDirs)
    
    observableDict = defaultdict(list)
    geomDict = defaultdict(list)
    dataDict = defaultdict(list)
  
    
    #loop through runs
    seed_dirs = []
    #cmap=['r', 'g', 'b', 'y']
    ind = 0
    min_len = []
    #thefile = open(savedir+"directorylist.txt",'w')
    #for rundir in runDirs:
    #    thefile.write("%s\n" %rundir)
        
        #observableDict,min_lentmp,filenames = getMeanStd(reactdir)
    print(BNGrootpath)
    BNGfilenames = getResultsFiles(BNGrootpath,"*"+substr)
    BNGfilenames = BNGfilenames[0]
    NUM_COLORS = 2#len(BNGfilenames)
    print(NUM_COLORS)
    cm = pylab.get_cmap('gist_rainbow')
    cmap = []
    for i in range(NUM_COLORS):
        cmap.append(cm(1.*i/NUM_COLORS)) # color will now be an RGBA tuple
    #min_len.append(min_lentmp)
    #geomDict[rundir].append(observableDict)
    #sampleDict = geomDict[rundir]
    #ind += 1

    print(MCellrunDirs)
    MCellfilenames = getMCellResults(MCellrunDirs[0])
    MCellfilenames = MCellfilenames[0]

    #need to isolate observable name for MCell so we can match it with BNGL
    Mnames = []
    print(MCellfilenames)
    for Mfile in MCellfilenames:
        filesplits = Mfile.split("/")
        namesplit = filesplits[-1].split(".")
        Mnames.append(namesplit[0])
    #print(Mnames)


    #cut to minsize
    mean_data = {}
    std_data = {}
    mu_plus_std = {}
    mu_minus_std = {}
    #print('printing GD')
    #print(geomDict)
    #print(sampleDict)

    #print(observableDict)
    #for datakey in observableDict:
    BNGcurrcolor = [float(x) for x in cmap[0]]
    MCellcurrcolor = [float(x) for x in cmap[1]]

    for datakey in BNGfilenames:
        print('printing datakey')
        #print(datakey)
        print(datakey)
        #observableDict,min_len = getMeanStd(reactdir,datakey)
        observableDict,observableNames = parse_gdat(datakey)
        print(observableNames)
        data = observableDict[datakey]#currDict[datakey]
        #data2 = [x[0:min_len] for x in data]
        #data2 = [numpy.compress(numpy.ones(min_len),x,axis=0) for x in data]
        #data2 = [[y[0:min_len] for y in x] for x in data]
        dataarray = numpy.array(data)
        dataarray = dataarray[0]
        #print('printing dataarray')
        #print(dataarray)
        #print(numpy.size(dataarray,axis=0))
        #print(numpy.size(dataarray,axis=1))
        #            print(numpy.size(dataarray,axis=2))
        print('getting time')
        time = dataarray[:,0]
        print(time)
        observableNames = observableNames[2:]#remove "#" and "time" observables
        print(len(observableNames))
        dataarray = dataarray[:,1:] #remove time column
        print(type(dataarray))
        print(numpy.size(dataarray,axis=1))
        print(len(MCellfilenames)) #These should all be the same (34)

        for observable,observableName in zip(dataarray.transpose(),observableNames):
            print('printing observable')
            print(observableName)
            pylab.rcParams['figure.figsize'] =  27, 18
            pyplot.plot(time,observable,c=BNGcurrcolor)


            #Check to find matching substring of mcell names
            miter = 0
            print("checking mcell")
            for Mname,Mfilename in zip(Mnames,MCellfilenames):
                print(Mname)
                if Mname != observableName:
                    continue
                #When we do find the file with a matching name, look it up and load it
                datatmp = pylab.loadtxt(Mfilename)
                datatmp = numpy.array(datatmp)
                print(datatmp)
                meandata = numpy.mean(datatmp,axis=1)
                print("mean of data")
                print(meandata)
                std_data = numpy.std(datatmp,axis=1)
                print("std of data")
                print(std_data)
                      
                      
                #plot the mcell stuff
                pyplot.plot(time,meandata,c=MCellcurrcolor)
                mu_plus_std = meandata+std_data
                pyplot.plot(time,mu_plus_std,'--',c=MCellcurrcolor)
                mu_plus_std = None
                mu_minus_std = meandata-std_data
                pyplot.plot(time,mu_minus_std,'--',c=MCellcurrcolor)
                mu_minus_std = None

            #pylab.rcParams['figure.figsize'] =  27, 18
            #currcolor = [float(x) for x in cmap[ind]]
            #pyplot.plot(time,observable,c=currcolor)
            #pyplot.show()
            pylab.suptitle(observableName+" count plot",fontsize=24)
            #pylab.xlabel("Time (s)",fontsize=24)
            pylab.xlabel("Time (s)",fontsize=32,fontweight='bold')
            pylab.ylabel("Molecule count",fontsize=32,fontweight='bold')
            pyplot.tick_params(axis='both',labelsize=32)
            savename = datakey.split('/')
            savename = savename[-1]
            savename = savename + "_" + observableName
            #print(savename)
            savestring = savedir+substr+observableName#savename[0:len(datakey)-4]+".png"
            pylab.savefig(savestring, dpi=72) # dots per inch
            pyplot.clf()
            print(breakme)

        
        
        #mean_data[datakey] = numpy.mean(dataarray,axis=0)
        #std_data[datakey] = numpy.std(dataarray,axis=0)
        #mu_plus_std[datakey] = mean_data[datakey]+std_data[datakey]
        #mu_minus_std[datakey] = mean_data[datakey]-std_data[datakey]
        # figure size in inches
        #pylab.rcParams['figure.figsize'] =  27, 18
        #plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
        #here we keep the mean_data[:,0] for all the time components, though it shouldn't matter.
        #pyplot.plot(mean_data[datakey][:,0],mu_plus_std[datakey][:,1],mean_data[datakey][:,0],mean_data[datakey][:,1],color=ind,mean_data[datakey][:,0],mu_minus_std[datakey][:,1],color=ind)
        #print(ind)
        #currcolor = [float(x) for x in cmap[ind]]
        #print('current color')
        #print(currcolor)
        #pyplot.plot(mean_data[datakey][:,0],mu_plus_std[datakey][:,1],'--',c=currcolor)
        #meanplots.append(pyplot.plot(mean_data[datakey][:,0],mean_data[datakey][:,1],c=currcolor))
        #pyplot.plot(mean_data[datakey][:,0],mu_minus_std[datakey][:,1],'--',c=currcolor)
        #pyplot.show()
        #print(cellname)
        #ind += 1
        #Plot and save the figure for the given observable (datakey)
        #savestring = savedir+datakey[0:len(datakey)-4]+".png"
        #0:len(datakey)-4 removes the '.dat'
        #pylab.suptitle(datakey[0:len(datakey)-4]+" count plot",fontsize=24)
        #pylab.xlabel("Time (s)",fontsize=24)
        #pylab.ylabel("Molecule count",fontsize=24)
        #pyplot.tick_params(axis='both',labelsize=24)
        #pylab.savefig(savestring, dpi=72) # dots per inch
        pyplot.clf()

    #filename = '/Users/admin/MurphyLab/HTM/FilesToExport/mean_cell5_seed5_files/mcell/react_data/seed_00001/Phos_TF.World.dat'





'''
    data = (pylab.loadtxt(filename))

X = data[:,0]#pylab.np.random.normal(0,1,500)
Y = data[:,1]#pylab.np.random.normal(0,1,500)
pyplot.scatter(X,Y)
pyplot.title("Scatter Plot Example")
pyplot.xlabel("X-Axis")
pyplot.ylabel("Y-Axis")
# figure size in inches
pylab.rcParams['figure.figsize'] =  9, 6
pylab.plot(X,Y)
pylab.savefig("graph.png", dpi=72) # dots per inch

#datalist = [ ( pylab.loadtxt(filename), label ) for filename, label in list_of_files ]

#for data, label in datalist:
#pylab.plot( data[:,0], data[:,1], 'k' )

#pylab.legend()
#pylab.title("Title of Plot")
#pylab.xlabel("X Axis Label")
#pylab.ylabel("Y Axis Label")'''


