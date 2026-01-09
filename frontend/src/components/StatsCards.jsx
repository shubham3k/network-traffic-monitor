import React from 'react';
import { formatBytes, formatBandwidth } from '../utils/formatters';

function StatsCards({ stats }) {
    if (!stats) {
        return null;
    }

    return (
        <div className="stats-grid">
            <div className="stat-card">
                <div className="stat-label">Total Upload</div>
                <div className="stat-value upload">
                    {formatBytes(stats.total_upload || 0)}
                </div>
            </div>

            <div className="stat-card">
                <div className="stat-label">Total Download</div>
                <div className="stat-value download">
                    {formatBytes(stats.total_download || 0)}
                </div>
            </div>

            <div className="stat-card">
                <div className="stat-label">Active Connections</div>
                <div className="stat-value connections">
                    {stats.active_connections || 0}
                </div>
            </div>

            <div className="stat-card">
                <div className="stat-label">Peak Bandwidth</div>
                <div className="stat-value peak">
                    {formatBandwidth(Math.max(stats.peak_upload || 0, stats.peak_download || 0))}
                </div>
            </div>
        </div>
    );
}

export default StatsCards;
