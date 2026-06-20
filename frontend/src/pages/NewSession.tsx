import Layout from "../components/Layout";
import "../App.css";
import { useState } from "react";
import { createSession } from "../services/sessionService";
import { useNavigate } from "react-router-dom";

type FormData = {
  casino: string;
  startedAt: string;
  notes: string;
};

function NewSession() {

  const [formData, setFormData] = useState<FormData>({
    casino: "",
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
    casino: formData.casino,
    startedAt: formData.startedAt,
    notes: formData.notes,
  };

  try {
    const createdSession = await createSession(payload);
    console.log("Created session:", createdSession);
    navigate("/sessions/active");
  } catch (error) {
    console.error("Failed to create session:", error);
  }
}

  return (
    <Layout>
      <section>
        <h2 className="section-title">New Session</h2>

        <form id="newSession" className="entity-form" onSubmit={handleSubmit}>
          <label htmlFor="casino">Casino</label>
          <input
            type="text"
            id="casino"
            name="casino"
            value={formData.casino}
            onChange={handleInputChange}
            placeholder="Enter casino name"
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

          <button type="submit">Create Session</button>
        </form>
      </section>
    </Layout>
  );

}

export default NewSession;