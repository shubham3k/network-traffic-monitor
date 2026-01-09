import React, { useEffect, useRef } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { formatTimestamp, formatBandwidth } from '../utils/formatters';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

function BandwidthChart({ bandwidthData }) {
    const chartRef = useRef(null);

    if (!bandwidthData || bandwidthData.length === 0) {
        return (
            <div className="card large">
                <h2 className="card-title">📊 Real-time Bandwidth</h2>
                <div className="empty-state">Waiting for traffic data...</div>
            </div>
        );
    }

    // Prepare data for Chart.js
    const labels = bandwidthData.map(d => formatTimestamp(d.timestamp));
    const uploadData = bandwidthData.map(d => d.upload || 0);
    const downloadData = bandwidthData.map(d => d.download || 0);

    const data = {
        labels,
        datasets: [
            {
                label: 'Upload',
                data: uploadData,
                borderColor: 'rgb(239, 68, 68)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                borderWidth: 2,
            },
            {
                label: 'Download',
                data: downloadData,
                borderColor: 'rgb(0, 217, 255)',
                backgroundColor: 'rgba(0, 217, 255, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                borderWidth: 2,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#a0aec0',
                    font: {
                        family: 'Inter',
                        size: 12,
                    },
                    usePointStyle: true,
                    padding: 15,
                },
            },
            tooltip: {
                backgroundColor: 'rgba(26, 31, 58, 0.95)',
                titleColor: '#ffffff',
                bodyColor: '#a0aec0',
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 1,
                padding: 12,
                displayColors: true,
                callbacks: {
                    label: function (context) {
                        return `${context.dataset.label}: ${formatBandwidth(context.parsed.y)}`;
                    }
                }
            },
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                    drawBorder: false,
                },
                ticks: {
                    color: '#718096',
                    font: {
                        family: 'Inter',
                        size: 10,
                    },
                    maxTicksLimit: 10,
                },
            },
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                    drawBorder: false,
                },
                ticks: {
                    color: '#718096',
                    font: {
                        family: 'Inter',
                        size: 10,
                    },
                    callback: function (value) {
                        return formatBandwidth(value);
                    },
                },
            },
        },
        animation: {
            duration: 300,
        },
    };

    return (
        <div className="card" style={{ gridColumn: '1 / -1' }}>
            <h2 className="card-title">📊 Real-time Bandwidth</h2>
            <div className="chart-container large">
                <Line ref={chartRef} data={data} options={options} />
            </div>
        </div>
    );
}

export default BandwidthChart;
