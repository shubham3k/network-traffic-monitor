"""
Network Traffic Monitor - Data Processing Module
Aggregates packet data into meaningful metrics:
- Real-time bandwidth calculation
- Traffic by device (IP address)
- Traffic by application
- Protocol breakdown
- Active connection tracking
"""

import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from threading import Lock


class TrafficStats:
    """Manages time-series bandwidth data with rolling window."""
    
    def __init__(self, window_seconds: int = 300):
        """
        Initialize traffic statistics.
        
        Args:
            window_seconds: Time window to keep data (default 5 minutes)
        """
        self.window_seconds = window_seconds
        self.data_points = deque()  # (timestamp, upload_bytes, download_bytes)
        self.lock = Lock()
        
        # Current second aggregation
        self.current_second = int(time.time())
        self.current_upload = 0
        self.current_download = 0
        
        # Peak tracking
        self.peak_upload = 0
        self.peak_download = 0
    
    def add_packet(self, packet_data: Dict, is_outbound: bool):
        """
        Add packet to statistics.
        
        Args:
            packet_data: Parsed packet dictionary
            is_outbound: True if packet is outbound (upload), False if inbound
        """
        with self.lock:
            current_time = int(time.time())
            packet_size = packet_data['size']
            
            # If we've moved to a new second, save the previous second's data
            if current_time > self.current_second:
                self.data_points.append((
                    self.current_second,
                    self.current_upload,
                    self.current_download
                ))
                
                # Update peaks
                self.peak_upload = max(self.peak_upload, self.current_upload)
                self.peak_download = max(self.peak_download, self.current_download)
                
                # Reset for new second
                self.current_second = current_time
                self.current_upload = 0
                self.current_download = 0
                
                # Cleanup old data
                self._cleanup_old_data()
            
            # Add to current second
            if is_outbound:
                self.current_upload += packet_size
            else:
                self.current_download += packet_size
    
    def _cleanup_old_data(self):
        """Remove data points older than the time window."""
        cutoff_time = int(time.time()) - self.window_seconds
        
        while self.data_points and self.data_points[0][0] < cutoff_time:
            self.data_points.popleft()
    
    def get_bandwidth_history(self, seconds: int = 60) -> List[Dict]:
        """
        Get bandwidth history for charting.
        
        Args:
            seconds: Number of seconds to retrieve
        
        Returns:
            List of {timestamp, upload, download} dictionaries
        """
        with self.lock:
            # Include current second
            all_points = list(self.data_points) + [(
                self.current_second,
                self.current_upload,
                self.current_download
            )]
            
            # Get last N seconds
            recent = all_points[-seconds:] if len(all_points) > seconds else all_points
            
            return [
                {
                    'timestamp': ts,
                    'upload': upload,
                    'download': download
                }
                for ts, upload, download in recent
            ]
    
    def get_current_bandwidth(self) -> Tuple[int, int]:
        """
        Get current bandwidth (bytes/second).
        
        Returns:
            Tuple of (upload_bps, download_bps)
        """
        with self.lock:
            return (self.current_upload, self.current_download)
    
    def get_total_transferred(self) -> Tuple[int, int]:
        """
        Get total data transferred in the time window.
        
        Returns:
            Tuple of (total_upload, total_download)
        """
        with self.lock:
            total_upload = sum(up for _, up, _ in self.data_points) + self.current_upload
            total_download = sum(down for _, _, down in self.data_points) + self.current_download
            return (total_upload, total_download)
    
    def get_peak_bandwidth(self) -> Tuple[int, int]:
        """
        Get peak bandwidth observed.
        
        Returns:
            Tuple of (peak_upload, peak_download)
        """
        with self.lock:
            return (self.peak_upload, self.peak_download)


class DeviceTracker:
    """Tracks traffic by device (IP address)."""
    
    def __init__(self):
        self.devices = defaultdict(lambda: {'bytes': 0, 'packets': 0, 'hostname': None})
        self.lock = Lock()
    
    def add_packet(self, packet_data: Dict, is_outbound: bool):
        """Add packet to device statistics.
        
        Args:
            packet_data: Parsed packet dictionary
            is_outbound: True if packet is outbound (upload), False if inbound
        """
        with self.lock:
            src_ip = packet_data['src_ip']
            dst_ip = packet_data['dst_ip']
            size = packet_data['size']
            
            # Only track the remote device (not local machine)
            # If outbound, track destination; if inbound, track source
            remote_ip = dst_ip if is_outbound else src_ip
            
            self.devices[remote_ip]['bytes'] += size
            self.devices[remote_ip]['packets'] += 1
    
    def get_top_devices(self, limit: int = 10) -> List[Dict]:
        """
        Get top devices by data usage.
        
        Args:
            limit: Number of devices to return
        
        Returns:
            List of device dictionaries sorted by bytes
        """
        with self.lock:
            sorted_devices = sorted(
                self.devices.items(),
                key=lambda x: x[1]['bytes'],
                reverse=True
            )
            
            return [
                {
                    'ip': ip,
                    'bytes': data['bytes'],
                    'packets': data['packets'],
                    'hostname': data['hostname']
                }
                for ip, data in sorted_devices[:limit]
            ]


class ApplicationTracker:
    """Tracks traffic by application/service."""
    
    def __init__(self):
        self.applications = defaultdict(lambda: {'bytes': 0, 'packets': 0})
        self.lock = Lock()
    
    def add_packet(self, packet_data: Dict):
        """Add packet to application statistics."""
        with self.lock:
            app = packet_data['application']
            size = packet_data['size']
            
            self.applications[app]['bytes'] += size
            self.applications[app]['packets'] += 1
    
    def get_top_applications(self, limit: int = 10) -> List[Dict]:
        """
        Get top applications by data usage.
        
        Args:
            limit: Number of applications to return
        
        Returns:
            List of application dictionaries sorted by bytes
        """
        with self.lock:
            sorted_apps = sorted(
                self.applications.items(),
                key=lambda x: x[1]['bytes'],
                reverse=True
            )
            
            return [
                {
                    'name': name,
                    'bytes': data['bytes'],
                    'packets': data['packets']
                }
                for name, data in sorted_apps[:limit]
            ]


class ProtocolTracker:
    """Tracks traffic by protocol."""
    
    def __init__(self):
        self.protocols = defaultdict(lambda: {'bytes': 0, 'packets': 0})
        self.lock = Lock()
    
    def add_packet(self, packet_data: Dict):
        """Add packet to protocol statistics."""
        with self.lock:
            protocol = packet_data['protocol']
            size = packet_data['size']
            
            self.protocols[protocol]['bytes'] += size
            self.protocols[protocol]['packets'] += 1
    
    def get_breakdown(self) -> Dict:
        """
        Get protocol breakdown.
        
        Returns:
            Dictionary of protocol stats
        """
        with self.lock:
            return {
                protocol: {
                    'bytes': data['bytes'],
                    'packets': data['packets']
                }
                for protocol, data in self.protocols.items()
            }


class ConnectionTracker:
    """Tracks active network connections."""
    
    def __init__(self, timeout_seconds: int = 60):
        """
        Initialize connection tracker.
        
        Args:
            timeout_seconds: Time before considering connection inactive
        """
        self.timeout_seconds = timeout_seconds
        self.connections = {}  # (src_ip, dst_ip, dst_port, protocol) -> data
        self.lock = Lock()
    
    def add_packet(self, packet_data: Dict):
        """Add/update connection from packet."""
        with self.lock:
            if packet_data['dst_port'] is None:
                return  # Skip packets without port info
            
            key = (
                packet_data['src_ip'],
                packet_data['dst_ip'],
                packet_data['dst_port'],
                packet_data['protocol']
            )
            
            if key in self.connections:
                # Update existing connection
                self.connections[key]['bytes'] += packet_data['size']
                self.connections[key]['packets'] += 1
                self.connections[key]['last_seen'] = time.time()
            else:
                # New connection
                self.connections[key] = {
                    'bytes': packet_data['size'],
                    'packets': 1,
                    'first_seen': time.time(),
                    'last_seen': time.time(),
                    'application': packet_data['application']
                }
            
            # Cleanup old connections
            self._cleanup_old_connections()
    
    def _cleanup_old_connections(self):
        """Remove inactive connections."""
        current_time = time.time()
        cutoff_time = current_time - self.timeout_seconds
        
        keys_to_remove = [
            key for key, data in self.connections.items()
            if data['last_seen'] < cutoff_time
        ]
        
        for key in keys_to_remove:
            del self.connections[key]
    
    def get_active_connections(self, limit: int = 50) -> List[Dict]:
        """
        Get active connections.
        
        Args:
            limit: Maximum number of connections to return
        
        Returns:
            List of connection dictionaries
        """
        with self.lock:
            sorted_connections = sorted(
                self.connections.items(),
                key=lambda x: x[1]['last_seen'],
                reverse=True
            )
            
            return [
                {
                    'src_ip': key[0],
                    'dst_ip': key[1],
                    'dst_port': key[2],
                    'protocol': key[3],
                    'bytes': data['bytes'],
                    'packets': data['packets'],
                    'duration': int(data['last_seen'] - data['first_seen']),
                    'application': data['application']
                }
                for key, data in sorted_connections[:limit]
            ]
    
    def get_connection_count(self) -> int:
        """Get number of active connections."""
        with self.lock:
            return len(self.connections)


class DataProcessor:
    """Main data processor coordinating all trackers."""
    
    def __init__(self, local_ips: List[str] = None):
        """
        Initialize data processor.
        
        Args:
            local_ips: List of local IP addresses to determine traffic direction
        """
        self.local_ips = set(local_ips or [])
        
        self.traffic_stats = TrafficStats()
        self.device_tracker = DeviceTracker()
        self.app_tracker = ApplicationTracker()
        self.protocol_tracker = ProtocolTracker()
        self.connection_tracker = ConnectionTracker()
    
    def process_packet(self, packet_data: Dict):
        """
        Process a packet through all trackers.
        
        Args:
            packet_data: Parsed packet dictionary
        """
        # Determine if packet is outbound
        is_outbound = packet_data['src_ip'] in self.local_ips
        
        # Update all trackers
        self.traffic_stats.add_packet(packet_data, is_outbound)
        self.device_tracker.add_packet(packet_data, is_outbound)
        self.app_tracker.add_packet(packet_data)
        self.protocol_tracker.add_packet(packet_data)
        self.connection_tracker.add_packet(packet_data)
    
    def get_dashboard_data(self) -> Dict:
        """
        Get all data for dashboard update.
        
        Returns:
            Dictionary with all statistics
        """
        upload, download = self.traffic_stats.get_current_bandwidth()
        total_up, total_down = self.traffic_stats.get_total_transferred()
        peak_up, peak_down = self.traffic_stats.get_peak_bandwidth()
        
        return {
            'bandwidth': {
                'current': {
                    'upload': upload,
                    'download': download
                },
                'history': self.traffic_stats.get_bandwidth_history(60)
            },
            'stats': {
                'total_upload': total_up,
                'total_download': total_down,
                'peak_upload': peak_up,
                'peak_download': peak_down,
                'active_connections': self.connection_tracker.get_connection_count()
            },
            'devices': self.device_tracker.get_top_devices(10),
            'applications': self.app_tracker.get_top_applications(10),
            'protocols': self.protocol_tracker.get_breakdown(),
            'connections': self.connection_tracker.get_active_connections(50)
        }
