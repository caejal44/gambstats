import './App.css';


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
      <div className="card">
        <div className="card-body">
          <h3 className="card-title">Active Trip</h3>
          <p className="card-text">No active trip</p>
          <button className="card-btn">View Trip</button>
        </div>
      </div>

      <div className="card">
        <div className="card-body">
          <h3 className="card-title">Active Session</h3>
          <p className="card-text">No active session</p>
          <button className="card-btn">View Session</button>
        </div>
      </div>

      <div className="card">
        <div className="card-body">
          <h3 className="card-title">Active Games</h3>
          <p className="card-text">No active games</p>
          <button className="card-btn">View Games</button>
        </div>
      </div>
    </div>
  </section>

  <section>
    <h2 className="section-title">Start Now</h2>

    <div className="card-row">
      <div className="card">
        <h3 className="card-title">New Trip</h3>
        <button className="card-btn">Create Trip</button>
      </div>

      <div className="card">
        <h3 className="card-title">New Session</h3>
        <button className="card-btn">Create Session</button>
      </div>

      <div className="card">
        <h3 className="card-title">New Game</h3>
        <button className="card-btn">Create Game</button>
      </div>
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
