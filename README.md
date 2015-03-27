# Algorthim-to-calculate-node-importance
-------------------------------------------------------------------
calc_node_importance calculated the node importance for a network 
with a decomposition process

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
create a mian function to include such code:

    #set the path and filename to read a file
    path = r'C:\Users\qyh\Desktop\code for Nimp_python'
    filename = 'ErodeNetwork.txt'

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
