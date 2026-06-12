import '../App.css';
import Card from "../components/Card";
import Layout from "../components/Layout";

const activeCards = [
  { title: "Active Trip", text: "No active trip", buttonText: "View Trip", path: "/trips/active"},
  { title: "Active Session", text: "No active session", buttonText: "View Session", path: "/sessions/active" },
  { title: "Active Games", text: "No active games", buttonText: "View Games", path: "/games/active" },
];

const newCards = [
  { title: "New Trip", text: "Create a new trip", buttonText: "Create Trip", path: "/trips/new"},
  { title: "New Session", text: "Create a new session", buttonText: "Create Session", path: "/sessions/new" },
  { title: "New Game", text: "Create a new game", buttonText: "Create Game", path: "/games/new" },
];

const historyCards = [
  { title: "Trip History", text: "View your trip history", buttonText: "View Trips", path: "/trips" },
  { title: "Session History", text: "View your session history", buttonText: "View Sessions", path: "/sessions" },
  { title: "Game History", text: "View your game history", buttonText: "View Games", path: "/games" },
];

function Dashboard() {

  return (
      <>

<Layout>
<main className="dashboard-panel">
  <section>
    <h2 className="section-title">Active Now</h2>

    <div className="card-row">

      {activeCards.map((card) => (
    <Card
      key={card.title}
      title={card.title}
      text={card.text}
      buttonText={card.buttonText}
      path={card.path}
      />
    ))}
    </div>
  </section>

  <section>
    <h2 className="section-title">Start Now</h2>

    <div className="card-row">
      
      {newCards.map((card) => (
        <Card
          key={card.title}
          title={card.title}
          text={card.text}
          buttonText={card.buttonText}
          path={card.path}
        />
      ))}
    </div>
  </section>
  <section>
    <h2 className="section-title">My History</h2>
    <div className="card-row">
      {historyCards.map((card) => (
        <Card
          key={card.title}
          title={card.title}
          text={card.text}
          buttonText={card.buttonText}
          path={card.path}
        />
      ))}
    </div>
  </section>
      </main>
      </Layout>
    </>
  )
}
export default Dashboard
