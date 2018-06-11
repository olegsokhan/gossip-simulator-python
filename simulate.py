import random
import argparse


class Connection:

    connections = []

    def __init__(self, from_node, to_node, msg):
        self.from_node = from_node
        self.to_node = to_node
        self.msg = msg
        Connection.connections.append(self)


class Node:

    all_nodes = []
    use_my_algorithm = False

    def __init__(self, ip, port, max_connections):
        self.ip = ip
        self.port = port
        self.nodes_pool = []
        self.msgs = []
        self.max_connections = max_connections

    def get_identity(self):
        return '%s:%s' % (self.ip, self.port)

    def send_msg(self, other_node, msg):
        other_node.receive_msg(other_client=self, msg=msg)

    def receive_msg(self, other_client, msg):
        if msg is not None and len(msg) > 0:
            message_exists = False
            for i in range(0, len(self.msgs)):
                if self.msgs[i] == msg:
                    return
            if not message_exists:
                self.msgs.append(msg)
                self.gossip_to_random_nodes(msg, other_client.get_identity())

    def gossip_to_random_nodes(self, msg, connected_node_identity):
        while len(self.nodes_pool) < self.max_connections:
            node = Node.all_nodes[random.randint(0, len(Node.all_nodes) - 1)]
            node_identity = node.get_identity()
            if Node.use_my_algorithm and node_identity == connected_node_identity:
                pass
            elif node_identity != self.get_identity():
                add_node_to_pool = True
                for i in range(0, len(self.nodes_pool)):
                    node_from_pool_identity = self.nodes_pool[i].get_identity()
                    if node_from_pool_identity == node.get_identity():
                        add_node_to_pool = False
                        break
                if add_node_to_pool:
                    self.nodes_pool.append(node)
                    Connection(self, node, msg)
        self.nodes_pool = []


class Simulation:

    def __init__(self, nodes=20, connections_per_node=4, simulate_times=1000, use_my_algorithm=True):
        self.nodes = nodes
        self.connections_per_node = connections_per_node
        self.simulate_times = simulate_times
        self.use_my_algorithm = use_my_algorithm

        self.total_iterations = None
        self.all_nodes_received_the_packet_freq = None

    def run(self):

        Connection.connections = []
        Node.all_nodes = []
        Node.use_my_algorithm = False
        not_all_nodes_received_msg_times = 0
        received_times = 0

        for i in range(0, self.nodes):
            Node.all_nodes.append(
                Node("127.0.0.1", str(800+i), self.connections_per_node))
            if self.use_my_algorithm:
                Node.use_my_algorithm = True
        total_iterations = 0

        for run_times in range(0, self.simulate_times):
            if run_times > 0:
                for i in range(0, len(Node.all_nodes)):
                    Node.all_nodes[i].msgs = []
            Node.all_nodes[random.randint(0, len(Node.all_nodes) - 1)].gossip_to_random_nodes('test-packet', None)

            while len(Connection.connections) > 0:
                total_iterations += 1
                tmp_connections = list(Connection.connections)
                Connection.connections = []
                for i in range(0, len(tmp_connections)):
                    tmp_connections[i].from_node.send_msg(tmp_connections[i].to_node, tmp_connections[i].msg)
                tmp_connections = []

            for i in range(0, len(Node.all_nodes)):
                if len(Node.all_nodes[i].msgs) == 0:
                    not_all_nodes_received_msg_times += 1
                    break

        self.total_iterations = total_iterations
        self.all_nodes_received_the_packet_freq = 100 - (not_all_nodes_received_msg_times / self.simulate_times * 100)

        print("In "+str(self.all_nodes_received_the_packet_freq) +
              "% cases all nodes received the packet")
        print("Total iterations for algorithm: " + str(total_iterations))


parser = argparse.ArgumentParser(description='Run gossip simulation')
parser.add_argument('-n', dest='nodes', type=int,
                    help='Number of nodes to run the simulation with')
parser.add_argument('-i', dest='simulate_times', type=int,
                    help='Number of algorithm run times')
parser.add_argument('--your-algorithm', action='store_true', dest='use_my_algorithm',
                    help='Use my algorithm')

if __name__ == '__main__':
    args = parser.parse_args()
    Simulation(nodes=args.nodes, simulate_times=args.simulate_times, use_my_algorithm=args.use_my_algorithm).run()