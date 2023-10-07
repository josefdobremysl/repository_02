'''
"readMesh", "elm_types" methods from: "https://github.com/lukeolson/python-mesh-scripts/blob/master/gmsh.py"
'''
from __future__ import print_function
import numpy as np
import scipy as sp
import sys


class GMSH_READER:
    """
    Reads and extracts mesh data from a *.msh file. Note that in the moment only 4 node (linear) quad elements are supported.
    One has to assure that the imported mesh consists only of one physical domain.
         
    raw parameters (directly read from gmsh file)
    ----------
    :meshname: name of the mesh file
    :nDomains: number of physical domains
    :nNodes: number of nodes in the domain
    :nodeCoord: nodes coordinate matrix extracted from gmsh (nNodes,3)
    :PhysNames: domain names     dictionary ... {key=<physical number>: value='<domain name>'}
    :PhysDims: domain dimension dictionary ... {key=<physical number>: value=<physical dimention>}
    :nElmts: number of element dictionary... {key=<element type>   : value=<number>}
    :Elmts: elements dictionary         ... {key=<element type>   : value=<connectivity>}
    :elm_types: element types dictionary
    
    CO BUDEME POUZIVAT MY:
    ---------------------
    nNodes      jako vyse
    :nodeXY:   TENTOKRAT CISTE POLE
    :nTri:      POCET TROJUHLENIKU
    :triangles: VRCHOLY TROJUHLENIKU
    :triTag:    INDEX trojuhelniku ze site
    :nBsides:   POCET STRAN
    :Bsides:    VRCHOLY USECEK 
    :sideTag:   INDEX dane usecky

    
    
    methods
    ----------
    :readMesh: reads a 2.* ascii gmsh file
    :elm_types: sets a dictionary of the possible elements written by gmsh
    """
    
    def __init__(self): 
        # raw variables extracted from the gmsh
        self.meshname = ''
        self.nDomains = 0
        self.nNodes = 0
        self.nodeCoord = []
        # 
        self.elm_types()
        self.Elmts = {}
        self.PhysNames = {}
        self.PhysDims = {}
        self.nElmts = {}
        
        
        ### CO BUDEME POUZIVAT
        #self.meshname = ''
        #self.nNodes
        self.nodeXY = [] # 2D array
        #
        self.nBsides = 0
        self.Bsides = []
        self.sideTag = []
        #
        self.nTri = 0
        self.triangles = []
        self.triTag = []
      
        
#===============================================================================================================================================================================================
    def readMesh(self, meshfile):
        """Read a Gmsh .msh file.
        Reads Gmsh 2.* mesh files
        
        parameters
        ----------
        :meshname: name of the mesh file
        :nDomains: number of physical domains
        :nNodes: number of nodes in the domain
        :nodeCoord: nodes coordinate matrix extracted from gmsh (nNodes,3)
        :PhysNames: domain names dictionary ... {key=<physical number>: value='<domain name>'}
        :PhysDims: domain dimension dictionary ... {key=<physical number>: value=<physical dimention>}
        :nElmts: number of element dictionary... {key=<element type>   : value=<number>}
        :Elmts: elements dictionary ... {key=<element type>   : value=<connectivity>}
        """
        
        print('----------------------------------------------------------------------')
        print('Searching for a mesh file...', end='')
        self.meshname = meshfile
        try:
            fid = open(meshfile, 'r')
        except IOError:
            print('----------------------------------------------------------------------')
            print("File '%s' not found." % meshfile)
            sys.exit()
        print('DONE')
        print('----------------------------------------------------------------------')
        print('Reading mesh...')
        line = 'start'
        while line:
            # start to read the mesh file line by line
            line = fid.readline()                       # reads the ACTUAL LINE (while-loop)
            
            
            # checks is the $MeshFormat-line is "active"
            if line.find('$MeshFormat') == 0:           # checks if there is a "$MeshFormat"-line it should be on the [0] position
                print('   Reading mesh format...', end='')
                line = fid.readline()                   # e.g. line="2.2 0 8" is a 1x3 matrix
                if line.split()[0][0] is not '2':       # checks the version of gmsh (e.g. [0]column [0]row -> "2")
                    print('wrong gmsh version')
                    sys.exit()
                line = fid.readline()
                if line.find('$EndMeshFormat') != 0:    # checks if '$MeshFormat' is closed properly with "$EndMeshFormat" at the [0] position
                    raise ValueError('expecting EndMeshFormat')
            
            # checks if the $PhysicalNames-line is "active"     
            if line.find('$PhysicalNames') == 0:
                print('DONE')
                print('   Reading physical names...', end='')
                line = fid.readline()
                self.nDomains = int(line.split()[0])               # reads the number of physical domains
                for i in range(0, self.nDomains):                  # loops over all physical domains
                    line = fid.readline()
                    physDim = int(line.split()[0][0])              # reads the physical-dimention [0]column [0]row (e.g. here =2)
                    physNum = int(line.split()[1][0])              # reads the physical-number    [1]column [0]row (e.g. here =1)          
                    qstart = line.find('"')+1                      # defines the first position of the domain name (e.g. [2 1 "Domain"] -> D=[5])
                    qend = line.find('"', -1, 0)-1                 # defines the last  position of the domain name (e.g. [2 1 "Domain"] -> n=[-2])
                    self.PhysDims[physNum] = physDim               # sets a new dictionary with {key=<physical-number> : value=<physical-dimention>}
                    self.PhysNames[physNum] = line[qstart:qend]    # sets a new dictionary with {key=<physical-number> : value='<physical-name>'}
                line = fid.readline()
                if line.find('$EndPhysicalNames') != 0:            # checks if '$PhysicalNames' is closed properly with "$EndPhysicalNames" at the [0] position
                    raise ValueError('expecting EndPhysicalNames')

            # checks if the $PhysicalNames-line is "active"
            if line.find('$Nodes') == 0:
                print('DONE')
                print('   Reading nodes...', end='')
                line = fid.readline()
                self.nNodes = int(line.split()[0])                            # reads the number of nodes   (e.g. here =15)
                self.nodeCoord = np.zeros((self.nNodes, 3), dtype=float)      # sets a node matrix of zeros (e.g. here (15,3) matrix)
                for i in range(0, self.nNodes):                               # loops over all nodes        (e.g. here 0->14)
                    line = fid.readline()
                    data = line.split()                                       # makes an array from the "active" line
                    idx = int(data[0])-1                                      # fix gmsh 1-based node number indexing   (e.g. from 1->15 to 0->14)
                    if i != idx:                                              # checks if the node number indexing is correct
                        raise ValueError('problem with vertex ids')
                    self.nodeCoord[idx, :] = list(map(float, data[1:]))       # fills the node matrix with their coordinates
                line = fid.readline()
                if line.find('$EndNodes') != 0:                               # checks if '$Nodes' is closed properly with "$EndNodes" at the [0] position
                    raise ValueError('expecting EndNodes')
            
            # checks if the $Elements-line is "active"
            if line.find('$Elements') == 0:
                print('DONE')
                print('   Reading elements...', end='')
                line = fid.readline()
                self.nEl = int(line.split()[0])                                      # reads the number of elements (e.g. here 8)              
                for i in range(0, self.nEl):                                         # loops over all elements      (e.g. here 0->7)
                    line = fid.readline()
                    data = line.split()                                              # makes an array from the "active" line
                    idx = int(data[0])-1                                             # fix gmsh 1-based element indexing (e.g. from 1->8 to 0->7)
                    if i != idx:
                        raise ValueError('problem with elements ids')
                    
                    eType = int(data[1])                                             # element type (e.g. here 3=4-node quadrangle)
                    nTags = int(data[2])                                             # number of tags following in the *.msh file before one gets to the connectivity entries (e.g. here =2)
                    k = 3
                    if nTags > 0:                                                    # set physical id
                        physId = int(data[k])                                        # reads the number of the mesh partition (<=> physical-number) to which the elements belongs (e.g. here =1)
                        if physId not in self.PhysNames:                             # checks if the physical-number is already in the "PhysNames" dictionary
                            self.PhysNames[physId] = 'Physical Entity %d' % physId   # sets a new entity, IF the above condition not satisfied
                            self.nDomains += 1                                       # sets the number of domains with +1
                        k += nTags                                                   # "move the cursor" to the (e.g. here =5) column. From the 6. starts the connectivity matrix
                    connec = list(map(int, data[k:]))                                # fills the element connectivity matrix
                    connec = np.array(connec)-1                                      # fix gmsh 1-based node number indexing (e.g. from 1->15 to 0->14)
                    if (eType not in self.Elmts) or\
                            (len(self.Elmts[eType]) == 0):                           # checks if the element type is not in the dictionary OR dictionary has the lenght=0
                        # initialize the "Elmts"-dictionary
                        self.Elmts[eType] = (physId, connec)
                        self.nElmts[eType] = 1                                       # fills the number of elements dictionary with type (e.g. here =3) and number(e.g. here =8) 
                    else:
                        # append to the "Elmts"-dictionary
                        self.Elmts[eType] = \
                            (np.hstack((self.Elmts[eType][0], physId)),
                             np.vstack((self.Elmts[eType][1], connec)))
                        self.nElmts[eType] += 1
                line = fid.readline()
                if line.find('$EndElements') != 0:                                   # checks if '$Elements' is closed properly with "$EndElements" at the [0] position
                    raise ValueError('expecting EndElements')
        fid.close()

        self.nodeXY = self.nodeCoord[:,[0,1]]        
        print('self.nElmts:',self.nElmts)
        print('self.Elmts:',self.Elmts)

        self.nBsides = self.nElmts[1] # 1 je typ usecka
        print('self.nBsides:',self.nBsides)
        self.Bsides = self.Elmts[1][1] # pole vrcholu jednotlivych usecek
        print('self.Bsides:',self.Bsides)
        self.sideTag = self.Elmts[1][0] # seznam indexu jednotlivych usecek
        print('self.sideTag:',self.sideTag)
        print("self.nElmts:",self.nElmts)
        self.nTri = self.nElmts[2] # 2 je typ trojuhelniku
        print('self.nTri:',self.nTri)
        self.triangles = self.Elmts[2][1] # pole vrcholu jednotlivych troj.
        print('self.triangles:',self.triangles)
        self.triTag = self.Elmts[2][0] # seznam indexu jednotlivych troj.
        print('self.triTag:',self.triTag)
       
        print('DONE')
        
        
#===============================================================================================================================================================================================

    def elm_types(self):
        '''
        Sets an informational element types dictionary. It is not beeing used actively in this code, but it gives a information on the element types from gmsh
        
        parameters
        -----------
        :elm_type: gmsh element dictionary
        '''
        print('----------------------------------------------------------------------')
        print('Setting gmsh element type dictionary...', end="")
        
        # initialize the dictionary
        elm_type = {}    

        # fill the dictionary {key=<element code>   : value=<node number>}
        elm_type[1] = 2     #   2-node line
        elm_type[2] = 3     #   3-node triangle
        elm_type[3] = 4     #   4-node quadrangle
        elm_type[4] = 4     #   4-node tetrahedron
        elm_type[5] = 8     #   8-node hexahedron
        elm_type[6] = 6     #   6-node prism
        elm_type[7] = 5     #   5-node pyramid
        elm_type[8] = 3     #   3-node second order line                (2 nodes at vertices and 1 with edge)
        elm_type[9] = 6     #   6-node second order triangle            (3 nodes at vertices and 3 with edges)
        elm_type[10] = 9    #   9-node second order quadrangle          (4 nodes at vertices, 4 with edges and 1 with face)
        elm_type[11] = 10   #  10-node second order tetrahedron         (4 nodes at vertices and 6 with edges)
        elm_type[12] = 27   #  27-node second order hexahedron          (8 nodes at vertices, 12 with edges, 6 with faces and 1 with volume)
        elm_type[13] = 18   #  18-node second order prism               (6 nodes at vertices, 9 with edges and 3 with quadrangular faces)
        elm_type[14] = 14   #  14-node second order pyramid             (5 nodes at vertices, 8 with edges and 1 with quadrangular face)
        elm_type[15] = 1    #   1-node point
        elm_type[16] = 8    #   8-node second order quadrangle          (4 nodes at vertices and 4 with edges)
        elm_type[17] = 20   #  20-node second order hexahedron          (8 nodes at vertices and 12 with edges)
        elm_type[18] = 15   #  15-node second order prism               (6 nodes at vertices and 9 with edges)
        elm_type[19] = 13   #  13-node second order pyramid             (5 nodes at vertices and 8 with edges)
        elm_type[20] = 9    #   9-node third order incomplete triangle  (3 nodes at vertices, 6 with edges)
        elm_type[21] = 10   #  10-node third order triangle             (3 nodes at vertices, 6 with edges, 1 with face)
        elm_type[22] = 12   #  12-node fourth order incomplete triangle (3 nodes at vertices, 9 with edges)
        elm_type[23] = 15   #  15-node fourth order triangle            (3 nodes at vertices, 9 with edges, 3 with face)
        elm_type[24] = 15   #  15-node fifth order incomplete triangle  (3 nodes at vertices, 12 with edges)
        elm_type[25] = 21   #  21-node fifth order complete triangle    (3 nodes at vertices, 12 with edges, 6 with face)
        elm_type[26] = 4    #   4-node third order edge                 (2 nodes at vertices, 2 internal to edge)
        elm_type[27] = 5    #   5-node fourth order edge                (2 nodes at vertices, 3 internal to edge)
        elm_type[28] = 6    #   6-node fifth order edge                 (2 nodes at vertices, 4 internal to edge)
        elm_type[29] = 20   #  20-node third order tetrahedron          (4 nodes at vertices, 12 with edges, 4 with faces)
        elm_type[30] = 35   #  35-node fourth order tetrahedron         (4 nodes at vertices, 18 with edges, 12 with faces, 1 in volume)
        elm_type[31] = 56   #  56-node fifth order tetrahedron          (4 nodes at vertices, 24 with edges, 24 with faces, 4 in volume)
        elm_type[92] = 64   #  64-node third order hexahedron           (8 nodes at vertices, 24 with edges, 24 with faces, 8 in volume)
        elm_type[93] = 125  # 125-node third order hexahedron           (8 nodes at vertices, 24 with edges, 24 with faces, 8 in volume)
        self.elm_type = elm_type
        #DEBUG
        print('DONE')
