import React from 'react';

function Header({ connected }) {
    return (
        <header className="header">
            <h1 className="header-title">Network Traffic Monitor</h1>
            <div className="connection-status">
                <span className={`status-indicator ${connected ? '' : 'disconnected'}`}></span>
                <span>{connected ? 'Connected' : 'Disconnected'}</span>
            </div>
        </header>
    );
}

export default Header;
