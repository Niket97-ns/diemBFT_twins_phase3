from typing_extensions import OrderedDict
import random


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
                          #   number_of_partitions_sets=None,
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

        partitions = self.step1_partitions(total_number_of_nodes)

        partition_sets = []
        if selection_type_for_partitions == "RANDOM":
            partition_sets = [partitions[random.randint(
                0, len(partitions))] for _ in range(number_of_partitions_pruned)]
        else:
            partition_sets = [partitions[i]
                              for i in range(number_of_partitions_pruned)]

        partition_with_leaders = []
        for p in partition_sets:
            for l in range(1, number_of_twins):
                partition_with_leaders.append(
                    {"partitions": p, "leaders": [l, l + number_of_nodes]})
            if not leaders_only_faulty:
                for l in range(number_of_twins, number_of_nodes):
                    partition_with_leaders.append(
                        {"partitions": p, "leaders": [l]})

        pruned_partition_with_leaders = []
        if selection_type_for_partitions_leaders_pruned == "RANDOM":
            pruned_partition_with_leaders = [partition_with_leaders[random.randint(0, len(
                partition_with_leaders))] for _ in range(number_of_partitions_leaders_pruned)]
        else:
            pruned_partition_with_leaders = [
                partition_with_leaders[i] for i in range(number_of_partitions_leaders_pruned)]

        configs = []
        for _ in range(number_of_configs_pruned):
            config = {}
            if selection_type_for_configs_pruned == "RANDOM":
                if with_replacement:
                    for i in range(rounds):
                        config[i] = pruned_partition_with_leaders[random.randint(
                            0, len(pruned_partition_with_leaders))]
                else:
                    already_included_cofig = set()
                    i = 0
                    while i < rounds:
                        itr = random.randint(
                            0, len(pruned_partition_with_leaders))
                        if itr not in already_included_cofig:
                            config[i] = pruned_partition_with_leaders[itr]
            else:
                for i in range(rounds):
                    config[i] = pruned_partition_with_leaders[i]

            # write to file "config"

            configs.append(config)

    def execute_scenario(self, file):
        pass

    '''
    Scenario generated in output file which will be of the form:
    {
        test_case_1: {
            num_of_nodes: 4,
            num_of_faulty: 1,
            nodes: [1,2,3,4,5],
            test_case_config: {
                ...
            }
        }
    }

    test_case_config is of the form:
    {
        1: {
            partitions = [[1,2,3], [4,5]],
            leader = [2]
        },
        2: {
            partitions = [[1,3], [2], [4,5]],
            leader = [1,5]
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
