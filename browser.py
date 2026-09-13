from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem, QLineEdit, QSplitter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Browser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        header_layout = QHBoxLayout()
        title_label = QLabel("Browser")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #ff6600;")
        header_layout.addWidget(title_label)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search...")
        search_input.setStyleSheet("""
            QLineEdit {
                background-color: #3a3a3a;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        header_layout.addWidget(search_input)
        
        main_layout.addLayout(header_layout)
        
        splitter = QSplitter(Qt.Vertical)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #1e1e1e;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
            }
            QTreeWidget::item {
                padding: 3px;
            }
            QTreeWidget::item:selected {
                background-color: #ff6600;
            }
            QTreeWidget::branch:selected {
                background-color: #ff6600;
            }
        """)
        
        self.populate_tree()
        
        splitter.addWidget(self.tree)
        
        self.preview_panel = QWidget()
        self.preview_panel.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 3px;
            }
        """)
        preview_layout = QVBoxLayout(self.preview_panel)
        
        preview_label = QLabel("Preview")
        preview_label.setFont(QFont("Arial", 12, QFont.Bold))
        preview_label.setStyleSheet("color: #ff6600;")
        preview_layout.addWidget(preview_label)
        
        self.preview_info = QLabel("Select an item to preview")
        self.preview_info.setStyleSheet("color: #aaa;")
        preview_layout.addWidget(self.preview_info)
        
        play_preview_btn = QPushButton("▶ Preview")
        play_preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
        preview_layout.addWidget(play_preview_btn)
        
        splitter.addWidget(self.preview_panel)
        splitter.setSizes([400, 200])
        
        main_layout.addWidget(splitter)
        
    def populate_tree(self):
        categories = [
            ("Packs", [
                ("Drums", ["Kick", "Snare", "HiHat", "Clap", "Tom", "Cymbal"]),
                ("Instruments", ["Bass", "Lead", "Pad", "Strings", "Brass"]),
                ("Effects", ["Reverb", "Delay", "Distortion", "Chorus", "Flanger"]),
                ("Samples", ["Vocals", "FX", "Loops", "One Shots"])
            ]),
            ("Projects", []),
            ("Plugins", [
                ("Synthesizers", ["3x Osc", "Sytrus", "Harmor", "Sakura"]),
                ("Effects", ["Fruity Reverb 2", "Fruity Delay 3", "Fruity Limiter", "Maximus"])
            ]),
            ("Recent Files", []),
            ("Favorite", [])
        ]
        
        for category, subcategories in categories:
            category_item = QTreeWidgetItem([category])
            category_item.setFont(0, QFont("Arial", 10, QFont.Bold))
            
            if subcategories:
                for subcat, items in subcategories:
                    subcat_item = QTreeWidgetItem([subcat])
                    subcat_item.setFont(0, QFont("Arial", 9))
                    
                    for item in items:
                        item_widget = QTreeWidgetItem([item])
                        subcat_item.addChild(item_widget)
                        
                    category_item.addChild(subcat_item)
                    
            self.tree.addTopLevelItem(category_item)
            
        self.tree.expandAll()