'''
-------------------------------------------------------------------
This file calulate the node importance with a decompostion process

This file is composed by four function:
(1)The first one is used to create test data to test the model
(2)The second one is used to replace the nodes label for an edge list
(3)The third one is used to find an element in a list
(4)The forth one is used to calculated the score for each node

Notes:
    (1)Each line includes to elements which is splited by '\t'
        example:
            1\t2
            2\t3
            3\t4
Example:
create a mian function to end of file which include such code:

    #set the path and filename to read a file
    path = r'C:\Users\qyh\Desktop\code for Nimp_python'
    filename = 'withourE.txt'

    #replace node labels with consistent labels
    edges, total_node = replace_network_line(path, filename)

    #calulate the node score
    node_score,node_degree = get_node_score(edges, total_node)

    #write results to a text file:
    wfile = open('Erdos_score.txt','w')

    max_node_score = max(node_score)
    max_node_degree = max(node_degree)-1

    ##the format for the output file is shown as follows:
    ##node label\tdegree\tscore\tnomalized degree\tnormalized score
    
    for i in range(len(node_score)):
        wfile.write(str(i+1)+'\t'+str(node_degree[i])+'\t'+str(node_score[i]) \
                    +'\t'+str(1.0*(node_degree[i]-1)/max_node_degree)+'\t'+ \
                    str(1.0*node_score[i]/max_node_score)+'\n')
    wfile.close()
    print "ok"

The detail for the process can be seen the file:


-------------------------------------------------------------------
'''


##create test data to test the model
def create_testdata(edges):
    '''
    create test data to test the model
    ---
    Parameters
    %edges: edge list data
    ---
    Return
    %new_edges: the replaced edge list,
    where the node label is consecutive 
    %total_nodes: the total number of nodes
    '''
    node_dict = {}
    edge_list = []
    total_nodes = 0
    for edge in edges:
        if edge[0] not in node_dict:
            node_dict[edge[0]] = total_nodes
            total_nodes = total_nodes+1
        if edge[1] not in node_dict:
            node_dict[edge[1]] = total_nodes
            total_nodes = total_nodes+1
        edge_list.append(edge) 

    ##replace node label for each edge,
        ##to ensure the label is consecutive
    new_edges = []
    for edge in edge_list:
        new_edges.append([node_dict[edge[0]],node_dict[edge[1]]])
    return new_edges, total_nodes


##replace the nodes label for an edge list
def replace_network(path, filename):
    '''
    open a file where eachline is split by '\t'.
    The file stors an edge list for a graph
    example:
        1\t2
        2\t3
        3\t5
    ------
    Parameters
    %path: the path for a file
    %filename: the name for a file
    ------
    Return
    %replace_edgelist:the replaced edge list,
    where the node label is consecutive 
    %total_nodes: the total number of nodes
    '''

    ##open a file, to test whether the file is exist
    try:
        file = open(path+'\\'+filename, 'r')
    except IOError, e:
        print "Sorry, you cannot open the file"
        return

    node_dict = {}##dictionary to store the label for nodes
    edge_list = []##the edge list
    total_node = 0##record the total number of nodes
    for eachline in file:
        element = eachline.strip().split('\t')
        if len(element)>1:
            if element[0] not in node_dict:
                node_dict[element[0]] = total_node
                total_node = total_node+1
            if element[1] not in node_dict:
                node_dict[element[1]] = total_node
                total_node = total_node+1
            edge_list.append(element)
        else:
            print "error to load an edge"
    file.close()

    ##replace the edge list
    replace_edgelist = []
    for edge in edge_list:
        replace_edgelist.append([node_dict[edge[0]],node_dict[edge[1]]])
    return replace_edgelist,total_node

##find all locations for an element in a list
def find_all_index(arr,item):
    '''
    find all locations for an element in a list

    ----
    Parameters：
    %arr: a one-dimension list
    %item: the element need to find

    ---
    Return：
    %list: an list which stores all locations for an element
    '''
    return [i for i,a in enumerate(arr) if a==item]

def get_node_score(edges, total_node):
    '''
    get the score for all nodes
    ----
    参数
    %edges：edge list data, where the node label is consecutive
    %total_node: the total number of nodes

    ----
    返回
    %node_weight: list to store the scroes for nodes 
    %initial_node_degree: list to store the scores for nodes
    '''
    ##an adjacent list representation for a graph
    adj_list = {} 

    ##list to store the degree, score and
    ##state for each node at certain time step
    node_degree = [0 for i in range(total_node)]
    node_weight = [0 for i in range(total_node)]
    is_deleted = [0 for i in range(total_node)]
    initial_node_degree = [0 for i in range(total_node)]

    ##list to store the score for each node at a time step
    ## Notice: the time step is the pre-time step for node_weight
    time_weight = [0 for i in range(total_node)]

    ##to label the node is deleted
    no_exist = 1e8
    for edge in edges:
        ##to create an adjacent edge list
        if edge[0] not in adj_list:
            adj_list[edge[0]] = []
        if edge[1] not in adj_list:
            adj_list[edge[1]] = []
        adj_list[edge[0]].append(edge[1])
        adj_list[edge[1]].append(edge[0])

        ##calculate the degree for each node
        node_degree[edge[0]]+=1
        node_degree[edge[1]]+=1
    
    initial_node_degree = node_degree[:] 
    while sum(is_deleted)<total_node:
        deleted_nodes= find_all_index(node_degree, min(node_degree))
       
        ##calculate the score for each node, where the deleted node is
        ##include the calculation process
        for deleted_node in deleted_nodes:
            for adj_node in adj_list[deleted_node]:
                if is_deleted[adj_node]==0:
                    node_weight[adj_node]+=(1+float(time_weight[deleted_node]) \
                                            / node_degree[deleted_node])
                   
        ##updata the time_weight
        time_weight = node_weight[:]

        ##update the degree for each node and
        ##ensure which node is needed to delted
        for deleted_node in deleted_nodes:
            for adj_node in adj_list[deleted_node]:
                node_degree[adj_node]-=1
                if node_degree[adj_node]==0:
                    node_degree[adj_node] = no_exist
                    is_deleted[adj_node] =1
            node_degree[deleted_node] = no_exist
            is_deleted[deleted_node] =1
            
    return node_weight, initial_node_degree


    
    
