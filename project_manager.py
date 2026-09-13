import json
import os
from datetime import datetime

class ProjectManager:
    def __init__(self):
        self.current_project = None
        self.project_path = None
        
    def create_new_project(self):
        self.current_project = {
            'version': '1.0.0',
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'bpm': 140,
            'time_signature': '4/4',
            'channels': [],
            'patterns': [],
            'playlist': [],
            'mixer_tracks': [],
            'metadata': {
                'name': 'Untitled',
                'author': '',
                'description': ''
            }
        }
        self.project_path = None
        return self.current_project
    
    def save_project(self, project_data, filepath=None):
        if filepath:
            self.project_path = filepath
        
        if not self.project_path:
            self.project_path = 'untitled.flp'
        
        project_data['modified'] = datetime.now().isoformat()
        
        with open(self.project_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)
        
        return self.project_path
    
    def load_project(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Project file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            self.current_project = json.load(f)
        
        self.project_path = filepath
        return self.current_project
    
    def export_as_json(self, project_data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def get_recent_projects(self, max_count=10):
        recent_file = os.path.join(os.path.expanduser('~'), '.flstudio_recent.json')
        
        if not os.path.exists(recent_file):
            return []
        
        with open(recent_file, 'r') as f:
            recent = json.load(f)
        
        return recent[:max_count]
    
    def add_to_recent(self, filepath):
        recent_file = os.path.join(os.path.expanduser('~'), '.flstudio_recent.json')
        
        recent = []
        if os.path.exists(recent_file):
            with open(recent_file, 'r') as f:
                recent = json.load(f)
        
        if filepath in recent:
            recent.remove(filepath)
        
        recent.insert(0, filepath)
        recent = recent[:20]
        
        with open(recent_file, 'w') as f:
            json.dump(recent, f, indent=2)