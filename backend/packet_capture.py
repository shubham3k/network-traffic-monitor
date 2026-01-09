"""
Network Traffic Monitor - Packet Capture Module
Captures and parses network packets using Scapy.
Extracts metadata: IPs, ports, protocols, packet sizes, timestamps.
"""

import threading
import time
from collections import deque
from datetime import datetime
from typing import Dict, Optional, Callable
from scapy.all import sniff, IP, TCP, UDP, ICMP
from utils import get_application_name, get_protocol_name


class PacketCapture:
    """Handles packet capture and parsing using Scapy."""
    
    def __init__(self, interface: Optional[str] = None, callback: Optional[Callable] = None):
        """
        Initialize packet capture.
        
        Args:
            interface: Network interface to capture on (None = default)
            callback: Function to call with parsed packet data
        """
        self.interface = interface
        self.callback = callback
        self.running = False
        self.capture_thread = None
        self.packet_buffer = deque(maxlen=1000)  # Circular buffer
        
    def start(self):
        """Start packet capture in a background thread."""
        if self.running:
            print("Packet capture already running")
            return
        
        self.running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        print(f"Packet capture started on interface: {self.interface or 'default'}")
    
    def stop(self):
        """Stop packet capture."""
        self.running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2)
        print("Packet capture stopped")
    
    def _capture_loop(self):
        """Main capture loop - runs in background thread."""
        try:
            # Capture only IP packets (TCP, UDP, ICMP)
            sniff(
                iface=self.interface,
                prn=self._packet_callback,
                store=False,
                stop_filter=lambda _: not self.running,
                filter="ip"  # BPF filter for IP packets only
            )
        except PermissionError:
            print("ERROR: Packet capture requires root/administrator privileges!")
            print("Please run with: sudo python3 server.py")
            self.running = False
        except Exception as e:
            print(f"Packet capture error: {e}")
            self.running = False
    
    def _packet_callback(self, packet):
        """
        Process each captured packet.
        
        Args:
            packet: Scapy packet object
        """
        try:
            parsed = self.parse_packet(packet)
            if parsed:
                self.packet_buffer.append(parsed)
                
                # Call external callback if provided
                if self.callback:
                    self.callback(parsed)
                    
        except Exception as e:
            # Silently ignore malformed packets
            pass
    
    def parse_packet(self, packet) -> Optional[Dict]:
        """
        Extract metadata from packet.
        
        Args:
            packet: Scapy packet object
        
        Returns:
            Dictionary with packet metadata or None
        """
        if not packet.haslayer(IP):
            return None
        
        ip_layer = packet[IP]
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'src_ip': ip_layer.src,
            'dst_ip': ip_layer.dst,
            'protocol': get_protocol_name(ip_layer.proto),
            'protocol_num': ip_layer.proto,
            'size': len(packet),
            'src_port': None,
            'dst_port': None,
            'application': 'Unknown'
        }
        
        # Extract port information and identify application
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            data['src_port'] = tcp_layer.sport
            data['dst_port'] = tcp_layer.dport
            data['application'] = get_application_name(tcp_layer.dport, 'TCP')
            
        elif packet.haslayer(UDP):
            udp_layer = packet[UDP]
            data['src_port'] = udp_layer.sport
            data['dst_port'] = udp_layer.dport
            data['application'] = get_application_name(udp_layer.dport, 'UDP')
            
        elif packet.haslayer(ICMP):
            data['application'] = 'ICMP'
        
        return data
    
    def get_recent_packets(self, count: int = 100) -> list:
        """
        Get most recent packets from buffer.
        
        Args:
            count: Number of packets to retrieve
        
        Returns:
            List of packet dictionaries
        """
        return list(self.packet_buffer)[-count:]


# Test function for standalone execution
if __name__ == "__main__":
    def print_packet(packet_data):
        """Print packet info to console."""
        print(f"{packet_data['timestamp']}: {packet_data['src_ip']}:{packet_data['src_port']} -> "
              f"{packet_data['dst_ip']}:{packet_data['dst_port']} | "
              f"{packet_data['protocol']} | {packet_data['application']} | {packet_data['size']} bytes")
    
    print("Starting packet capture test...")
    print("Press Ctrl+C to stop\n")
    
    capture = PacketCapture(callback=print_packet)
    capture.start()
    
    try:
        while capture.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        capture.stop()
