import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function EventTypeChart({ data }) {
  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Events by Type</h2>

      <ResponsiveContainer width="100%" height={600}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="event_type" />

          <YAxis />

          <Tooltip />

          <Bar dataKey="count" fill="#22c55e" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default EventTypeChart;