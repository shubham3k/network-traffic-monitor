"""
Network Traffic Monitor - Utility Functions
Provides helper functions for application identification, network interface detection,
hostname resolution, and data formatting.
"""

import socket
import netifaces
from typing import Optional, Dict

# Port to application mapping (common services)
PORT_MAP: Dict[int, str] = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    465: "SMTPS",
    587: "SMTP",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}


def get_application_name(port: int, protocol: str = "TCP") -> str:
    """
    Map port number to application/service name.
    
    Args:
        port: Port number
        protocol: Protocol type (TCP/UDP)
    
    Returns:
        Application name or "Unknown"
    """
    if port in PORT_MAP:
        return PORT_MAP[port]
    
    # Additional heuristics
    if 6881 <= port <= 6889:
        return "BitTorrent"
    elif 49152 <= port <= 65535:
        return "Ephemeral"
    
    return f"Unknown:{port}"


def get_default_interface() -> Optional[str]:
    """
    Detect the primary network interface.
    
    Returns:
        Interface name (e.g., 'eth0', 'wlan0') or None
    """
    try:
        gateways = netifaces.gateways()
        default_gateway = gateways.get('default', {})
        
        if netifaces.AF_INET in default_gateway:
            return default_gateway[netifaces.AF_INET][1]
        
        # Fallback: return first non-loopback interface
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            if iface != 'lo' and not iface.startswith('docker'):
                return iface
                
    except Exception as e:
        print(f"Error detecting interface: {e}")
    
    return None


def resolve_hostname(ip: str) -> Optional[str]:
    """
    Attempt DNS reverse lookup for IP address.
    
    Args:
        ip: IP address string
    
    Returns:
        Hostname or None if lookup fails
    """
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.gaierror, OSError):
        return None


def format_bytes(bytes_val: int) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        bytes_val: Number of bytes
    
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 ** 2:
        return f"{bytes_val / 1024:.2f} KB"
    elif bytes_val < 1024 ** 3:
        return f"{bytes_val / (1024 ** 2):.2f} MB"
    else:
        return f"{bytes_val / (1024 ** 3):.2f} GB"


def format_bandwidth(bytes_per_sec: float) -> str:
    """
    Format bandwidth with appropriate units.
    
    Args:
        bytes_per_sec: Bytes per second
    
    Returns:
        Formatted string (e.g., "1.5 MB/s")
    """
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.2f} B/s"
    elif bytes_per_sec < 1024 ** 2:
        return f"{bytes_per_sec / 1024:.2f} KB/s"
    else:
        return f"{bytes_per_sec / (1024 ** 2):.2f} MB/s"


def get_protocol_name(proto_num: int) -> str:
    """
    Convert protocol number to name.
    
    Args:
        proto_num: IP protocol number
    
    Returns:
        Protocol name
    """
    protocol_map = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
    }
    return protocol_map.get(proto_num, f"Protocol-{proto_num}")
