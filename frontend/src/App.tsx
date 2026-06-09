import './App.css';
import Card from "./components/Card";

const activeCards = [
  { title: "Active Trip", text: "No active trip", buttonText: "View Trip" },
  { title: "Active Session", text: "No active session", buttonText: "View Session" },
  { title: "Active Games", text: "No active games", buttonText: "View Games" },
];

const newCards = [
  { title: "New Trip", text: "Create a new trip", buttonText: "Create Trip" },
  { title: "New Session", text: "Create a new session", buttonText: "Create Session" },
  { title: "New Game", text: "Create a new game", buttonText: "Create Game" },
];

function App() {

  return (
      <>

      <header className="main-header">
  <div className="brand-box">
    <h1>GambStats</h1>
  </div>
</header>

<hr />

<main className="page-content">
  <section>
    <h2 className="section-title">Active Now</h2>

    <div className="card-row">

      {activeCards.map((card) => (
    <Card
      key={card.title}
      title={card.title}
      text={card.text}
      buttonText={card.buttonText}
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
        />
      ))}
    </div>
  </section>
  <section>
    <h2 className="section-title">My History</h2>
  </section>
      </main>
    </>
  )
}

export default App
