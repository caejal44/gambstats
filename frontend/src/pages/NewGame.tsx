import Layout from "../components/Layout";
import "../App.css";
import { useState } from "react";
import { createGame } from "../services/gameService";
import { useNavigate } from "react-router-dom";

type FormData = {
  gameName: string;
  gameType: string;
  cashIn: number;
  startedAt: string;
  notes: string;
  freeplayUsed: number;
};

function NewGame() {

  const [formData, setFormData] = useState<FormData>({
    gameName: "",
    gameType: "",
    cashIn: 0,
    startedAt: "",
    notes: "",
    freeplayUsed: 0,
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
    gameName: formData.gameName,
    gameType: formData.gameType,
    cashIn: formData.cashIn,
    startedAt: formData.startedAt,
    notes: formData.notes,
    freeplayUsed: formData.freeplayUsed
  };

  try {
    const createdGame = await createGame(payload);
    console.log("Created game:", createdGame);
    navigate("/games/active");
  } catch (error) {
    console.error("Failed to create game:", error);
  }
}

  return (
    <Layout>
      <section>
        <h2 className="section-title">New Game</h2>

        <form id="newGame" className="entity-form" onSubmit={handleSubmit}>
          <label htmlFor="gameName">Game Name</label>
          <input
            type="text"
            id="gameName"
            name="gameName"
            value={formData.gameName}
            onChange={handleInputChange}
            placeholder="Enter game name"
            required
          />

          <label htmlFor="gameType">Game Type</label>
          <input
            type="text"
            id="gameType"
            name="gameType"
            value={formData.gameType}
            onChange={handleInputChange}
            placeholder="Enter game type"
            required
          />

          <label htmlFor="cashIn">Cash In</label>
          <input
            type="number"
            id="cashIn"
            name="cashIn"
            value={formData.cashIn}
            onChange={handleInputChange}
            placeholder="Enter cash in amount"
            required
          />

          <label htmlFor="startedAt">Start Date</label>
          <input
            type="date"
            id="startedAt"
            name="startedAt"
            value={formData.startedAt}
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

          <label htmlFor="freeplayUsed">Freeplay Used</label>
          <input
            type="number"
            id="freeplayUsed"
            name="freeplayUsed"
            value={formData.freeplayUsed}
            onChange={handleInputChange}
            placeholder="Enter freeplay amount (optional)"
          />

          <button type="submit">Create Game</button>
        </form>
      </section>
    </Layout>
  );

}

export default NewGame;