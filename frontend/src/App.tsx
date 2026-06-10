import { useEffect, useState } from "react";
import "./App.css";

type Note = {
  id: number;
  title: string;
  body: string;
  tags: string[];
  created_at: string;
};

const API_BASE_URL = "http://localhost:8001";

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadNotes() {
      try {
        const response = await fetch(`${API_BASE_URL}/notes`);

        if (!response.ok) {
          throw new Error("Failed to load notes");
        }

        const data = await response.json();
        setNotes(data);
      } catch (error) {
        setErrorMessage("Could not load notes.");
      } finally {
        setIsLoading(false);
      }
    }

    loadNotes();
  }, []);

  return (
    <main className="app-shell">
      <h1>Mini Notes</h1>

      {isLoading && <p>Loading notes...</p>}

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      {!isLoading && !errorMessage && notes.length === 0 && (
        <p>No notes yet.</p>
      )}

      {!isLoading && !errorMessage && notes.length > 0 && (
        <ul className="notes-list">
          {notes.map((note) => (
            <li key={note.id} className="note-card">
              <h2>{note.title}</h2>
              <p>{note.body}</p>

              {note.tags.length > 0 && (
                <div className="tag-list">
                  {note.tags.map((tag) => (
                    <span key={tag} className="tag">
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              <time>{new Date(note.created_at).toLocaleString()}</time>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}

export default App;