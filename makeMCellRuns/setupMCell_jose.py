#def setupMcCll(geometry,biochem)

import bpy
from cellblender import bng
import argparse

def argOptions(arguments):
    #define command line parser
    parser = argparse.ArgumentParser(description='Model pipeline batch helper. Execute like blender --background  --python setupMcell.py -- <arguments>')
    parser.add_argument("-g","--geometry",dest="inputGeometry",
    type=str,help="The input SBML geometry file in xml format.")
    parser.add_argument("-b","--biochemistry",dest="sbmlfilepath",
		type=str,
		help="the input SBML biochemistry file in xml format")

    #if there's no arguments print the command line help
    if not arguments:
        parser.print_help()
        return
    
    #otherwise parser those arguments
    args = parser.parse_args(arguments)  # In this example we wont use the args
    return args

def processFile(options):
    #make sure blend is up to date
    bpy.ops.mcell.upgrade()
    
    #Import geometry
    bng.sbml_operators.execute_sbml2blender(options.inputGeometry,bpy.context)
    #Import biochemistry
    #sbmlfilepath = inputBioChemistry
    bng.sbml_operators.execute_externally(options.sbmlfilepath,bpy.context)
    bng.external_operators.filePath = options.sbmlfilepath
    print ( "Loading parameters from external model..." )
    bpy.ops.external.parameter_add()         # This processes all entries in the par_list parameter list
    print ( "Loading molecules from external model..." )
    bpy.ops.external.molecule_add()
    print ( "Loading reactions from external model..." )
    bpy.ops.external.reaction_add()
    print ( "Loading release sites from external model..." )
    bpy.ops.external.release_site_add()
    print ( "Done Loading external model" )
    #if ('.xml') in self.filepath:
       #TODO:this is sbml only until we add this information on the bng side
    print("Loading reaction output ...")
    bpy.ops.external.reaction_output_add()


    #bng.sbml_operators.execute_sbml2mcell("/Users/admin/Dropbox/HighThroughputModeling/BNGLFilesforSim/xmlfiles_t0/Motivational_example_cbngl_fixedparameterswoParam_lowEN0_5std_cell_8seed3.xml",bpy.context)

    #set total time and timestep
    bpy.context.scene.mcell.parameter_system.panel_parameter_list[0].expr="4000000"
    bpy.context.scene.mcell.parameter_system.panel_parameter_list[1].expr="1e-4"

    #Turn off viz data
    bpy.context.scene.mcell.viz_output.export_all = False
    bpy.context.scene.mcell.viz_output.all_iterations = False

    #Set partitions
    bpy.context.scene.mcell.partitions.include = True
    bpy.ops.mcell.auto_generate_boundaries()
    bpy.context.scene.mcell.partitions.x_step = 0.1
    bpy.context.scene.mcell.partitions.y_step = 0.1
    bpy.context.scene.mcell.partitions.z_step = 0.1

    #Set target only for receptor
    bpy.context.scene.mcell.molecules.molecule_list[1].target_only = True

    #Write out blend file
    #get var
    geompath = options.inputGeometry
    #split path
    fileparts = geompath.split("/")
    #get file name
    full_filename = fileparts[-1]
    #split prefix
    filename = full_filename.split(".xml")
    savename = filename[0]
    parentsavepath = "/Users/admin/MurphyLab/HTM/MCellRuns/"+savename
    saveloc = parentsavepath+".blend"
    bpy.ops.wm.save_mainfile(filepath=saveloc)
    #bpy.ops.wm.save_mainfile(filepath="/Users/admin/Murphylab/HTM/FilesToExport2/fullImportTest3.blend")
    #bpy.ops.wm.save_mainfile(filepath=["/Users/admin/MurphyLab/HTM/FilesToExport2/"+geometry[0:(len(geometry)-4)]

    #Export mcell 
    bpy.ops.mcell.export_project()
    
    print("this should have exportedt!")

    '''#Now that we have the project exported let's get the parameters for the BNG
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.data.objects['CP'].select = True
    bpy.ops.mcell.meshalyzer()
    mobj = bpy.context.scene.mcell.meshalyzer
    print(mobj.volume)
    #cpvol = 'vol_CP {0}'.format(volume)
    cpvol = '\t vol_{0} {1}\n'.format(mobj.object_name,mobj.volume)
    cpsa = '\t sa_PM {0}\n'.format(mobj.area)
    
    #open file
    f = open(parentsavepath+'_spatialParams.bngl', 'w')
    f.write('begin  parameters\n')
    f.write(cpvol)
    f.write(cpsa)

    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.data.objects['NU'].select = True
    bpy.ops.mcell.meshalyzer()
    mobj = bpy.context.scene.mcell.meshalyzer
    print(mobj.volume)
    #cpvol = 'vol_CP {0}'.format(volume)
    nuvol = '\t vol_{0} {1}\n'.format(mobj.object_name,mobj.volume)
    nusa = '\t sa_NM {0}\n'.format(mobj.area)
    f.write(nuvol)
    f.write(nusa)

    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.data.objects['EN'].select = True
    bpy.ops.mcell.meshalyzer()
    mobj = bpy.context.scene.mcell.meshalyzer
    print(mobj.volume)
    #cpvol = 'vol_CP {0}'.format(volume)
    envol = '\t vol_{0} {1}\n'.format(mobj.object_name,mobj.volume)
    ensa = '\t sa_EM {0}\n'.format(mobj.area)
    f.write(envol)
    f.write(ensa)
    
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.data.objects['EC'].select = True
    bpy.ops.mcell.meshalyzer()
    mobj = bpy.context.scene.mcell.meshalyzer
    print(mobj.volume)
    #cpvol = 'vol_CP {0}'.format(volume)
    ecvol = '\t vol_{0} {1}\n'.format(mobj.object_name,mobj.volume)
    ecsa = '\t sa_{0} {1}\n'.format(mobj.object_name,mobj.area)
    f.write(ecvol)
    f.write(ecsa)

    f.write('end  parameters')
    f.close()'''

def main():
    import sys       # to get command line args

    # get the args passed to blender after "--", all of which are ignored by
    # blender so scripts may receive their own arguments
    argv = sys.argv

    if "--" not in argv:
        print('noargs')
        argv = []  # as if no args are passed
    else:
        print('found something')
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    commandLineArguments = argOptions(argv)
    if not commandLineArguments:
        return

    processFile(commandLineArguments)


if __name__ == "__main__":
    main()
