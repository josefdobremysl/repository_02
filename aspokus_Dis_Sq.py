import my_importGmsh as impG
import my_assemble_Dis_Sq as my

meshfile = 'sit_DNNSS_0.03_zjemneni.msh'

mesh = impG.GMSH_READER()        # create a object 'mesh'
mesh.readMesh(meshfile)  
tripletvst=([0,0],0)

triplet=my.assembleSystemMECH(mesh,1,0,tripletvst)



print(triplet)

