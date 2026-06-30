import { useParams } from "react-router-dom";
import Layout from "../components/Layout";
import "../App.css";
import { useState } from "react";
import { editGame } from "../services/gameService";
import { useNavigate } from "react-router-dom";
import { getGameById } from "../services/gameService";
import { useEffect } from "react";
import { toDateTimeLocal } from "../utils/formatters";

type FormData = {
 gameName: string;
 gameType: string;
 cashIn: string;
 cashOut: string;
 startedAt: string;
 endedAt: string;
 notes: string;
 freeplayUsed: string;
};

function EditGames() {
  const { gameId } = useParams();

  const [formData, setFormData] = useState<FormData>({
    gameName: "",
    gameType: "",
    cashIn: "",
    cashOut: "",
    startedAt: "",
    endedAt: "",
    notes: "",
    freeplayUsed: "",
  });

  useEffect(() => {
  async function loadGame() {
    if (!gameId) return;

    const game = await getGameById(gameId);

    setFormData({
      gameName: game.game_name,
      gameType: game.game_type,
      cashIn: String(game.cash_in),
      cashOut: game.cash_out === null ? "" : String(game.cash_out),
      startedAt: toDateTimeLocal(game.started_at),
      endedAt: toDateTimeLocal(game.ended_at),
      notes: game.notes ?? "",
      freeplayUsed: game.freeplay_used === null ? "" : String(game.freeplay_used),
    });
  }

  loadGame();
}, [gameId]);

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
    cashIn: formData.cashIn === "" ? null : Number(formData.cashIn),
    cashOut: formData.cashOut === "" ? null : Number(formData.cashOut),
    startedAt: formData.startedAt || null,
    endedAt: formData.endedAt || null,
    notes: formData.notes,
    freeplayUsed: formData.freeplayUsed === "" ? null : Number(formData.freeplayUsed),
  };

  try {
    const editedGame = await editGame(gameId!, payload);
    console.log("Edited game:", editedGame);
    navigate("/");
  } catch (error) {
    console.error("Failed to edit game:", error);
  }
}
  return (
    <Layout>
      <h2 className="section-title">Edit Game</h2>
      <form id="newGame" className="entity-form" onSubmit={handleSubmit}>
          <label htmlFor="gameName">Game Name</label>
          <input
            type="text"
            id="gameName"
            name="gameName"
            value={formData.gameName}
            onChange={handleInputChange}
          />

          <label htmlFor="gameType">Game Type</label>
          <input
            type="text"
            id="gameType"
            name="gameType"
            value={formData.gameType}
            onChange={handleInputChange}
            placeholder="Enter game type"
          />

          <label htmlFor="cashIn">Cash In</label>
          <input
            type="number"
            id="cashIn"
            name="cashIn"
            value={formData.cashIn}
            onChange={handleInputChange}
            placeholder="Enter cash in amount"
          />

          <label htmlFor="cashOut">Cash Out</label>
          <input
            type="number"
            id="cashOut"
            name="cashOut"
            value={formData.cashOut}
            onChange={handleInputChange}
            placeholder="Enter cash out amount"
          />

          <label htmlFor="startedAt">Start Date</label>
          <input
            type="datetime-local"
            id="startedAt"
            name="startedAt"
            value={formData.startedAt}
            onChange={handleInputChange}
          />

          <label htmlFor="endeddAt">End Date</label>
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

          <label htmlFor="freeplayUsed">Freeplay Used</label>
          <input
            type="number"
            id="freeplayUsed"
            name="freeplayUsed"
            value={formData.freeplayUsed}
            onChange={handleInputChange}
            placeholder="Enter freeplay amount (optional)"
          />

          <button type="submit">Submit Changes</button>
        </form>
    </Layout>
  );
}

export default EditGames;