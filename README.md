# Network Traffic Monitor Dashboard

A real-time web-based dashboard that captures, analyzes, and visualizes network traffic with bandwidth monitoring, application identification, and interactive charts.

![Network Traffic Monitor](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18.2-61dafb)

## Features

- 🚀 **Real-time Packet Capture**: Captures network packets using Scapy
- 📊 **Live Bandwidth Monitoring**: Visualizes upload/download speeds in real-time
- 💻 **Device Tracking**: Identifies and ranks devices by data usage
- 🔌 **Application Identification**: Recognizes applications by port numbers
- 📈 **Protocol Analysis**: Breaks down traffic by protocol (TCP/UDP/ICMP)
- 🔗 **Connection Tracking**: Monitors active network connections
- 🎨 **Modern UI**: Beautiful dark theme with glassmorphism effects
- ⚡ **WebSocket Updates**: Real-time data updates every second

## Architecture

### Backend (Python)
- **Scapy**: Raw packet capture and parsing
- **Flask**: Web server and REST API
- **Flask-SocketIO**: WebSocket communication for real-time updates
- **Threading**: Concurrent packet capture and data processing

### Frontend (React)
- **React 18**: Component-based UI with hooks
- **Vite**: Fast development and build tool
- **Chart.js**: Interactive data visualizations
- **Socket.IO Client**: Real-time WebSocket connection

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **npm**: 8 or higher

### Permissions
⚠️ **IMPORTANT**: Packet capture requires **root/administrator privileges**

- **Linux/macOS**: Run with `sudo`
- **Windows**: Run terminal as Administrator

## Installation

### 1. Clone the repo link

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install
```

## Usage

### Starting the Application

You need to run **two separate terminals**:

#### Terminal 1: Backend Server

```bash
cd backend
source venv/bin/activate  # If using virtual environment

# Run with sudo for packet capture
sudo python3 server.py
```

The backend will start on `http://localhost:5000`

#### Terminal 2: Frontend Dev Server

```bash
cd frontend

# Start Vite development server
npm run dev
```

The frontend will start on `http://localhost:5173`

### Accessing the Dashboard

Open your web browser and navigate to:
```
http://localhost:5173
```

You should see the Network Traffic Monitor dashboard with real-time updates.

## Dashboard Components

### 1. **Statistics Cards**
- Total Upload/Download
- Active Connections Count
- Peak Bandwidth

### 2. **Real-time Bandwidth Chart**
- Line chart showing upload/download speeds over time
- 60-second rolling window
- Updates every second

### 3. **Top Devices**
- Bar chart of devices ranked by data usage
- Shows IP addresses and data transferred

### 4. **Top Applications**
- Bar chart of applications/services by traffic
- Identifies HTTP, HTTPS, DNS, SSH, etc.

### 5. **Protocol Breakdown**
- Donut chart showing distribution of protocols
- TCP, UDP, ICMP percentages

### 6. **Active Connections Table**
- Scrollable list of current connections
- Source/destination IPs, ports, protocols
- Data transferred per connection

## Configuration

### Network Interface

By default, the system auto-detects your primary network interface. To specify a different interface:

Edit `backend/server.py`:
```python
interface = "eth0"  # or "wlan0", etc.
packet_capture = PacketCapture(interface=interface, callback=packet_callback)
```

### Update Frequency

To change the WebSocket broadcast frequency, edit `backend/server.py`:
```python
time.sleep(1)  # Change to desired interval in seconds
```

## Troubleshooting

### Permission Denied Error

**Problem**: `PermissionError: [Errno 1] Operation not permitted`

**Solution**: Run the backend with `sudo`:
```bash
sudo python3 server.py
```

### No Packets Captured

**Problem**: Dashboard shows no traffic

**Solutions**:
1. Verify you're running with sudo/administrator privileges
2. Check that the correct network interface is selected
3. Generate some network traffic (browse websites, download files)
4. Verify firewall isn't blocking packet capture

### WebSocket Connection Failed

**Problem**: Dashboard shows "Disconnected"

**Solutions**:
1. Ensure backend server is running on port 5000
2. Check that no firewall is blocking the connection
3. Verify the proxy configuration in `frontend/vite.config.js`

### Charts Not Updating

**Problem**: Charts are static or not showing data

**Solutions**:
1. Check browser console for JavaScript errors
2. Verify WebSocket connection is established (green indicator)
3. Ensure backend is processing packets (check terminal output)

## Security & Privacy

### Data Handling
- **Only packet headers are captured** (metadata like IPs, ports, protocols)
- **No payload data is logged or stored**
- Data is kept in memory only (not persisted to disk)
- 5-minute rolling window for historical data

### Network Security
- Dashboard should only be accessed on localhost
- Do not expose the dashboard to the public internet without authentication
- Be aware that IP addresses and traffic patterns are visible

## Development

### Building for Production

```bash
# Frontend
cd frontend
npm run build

# The build output will be in frontend/dist
# Configure backend to serve from this directory
```

### Project Structure

```
/home/sk/Web dev/net/
├── backend/
│   ├── packet_capture.py      # Scapy packet sniffing
│   ├── data_processor.py      # Traffic aggregation & analysis
│   ├── server.py              # Flask + SocketIO server
│   ├── utils.py               # Helper functions
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── styles/            # CSS styles
│   │   ├── utils/             # Utility functions
│   │   ├── App.jsx            # Main component
│   │   └── main.jsx           # React entry point
│   ├── index.html             # Root HTML
│   ├── vite.config.js         # Vite configuration
│   └── package.json           # Dependencies
└── README.md                  # This file
```

## Performance Considerations

- **High Traffic Networks**: On very high-bandwidth networks (1Gbps+), consider implementing packet sampling
- **Memory Usage**: The system uses circular buffers to prevent memory growth
- **CPU Usage**: Packet processing is CPU-intensive; monitor system resources
- **Browser Performance**: Chart updates every second; older browsers may experience lag

## Known Limitations

1. **Requires elevated privileges**: Cannot run without root/admin access
2. **Local network only**: Designed for monitoring the local machine's traffic
3. **Port-based identification**: Application detection relies on standard port numbers
4. **No deep packet inspection**: Only analyzes packet headers, not content
5. **Single interface**: Monitors one network interface at a time

## Future Enhancements

- [ ] Historical data persistence (database storage)
- [ ] Traffic filtering by IP, port, or protocol
- [ ] Alert system for bandwidth thresholds
- [ ] Export data to CSV/JSON
- [ ] Geolocation mapping for external IPs
- [ ] Multi-interface support
- [ ] User authentication for remote access
- [ ] Mobile-responsive improvements

## License

This project is provided as-is for educational and monitoring purposes.

## Acknowledgments

- **Scapy**: Powerful packet manipulation library
- **Chart.js**: Beautiful and responsive charts
- **Flask-SocketIO**: Real-time WebSocket communication
- **React**: Modern UI framework

---

**Created**: 2026-01-08  
**Author**: Network Traffic Monitor Team
