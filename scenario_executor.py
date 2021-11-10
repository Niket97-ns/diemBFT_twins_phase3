
class NetworkPlayground(process):
    def setup(self, node_id_to_node, account_addr_to_node_ids, x, test_case_config):
        self.current_round = 0
        self.msgs_rcvd_in_current_round = 0
        self.max_msgs_per_round = x # some x for now
        self.node_id_to_node = node_id_to_node
        self.account_addr_to_node_ids = account_addr_to_node_ids

        self.test_case_config = test_case_config
    
    def advance_round_if_needed():
        self.msgs_rcvd_in_current_round = self.msgs_rcvd_in_current_round + 1
        if self.num_msgs_per_round >= self.max_msgs_per_round:
            self.current_round = self.current_round + 1
            self.num_msgs_per_round = 0

    def infer_round_from_msg(msg):
        # get round number from msg
        # round_inferred_from_msg = msg.block.round?
        return 0

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
            from_node_id = 1 # some value
            to_node_id = 3 # some value

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
    def __init__(self):
        # read config from file ? or receive config for one testcase from another function that reads all configs from file and creates scenario executor instance for each testcase
        # generate nodes/procs for each node for that testcase
        # make leaders?? - network playground will have to create leaders?
        # create mapping node_id to actual node i.e. node_id_to_node
        # node_id's are [1,2,3,4,5] where 5 is 1's twin
        # create mapping account address to node_id i.e. account_addr_to_node_ids
        # this is because account address for 1 and 5 is same
        # pass all these values to network playground
        pass
    
    

