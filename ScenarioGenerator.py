import copy
import random
import json
from pprint import pprint
class ScenarioGenerator:
    def __init__(self):
        self.all_first_conbinations = []

    # Recursive helper function to create the partition combinations.
    def genp(self, parts:list, empty, n, k, m, lastfilled):
        if m == n:
            # print("this shit is printing", parts, type(parts))
            self.all_first_conbinations.append(copy.deepcopy(parts))
            return
        if n - m == empty:
            start = k - empty
        else:
            start = 0
        for i in range(start, min(k, lastfilled + 2)):
            parts[i].append(m)
            if len(parts[i]) == 1:
                empty -= 1
            self.genp(parts, empty, n, k, m+1, max(i, lastfilled))
            parts[i].pop()
            if len(parts[i]) == 0:
                empty += 1

    # Main helper function to create all possible combinations with k number of partitions in total n elements.
    def setkparts(self, n, k):
        parts = [[] for _ in range(k)]
        cnts = [0]*k
        self.genp(parts, k, n, k, 0, -1)

    # Partition creation and filtering for step 1
    def step1_partitions(self, total_number_of_nodes, number_of_partition, number_of_nodes, number_of_twins):
        partitions = []
        for k in range(1, total_number_of_nodes):
            self.all_first_conbinations = []

            # Create partitions based on this source code and add it to list with differnt number of partitions.
            # https://stackoverflow.com/questions/64458592/recursively-finding-all-partitions-of-a-set-of-n-objects-into-k-non-empty-subset
            self.setkparts(total_number_of_nodes, k)
            for parts in self.all_first_conbinations:
                flag = False

                # Fileter partitions which have atleast one partition which can create TC or QC.
                for p in parts:
                    count = len(p)
                    for x in p:
                        if x + number_of_nodes in p:
                            count -= 1
                    if count >= 2 * number_of_twins + 1:
                        flag = True
                if flag:
                    partitions.append(parts)        
        return partitions

    # Partition and leader combinations for step 2
    def step2_partitions(self, partition_sets, number_of_twins, number_of_nodes, leaders_only_faulty):
        partition_with_leaders = []
        
        # Iterate over paritions
        for p in partition_sets:

            # Map partitions to all possible leaders.
            for l in range(0, number_of_twins):
                partition_with_leaders.append({"proposal_partition": p, "vote_partition": p, "timeout_partition": p, "leader":[l]})
            
            # Check for faulty leader only condition
            if not leaders_only_faulty:
                for l in range(number_of_twins, number_of_nodes):
                    partition_with_leaders.append({"proposal_partition": p, "vote_partition": p, "timeout_partition": p, "leader":[l]})
        return partition_with_leaders

    # Partition, leaders and rounds combinations for step 3
    def step3_partitions(self, number_of_configs_pruned, selection_type_for_configs_pruned, with_replacement, rounds, pruned_partition_with_leaders):
        configs = []
        # Creating millions of combinations just to select 10 to 15 for testing wasn't very efficient for normal execution.
        # Therefore iterate over the total required number of combinations and randomly generating possible combinations
        for _ in range(number_of_configs_pruned):
            leaders = []
            partitions = []

            # Check for the type of pruning
            if selection_type_for_configs_pruned == "RANDOM":

                # Select for pruning with or without replacement of round 
                if with_replacement:
                    for i in range(rounds):
                        leaders.append(pruned_partition_with_leaders[random.randint(0, len(pruned_partition_with_leaders)-1)]["leader"][0])
                        partitions.append(pruned_partition_with_leaders[random.randint(0, len(pruned_partition_with_leaders)-1)]["proposal_partition"])
                else:

                    # Set track to avoid replacememnt
                    already_included_cofig = set()
                    i = 0
                    while i < rounds:
                        itr = random.randint(0, len(pruned_partition_with_leaders))
                        if itr not in already_included_cofig:
                            partitions.append(pruned_partition_with_leaders[itr][0])
                            leaders.append(pruned_partition_with_leaders[itr][0])
                            i += 1
            else:
                # Use a fixed seed in random generation to get deterministic results
                for i in range(rounds):
                    random_deterministic = random.Random(42)
                    leaders.append(pruned_partition_with_leaders[random_deterministic.randint(0, len(pruned_partition_with_leaders)-1, seed=42)]["leader"][0])
                    partitions.append(pruned_partition_with_leaders[random_deterministic.randint(0, len(pruned_partition_with_leaders)-1, seed=42)]["proposal_partition"])

            scenario = {"partitions" : partitions, "leaders": leaders}
            # write scenario to file
            configs.append(scenario)
        pprint(configs)

        # Write all generated scenarios to json file
        with open("scenrios.json", 'w') as f:
            json_str = json.dumps(configs)
            f.write(json_str)

    def generate_scenario(self,
                          number_of_nodes,
                          number_of_twins,
                          rounds = 10,
                          number_of_partition=3,
                          leaders_only_faulty=False,
                          number_of_partitions_pruned=4,
                          selection_type_for_partitions="RANDOM",
                          number_of_partitions_leaders_pruned=4,
                          selection_type_for_partitions_leaders_pruned="RANDOM",
                          number_of_configs_pruned=4,
                          selection_type_for_configs_pruned="RANDOM",
                          with_replacement=True,
                          ):

        # Generate all possible partition sets based on the
        total_number_of_nodes = number_of_nodes + number_of_twins

        # Generate partitions based on step 1
        partitions = self.step1_partitions(total_number_of_nodes, number_of_partition, number_of_nodes, number_of_twins)
 
        # Pruning partitions after step 1
        partition_sets = []
        if selection_type_for_partitions == "RANDOM":
            partition_sets = [partitions[random.randint(0, len(partitions)-1)] for _ in range(number_of_partitions_pruned)]
        else:
            partition_sets = [partitions[i] for i in range(number_of_partitions_pruned)]


        # Generate partitions with leaders based on step 2
        partition_with_leaders = self.step2_partitions(partition_sets, number_of_twins, number_of_nodes, leaders_only_faulty)

        # Pruning partitions and leader combination after step 2
        pruned_partition_with_leaders = []
        if selection_type_for_partitions_leaders_pruned == "RANDOM":
            pruned_partition_with_leaders = [partition_with_leaders[random.randint(0, len(partition_with_leaders) - 1)] for _ in range(number_of_partitions_leaders_pruned)]
        else:
            pruned_partition_with_leaders = [partition_with_leaders[i] for i in range(number_of_partitions_leaders_pruned)]

        # Step 3 function call
        self.step3_partitions(number_of_configs_pruned, selection_type_for_configs_pruned, with_replacement, rounds, pruned_partition_with_leaders)

sg = ScenarioGenerator()
sg.generate_scenario(4, 1, 10) 