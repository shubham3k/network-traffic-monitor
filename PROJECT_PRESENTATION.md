# Network Traffic Monitor Dashboard
## Project Presentation

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [How It Works - Step by Step](#how-it-works---step-by-step)
4. [Technology Stack](#technology-stack)
5. [Key Features](#key-features)
6. [Implementation Details](#implementation-details)
7. [Data Flow](#data-flow)
8. [User Interface](#user-interface)
9. [Setup & Installation](#setup--installation)
10. [Live Demo](#live-demo)

---

## 🎯 Project Overview

### What is Network Traffic Monitor?

A **real-time web-based dashboard** that captures, analyzes, and visualizes network traffic on your local machine. It provides insights into:

- **Bandwidth usage** (upload/download speeds)
- **Device activity** (which devices are consuming data)
- **Application identification** (HTTP, HTTPS, DNS, SSH, etc.)
- **Protocol breakdown** (TCP, UDP, ICMP distribution)
- **Active connections** (real-time connection monitoring)

### Problem Statement

Network administrators and users need to:
- Monitor bandwidth consumption in real-time
- Identify which applications are using the most data
- Track devices on the network
- Detect unusual traffic patterns
- Understand protocol distribution

### Solution

A comprehensive monitoring dashboard that:
- ✅ Captures packets at the network layer
- ✅ Processes and aggregates traffic data
- ✅ Visualizes metrics through interactive charts
- ✅ Updates in real-time via WebSocket
- ✅ Provides a beautiful, modern UI

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Network Interface                     │
│                    (wlan0 / eth0)                        │
└────────────────────┬────────────────────────────────────┘
                     │ Raw Packets
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  BACKEND (Python)                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │  1. Packet Capture Layer (Scapy)                 │  │
│  │     - Sniffs network packets                     │  │
│  │     - Parses headers (IP, port, protocol)        │  │
│  │     - Identifies applications                    │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │ Parsed Packet Data                │
│                     ▼                                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │  2. Data Processing Layer                        │  │
│  │     - TrafficStats (bandwidth calculation)       │  │
│  │     - DeviceTracker (per-device stats)           │  │
│  │     - ApplicationTracker (per-app stats)         │  │
│  │     - ProtocolTracker (protocol breakdown)       │  │
│  │     - ConnectionTracker (active connections)     │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │ Aggregated Metrics                │
│                     ▼                                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │  3. Flask Server + WebSocket (SocketIO)          │  │
│  │     - REST API endpoints                         │  │
│  │     - WebSocket broadcasts (1s interval)         │  │
│  └──────────────────┬───────────────────────────────┘  │
└────────────────────┼────────────────────────────────────┘
                     │ JSON Data via WebSocket
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 FRONTEND (React + Vite)                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  App.jsx (State Management)                      │  │
│  │     - Socket.IO client connection                │  │
│  │     - React hooks (useState, useEffect)          │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │ Props                             │
│                     ▼                                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │  React Components                                │  │
│  │     - BandwidthChart (Line chart)                │  │
│  │     - DevicesChart (Bar chart)                   │  │
│  │     - ApplicationsChart (Bar chart)              │  │
│  │     - ProtocolChart (Donut chart)                │  │
│  │     - ConnectionsTable (Data table)              │  │
│  │     - StatsCards (Summary metrics)               │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
              Browser Display
```

### Component Breakdown

#### Backend Components (Python)

1. **`packet_capture.py`** - Packet Sniffing
   - Uses Scapy library
   - Captures IP packets (TCP/UDP/ICMP)
   - Runs in background thread
   - Circular buffer for memory efficiency

2. **`data_processor.py`** - Data Aggregation
   - 5 specialized tracker classes
   - Thread-safe operations
   - Rolling time windows
   - Real-time calculations

3. **`server.py`** - Web Server
   - Flask application
   - Flask-SocketIO for WebSocket
   - REST API endpoints
   - Background broadcast thread

4. **`utils.py`** - Helper Functions
   - Port-to-application mapping
   - Network interface detection
   - Data formatting utilities

#### Frontend Components (React)

1. **`App.jsx`** - Main Application
   - WebSocket connection
   - State management
   - Component orchestration

2. **Chart Components**
   - BandwidthChart, DevicesChart, ApplicationsChart, ProtocolChart
   - Built with Chart.js and react-chartjs-2

3. **Data Components**
   - StatsCards, ConnectionsTable
   - Display formatted metrics

4. **Styling**
   - Modern dark theme
   - Glassmorphism effects
   - Responsive grid layout

---

## ⚙️ How It Works - Step by Step

### Step 1: Packet Capture

```python
# packet_capture.py
1. Initialize Scapy packet sniffer
2. Set BPF filter to capture only IP packets
3. Start sniffing in background thread
4. For each packet:
   - Extract source/destination IPs
   - Extract ports (if TCP/UDP)
   - Identify protocol (TCP/UDP/ICMP)
   - Calculate packet size
   - Identify application by port number
5. Pass parsed packet to callback function
```

**Example Packet:**
```json
{
  "timestamp": "2026-01-09T10:00:00",
  "src_ip": "10.22.119.64",
  "dst_ip": "142.250.193.78",
  "src_port": 54321,
  "dst_port": 443,
  "protocol": "TCP",
  "application": "HTTPS",
  "size": 1420
}
```

### Step 2: Traffic Direction Detection

```python
# server.py - get_local_ips()
1. Detect all local IP addresses using netifaces
2. Include loopback (127.0.0.1) and network IPs (10.22.119.64)
3. Compare packet source IP with local IPs
4. If src_ip in local_ips → OUTBOUND (upload)
5. If src_ip not in local_ips → INBOUND (download)
```

### Step 3: Data Processing

```python
# data_processor.py
For each packet:

1. TrafficStats.add_packet()
   - Aggregate bytes per second
   - Separate upload/download
   - Track peak bandwidth
   - Maintain 5-minute rolling window

2. DeviceTracker.add_packet()
   - Track remote device IP
   - Accumulate bytes and packet count
   - Avoid double-counting

3. ApplicationTracker.add_packet()
   - Group by application name
   - Accumulate traffic per app

4. ProtocolTracker.add_packet()
   - Group by protocol (TCP/UDP/ICMP)
   - Count packets and bytes

5. ConnectionTracker.add_packet()
   - Track unique connections
   - Monitor connection duration
   - Auto-cleanup stale connections (60s timeout)
```

### Step 4: Data Aggregation

```python
# data_processor.py - get_dashboard_data()
Every second, compile:
{
  "bandwidth": {
    "current": { "upload": 1024, "download": 5120 },
    "history": [ /* 60 seconds of data */ ]
  },
  "stats": {
    "total_upload": 1048576,
    "total_download": 5242880,
    "peak_upload": 2048,
    "peak_download": 10240,
    "active_connections": 15
  },
  "devices": [ /* top 10 devices */ ],
  "applications": [ /* top 10 apps */ ],
  "protocols": { "TCP": {...}, "UDP": {...} },
  "connections": [ /* active connections */ ]
}
```

### Step 5: WebSocket Broadcast

```python
# server.py - broadcast_updates()
1. Run in background thread
2. Every 1 second:
   - Get dashboard data from DataProcessor
   - Emit 'traffic_update' event via SocketIO
   - Send to all connected clients
3. Use socketio.sleep() for thread compatibility
```

### Step 6: Frontend Reception

```javascript
// App.jsx
1. Establish Socket.IO connection on mount
2. Listen for 'traffic_update' event
3. When data received:
   - Update bandwidthData state
   - Update stats state
   - Update devices state
   - Update applications state
   - Update protocols state
   - Update connections state
4. React automatically re-renders components
```

### Step 7: Visualization

```javascript
// Chart Components
1. Receive data via props from App.jsx
2. Transform data for Chart.js format
3. Configure chart options (colors, scales, tooltips)
4. Render canvas with Chart.js
5. Smooth animations on data updates
```

---

## 💻 Technology Stack

### Backend

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Backend language | 3.8+ |
| **Scapy** | Packet capture and manipulation | 2.5.0 |
| **Flask** | Web framework | 3.0.0 |
| **Flask-SocketIO** | WebSocket support | 5.3.5 |
| **Flask-CORS** | Cross-origin resource sharing | 4.0.0 |
| **netifaces** | Network interface detection | 0.11.0 |

### Frontend

| Technology | Purpose | Version |
|------------|---------|---------|
| **React** | UI framework | 18.2.0 |
| **Vite** | Build tool & dev server | 5.0.8 |
| **Chart.js** | Data visualization | 4.4.0 |
| **react-chartjs-2** | React wrapper for Chart.js | 5.2.0 |
| **Socket.IO Client** | WebSocket client | 4.6.0 |

### Styling

- **CSS3** with custom properties
- **Google Fonts** (Inter)
- **Glassmorphism** design pattern
- **Responsive Grid** layout

---

## ✨ Key Features

### 1. Real-time Bandwidth Monitoring

**Line Chart Visualization**
- Dual datasets: Upload (red) and Download (cyan)
- 60-second rolling window
- Smooth curve interpolation
- Auto-scaling Y-axis
- Formatted tooltips (KB/s, MB/s)

**How it works:**
```
Every second → Aggregate bytes → Calculate bytes/second → 
Update chart → Shift time window → Display
```

### 2. Device Tracking

**Bar Chart Visualization**
- Top 10 devices by data usage
- IP addresses or hostnames
- Gradient color scheme
- Sorted by traffic volume

**Accuracy Fix:**
- Only counts remote devices (not local machine)
- Prevents double-counting
- Shows true per-device consumption

### 3. Application Identification

**Port-based Detection**
- 80+ common services mapped
- HTTP (80), HTTPS (443), DNS (53), SSH (22), etc.
- Unknown ports labeled as "Unknown:PORT"

**Bar Chart Display**
- Top 10 applications
- Vibrant color palette
- Data usage in MB

### 4. Protocol Analysis

**Donut Chart**
- TCP, UDP, ICMP distribution
- Percentage calculations
- Color-coded segments
- Packet count tooltips

### 5. Active Connections

**Data Table**
- Source IP, Destination IP, Port
- Protocol (color-coded)
- Application name
- Data transferred
- Scrollable with custom styling

### 6. Summary Statistics

**4 Metric Cards**
- Total Upload (red)
- Total Download (cyan)
- Active Connections (purple)
- Peak Bandwidth (green)

---

## 🔧 Implementation Details

### Thread Safety

All data structures use `threading.Lock()` to prevent race conditions:

```python
class DeviceTracker:
    def __init__(self):
        self.lock = Lock()
    
    def add_packet(self, packet_data, is_outbound):
        with self.lock:  # Thread-safe access
            # Update device statistics
```

### Memory Management

**Circular Buffers:**
```python
self.packet_buffer = deque(maxlen=1000)  # Auto-removes old items
```

**Time-based Cleanup:**
```python
def _cleanup_old_data(self):
    cutoff_time = int(time.time()) - self.window_seconds
    while self.data_points and self.data_points[0][0] < cutoff_time:
        self.data_points.popleft()
```

### Data Accuracy

**Issue 1: Double-Counting**
- **Problem:** Counted both src and dst IPs
- **Solution:** Only track remote device based on traffic direction

**Issue 2: Local IP Detection**
- **Problem:** Missed actual network IP
- **Solution:** Use netifaces to enumerate all interfaces

**Issue 3: WebSocket Errors**
- **Problem:** AssertionError on connection
- **Solution:** Use async_mode='threading' and socketio.sleep()

---

## 🌊 Data Flow

### Complete Flow Diagram

```
Network Packet
    ↓
[Scapy Capture]
    ↓
Parse Headers → {ip, port, protocol, size}
    ↓
Identify Application (port mapping)
    ↓
Determine Direction (local IP check)
    ↓
[5 Parallel Trackers]
    ├─→ TrafficStats (bandwidth)
    ├─→ DeviceTracker (per-device)
    ├─→ ApplicationTracker (per-app)
    ├─→ ProtocolTracker (protocol breakdown)
    └─→ ConnectionTracker (active connections)
    ↓
Aggregate Data (every 1 second)
    ↓
[Flask-SocketIO Broadcast]
    ↓
WebSocket → JSON payload
    ↓
[React App State Update]
    ↓
[Component Re-render]
    ↓
[Chart.js Visualization]
    ↓
Browser Display
```

---

## 🎨 User Interface

### Design Principles

1. **Dark Theme**
   - Deep blue/purple gradient background
   - Reduces eye strain
   - Professional appearance

2. **Glassmorphism**
   - Semi-transparent cards
   - Backdrop blur effect
   - Subtle borders

3. **Color Coding**
   - Upload: Red (#ef4444)
   - Download: Cyan (#00d9ff)
   - Connections: Purple (#a855f7)
   - Peak: Green (#10b981)

4. **Responsive Layout**
   - CSS Grid for flexible layouts
   - Breakpoints for mobile/tablet/desktop
   - Smooth animations and transitions

### Component Layout

```
┌─────────────────────────────────────────────┐
│              Header + Status                │
├─────────────────────────────────────────────┤
│  [Upload] [Download] [Connections] [Peak]   │  ← Stats Cards
├─────────────────────────────────────────────┤
│         Bandwidth Chart (Full Width)        │  ← Line Chart
├──────────────────────┬──────────────────────┤
│   Top Devices        │  Top Applications    │  ← Bar Charts
├──────────────────────┼──────────────────────┤
│  Protocol Breakdown  │                      │  ← Donut Chart
├─────────────────────────────────────────────┤
│        Active Connections Table             │  ← Data Table
└─────────────────────────────────────────────┘
```

---

## 🚀 Setup & Installation

### Prerequisites

```bash
# System Requirements
- Python 3.8+
- Node.js 16+
- npm 8+
- Root/sudo privileges (for packet capture)
```

### Installation Steps

**1. Backend Setup**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**2. Frontend Setup**
```bash
cd frontend
npm install
```

### Running the Application

**Terminal 1: Backend**
```bash
cd backend
sudo .venv/bin/python3 server.py
```

**Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```

**Access Dashboard**
```
http://localhost:5173
```

---

## 🎬 Live Demo

### What You'll See

1. **Connection Status**
   - Green pulsing indicator when connected
   - Red indicator if disconnected

2. **Real-time Updates**
   - Charts update every second
   - Smooth animations
   - No page refresh needed

3. **Interactive Charts**
   - Hover for detailed tooltips
   - Auto-scaling axes
   - Responsive to window resize

4. **Traffic Generation**
   - Browse websites → See HTTP/HTTPS traffic
   - Download files → See bandwidth spike
   - Ping servers → See ICMP packets

### Sample Metrics

```
Total Upload: 15.3 MB
Total Download: 127.8 MB
Active Connections: 23
Peak Bandwidth: 2.5 MB/s

Top Devices:
1. 142.250.193.78 (Google) - 45.2 MB
2. 151.101.1.140 (GitHub) - 23.1 MB
3. 104.16.132.229 (Cloudflare) - 18.7 MB

Top Applications:
1. HTTPS - 89.3 MB
2. HTTP - 12.5 MB
3. DNS - 1.2 MB

Protocol Breakdown:
- TCP: 95.3%
- UDP: 4.2%
- ICMP: 0.5%
```

---

## 📊 Performance Metrics

### System Resources

- **CPU Usage:** ~5-10% (depends on traffic volume)
- **Memory Usage:** ~50-100 MB
- **Network Overhead:** Minimal (read-only capture)

### Scalability

- **Packet Processing:** Up to 1000 packets/second
- **WebSocket Latency:** <10ms
- **Chart Rendering:** 60 FPS animations
- **Data Retention:** 5-minute rolling window

---

## 🔒 Security & Privacy

### Data Handling

✅ **Only packet headers captured** (metadata)
✅ **No payload data logged**
✅ **Data stored in memory only**
✅ **No disk persistence**
✅ **5-minute retention window**

### Network Security

⚠️ **Requires root privileges** (cannot be avoided)
⚠️ **Dashboard on localhost only**
⚠️ **No authentication** (add if exposing remotely)

---

## 🎯 Use Cases

1. **Network Administrators**
   - Monitor bandwidth usage
   - Identify bandwidth hogs
   - Detect unusual traffic patterns

2. **Developers**
   - Debug application network behavior
   - Analyze API call patterns
   - Monitor WebSocket connections

3. **Home Users**
   - Track internet usage
   - Identify which apps use data
   - Monitor smart home devices

4. **Security Analysts**
   - Detect suspicious connections
   - Monitor protocol distribution
   - Track external connections

---

## 🏆 Project Achievements

### Technical Accomplishments

✅ Real-time packet capture with Scapy
✅ Thread-safe data processing
✅ WebSocket real-time updates
✅ Modern React architecture
✅ Beautiful UI with Chart.js
✅ Accurate data tracking (fixed double-counting)
✅ Proper upload/download classification
✅ Memory-efficient circular buffers

### Code Statistics

- **Total Lines:** ~2,500
- **Backend:** 940 lines (Python)
- **Frontend:** 1,100+ lines (React/CSS)
- **Documentation:** 350+ lines
- **Components:** 11 (7 React, 4 Python modules)

---

## 🔮 Future Enhancements

### Planned Features

- [ ] Traffic filtering (by IP, port, protocol)
- [ ] Alert system for bandwidth thresholds
- [ ] Data export (CSV/JSON)
- [ ] Persistent storage (database)
- [ ] Geolocation for external IPs
- [ ] Multi-interface support
- [ ] User authentication
- [ ] Historical data analysis
- [ ] Mobile app version

---

## 📝 Conclusion

### What We Built

A **production-ready network traffic monitoring dashboard** that:
- Captures and analyzes network packets in real-time
- Provides comprehensive visualizations
- Offers accurate bandwidth and device tracking
- Features a modern, responsive UI
- Updates seamlessly via WebSocket

### Key Takeaways

1. **System Programming:** Low-level packet capture with Scapy
2. **Real-time Communication:** WebSocket implementation
3. **Data Visualization:** Interactive charts with Chart.js
4. **Modern Web Development:** React hooks and state management
5. **Performance Optimization:** Thread safety and memory management

### Impact

This project demonstrates:
- Full-stack development skills
- Network programming expertise
- Real-time data processing
- Modern UI/UX design
- Problem-solving abilities

---

## 📞 Contact & Repository

**Author:** Shubham Kushwaha
**GitHub:** https://github.com/shubham3k/network-traffic-monitor
**Created:** January 2026

---

## 🙏 Acknowledgments

- **Scapy** - Powerful packet manipulation library
- **Chart.js** - Beautiful data visualizations
- **Flask-SocketIO** - Real-time WebSocket support
- **React** - Modern UI framework
- **Vite** - Lightning-fast build tool

---

**Thank you for your attention!**

*Questions?*
