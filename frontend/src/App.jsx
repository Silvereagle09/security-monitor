import "./App.css";
import { useEffect, useState } from "react";
import StatsCard from "./components/StatsCard";
import API from "./services/api";
import AlertsTable from "./components/AlertsTable";
import EventHistory from "./components/EventHistory";

function App() {
  const [stats, setStats] = useState({
    total_events: 0,
    total_alerts: 0,
    high_severity_alerts: 0,
  });
  const [alerts, setAlerts] = useState([]);
  const [events, setEvents] = useState([]);

  const fetchData = () => {
    API.get("/stats")
      .then((response) => {
        setStats(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

    API.get("/alerts")
      .then((response) => {
        setAlerts(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

    API.get("/events")
      .then((response) => {
        setEvents(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

  };
  useEffect(() => {
    fetchData();

    const interval = setInterval(() => {
      fetchData();
    }, 5000);

    return () => {
      clearInterval(interval);
    };

  }, []);

  return (
    <div className="dashboard">
      <h1>Security Monitor Dashboard</h1>

      <div className="cards">
        <StatsCard
          title="Total Events"
          value={stats.total_events}
        />

        <StatsCard
          title="Total Alerts"
          value={stats.total_alerts}
        />

        <StatsCard
          title="High Severity Alerts"
          value={stats.high_severity_alerts}
        />
      </div>

      <AlertsTable alerts={alerts} />
      <EventHistory events={events} />
    </div>
  );
}

export default App;