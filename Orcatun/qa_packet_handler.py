#!/usr/bin/python2.7
import unittest
import socket
import dpkt
from packet_handler import PacketHandler
from ot import OT

class qa_packet_handler(unittest.TestCase):

    def test_ot_to_ip(self):
        # Buffer of valid OT Packet (id=42,len=26,data='foobar',src='10.8.0.2',dst='10.8.0.1',df=1)
        ot_packet_buffer = "\x00\x2a\x40\x00\x00\x66\x6f\x6f\x62\x61\x72"

        # IP addresses used for IP packet creation
        ip_src = '10.8.0.2'
        ip_dst = '10.8.0.1'

        # Create an IP packet from the previously defined OT packet buffer and adresses
        ip_packet = PacketHandler.to_ip(ot_packet_buffer, ip_src, ip_dst)

        self.assertEqual(ip_packet.id, 42)
        self.assertEqual(ip_packet.len, 26)
        self.assertEqual(ip_packet.data, 'foobar')

        # Convert adresses to binary representation for comparsion
        expected_ip_src = socket.inet_aton(ip_src)
        expected_ip_dst = socket.inet_aton(ip_dst)

        self.assertEqual(ip_packet.src, expected_ip_src)
        self.assertEqual(ip_packet.dst, expected_ip_dst)

        self.assertEqual(ip_packet.data, 'foobar')
        self.assertEqual(ip_packet.df, 1)

    def test_ip_to_ot(self):
        # Create valid IP packet buffer
        ip_packet = dpkt.ip.IP(id=12, data='barfoo', p=48)
        ip_packet_buffer = str(ip_packet)

        # Create an OT packet from the previously defined IT packet buffer
        ot_packet = PacketHandler.to_ot(ip_packet_buffer)

        self.assertEqual(ip_packet.data, ot_packet.data)
        self.assertEqual(ip_packet.id, ot_packet.id)
        self.assertEqual(ip_packet.p, ot_packet.p)

    def test_show_ip(self):

        # Create intern binary representation of the IP addresses used for IP packet creation
        ip_src = socket.inet_aton('10.8.0.2')
        ip_dst = socket.inet_aton('10.8.0.1')

        # Create valid IP packet using the addresses previously defined
        ip_packet = dpkt.ip.IP(data='hello',
                               src=ip_src,
                               dst=ip_dst)

        # Create a String containing information about the IP packet
        ip_packet_information = PacketHandler.show(ip_packet)

        expected_result = 'IP: 10.8.0.2 -> 10.8.0.1	(len=25, ttl=64, DF=0, MF=0, offset=0, p=0, id=0)'
        self.assertEqual(ip_packet_information, expected_result)

    def test_show_ot(self):
        # Create OT packet with parsed values of IP packet
        ot_packet = OT(id=7,
                       p=20,
                       off=12,
                       data='abc')

        expected_result = PacketHandler.show(ot_packet)
        ot_packet_information = 'OT: (len=8, DF=0, MF=0, offset=12, p=20, id=7)'

        self.assertEqual(ot_packet_information, expected_result)

if __name__ == '__main__':
    unittest.main()
