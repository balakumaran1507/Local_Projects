from scapy.all import sniff

# Define a callback function to process each captured packet
def packet_callback(packet):
    print(f"Packet captured: {packet.summary()}")

# Start sniffing packets
def start_sniffer(interface=None):
    print(f"Starting packet sniffer on interface: {interface if interface else 'all interfaces'}")
    # Use 'iface' to specify a network interface, e.g., 'eth0' or 'wlan0'
    # 'prn' specifies the callback function to be called for each packet
    # 'count' specifies how many packets to capture (None means capture indefinitely)
    sniff(iface=interface, prn=packet_callback, count=0)

if __name__ == "__main__":
    # You can specify a network interface if needed, e.g., 'eth0'
    start_sniffer()
