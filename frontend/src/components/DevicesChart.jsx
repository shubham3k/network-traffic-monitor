import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { formatBytes } from '../utils/formatters';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

function DevicesChart({ devices }) {
    if (!devices || devices.length === 0) {
        return (
            <div className="card">
                <h2 className="card-title">💻 Top Devices</h2>
                <div className="empty-state">No device data available</div>
            </div>
        );
    }

    const labels = devices.map(d => d.hostname || d.ip);
    const dataValues = devices.map(d => d.bytes || 0);

    const data = {
        labels,
        datasets: [
            {
                label: 'Data Usage',
                data: dataValues,
                backgroundColor: devices.map((_, i) => {
                    const ratio = i / devices.length;
                    return `rgba(${0 + ratio * 168}, ${217 - ratio * 50}, ${255 - ratio * 100}, 0.8)`;
                }),
                borderColor: devices.map((_, i) => {
                    const ratio = i / devices.length;
                    return `rgb(${0 + ratio * 168}, ${217 - ratio * 50}, ${255 - ratio * 100})`;
                }),
                borderWidth: 1,
            },
        ],
    };

    const options = {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
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
                        return `Data: ${formatBytes(context.parsed.x)}`;
                    }
                }
            },
        },
        scales: {
            x: {
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
                        return formatBytes(value);
                    },
                },
            },
            y: {
                grid: {
                    display: false,
                },
                ticks: {
                    color: '#a0aec0',
                    font: {
                        family: 'Inter',
                        size: 11,
                    },
                },
            },
        },
    };

    return (
        <div className="card">
            <h2 className="card-title">💻 Top Devices</h2>
            <div className="chart-container">
                <Bar data={data} options={options} />
            </div>
        </div>
    );
}

export default DevicesChart;
