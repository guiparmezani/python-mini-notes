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
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [tagsText, setTagsText] = useState("");
  const [formError, setFormError] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [deletingNoteId, setDeletingNoteId] = useState<number | null>(null);
  const [searchText, setSearchText] = useState("");

  useEffect(() => {
    loadNotes();
  }, []);

  async function loadNotes(searchQuery = "") {
    try {
      setIsLoading(true);
      setErrorMessage("");
  
      const url = new URL(`${API_BASE_URL}/notes`);
  
      if (searchQuery.trim()) {
        url.searchParams.set("q", searchQuery.trim());
      }
  
      const response = await fetch(url);
  
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

  async function handleCreateNote(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
  
    const trimmedTitle = title.trim();
    const trimmedBody = body.trim();
    const tags = tagsText
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean);
  
    if (!trimmedTitle) {
      setFormError("Title is required.");
      return;
    }
  
    if (!trimmedBody) {
      setFormError("Body is required.");
      return;
    }
  
    try {
      setIsSaving(true);
      setFormError("");
  
      const response = await fetch(`${API_BASE_URL}/notes`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: trimmedTitle,
          body: trimmedBody,
          tags,
        }),
      });
  
      if (!response.ok) {
        throw new Error("Failed to create note");
      }
  
      const createdNote = await response.json();
  
      setNotes((currentNotes) => [createdNote, ...currentNotes]);
      setTitle("");
      setBody("");
      setTagsText("");
    } catch (error) {
      setFormError("Could not save note.");
    } finally {
      setIsSaving(false);
    }
  }

  async function handleDeleteNote(noteId: number) {
    try {
      setDeletingNoteId(noteId);
  
      const response = await fetch(`${API_BASE_URL}/notes/${noteId}`, {
        method: "DELETE",
      });
  
      if (!response.ok) {
        throw new Error("Failed to delete note");
      }
  
      setNotes((currentNotes) =>
        currentNotes.filter((note) => note.id !== noteId),
      );
    } catch (error) {
      setErrorMessage("Could not delete note.");
    } finally {
      setDeletingNoteId(null);
    }
  }

  function handleSearchSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    loadNotes(searchText);
  }

  function handleClearSearch() {
    setSearchText("");
    loadNotes();
  }

  return (
    <main className="app-shell">
      <h1>Mini Notes</h1>
      <form className="note-form" onSubmit={handleCreateNote}>
        <label>
          Title
          <input
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="Study Python"
          />
        </label>

        <label>
          Body
          <textarea
            value={body}
            onChange={(event) => setBody(event.target.value)}
            placeholder="Practice classes, SQL, and APIs"
          />
        </label>

        <label>
          Tags
          <input
            value={tagsText}
            onChange={(event) => setTagsText(event.target.value)}
            placeholder="python, sql, api"
          />
        </label>

        {formError && <p className="error-message">{formError}</p>}

        <button type="submit" disabled={isSaving}>
          {isSaving ? "Saving..." : "Save note"}
        </button>
      </form>

      {isLoading && <p>Loading notes...</p>}

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      {!isLoading && !errorMessage && notes.length === 0 && (
        <p>No notes yet.</p>
      )}

    <form className="search-form" onSubmit={handleSearchSubmit}>
      <input
        value={searchText}
        onChange={(event) => setSearchText(event.target.value)}
        placeholder="Search notes..."
      />

      <button type="submit">Search</button>

      {searchText && (
        <button type="button" onClick={handleClearSearch}>
          Clear
        </button>
      )}
    </form>

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
              <button
                className="delete-button"
                type="button"
                disabled={deletingNoteId === note.id}
                onClick={() => handleDeleteNote(note.id)}
              >
                {deletingNoteId === note.id ? "Deleting..." : "Delete"}
              </button>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}

export default App;