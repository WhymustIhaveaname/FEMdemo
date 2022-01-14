import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
import scipy.sparse.linalg


def sample_node(bd_node, int_node):
    bd_angle = (0.01+np.array(range(bd_node)))/bd_node*2*np.pi
    bdp = np.stack((np.cos(bd_angle), np.sin(bd_angle))).T
    int_angle = np.random.rand(int_node)*2*np.pi
    int_radius = np.sqrt(np.random.rand(int_node))
    intp = np.stack((int_radius*np.cos(int_angle), int_radius*np.sin(int_angle))).T
    return np.concatenate((bdp, intp))[:-10,:], np.concatenate((bd_angle, int_angle))[:-10], np.concatenate((np.ones(num_bd_nodes), int_radius))[:-10]


def gen_A(nodes, tri):
    A = np.zeros((len(nodes) , len(nodes)))
    for e in tri:
        Le = np.zeros((3, len(nodes)))
        for i, n in enumerate(e):
            Le[i, n] = 1
        Me = np.zeros((3,3))
        Me[:,0] = 1
        # n is global index, i is local index
        for i,n in enumerate(e):
            Me[i, 1] = nodes[n, 0]
            Me[i, 2] = nodes[n, 1]
        P2 = np.zeros((3,3))
        P2[1, 1] = 1
        P2[2, 2] = 1
        Meinv = np.linalg.inv(Me)
        A+=Le.T@Meinv.T@P2@Meinv@Le
    return A


def boundary_condition(nodes, tri, num_bdp):
    bdt = np.zeros((num_bdp, 1))
    for i,node in enumerate(nodes):
        if i == num_bdp:
            break
        if node[1]>0:
            bdt[i,0] = 100
        else:
            bdt[i,0] = 0
    return bdt


if __name__=="__main__":
    np.random.seed(0)
    num_interior_nodes = 400
    num_bd_nodes = 50

    # generate node
    nodes, thetas, rs = sample_node(num_bd_nodes,num_interior_nodes)

    # generate mesh by Delauny triangulations
    tri = Delaunay(nodes)
    tri = tri.simplices

    #plt.scatter(nodes[:,0], nodes[:,1])
    #plt.triplot(nodes[:, 0], nodes[:, 1], tri)
    #plt.savefig('mesh.png', bbox_inches='tight')

    print("number of triangles: {}".format(len(tri)))
    print("number of nodes: {}".format(len(nodes)))

    # generate matrix A
    A = gen_A(nodes, tri)
    # separate matrix A
    A21 = A[num_bd_nodes:,:num_bd_nodes]
    A22 = A[num_bd_nodes:,num_bd_nodes:]

    bd_vec = boundary_condition(nodes, tri, num_bd_nodes)
    RHS = -A21@bd_vec
    solution = scipy.sparse.linalg.spsolve(A22, RHS)

    # print and plot the solution
    # Create triangulation.
    triang = mtri.Triangulation(nodes[:,0], nodes[:,1], tri)

    # Interpolate to regularly-spaced quad grid.
    xi, yi = np.meshgrid(np.linspace(-1, 1, 100), np.linspace(-1, 1, 100))
    z = np.concatenate((bd_vec[:,0],solution))
    theoretical_solution = 50+(200/np.pi)*sum((1/(2*m+1))*rs**(m+1)*np.sin((2*m+1)*thetas) for m in range(4000))

    # Set up the figure
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

    # Plot the triangulation.
    femcntr = axs[0].tricontourf(triang, z, levels=100, cmap="turbo")
    #axs[0].triplot(triang, 'ko-', alpha=0.01)
    axs[0].set_title('FEM solution')
    fig.colorbar(femcntr, ax=axs[0])
    tcntr = axs[1].tricontourf(triang, theoretical_solution, levels=100, cmap="turbo")
    fig.colorbar(femcntr, ax=axs[1])
    axs[1].set_title('Theoretical solution')

    plt.show()
