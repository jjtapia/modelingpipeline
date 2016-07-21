#----------------------------------------------------------
# File objects.py
#----------------------------------------------------------
import bpy
import mathutils
from mathutils import Vector
from numpy import arange 
 
def createSphereFromPrimitive(name, location, size):
    diameter = (size ** (1.0/3) ) /3.141592*2
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, location=location, size=diameter)
    ob = bpy.context.object
# Object  Surface Area  Volume

    ob.name = name
    me = ob.data
    me.name = name
    return ob

def createEndosomes(cytoplasmsize, nucleussize, endosomesize,nendosomes): 
    cradius = (cytoplasmsize ** (1.0/3) ) /3.141592*2
    nradius = (nucleussize ** (1.0/3) ) /3.141592*2
    workvolume = cytoplasmsize - nucleussize
    wradius = cradius - nradius
    
    indvsize = endosomesize/nendosomes
    eradius = (indvsize **(1.0/3))/3.141592*2
    pdiameter = eradius
    spacing = cradius  / (nendosomes ** (1.0/3))
    for x in arange(-cradius,cradius,spacing):
        for y in arange(-cradius, cradius,spacing):
            for z in arange(-cradius, cradius,spacing):
                distance = (abs(x)**2 + abs(y)**2 + abs(z)**2)**(0.5)
                print(x,y,z,distance)
                if(distance+pdiameter <= cradius and distance-pdiameter>= nradius):
                    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, location=Vector((x,y,z)), size=pdiameter)                

    ob = bpy.context.object
    if ob:
        ob.name = 'EN'
        me = ob.data
        me.name = 'EN'
    return ob
 
def run(cellsize, nucleussize, endosomesize, nendosomes):
    
    createEndosomes(cellsize,nucleussize, endosomesize, nendosomes)
    bpy.ops.object.select_all()
    bpy.ops.object.select_all()
    bpy.ops.object.join()
    createSphereFromPrimitive('CP', Vector((0,0,0)),cellsize)
    createSphereFromPrimitive('NU', Vector((0,0,0)),nucleussize)
    return
 
if __name__ == "__main__":
    run(10,1,0.02,100)

