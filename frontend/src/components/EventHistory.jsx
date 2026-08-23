function EventHistory({ events }) {
  return (
    <div className="events-container">
      <h2>Event History</h2>

      <table className="alerts-table">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Event Type</th>
            <th>Username</th>
            <th>IP Address</th>
          </tr>
        </thead>

        <tbody>
          {events.map((event) => (
            <tr key={event.id}>
              <td>{event.timestamp}</td>
              <td>{event.event_type}</td>
              <td>{event.username}</td>
              <td>{event.ip_address}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EventHistory;