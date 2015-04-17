#!/bin/bash

#SBMLPATH="/Users/admin/Dropbox/HighThroughputModeling/BNGLFilesforSim/xmlfiles_t0/Motivational_example_cbngl_fixedparameterswoParam_lowEN0_5std_cell_8seed3.xml" 
#SBMLPATH="/Users/admin/DropBox/HighThroughputModeling/BNGLFilesforSim/xmlfiles_t0/*.xml"
SBMLPATH="/Users/admin/MurphyLab/HTM/BNGsetups_t0/*.xml"
GEOPATH="/Users/admin/MurphyLab/HTM/newxmlfiles2/*.xml"
#GEOPATH="/Users/admin/Dropbox/HighThroughputModeling/BNGLFilesforSim/newxmlfiles2/*seed3.xml"
#GEOPATH="/Users/admin/MurphyLab/HTM/newxmlfiles2/*.xml"

biodirlist=(`ls ${SBMLPATH}`)
geodirlist=(`ls ${GEOPATH}`)
numfiles=${#biodirlist[*]}

#for ((a=0; a<=2; a=a+1)); do
for ((a=0; a<=$numfiles; a=a+1)); do
    echo item: $a
    echo ${geodirlist[a]}
    echo ${biodirlist[a]}
    /Users/admin/Documents/Blender/blender.app/Contents/MacOS/blender -b --python setupMCell_jose.py -- -g ${geodirlist[a]} -b ${biodirlist[a]}
done

#for geopath in $( ls /Users/admin/Dropbox/HighThroughputModeling/newxmlfiles2/*.xml); do
#    CURRGEOPATH=geopath
#    CURRBIOPATH=dirlist[
#    /Users/admin/Documents/Blender/blender.app/Contents/MacOS/blender -b --python setupMCell_jose.py -- -g $GEOPATH -b $SBMLPATH
#    echo item: $i
#done
#  ~/localbin/mcell -seed ${a} Scene.main.mdl >> run.1_${a}.log 

#/Users/admin/Documents/Blender/blender.app/Contents/MacOS/blender -b --python setupMCell_jose.py -- -g $GEOPATH -b $SBMLPATH

