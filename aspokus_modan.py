import my_importGmsh as impG
import my_assemble_modan as my

meshfile = 'obdelnik.msh'

mesh = impG.GMSH_READER()        # create a object 'mesh'
mesh.readMesh(meshfile)  
tripletvst=([0,0],0)

triplet=my.assembleSystemMECH(mesh,1,0,tripletvst)



print(triplet)

