from scapy.all import sniff

def show_packet(packet):
    print(packet.summary())

print("Testing packet capture...")

sniff(prn=show_packet, store=False)