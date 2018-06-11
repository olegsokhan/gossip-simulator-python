import unittest
from simulate import Simulation


class TestGossipSimulation(unittest.TestCase):

    def test_with_and_with_out_my_algorithm(self):
        s = Simulation(nodes=20, simulate_times=1000, use_my_algorithm=False)
        s.run()
        print("With out my algorithm: "+str(s.all_nodes_received_the_packet_freq))

        s = Simulation(nodes=20, simulate_times=1000, use_my_algorithm=True)
        s.run()
        print("With my algorithm: " + str(s.all_nodes_received_the_packet_freq))


if __name__ == '__main__':
    unittest.main()