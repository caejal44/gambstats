import '../App.css';
import Card from "../components/Card";
import Layout from "../components/Layout";
import { Link } from 'react-router-dom';
import { useEffect, useState } from "react";
import { getTrips, type TripResponse } from "../services/tripService";
import { getSessions, type SessionResponse } from '../services/sessionService';
import { getGames, type GameResponse } from '../services/gameService';
import { formatDate } from "../utils/formatters";

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

  const [activeSession, setActiveSession] = useState<SessionResponse | null>(null);

  useEffect(() => {
    async function loadSession() {
      const data = await getSessions();
      const active = data.sessions.find((session) => session.status === "active") ?? null;
      setActiveSession(active);
    }

    loadSession();
  }, []);
  const [activeGames, setActiveGames] = useState<GameResponse[]>([]);

  useEffect(() => {
  async function loadGames() {
    const data = await getGames();
    const active = data.games.filter((game) => game.status === "active");
    setActiveGames(active);
  }

  loadGames();
}, []);

  return (
    <Layout showNav={false}>
      <section>
        <h2 className="section-title">Active Now</h2>

        <div className="card-row">
          {activeTrip ? (
            <Card
              title={activeTrip.trip_name}
              text={`${activeTrip.location} • $${activeTrip.trip_budget}`}
              buttonText="Trip Details"
              path={`/trips/${activeTrip.trip_id}/edit`}
            />
          ) : (
            <Card
              title="No Active Trip"
              text="Create a new trip to begin tracking."
              buttonText="New Trip"
              path="/trips/new"
            />
          )}
          {activeSession ? (
            <Card
              title={activeSession.casino}
              text={`Started: ${formatDate(activeSession.started_at)}`}
              buttonText="Session Details"
              path={`/sessions/${activeSession.session_id}/edit`}
            />
          ) : (
            <Card
              title="No Active Session"
              text="Create a new session to begin tracking."
              buttonText="New Session"
              path="/sessions/new"
            />
          )}
          {activeGames.length > 0 ? (
            activeGames.map((game) => (
            <Card
              key={game.game_id}
              title={game.game_name}
              text={`${game.game_type} • Cash in: $${game.cash_in}`}
              buttonText="Game Details"
              path={`/games/${game.game_id}/edit`}
            />
          ))
          ) : (
          <Card
            title="No Active Games"
            text="Create a new game to begin tracking."
            buttonText="New Game"
            path="/games/new"
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