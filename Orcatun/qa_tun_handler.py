##
# @author Paul Schmidt
# @brief Reads packets from the TUN device, swaps the destination address
#        with the source address and writes them back to the TUN Device
# @details To perform this test external tools are needed to compare the
#          incoming and outgoing packets such as netcat.
#          With netcat, for instance, you can start two terminals, 
#          one with 'netcat -u 10.8.0.1 42 42' (A)
#          and the other one with 'netcat -lu 42' (B).
#          Then type messages in terminal A and compare them with the
#          receiving messages in terminal B.

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from tun_handler import TunHandler
import dpkt

class qa_tun_handler (gr_unittest.TestCase):

    def setUp (self):
        self.handler = TunHandler("orca")
        self.handler.set_ip_adresses("10.8.0.2", "10.8.0.1")
        print "Local IP address:        10.8.0.2"
        print "Destination IP address:  10.8.0.1"

    def tearDown (self):
        self.handler = None

    def test_001_t (self):
        print "Awaiting Input..."
        raw_packet = self.handler.read()
        
        # Swap IP addresses
        packet = dpkt.ip.IP(raw_packet)
        temp = packet.src
        packet.src = packet.dst
        packet.dst = temp
        
        self.handler.write(str(packet))


if __name__ == '__main__':
    gr_unittest.run(qa_tun_handler)
