from scapy.all import sniff

def show_packet(packet):
    print(packet.summary())

print("Capturing packets...")

sniff(
    prn=show_packet,
    store=False,
    iface=r"\Device\NPF_{2414B7B8-CBD7-455E-98E9-6DEC2184B25F}"
)