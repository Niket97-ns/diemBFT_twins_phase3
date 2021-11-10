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

        #

        rounds = 10  # number of rounds
        # vector of vectors for partitions from 1-n rounds
        partitions = [[(A, B), (C, D)], [(A, D), (B, C)]]
        leaders = []  # vector of leaders for round 1-n
        scenario = {}
        for round in range(1, rounds+1):
            scenario[round] = {
                "partitions": partitions[round-1],
                "leader": leaders[round-1]
            }

        pass

    def execute_scenario(self, file):
        pass
