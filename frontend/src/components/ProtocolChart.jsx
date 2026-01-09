import React from 'react';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend
} from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

function ProtocolChart({ protocols }) {
    if (!protocols || Object.keys(protocols).length === 0) {
        return (
            <div className="card">
                <h2 className="card-title">🔌 Protocol Breakdown</h2>
                <div className="empty-state">No protocol data available</div>
            </div>
        );
    }

    const protocolNames = Object.keys(protocols);
    const protocolPackets = protocolNames.map(name => protocols[name].packets || 0);

    const colorMap = {
        'TCP': 'rgba(0, 217, 255, 0.8)',
        'UDP': 'rgba(168, 85, 247, 0.8)',
        'ICMP': 'rgba(16, 185, 129, 0.8)',
    };

    const data = {
        labels: protocolNames,
        datasets: [
            {
                label: 'Packets',
                data: protocolPackets,
                backgroundColor: protocolNames.map(name => colorMap[name] || 'rgba(245, 158, 11, 0.8)'),
                borderColor: protocolNames.map(name =>
                    (colorMap[name] || 'rgba(245, 158, 11, 0.8)').replace('0.8', '1')
                ),
                borderWidth: 2,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: '#a0aec0',
                    font: {
                        family: 'Inter',
                        size: 12,
                    },
                    padding: 15,
                    usePointStyle: true,
                },
            },
            tooltip: {
                backgroundColor: 'rgba(26, 31, 58, 0.95)',
                titleColor: '#ffffff',
                bodyColor: '#a0aec0',
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 1,
                padding: 12,
                callbacks: {
                    label: function (context) {
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((context.parsed / total) * 100).toFixed(1);
                        return `${context.label}: ${context.parsed} packets (${percentage}%)`;
                    }
                }
            },
        },
    };

    return (
        <div className="card">
            <h2 className="card-title">🔌 Protocol Breakdown</h2>
            <div className="chart-container">
                <Doughnut data={data} options={options} />
            </div>
        </div>
    );
}

export default ProtocolChart;
