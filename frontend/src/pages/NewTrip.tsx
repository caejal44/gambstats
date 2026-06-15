import Layout from "../components/Layout";
import '../App.css';



function NewTrip() {
  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault();

  console.log("Trip form submitted");
}
  return (
    <Layout>
      <section>
        <h2 className="section-title">New Trip</h2>
        <form id="newTrip" className="trip-form" onSubmit={handleSubmit}>
          <label htmlFor="tripName">Trip Name</label>
          <input type="text" id="tripName" name="tripName" placeholder="Enter trip name" required/>
          <label htmlFor="location">Location</label>
          <input type="text" id="location" name="location" placeholder="Enter location" required/>
          <label htmlFor="tripBudget">Trip Budget</label>
          <input type="number" id="tripBudget" name="tripBudget" placeholder="Enter trip budget" required/>
          <label htmlFor="startedAt">Start Date</label>
          <input type="date" id="startedAt" name="startedAt" placeholder="Enter start date" required/>
          <label htmlFor="notes">Notes</label>
          <textarea id="notes" name="notes" rows={4} placeholder="Enter notes (optional)"></textarea> 
        <button type="submit">
            Create Trip
        </button>
      </form>
      </section>
    </Layout>
  );
}

export default NewTrip;