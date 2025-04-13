from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, tcp, udp, icmp
from datetime import datetime
import csv
import os

class PacketSniffer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(PacketSniffer, self).__init__(*args, **kwargs)
        self.csv_file = "/home/ubuntu/sdn-lab/logs/pacotes.csv"
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
        with open(self.csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "src_mac", "dst_mac", "ip_src", "ip_dst",
                "proto", "icmp_type", "tcp_sport", "tcp_dport", "udp_sport", "udp_dport"
            ])

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=0, match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        pkt = packet.Packet(msg.data)

        eth = pkt.get_protocol(ethernet.ethernet)
        ip = pkt.get_protocol(ipv4.ipv4)
        icmp_pkt = pkt.get_protocol(icmp.icmp)
        tcp_pkt = pkt.get_protocol(tcp.tcp)
        udp_pkt = pkt.get_protocol(udp.udp)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        row = [
            timestamp,
            eth.src if eth else "",
            eth.dst if eth else "",
            ip.src if ip else "",
            ip.dst if ip else "",
            ip.proto if ip else "",
            icmp_pkt.type if icmp_pkt else "",
            tcp_pkt.src_port if tcp_pkt else "",
            tcp_pkt.dst_port if tcp_pkt else "",
            udp_pkt.src_port if udp_pkt else "",
            udp_pkt.dst_port if udp_pkt else "",
        ]

        with open(self.csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        self.logger.info("[PACKET] " + ", ".join(map(str, row)))