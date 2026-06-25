import Layout from "../components/Layout";
import "../App.css";
import { useState } from "react";
import { createTrip } from "../services/tripService";
import { useNavigate } from "react-router-dom";

type FormData = {
  tripName: string;
  location: string;
  tripBudget: number;
  startedAt: string;
  notes: string;
};

function NewTrip() {

  const [formData, setFormData] = useState<FormData>({
    tripName: "",
    location: "",
    tripBudget: 0,
    startedAt: "",
    notes: "",
  });

  const navigate = useNavigate();
  
  function handleInputChange(
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    const { name, value } = event.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault();

  const payload = {
    tripName: formData.tripName,
    location: formData.location,
    tripBudget: formData.tripBudget,
    startedAt: formData.startedAt,
    notes: formData.notes,
  };

  try {
    const createdTrip = await createTrip(payload);
    console.log("Created trip:", createdTrip);
    navigate("/");
  } catch (error) {
    console.error("Failed to create trip:", error);
  }
}

  return (
    <Layout>
      <section>
        <h2 className="section-title">New Trip</h2>

        <form id="newTrip" className="entity-form" onSubmit={handleSubmit}>
          <label htmlFor="tripName">Trip Name</label>
          <input
            type="text"
            id="tripName"
            name="tripName"
            value={formData.tripName}
            onChange={handleInputChange}
            placeholder="Enter trip name"
            required
          />

          <label htmlFor="location">Location</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            placeholder="Enter location"
            required
          />

          <label htmlFor="tripBudget">Trip Budget</label>
          <input
            type="number"
            id="tripBudget"
            name="tripBudget"
            value={formData.tripBudget}
            onChange={handleInputChange}
            placeholder="Enter trip budget"
            required
          />

          <label htmlFor="startedAt">Start Date</label>
          <input
            type="date"
            id="startedAt"
            name="startedAt"
            value={formData.startedAt}
            onChange={handleInputChange}
            required
          />

          <label htmlFor="notes">Notes</label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={handleInputChange}
            rows={4}
            placeholder="Enter notes (optional)"
          />

          <button type="submit">Create Trip</button>
        </form>
      </section>
    </Layout>
  );

}

export default NewTrip;