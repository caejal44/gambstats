import { useParams } from "react-router-dom";
import Layout from "../components/Layout";
import "../App.css";
import { useState } from "react";
import { editTrip } from "../services/tripService";
import { useNavigate } from "react-router-dom";
import { getTripById } from "../services/tripService";
import { useEffect } from "react";
import { toDateTimeLocal } from "../utils/formatters";


type FormData = {
 tripName: string;
 location: string;
 tripBudget: string;
 startedAt: string;
 endedAt: string;
 notes: string;
};

function EditTrip() {
  const { tripId } = useParams();

  const [formData, setFormData] = useState<FormData>({
    tripName: "",
    location:"",
    tripBudget:"",
    startedAt: "",
    endedAt: "",
    notes: "",
  });

  useEffect(() => {
  async function loadTrip() {
    if (!tripId) return;

    const trip = await getTripById(tripId);

    setFormData({
      tripName: trip.trip_name,
      location: trip.location,
      tripBudget: String(trip.trip_budget),
      startedAt: toDateTimeLocal(trip.started_at),
      endedAt: toDateTimeLocal(trip.ended_at),
      notes: trip.notes ?? "",
    });
  }

  loadTrip();
}, [tripId]);

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
    tripBudget: formData.tripBudget === "" ? null : Number(formData.tripBudget),
    startedAt: formData.startedAt || null,
    endedAt: formData.endedAt || null,
    notes: formData.notes
  };

  try {
    const editedTrip = await editTrip(tripId!, payload);
    console.log("Edited trip:", editedTrip);
    navigate("/");
  } catch (error) {
    console.error("Failed to edit trip:", error);
  }
}
  return (
    <Layout>
      <h2 className="section-title">Edit Trip</h2>
      <form id="newTrip" className="entity-form" onSubmit={handleSubmit}>
          <label htmlFor="tripName">Trip Name</label>
          <input
            type="text"
            id="tripName"
            name="tripName"
            value={formData.tripName}
            onChange={handleInputChange}
          />

          <label htmlFor="location">Location</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
          />

          <label htmlFor="tripBudget">Trip Budget</label>
          <input
            type="number"
            id="tripBudget"
            name="tripBudget"
            value={formData.tripBudget}
            onChange={handleInputChange}
          />

          <label htmlFor="startedAt">Start Date/Time</label>
          <input
            type="datetime-local"
            id="startedAt"
            name="startedAt"
            value={formData.startedAt}
            onChange={handleInputChange}
          />

          <label htmlFor="endedAt">End Date/Time</label>
          <input
            type="datetime-local"
            id="endedAt"
            name="endedAt"
            value={formData.endedAt}
            onChange={handleInputChange}
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

          <button type="submit">Submit Changes</button>
        </form>
    </Layout>
  );
}

export default EditTrip;