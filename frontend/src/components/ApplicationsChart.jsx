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

function ApplicationsChart({ applications }) {
    if (!applications || applications.length === 0) {
        return (
            <div className="card">
                <h2 className="card-title">🚀 Top Applications</h2>
                <div className="empty-state">No application data available</div>
            </div>
        );
    }

    const labels = applications.map(app => app.name);
    const dataValues = applications.map(app => app.bytes || 0);

    const colors = [
        'rgba(0, 217, 255, 0.8)',    // Cyan
        'rgba(168, 85, 247, 0.8)',   // Purple
        'rgba(16, 185, 129, 0.8)',   // Green
        'rgba(245, 158, 11, 0.8)',   // Yellow
        'rgba(239, 68, 68, 0.8)',    // Red
        'rgba(59, 130, 246, 0.8)',   // Blue
        'rgba(236, 72, 153, 0.8)',   // Pink
        'rgba(34, 197, 94, 0.8)',    // Lime
        'rgba(251, 146, 60, 0.8)',   // Orange
        'rgba(139, 92, 246, 0.8)',   // Violet
    ];

    const data = {
        labels,
        datasets: [
            {
                label: 'Data Usage',
                data: dataValues,
                backgroundColor: colors,
                borderColor: colors.map(c => c.replace('0.8', '1')),
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
            <h2 className="card-title">🚀 Top Applications</h2>
            <div className="chart-container">
                <Bar data={data} options={options} />
            </div>
        </div>
    );
}

export default ApplicationsChart;
