#import 

import os
import fnmatch
from subprocess import call 
import libsbml

def getParamFiles(directory):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*manmatch.bngl'):
            matches.append(os.path.join(root, filename))
        return matches

#bngDistro = '/home/proto/workspace/bionetgen/bng2/BNG2.pl'
#bngDistro = './BNG2.pl'
#bngDistro = '/Users/admin/Documents/RuleBender-2.0.382-osx64/BioNetGen-2.2.5/BNG2.pl'
bngDistro = '/Users/admin/bionetgen/bng2/BNG2.pl'

#this is a function
#for setting the DNA initial release number
#to molecule count
def modifyReleaseNumber(fileName):
        print('modifying {0}'.format(fileName))
        reader = libsbml.SBMLReader()
        document = reader.readSBMLFromFile(fileName)
        model = document.getModel()

        species = model.getSpecies('S4')
        species.setInitialAmount(species.getInitialConcentration())
        species.unsetInitialConcentration()

        writer = libsbml.SBMLWriter()
        writer.writeSBMLToFile(document,fileName)

if __name__ == "__main__":
    #read the filenames in folder paramfiles
    #parameterFiles =  getParamFiles('BlenderSpatialParams')
    parameterFiles = getParamFiles('paramfiles_adjECVol')
    #creates one sbml for every parameter file
    for paramFile in parameterFiles:
        print(paramFile)
        #read parameters action
        with open('SpatialParamsIntermediate.bngl','w') as f:
            f.write('readFile({{file=>"{0}"}})'.format(paramFile))
        #generate sbml action
        with open('SpatialActionsIntermediate.bngl','w') as f:
            f.write('generate_network({overwrite=>1,TextReaction=>0})\n')
            f.write('simulate_ode({{suffix=>"{0}",t_start=>0,t_end=>50,n_steps=>10000}})\n'.format(paramFile.split('.')[0].split('/')[1]))
            f.write('writeSBML({{suffix=>"{0}"}})\n'.format(paramFile.split('.')[0].split('/')[1]))
        #run bionetgen
        print('will I call the right file?')

        call(['perl',bngDistro,'Motivational_example_cbngl_fixedparameterswoParam_maninit.bngl'])

        modifyReleaseNumber('Motivational_example_cbngl_fixedparameterswoParam_test_{0}.xml'.format(paramFile.split('.')[0].split('/')[1]))
