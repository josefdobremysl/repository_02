import my_importGmsh as impG
import my_assemble_Kom_plus_09_02 as my

meshfile = 'sit_4Dir_0.001_1.msh'

mesh = impG.GMSH_READER()        # create a object 'mesh'
mesh.readMesh(meshfile)  
tripletvst=([0,0],0)

triplet=my.assembleSystemMECH(mesh,1,0,tripletvst)



print(triplet)

