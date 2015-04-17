def setupMcCll(biochemfilepath):

    import bpy
    from cellblender import bng

    #Import geometry
    geometryfilepath = "/Users/admin/cellorganizer/demos/3D/demo3D22/newxmlfiles2/lowEN0_5std_cell_8seed3.xml"
    bng.sbml_operators.execute_sbml2blender(geometryfilepath,bpy.context)
    #Import biochemistry
    #sbmlfilepath = "/Users/admin/Dropbox/HighThroughputModeling/BNGLFilesforSim/xmlfiles_t0/Motivational_example_cbngl_fixedparameterswoParam_lowEN0_5std_cell_8seed3.xml"
    bng.sbml_operators.execute_externally(sbmlfilepath,bpy.context)
    bng.external_operators.filePath = biochemfilepath#sbmlfilepath
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
    bpy.context.scene.mcell.parameter_system.panel_parameter_list[0].expr="5000000"
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
    bpy.ops.wm.save_mainfile(filepath="/Users/admin/Murphylab/HTM/FilesToExport2/fullImportTest2.blend")
    #bpy.ops.wm.save_mainfile(filepath=["/Users/admin/MurphyLab/HTM/FilesToExport2/"+geometry[0:(len(geometry)-4)]

    #Export mcell
    bpy.ops.mcell.export_project()
