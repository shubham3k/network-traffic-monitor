/**
 * Utility functions for formatting data in the dashboard
 */

/**
 * Convert bytes to human-readable format
 * @param {number} bytes - Number of bytes
 * @returns {string} Formatted string (e.g., "1.5 MB")
 */
export function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 ** 2) return `${(bytes / 1024).toFixed(2)} KB`;
    if (bytes < 1024 ** 3) return `${(bytes / (1024 ** 2)).toFixed(2)} MB`;
    return `${(bytes / (1024 ** 3)).toFixed(2)} GB`;
}

/**
 * Format bandwidth with appropriate units
 * @param {number} bytesPerSec - Bytes per second
 * @returns {string} Formatted string (e.g., "1.5 MB/s")
 */
export function formatBandwidth(bytesPerSec) {
    if (bytesPerSec === 0) return '0 B/s';
    if (bytesPerSec < 1024) return `${bytesPerSec.toFixed(2)} B/s`;
    if (bytesPerSec < 1024 ** 2) return `${(bytesPerSec / 1024).toFixed(2)} KB/s`;
    return `${(bytesPerSec / (1024 ** 2)).toFixed(2)} MB/s`;
}

/**
 * Format timestamp for chart labels
 * @param {number} timestamp - Unix timestamp
 * @returns {string} Formatted time (HH:MM:SS)
 */
export function formatTimestamp(timestamp) {
    const date = new Date(timestamp * 1000);
    return date.toLocaleTimeString('en-US', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

/**
 * Format duration in seconds
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration
 */
export function formatDuration(seconds) {
    if (seconds < 60) return `${seconds}s`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
}
