import { useParams } from "react-router-dom";
import Layout from "../components/Layout";
import "../App.css";
import { useState } from "react";
import { editSession } from "../services/sessionService";
import { useNavigate } from "react-router-dom";
import { getSessionById } from "../services/sessionService";
import { useEffect } from "react";
import { toDateTimeLocal } from "../utils/formatters";


type FormData = {
 casino: string
 startedAt: string;
 endedAt: string;
 notes: string;
};

function EditSession() {
  const { sessionId } = useParams();

  const [formData, setFormData] = useState<FormData>({
    casino: "",
    startedAt: "",
    endedAt: "",
    notes: "",
  });

  useEffect(() => {
  async function loadSession() {
    if (!sessionId) return;

    const session = await getSessionById(sessionId);

    setFormData({
      casino: session.casino,
      startedAt: toDateTimeLocal(session.started_at),
      endedAt: toDateTimeLocal(session.ended_at),
      notes: session.notes ?? "",
    });
  }

  loadSession();
}, [sessionId]);

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
    startedAt: formData.startedAt || null,
    endedAt: formData.endedAt || null,
    notes: formData.notes
  };

  try {
    const editedSession = await editSession(sessionId!, payload);
    console.log("Edited session:", editedSession);
    navigate("/");
  } catch (error) {
    console.error("Failed to edit session:", error);
  }
}
  return (
    <Layout>
      <h2 className="section-title">Edit Session</h2>
      <form id="newSession" className="entity-form" onSubmit={handleSubmit}>
          <label htmlFor="casino">Casino</label>
          <input
            type="text"
            id="casino"
            name="casino"
            value={formData.casino}
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

          <label htmlFor="endeddAt">End Date/Time</label>
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

export default EditSession;