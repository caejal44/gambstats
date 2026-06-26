import '../App.css';
import Card from "../components/Card";
import Layout from "../components/Layout";
import { Link } from 'react-router-dom';
import { useEffect, useState } from "react";
import { getTrips, type TripResponse } from "../services/tripService";

function Dashboard() {
  const [activeTrip, setActiveTrip] = useState<TripResponse | null>(null);

  useEffect(() => {
    async function loadTrips() {
      const data = await getTrips();
      const active = data.trips.find((trip) => trip.status === "active") ?? null;
      setActiveTrip(active);
    }

    loadTrips();
  }, []);

  return (
    <Layout>
      <section>
        <h2 className="section-title">Active Now</h2>

        <div className="card-row">
          {activeTrip ? (
            <Card
              title={activeTrip.trip_name}
              text={`${activeTrip.location} • $${activeTrip.trip_budget}`}
              buttonText="Edit Trip"
              path="/trips/edit"
            />
          ) : (
            <Card
              title="No Active Trip"
              text="Create a new trip to begin tracking."
              buttonText="New Trip"
              path="/trips/new"
            />
          )}
        </div>
      </section>

      <section>
        <div className="dashboard-actions">
          <h2 className="section-subtitle">Quick Actions </h2>

            <nav className="dashboard-links">
              <Link to="/trips/new">New Trip</Link>
              <Link to="/sessions/new">New Session</Link>
              <Link to="/games/new">New Game</Link>
            </nav>
        </div>
      </section>

      <section>
        <div className="dashboard-actions">
          <h2 className="section-subtitle">My History </h2>

            <nav className="dashboard-links">
              <Link to="/trips">Trip History</Link>
              <Link to="/sessions">Session History</Link>
              <Link to="/games">Game History</Link>
            </nav>
        </div>
      </section>

    </Layout>
  );
}
export default Dashboard