import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { getTrips, type TripResponse } from "../services/tripService";

function ActiveTrip() {
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
        <h2 className="section-title">Active Trip</h2>

        {activeTrip ? (
          <div>
            <p>{activeTrip.trip_name}</p>
            <p>{activeTrip.location}</p>
            <p>${activeTrip.trip_budget}</p>
            <p>{activeTrip.started_at}</p>
          </div>
        ) : (
          <p>No active trip</p>
        )}
      </section>
    </Layout>
  );
}

export default ActiveTrip;
