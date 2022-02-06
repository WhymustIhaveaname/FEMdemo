#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import numpy as np
import meshio
import matplotlib.pyplot as plt
from tqdm import tqdm

def read_mesh(filename):
    stick = meshio.read(filename)
    nodes = stick.points
    # the following sentence is equvalent to
    # cells = stick.cells[3].data
    cells = stick.cells_dict['tetra']
    print("load mesh from %s: %d nodes, %d cells"%(filename,len(nodes),len(cells)))
    return nodes,cells

def purge_mesh(nodes,cells):
    s=set(range(len(nodes)))
    for cell in cells:
        for i in cell:
            s.discard(i)
    print("point not used: %s"%(s))

    d={};ax=0
    for i in range(len(nodes)):
        if i not in s:
            d[i]=ax;ax+=1
    print("len(nodes): %d, ax: %d"%(len(nodes),ax))

    nodes_neo=[]
    for i in range(len(nodes)):
        if i not in s:
            nodes_neo.append(nodes[i])
    nodes_neo=np.array(nodes_neo)

    cells_neo=[]
    for cell in cells:
        cells_neo.append([d[i] for i in cell])
    cells_neo=np.array(cells_neo)

    s_neo=set(range(len(nodes_neo)))
    for cell in cells_neo:
        for i in cell:
            s_neo.discard(i)
    print("point not used after purging: %s"%(s_neo))

    return nodes_neo,cells_neo

def tetra_vol(cell,nodes):
    """
        cells: indices of tetrahedron vertices, should be a length-4 list
    """
    a = nodes[cell[0]]-nodes[cell[1]]
    b = nodes[cell[0]]-nodes[cell[2]]
    c = nodes[cell[0]]-nodes[cell[3]]
    return abs(np.linalg.det(np.stack((a,b,c)))) / 6.0

def tri_area(cell,nodes):
    """
        cells: indices of triangular vertices, should be a length-3 list
    """
    a = nodes[cell[0]]-nodes[cell[1]]
    b = nodes[cell[0]]-nodes[cell[2]]
    return np.linalg.norm(np.cross(a,b)) / 2.0

def gen_K(nodes, cells, E, nv):
    """
        E is in MPa
    """
    print("generating K matrix")
    # construct the D matrix in Hooke's law
    D = np.diag([1-nv,1-nv,1-nv,(1-2*nv)/2,(1-2*nv)/2,(1-2*nv)/2])
    for i in range(3):
        for j in range(3):
            if i != j:
                D[i,j] = nv
    D *= E/((1+nv)*(1-2*nv))

    K = np.zeros((3*len(nodes), 3*len(nodes)))
    for cell in tqdm(cells):
        Le = np.zeros((4*3, 3*len(nodes)))
        # i is local index, n is global index
        for i, n in enumerate(cell):
            Le[3*i, 3*n] = 1
            Le[3*i+1, 3*n+1] = 1
            Le[3*i+2, 3*n+2] = 1

        Me = np.zeros((4,4))
        Me[:,0] = 1
        # n is global index, i is local index
        for i, n in enumerate(cell):
            Me[i,1:4] = nodes[n,:]
        Meinv = np.linalg.inv(Me)

        Bevec = []
        for i in range(4):
            bei = np.zeros((6,3))
            bei[0,0] = Meinv[1,i]
            bei[1,1] = Meinv[2,i]
            bei[2,2] = Meinv[3,i]
            bei[3,0] = Meinv[2,i]
            bei[3,1] = Meinv[1,i]
            bei[4,0] = Meinv[3,i]
            bei[4,2] = Meinv[1,i]
            bei[5,1] = Meinv[3,i]
            bei[5,2] = Meinv[2,i]
            Bevec.append(bei)
        Be = np.concatenate(Bevec, axis=1)
        Klocal = tetra_vol(cell,nodes)*Be.T@D@Be
        K += Le.T@Klocal@Le
    return K

def gen_f(nodes, cells, F = np.array([[1.],[0],[0]])):
    """
        F is in Million Newton
    """
    print("gnerating f vector")
    A = 1
    f = np.zeros(( 3 * len(nodes), 1))
    area = 0
    for cell in cells:
        ct = sum([nodes[n,2]>0.999*A for i,n in enumerate(cell)])
        if ct <3:
            continue
        Le = np.zeros((4 * 3, 3 * len(nodes)))
        for i, n in enumerate(cell):
            # i is local index, n is global index
            Le[3 * i, 3 * n] = 1
            Le[3 * i + 1, 3 * n + 1] = 1
            Le[3 * i + 2, 3 * n + 2] = 1
        idx = [n for i,n in enumerate(cell) if nodes[n,2]>0.999*A]
        areae = tri_area(idx,nodes)
        Net = np.zeros((12,3))
        Me = np.zeros((4, 4))
        Me[:, 0] = 1
        # n is global index, i is local index
        for i, n in enumerate(cell):
            Me[i, 1] = nodes[n, 0]
            Me[i, 2] = nodes[n, 1]
            Me[i, 3] = nodes[n, 2]
        Meinv = np.linalg.inv(Me)
        centroid = np.mean(np.stack((nodes[idx[0]],nodes[idx[1]],nodes[idx[2]])), axis=0)
        centroid = np.concatenate((np.ones(1),centroid))
        Nje = []
        for j in range(4):
            Nje.append(np.sum(Meinv[:,j]*centroid))
        for j in range(4):
            for i in range(3):
                Net[3*j+i,i]=Nje[j]
        fe = Net@F*areae
        area+=areae
        f += Le.T@fe
    return f/area

def plot_tri_mesh(nodes, cells, ax=None, boundary_only=True, plot_nodes=True, color = 'g', linewidth = 0.2, markersize=8):
    if ax==None:
        fig=plt.figure()
        ax=fig.add_subplot(projection='3d')
    ax.set_box_aspect([max(nodes[:,0])-min(nodes[:,0]),max(nodes[:,1])-min(nodes[:,1]),max(nodes[:,2])-min(nodes[:,2])])

    if boundary_only:
        # bdind = boundary indices
        bdind1 = np.where(np.linalg.norm(nodes[:,0:2],axis=1)>0.09)[0]
        bdind2 = np.where(nodes[:,2]<0.01)[0]
        bdind3 = np.where(nodes[:,2]>0.99)[0]
        s_temp=set()
        s_temp.update(bdind1)
        s_temp.update(bdind2)
        s_temp.update(bdind3)
        bdind=np.array(list(s_temp))
    else:
        bdind = np.array(range(len(nodes)))

    bdind_set=set(bdind)
    plotted_set=set()
    for cell in cells:
        pts = nodes[cell,:]
        # pp stands for point pair
        for pp in [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]:
            ppidx=tuple(cell[pp])
            if ppidx[0] not in bdind_set or ppidx[1] not in bdind_set:
                continue
            if ppidx in plotted_set:
                continue
            ax.plot3D(pts[pp,0], pts[pp,1], pts[pp,2], color=color, lw=linewidth)
            plotted_set.add(ppidx)
    if plot_nodes:
        ax.scatter(nodes[bdind,0], nodes[bdind,1], nodes[bdind,2], color='b',s=markersize)
    return ax