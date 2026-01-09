import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import Header from './components/Header';
import StatsCards from './components/StatsCards';
import BandwidthChart from './components/BandwidthChart';
import DevicesChart from './components/DevicesChart';
import ApplicationsChart from './components/ApplicationsChart';
import ProtocolChart from './components/ProtocolChart';
import ConnectionsTable from './components/ConnectionsTable';
import './styles/App.css';

function App() {
    const [connected, setConnected] = useState(false);
    const [bandwidthData, setBandwidthData] = useState([]);
    const [stats, setStats] = useState(null);
    const [devices, setDevices] = useState([]);
    const [applications, setApplications] = useState([]);
    const [protocols, setProtocols] = useState({});
    const [connections, setConnections] = useState([]);

    useEffect(() => {
        // Initialize Socket.IO connection
        const socket = io('http://localhost:5000', {
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionAttempts: 10,
        });

        // Connection event handlers
        socket.on('connect', () => {
            console.log('Connected to server');
            setConnected(true);
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from server');
            setConnected(false);
        });

        socket.on('connection_status', (data) => {
            console.log('Connection status:', data);
        });

        // Traffic update handler
        socket.on('traffic_update', (data) => {
            console.log('Traffic update received:', data);

            // Update bandwidth history
            if (data.bandwidth && data.bandwidth.history) {
                setBandwidthData(data.bandwidth.history);
            }

            // Update statistics
            if (data.stats) {
                setStats(data.stats);
            }

            // Update devices
            if (data.devices) {
                setDevices(data.devices);
            }

            // Update applications
            if (data.applications) {
                setApplications(data.applications);
            }

            // Update protocols
            if (data.protocols) {
                setProtocols(data.protocols);
            }

            // Update connections
            if (data.connections) {
                setConnections(data.connections);
            }
        });

        // Error handler
        socket.on('error', (error) => {
            console.error('Socket error:', error);
        });

        // Cleanup on unmount
        return () => {
            socket.disconnect();
        };
    }, []);

    return (
        <div className="app">
            <Header connected={connected} />

            <div className="dashboard">
                <StatsCards stats={stats} />

                <BandwidthChart bandwidthData={bandwidthData} />

                <DevicesChart devices={devices} />

                <ApplicationsChart applications={applications} />

                <ProtocolChart protocols={protocols} />

                <ConnectionsTable connections={connections} />
            </div>
        </div>
    );
}

export default App;
