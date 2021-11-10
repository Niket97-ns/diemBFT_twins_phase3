from typing_extensions import OrderedDict

class TwinHandler:

    def __init_(self, number_of_nodes):
        self.validators = {}

        pass

    def generate_nodes(self, number_of_nodes):
        for i in range(number_of_nodes):
            self.validators[self.get_node_name(i)] = []

    def get_node_name(self, i):
        return chr(ord('A') + i)

    

    def step1_partitions(total_number_of_nodes):
        partitions = []
        for i in range(1, total_number_of_nodes):
            # Create partitions based on this source code and add it to list with differnt number of partitions.
            # https://stackoverflow.com/questions/64458592/recursively-finding-all-partitions-of-a-set-of-n-objects-into-k-non-empty-subset
            pass
        return partitions

    def generate_scenario(self,
                          number_of_nodes,
                          number_of_twins,
                          rounds,
                          number_of_partitions_sets=None,
                          leaders_only_faulty=False,
                          number_of_partitions_pruned=None,
                          selection_type_for_partitions="RANDOM",
                          number_of_partitions_leaders_pruned=None,
                          selection_type_for_partitions_leaders_pruned="RANDOM",
                          number_of_configs_pruned=None,
                          selection_type_for_configs_pruned="RANDOM",
                          with_replacement=False,
                          ):

        # Generate all possible partition sets based on the
        total_number_of_nodes = number_of_nodes + number_of_twins

        partitions = step1_partitions()

        partition_with_leaders = []
        for x in range(len(partitions)):
            if leaders_only_faulty:
                for l in range(1, number_of_twins):
                    
                    pass
            else:
                for l in total_number_of_nodes:
                    pass


    def execute_scenario(self, file):
        pass
