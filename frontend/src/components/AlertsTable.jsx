function AlertsTable({ alerts }) {
  return (
    <div className="alerts-container">
      <h2>Recent Alerts</h2>

      <table className="alerts-table">
        <thead>
          <tr>
            <th>IP Address</th>
            <th>Type</th>
            <th>Severity</th>
          </tr>
        </thead>

        <tbody>
            {alerts.map((alert) => (
                <tr key={alert.id}>
                    <td>{alert.ip_address}</td>
                    <td>{alert.alert_type}</td>
                    <td>
                        <span className={`severity ${alert.severity.toLowerCase()}`}>
                            {alert.severity}
                        </span>
                    </td>
                </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}

export default AlertsTable;