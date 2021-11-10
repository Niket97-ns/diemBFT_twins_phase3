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


    '''
    test_case_config is of the form:

    {
        1: {
            partitions = [[1,2,3], [4,5]],
            leaders = [2]
        },
        2: {
            partitions = [[1,3], [2], [4,5]],
            leaders = [1,5]
        }
    }
    '''
    def intrapartition_msg_drops(test_case_config, node_id, round_from, round_to):
        for i in range(round_from, round_to + 1):
            new_partitions = []
            for partition in test_case_config[i]["partitions"]:
                if node_id in partition:
                    # create separate partition for node_id
                    # create copy of partition
                    new_partition = partition.copy()
                    # remove node_id from partition
                    new_partition.remove(node_id)
                    new_partitions.append(new_partition)
                    # create separate list for node_id
                    node_id_partition = []
                    node_id_partition.append(node_id)
                    new_partitions.append(node_id_partition)
                else:
                    new_partitions.append(partition)

            test_case_config[i]["partitions"] = new_partitions
        return test_case_config

