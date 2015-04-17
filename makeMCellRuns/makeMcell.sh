#!/bin/bash

SBMLPATH="/Users/admin/Dropbox/HighThroughputModeling/BNGLFilesforSim/xmlfiles_t0/Motivational_example_cbngl_fixedparameterswoParam_meanEN0_5std_cell_10seed3.xml"
GEOPATH="/Users/admin/MurphyLab/HTM/newxmlfiles2/meanEN0_5std_cell_10seed3.xml"
#for i in $( ls /Users/admin/Dropbox/HighThroughputModeling/newxmlfiles2/*.xml); do
#    echo item: $i
#done
#  ~/localbin/mcell -seed ${a} Scene.main.mdl >> run.1_${a}.log 

/Users/admin/Documents/Blender/blender.app/Contents/MacOS/blender -b --python setupMCell_jose.py -- -g $GEOPATH -b $SBMLPATH

