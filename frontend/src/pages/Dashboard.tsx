import '../App.css';
import Card from "../components/Card";
import Layout from "../components/Layout";
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

      {/* Start Now and History sections here */}
    </Layout>
  );
}
export default Dashboard