import os
import uuid
from datetime import datetime
import yaml

class NoteManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.notes_path = os.path.join(base_path, 'notes')
        os.makedirs(self.notes_path, exist_ok=True)

    def save_note(self, content, title="Untitled", category="General", model="whisper-tiny", language="en"):
        note_id = str(uuid.uuid4())
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        frontmatter = {
            'id': note_id,
            'title': title,
            'created_at': now,
            'updated_at': now,
            'model': model,
            'language': language,
            'category': category
        }

        category_dir = os.path.join(self.notes_path, category)
        os.makedirs(category_dir, exist_ok=True)

        file_path = os.path.join(category_dir, f"{note_id}.md")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.dump(frontmatter, f, default_flow_style=False)
            f.write("---\n\n")
            f.write("# Transcription\n")
            f.write(content)

        return file_path

    def load_note(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---', 2)
        if len(parts) >= 3:
            metadata = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return metadata, body
        return None, content

    def list_categories(self):
        return [d for d in os.listdir(self.notes_path) if os.path.isdir(os.path.join(self.notes_path, d))]

    def list_notes_in_category(self, category):
        cat_path = os.path.join(self.notes_path, category)
        if not os.path.exists(cat_path):
            return []
        return [os.path.join(cat_path, f) for f in os.listdir(cat_path) if f.endswith('.md')]
