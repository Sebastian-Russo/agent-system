"""
Notes Tool
Save, read, list, and delete persistent notes

ANALOGY: A notebook on the agent's desk.
The agent can jot things down and look them up later.
Notes persist across questions within a session.
"""
import json
from pathlib import Path

NOTES_FILE = Path("results/notes.json")

def _load_notes():
    """Load notes from file"""
    if NOTES_FILE.exists():
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_notes(notes):
    """Save notes to file"""
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def save_note(title, content):
    """
    Save a note

    Input:  title="grocery list", content="milk, eggs, bread"
    Output: {"saved": "grocery list"}
    """
    notes = _load_notes()
    notes[title] = content
    _save_notes(notes)
    return {"saved": title}

def read_note(title):
    """
    Read a specific note

    Input:  title="grocery list"
    Output: {"title": "grocery list", "content": "milk, eggs, bread"}
    """
    notes = _load_notes()
    if title in notes:
        return {"title": title, "content": notes[title]}
    return {"error": f"Note '{title}' not found"}

def list_notes():
    """
    List all saved notes

    Output: {"notes": ["grocery list", "meeting notes"]}
    """
    notes = _load_notes()
    return {"notes": list(notes.keys())}

def delete_note(title):
    """
    Delete a note

    Input:  title="grocery list"
    Output: {"deleted": "grocery list"}
    """
    notes = _load_notes()
    if title in notes:
        del notes[title]
        _save_notes(notes)
        return {"deleted": title}
    return {"error": f"Note '{title}' not found"}
