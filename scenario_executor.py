
class NetworkPlayground(process):
    def setup(self, node_id_to_node, account_addr_to_node_ids, x, test_case_config):
        # self.current_round = 0
        # self.msgs_rcvd_in_current_round = 0
        # self.max_msgs_per_round = x  # some x for now
        # self.node_id_to_node = node_id_to_node
        # self.account_addr_to_node_ids = account_addr_to_node_ids

        self.test_case_config = test_case_config

    # def is_message_dropped(self, curr_round, src, dest):
    #     for partition in self.test_case_config[round]["partitions"]:

    # def find_possible_destination_process_ids(self, round, sender_process_id):
    #     possible_destination_process_ids = []
    #     for partition in self.test_case_config[round]["partitions"]:
    #         if sender_process_id in partition:
    #             possible_destination_process_ids = partition.copy()
    #     return possible_destination_process_ids

    # def forward_message(self, round, sender_process_id, msg_type="proposal|vote|timeout"):
    #     possible_destination_process_ids = self.find_possible_destination_process_ids(
    #         round, sender_process_id)
    #     # for j in possible_destination_process_ids:
    #     if msg_type == "vote":
    #         # TODO: get leader of next round
    #         # send to leader of next round if leader is in same partition as sender in this round

    #     else:

    def advance_round_if_needed(self):
        self.msgs_rcvd_in_current_round = self.msgs_rcvd_in_current_round + 1
        if self.num_msgs_per_round >= self.max_msgs_per_round:
            self.current_round = self.current_round + 1
            self.num_msgs_per_round = 0

    def get_node_process_id(self, node_id):
        process_id = self.node_number_to_credentials[node_id][0]
        return process_id

    def is_twin(self, process_id):
        return (process_id in self.twin_to_node)

    def infer_round_from_msg(self, msg, msg_type="proposal|vote|timeout"):
        if msg_type == "proposal":
            return msg.block.round
        elif msg_type == "vote":
            return msg.vote_info.round
        elif msg_type == "timeout":
            return msg.tmo_info.round

    def receive(msg, from_=p):
        advance_round_if_needed()
        msg_round = infer_round_from_msg(msg)

        # not sure if we should use self.current_round or msg_round for filtering criteria on msgs
        # according to Inferring rounds in paper, we should use msg_round

        if msg_round in self.test_case_config:
            # right now only checking if from and to belong in the same partition

            partitions_in_round = self.test_case_config[msg_round]

            # get node_id's of from and to nodes using self.account_addr_to_node_id's
            # or node_id's will be present in message?
            from_node_id = 1  # some value
            to_node_id = 3  # some value

            bool is_msg_tobe_dropped = False
            # check if these node_id's are in the same partition in that round
            for partition in partitions_in_round:
                if from_node_id in partition:
                    if to_node_id not in partition:
                        is_msg_tobe_dropped = True

            if not is_msg_tobe_dropped:
                to_node = self.node_id_to_node[to_node_id]
                send(msg, to=to_node)


class ScenarioExecutor:
    def __init__(self, number_of_nodes, number_of_twins):
        # {1 : (po1, pk1), 2: (p02,pk2) ...... n+f: p0...}
        self.node_number_to_credentials = {}

        self.validator_public_keys = {}
        self.validator_private_keys = {}
        self.node_to_twin = {}
        self.twin_to_node = {}

        self.validators = new(Validators, num=number_of_nodes)

        for v in range(1, number_of_nodes+1):
            public_key, private_key = generate_keys()
            self.validator_private_keys[v] = private_key
            self.node_number_to_credentials[v] = (
                self.validators[v-1], public_key)

        for idx, validator in enumerate(self.validators):
            # setup validators and send public key of all other validators, and private key of itself
            setup(validator, (self.validator_private_keys[idx+1],
                              self.node_number_to_credentials, (number_of_nodes-1)//3,))

        self.add_twins(number_of_twins)

        # create network playground as a process
        # setup network playground and pass to it:
        # scenario, all mapping_info for identifiers, process_ids ...

    def get_node_identifier(self, number):
        return self.identifiers_map[number]

    # def get_process_id_from_config_number(self, number):
    #     return self.identifier_to_process_id_map[number]

    # def create_process_identifier_to_process_id_map(self):
    #     for key in self.identifiers_map.keys():
    #         curr_identifier = self.identifiers_map[key]
    #         self.process_identifier_to_process_id_map[curr_identifier] = [
    #             self.validators[key-1]]
    #     return

    def add_twins(self, number_of_nodes, number_of_twins):
        self.twins = new(Validators, num=number_of_twins)

        for idx, twin in enumerate(self.twins):
            #         # setup validators and send public key of all other validators, and private key of itself
            setup(twin, (self.validator_private_keys[idx+1],
                         self.node_number_to_credentials, (number_of_nodes-1)//3,))

        for f in range(number_of_nodes+1, number_of_nodes + number_of_twins + 1):
            twin_process_id = self.twins[f-1-number_of_nodes]
            (node_process_id,
             node_public_key) = self.node_number_to_credentials[f-number_of_nodes]
            self.node_number_to_credentials[f] = (
                twin_process_id, node_public_key)
            self.node_to_twin[node_process_id] = twin_process_id
            self.twin_to_node[twin_process_id] = node_process_id

    #     for f in range(1, number_of_twins):
    #         curr_identifier = self.identifiers_map[f]
    #         self.process_identifier_to_process_id_map[curr_identifier].append(
    #             self.twins[f-1])
    #         self.identifier_to_process_id_map[f +
    #                                           number_of_nodes] = self.twins[f-1]


def execute_scenario(number_of_nodes, number_of_twins, scenario):
