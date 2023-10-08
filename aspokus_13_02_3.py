import my_importGmsh as impG
import my_assemble_Kom_13_02_3 as my

meshfile = 'sit_4Dir_0.1_2.msh'

mesh = impG.GMSH_READER()        # create a object 'mesh'
mesh.readMesh(meshfile)  
tripletvst=([0,0],0)

triplet=my.assembleSystemMECH(mesh,1,0,tripletvst)



print(triplet)

