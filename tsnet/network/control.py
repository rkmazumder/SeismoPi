"""
The tsnet.network.control module includes method to define
network controls of the pump and valve.These control modify
parameters in the network during transient simulation.

"""

class Distance:
    
    """Figure out the topology of the network
    Parameters
    ----------
    wn : wntr.network.model.WaterNetworkModel
        .inp file used for EPAnet simulation
    npipe : integer
        Number of pipes
    Returns
    -------
    links1 : list
        The id of adjacent pipe on the start node.
        The sign represents the direction of the pipe.
        + : flowing into the junction
        - : flowing out from the junction
    links2 : list
        The id of adjacent pipe on the end node.
        The sign represents the direction of the pipe.
        + : flowing into the junction
        - : flowing out from the junction
    utype : list
        The type of the upstream adjacent links.
        If the link is not pipe, the name of that link
        will also be included.
        If there is no upstream link, the type of the start node
        will be recorded.
    dtype : list
        The type of the downstream adjacent links.
        If the link is not pipe, the name of that link
        will also be included.
        If there is no downstream link, the type of the end node
        will be recorded.
    """
    # Constructor
    def __init__(self, ex, ey, M):
        self.ex = ex  # Create an instance variable
        self.ey = ey
        self.M=Mag
    def com_pga_dist(data,ex,ey,Mag):
        r = []
        PGA = []
        PGV = []
        pos = {}
        for index, row in data.iterrows():
            x = row['x']
            y = row['y']
            dist = distance.euclidean((ex,ey), (x,y))/1000
            P = (403.8*np.power(10, 0.265*Mag)*np.power(dist+30, -1.218))/981
            V = (np.power(10, -0.848 + 0.775*Mag + -1.834*np.log10(dist+17)))/100
            r.append(dist)
            PGA.append(P)
            PGV.append(V)
            pos[int(row['id'])]=(x,y)
        r = np.array(r)
        PGA = np.array(PGA)
        PGV = np.array(PGV)
        return r, PGA, PGV, pos

    def pga_for_link(link,node,ex,ey,Mag):
        r = []
        PGA = []
        PGV = []
        for index, row in link.iterrows():
            start_node = row['start_node']
            end_node = row['end_node']
            start_x, start_y = node.loc[node['id']==start_node, ['x','y']].values[0]
            end_x, end_y = node.loc[node['id']==end_node, ['x','y']].values[0]
            dist_start = distance.euclidean((ex,ey), (start_x,start_y))/1000
            P_start = (403.8*np.power(10, 0.265*Mag)*np.power(dist_start+30, -1.218))/980
            V_start = (np.power(10, -0.848 + 0.775*Mag + -1.834*np.log10(dist_start+17)))/100
            dist_end = distance.euclidean((ex,ey), (end_x,end_y))/1000
            P_end = 403.8*np.power(10, 0.265*Mag)*np.power(dist_end+30, -1.218)/980
            V_end = (np.power(10, -0.848 + 0.775*Mag + -1.834*np.log10(dist_end+17)))/100
            PGA.append((P_start+P_end)/2)
            PGV.append((V_start+V_end)/2)
        return PGA, PGV
