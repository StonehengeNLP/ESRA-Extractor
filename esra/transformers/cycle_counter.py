class Cycle_counter:
    """
        Cycle_counter class for ESRA validator module.

        To get the number of cycle in graph use .count_cycle(data).       
    """

    def __init__(self):
        # init the list of relation_types that this module going to check
        self.relation_types = ['PART-OF','EVALUATE-FOR','USED-FOR','FEATURE-OF','HYPONYM-OF','REFER-TO']



    def __get_adjancencyLists(self,data):
        """
            Retrieve adjancency_list of graph of all relation types.

            params:

                - data: data object.

            return:
                
                - adjancency_lists: adjancency_list of all relation types.
        """
        entities = data['entities']
        relations = data['relations']
    
        adjancency_lists = [[[] for i in range(len(entities))] for j in range(len(self.relation_types))]
    
        for (rt_index,rt) in enumerate(self.relation_types):
            for current_rt,s_index,e_index in relations:
                if current_rt == rt:
                    adjancency_lists[rt_index][s_index].append(e_index)
        return adjancency_lists



    def __isCyclicUtil(self,node_idx,visited,recStack,adjancency_list):
        """
            check isCyclic recursively.

            params:

                - node_idx: index of focusing node.

                - visited: list of boolean that keep visit status
                  of each node.

                - recStack: list of boolean that keep recursive stack
                  status of each node.
                
                - adjancency_list: adjancency_list of focusing relation type.

            return:
                
                - adjancency_lists: adjancency_list of all relation_types.
        """
        visited[node_idx] = True
        recStack[node_idx]= True
        
        for neighbour_idx in adjancency_list[node_idx]:
            if visited[neighbour_idx] == False:
                if self.__isCyclicUtil(neighbour_idx,visited,recStack,adjancency_list) == True:
                    return True
            elif recStack[neighbour_idx] == True:
                return True
        recStack[node_idx] = False
        return False



    def count_cycle(self,data):
        """
            Count the number of cycle in the graph including self-loop.
            Cycle in this context mean the cycles of directed graph 
            which have same relation type.

            params:

                - data: {entities:[entity_type,entity_name],
                         relations:[relation_type,from_idx,to_idx]}
            
            return:

                - n_cycle: the number of cycle in the graph.

        """
        adjancency_lists = self.__get_adjancencyLists(data)
        n_cycle = 0

        for adjancency_list in adjancency_lists:
            visited = [False] * len(adjancency_list)
            recStack = [False] * len(adjancency_list)
            for node_idx in range(len(adjancency_list)):
                if visited[node_idx] == False:
                    if self.__isCyclicUtil(node_idx,visited,recStack,adjancency_list) == True:
                        n_cycle += 1
        return n_cycle



# # for testing this module
# data = {'entities': [['OtherScientificTerm', 'black-box nature'],
#               ['Method', 'deep learning models'], 
#               ['Generic', 'methods'],
#               ['Generic', 'models'],
#               ['Method', 'model-agnostic and model-specific explanation methods'],
#               ['Method', 'CNNs'],
#               ['Task', 'text classification'],
#               ['Task', 'human-grounded evaluations'],
#               ['OtherScientificTerm', 'model behavior'],
#               ['Method', 'model predictions'],
#               ['Method', 'explanation methods'],
#               ['Generic', 'methods']],
#        'relations':[['USED-FOR', 1, 2],
#               ['USED-FOR', 2, 3],
#               ['USED-FOR', 7, 7]]
#         }
# cycleCounter = Cycle_counter()
# print(cycleCounter.count_cycle(data))
