import React from 'react';
import { formatBytes } from '../utils/formatters';

function ConnectionsTable({ connections }) {
    if (!connections || connections.length === 0) {
        return (
            <div className="card" style={{ gridColumn: '1 / -1' }}>
                <h2 className="card-title">🔗 Active Connections</h2>
                <div className="empty-state">No active connections</div>
            </div>
        );
    }

    return (
        <div className="card" style={{ gridColumn: '1 / -1' }}>
            <h2 className="card-title">🔗 Active Connections</h2>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Source IP</th>
                            <th>Destination IP</th>
                            <th>Port</th>
                            <th>Protocol</th>
                            <th>Application</th>
                            <th>Data Transferred</th>
                        </tr>
                    </thead>
                    <tbody>
                        {connections.map((conn, index) => (
                            <tr key={index}>
                                <td>{conn.src_ip}</td>
                                <td>{conn.dst_ip}</td>
                                <td>{conn.dst_port}</td>
                                <td>
                                    <span className={`text-${conn.protocol === 'TCP' ? 'cyan' : conn.protocol === 'UDP' ? 'purple' : 'green'}`}>
                                        {conn.protocol}
                                    </span>
                                </td>
                                <td>{conn.application}</td>
                                <td>{formatBytes(conn.bytes || 0)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default ConnectionsTable;
