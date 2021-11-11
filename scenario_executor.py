
'''
scenario is now of the form:
{
    partitions = [ [[1,2,3], [4,5]], [[1,3], [2], [4,5]] ],
    leader = [ [2], [1,5] ]
}
'''


class NetworkPlayground(process):

    '''
    number_of_nodes ,
    number_of_twins, 
    scenario, 
    scenario_number_mapping,
	node_to_twin, 
    twin_to_node
    '''
    def setup(self, number_of_nodes, number_of_twins, scenario, scenario_number_mapping, node_to_twin, twin_to_node):
        self.scenario = scenario
        self.rounds = len(scenario["partitions"])
        self.node_to_twin = node_to_twin
        self.twin_to_node = twin_to_node
        self.scenario_number_mapping = scenario_number_mapping
        self.number_of_nodes = number_of_nodes
        self.number_of_twins = number_of_twins

    def is_twin(self, process_id):
        return (process_id in self.twin_to_node)

    def infer_round_from_msg(self, msg, msg_type):
        if msg_type == "proposal":
            return msg.block.round
        elif msg_type == "vote":
            return msg.vote_info.round
        elif msg_type == "timeout":
            return msg.tmo_info.round

    def send_to_nodes(node_nums_to_send, msg, sender):
        node_pids = []
        for node_num in node_nums_to_send:
            # node_pid = self.node_num_to_pid[node_num]
            node_pids.append(self.scenario_number_mapping[node_num])
        send(msg, to=node_pids, from_=sender)

    def get_partition(partitions_in_round, p):
        for partition in partitions_in_round:
            if p in partition:
                return partition.copy()
        return []

    def get_destination_from_msg(msg):
        return msg.destination_node

    def get_twin(destination_node_num):
        if destination_node_num not in self.node_to_twin:
            return None
        return self.node_to_twin[destination_node_num]

    def get_msg_type(msg):
        if msg is of type 'proposal':
            return "proposal"
        elif msg is of type 'timeout':
            return "timeout"
        elif msg is of type 'vote':
            return "vote"

    def get_partitions_for_type(type_of_msg):
        if type_of_msg == "proposal":
            return self.scenario["proposal_partitions"]
        elif type_of_msg == "vote":
            return self.scenario["vote_partitions"]
        elif type_of_msg == "timeout":
            return self.scenario["timeout_partitions"]



    def replace_with_twin_if_needed(p):
        # Replace twin if needed
        actual_sender_node = p
        if is_twin(p):
            # means it is a twin
            # replace sender with actual node
            actual_sender_node = self.twin_to_node[p]
        return actual_sender_node

    def receive(msg, from_=p):

        msg_type = self.get_msg_type(msg)
        msg_round = self.infer_round_from_msg(msg, msg_type)

        if msg_round >= self.rounds + 3:
            # stop
            return

        if msg_round > self.rounds:
            # no partitions for this
            # no dropping messages based on partitions
            # still handle broadcast
            pass

        all_partitions = self.get_partitions_for_type(msg_type)[msg_round]

        if msg_type == 'proposal' or msg_type == 'timeout':

            # broadcast
            list_of_validators_to_send_to = self.get_partition(all_partitions, p)

            actual_sender_node = self.replace_with_twin_if_needed(p)

            self.send_to_nodes(list_of_validators_to_send_to,
                               msg, actual_sender_node)

        elif msg_type == 'vote':

            # unicast
            node_nums_in_partition = self.get_partition(all_partitions, p)
            destination_node_num = self.get_destination_from_msg(msg)

            destination_nodes = []
            if destination_node_num in node_nums_in_partition:
                # only then send msg to destination
                destination_nodes.append(destination_node_num)

            if self.get_twin(destination_node_num) and self.get_twin(destination_node_num) in node_nums_in_partition:
                # Replace twin if needed
                destination_nodes.append(self.get_twin(destination_node_num))

            actual_sender_node = self.replace_with_twin_if_needed(p)

            self.send_to_nodes(destination_nodes, msg, actual_sender_node)


class ScenarioExecutor(process):
    def __init__(self, number_of_nodes, number_of_twins):
        # {1 : (po1, pk1), 2: (p02,pk2) ...... n+f: p0...}
        self.node_credentials = {}

        self.validator_public_keys = {}
        self.validator_private_keys = {}
        self.node_to_twin = {}
        self.twin_to_node = {}

        self.validators = new(Validators, num=number_of_nodes)

        for v in range(1, number_of_nodes+1):
            public_key, private_key = generate_keys()
            self.validator_private_keys[v] = private_key
            self.node_credentials[v] = (
                self.validators[v-1], public_key)

        for idx, validator in enumerate(self.validators):
            personal_id = idx + 1
            # setup validators and send public key of all other validators, and private key of itself
            setup(validator, (personal_id, self.validator_private_keys[idx+1],
                              self.node_credentials, (number_of_nodes-1)//3,))

        self.add_twins(number_of_twins)

        # create network playground as a process
        # TODO: Create network playground
        # setup network playground and pass to it:
        # scenario, all mapping_info for identifiers, process_ids ...

    def get_node_identifier(self, number):
        return self.identifiers_map[number]

    def add_twins(self, number_of_nodes, number_of_twins):
        self.twins = new(Validators, num=number_of_twins)

        for idx, twin in enumerate(self.twins):
            personal_id = idx+1
            #         # setup validators and send public key of all other validators, and private key of itself
            setup(twin, (personal_id, self.validator_private_keys[idx+1],
                         self.node_credentials, (number_of_nodes-1)//3,))

        for f in range(number_of_nodes+1, number_of_nodes + number_of_twins + 1):
            twin_process_id = self.twins[f-1-number_of_nodes]
            (node_process_id,
             node_public_key) = self.node_credentials[f-number_of_nodes]
            self.node_credentials[f] = (
                twin_process_id, node_public_key)
            self.node_to_twin[node_process_id] = twin_process_id
            self.twin_to_node[twin_process_id] = node_process_id

    def execute_scenario(number_of_nodes, number_of_twins, scenario):
        pass
