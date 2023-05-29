from scapy.all import *
from scapy.layers.inet import UDP, TCP, IP, ICMP
from scapy.layers.l2 import ARP


def analyze_packets(count: int = 100):
    def handle(packet: Packet):
        fields = packet.fields
        dst_mac = fields['dst']
        src_mac = fields['src']
        packet_type = fields['type']
        timestamp = packet.time

        def format(args:dict, protocol:str):
            others = ""
            for k, v in args.items():
                if k in ["dport", "sport"]:
                    v = str(v).ljust(15, ' ')
                elif k in ["src", "dst"]:
                    v = str(v).ljust(17, ' ')
                elif k in ["on"]:
                    v = str(v).ljust(6, ' ')
                others += f" | {k}: {v}"
            print(f"{protocol.ljust(5, ' ')} [{str(timestamp).ljust(18, ' ')}]-> dst: {dst_mac} | src: {src_mac}{others}")

        if packet.haslayer(IP):
            ip_packet: IP = packet[IP]
            src = ip_packet.src
            dst = ip_packet.dst
            proto = ip_packet.proto
            interface = ip_packet.sniffed_on
            format({"on": interface, "src": src, "dst": dst}, "IP")
        if packet.haslayer(TCP):
            tcp_packet: TCP = packet[TCP]
            sport = tcp_packet.sport
            dport = tcp_packet.dport
            interface = tcp_packet.sniffed_on
            format({"on": interface, "sport": sport, "dport": dport}, "TCP")
        if packet.haslayer(UDP):
            udp_packet: TCP = packet[UDP]
            sport = udp_packet.sport
            dport = udp_packet.dport
            interface = udp_packet.sniffed_on
            format({"on": interface, "sport": sport, "dport": dport}, "UDP")
        if packet.haslayer(ICMP):
            icmp_packet: ICMP = packet[ICMP]
            load = icmp_packet.load
            interface = icmp_packet.sniffed_on

            format({"on": interface}, "ICMP")

    packets = sniff(count=count, prn=handle)
    # for packet in packets:
    #     if IP in packet:
    #         src_ip = packet[IP].src
    #         dst_ip = packet[IP].dst
    #         protocol = packet[IP].proto
    #         if protocol == 6 and TCP in packet:
    #             src_port = packet[TCP].sport
    #             dst_port = packet[TCP].dport
    #             print('TCP: {}:{} -> {}:{}'.format(src_ip, src_port, dst_ip, dst_port))
    #         elif protocol == 17 and UDP in packet:
    #             src_port = packet[UDP].sport
    #             dst_port = packet[UDP].dport
    #             print('UDP: {}:{} -> {}:{}'.format(src_ip, src_port, dst_ip, dst_port))
    #         elif protocol == 1 and ICMP in packet:
    #             print('ICMP: {} -> {}'.format(src_ip, dst_ip))