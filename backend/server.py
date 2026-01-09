"""
Network Traffic Monitor - Flask Server
Web server with WebSocket support for real-time traffic updates.
Coordinates packet capture and data processing.
"""

import socket
import time
from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading

from packet_capture import PacketCapture
from data_processor import DataProcessor
from utils import get_default_interface


# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/dist')
app.config['SECRET_KEY'] = 'network-traffic-monitor-secret'
CORS(app)

# Initialize SocketIO with threading mode
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=False, engineio_logger=False)

# Global instances
packet_capture = None
data_processor = None
broadcast_thread = None
running = False


def get_local_ips():
    """Get local IP addresses to determine traffic direction."""
    local_ips = ['127.0.0.1', '::1', '127.0.1.1']
    
    try:
        import netifaces
        
        # Get all network interfaces
        for interface in netifaces.interfaces():
            try:
                # Get IPv4 addresses for this interface
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        if ip and ip not in local_ips:
                            local_ips.append(ip)
            except Exception:
                continue
        
        # Also try hostname resolution as fallback
        hostname = socket.gethostname()
        ip_list = socket.gethostbyname_ex(hostname)[2]
        for ip in ip_list:
            if ip not in local_ips:
                local_ips.append(ip)
        
    except Exception as e:
        print(f"Error getting local IPs: {e}")
    
    return local_ips


def packet_callback(packet_data):
    """Callback for each captured packet."""
    global data_processor
    if data_processor:
        data_processor.process_packet(packet_data)


def broadcast_updates():
    """Background thread to broadcast traffic updates via WebSocket."""
    global running, data_processor
    
    print("Starting WebSocket broadcast thread...")
    
    while running:
        try:
            if data_processor:
                # Get current dashboard data
                dashboard_data = data_processor.get_dashboard_data()
                
                # Broadcast to all connected clients
                socketio.emit('traffic_update', dashboard_data, namespace='/')
            
            # Update every 1 second
            socketio.sleep(1)
            
        except Exception as e:
            print(f"Broadcast error: {e}")
            socketio.sleep(1)


def start_monitoring():
    """Start packet capture and data processing."""
    global packet_capture, data_processor, broadcast_thread, running
    
    if running:
        print("Monitoring already running")
        return
    
    print("Starting network traffic monitoring...")
    
    # Get local IPs for traffic direction detection
    local_ips = get_local_ips()
    print(f"Local IPs: {local_ips}")
    
    # Initialize data processor
    data_processor = DataProcessor(local_ips=local_ips)
    
    # Get network interface
    interface = get_default_interface()
    print(f"Monitoring interface: {interface or 'default'}")
    
    # Initialize and start packet capture
    packet_capture = PacketCapture(interface=interface, callback=packet_callback)
    packet_capture.start()
    
    # Start broadcast thread
    running = True
    broadcast_thread = threading.Thread(target=broadcast_updates, daemon=True)
    broadcast_thread.start()
    
    print("Monitoring started successfully!")


def stop_monitoring():
    """Stop packet capture and data processing."""
    global packet_capture, running
    
    print("Stopping network traffic monitoring...")
    
    running = False
    
    if packet_capture:
        packet_capture.stop()
    
    print("Monitoring stopped")


# REST API Endpoints

@app.route('/')
def index():
    """Serve the React frontend."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/stats')
def get_stats():
    """Get current traffic statistics."""
    if data_processor:
        data = data_processor.get_dashboard_data()
        return jsonify(data)
    return jsonify({'error': 'Monitoring not started'}), 503


@app.route('/api/devices')
def get_devices():
    """Get top devices by traffic."""
    if data_processor:
        devices = data_processor.device_tracker.get_top_devices(10)
        return jsonify(devices)
    return jsonify([])


@app.route('/api/applications')
def get_applications():
    """Get top applications by traffic."""
    if data_processor:
        apps = data_processor.app_tracker.get_top_applications(10)
        return jsonify(apps)
    return jsonify([])


@app.route('/api/connections')
def get_connections():
    """Get active connections."""
    if data_processor:
        connections = data_processor.connection_tracker.get_active_connections(50)
        return jsonify(connections)
    return jsonify([])


# WebSocket Events

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print(f"Client connected")
    emit('connection_status', {'connected': True})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print(f"Client disconnected")


@socketio.on('request_update')
def handle_request_update():
    """Handle manual update request from client."""
    if data_processor:
        data = data_processor.get_dashboard_data()
        emit('traffic_update', data)


# Application lifecycle

@app.before_request
def before_first_request():
    """Initialize monitoring before first request."""
    global running
    if not running:
        # Start monitoring in a separate thread to avoid blocking
        threading.Thread(target=start_monitoring, daemon=True).start()


if __name__ == '__main__':
    print("=" * 60)
    print("Network Traffic Monitor Dashboard")
    print("=" * 60)
    print()
    print("IMPORTANT: This application requires root/administrator privileges")
    print("Please run with: sudo python3 server.py")
    print()
    print("Starting server...")
    print()
    
    try:
        # Start monitoring
        start_monitoring()
        
        # Run Flask app with SocketIO
        # Note: In production, use a production WSGI server
        socketio.run(
            app,
            host='0.0.0.0',
            port=5000,
            debug=False,  # Set to False to avoid issues with threading
            use_reloader=False  # Disable reloader to prevent double initialization
        )
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_monitoring()
    except Exception as e:
        print(f"Server error: {e}")
        stop_monitoring()
