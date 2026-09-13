from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QFont

class Pattern:
    def __init__(self, name):
        self.name = name
        self.clips = []
        self.color = "#ff6600"

class Playlist(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.patterns = []
        self.tracks = 8
        self.steps = 64
        self.cell_width = 60
        self.cell_height = 40
        self.init_ui()
        self.add_default_patterns()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        header_layout = QHBoxLayout()
        title_label = QLabel("Playlist")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #ff6600;")
        header_layout.addWidget(title_label)
        
        add_pattern_btn = QPushButton("+ Add Pattern")
        add_pattern_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
        add_pattern_btn.clicked.connect(self.add_pattern)
        header_layout.addWidget(add_pattern_btn)
        
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444;
                background-color: #1e1e1e;
            }
        """)
        
        self.playlist_view = PlaylistView(self)
        scroll_area.setWidget(self.playlist_view)
        main_layout.addWidget(scroll_area)
        
    def add_default_patterns(self):
        colors = ["#ff6600", "#00ccff", "#ff0066", "#66ff00"]
        for i in range(4):
            pattern = Pattern(f"Pattern {i+1}")
            pattern.color = colors[i % len(colors)]
            self.patterns.append(pattern)
            
    def add_pattern(self):
        pattern = Pattern(f"Pattern {len(self.patterns) + 1}")
        pattern.color = ["#ff6600", "#00ccff", "#ff0066", "#66ff00", "#cc66ff", "#ffcc00"][len(self.patterns) % 6]
        self.patterns.append(pattern)
        self.playlist_view.update()
        
    def clear_all(self):
        self.patterns.clear()
        self.playlist_view.update()

class PlaylistView(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.playlist = parent
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border: 1px solid #444;
            }
        """)
        self.setMinimumSize(800, 400)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.fillRect(self.rect(), QColor("#1e1e1e"))
        
        self.draw_grid(painter)
        self.draw_track_labels(painter)
        self.draw_patterns(painter)
        
    def draw_grid(self, painter):
        cell_width = self.playlist.cell_width
        cell_height = self.playlist.cell_height
        
        for i in range(self.playlist.steps + 1):
            x = i * cell_width + 100
            if x < 100 or x > self.width():
                continue
                
            is_group = i % 8 == 0
            color = QColor("#444") if is_group else QColor("#2a2a2a")
            pen = QPen(color, 1 if is_group else 0.5)
            painter.setPen(pen)
            painter.drawLine(x, 0, x, self.height())
            
        for i in range(self.playlist.tracks + 1):
            y = i * cell_height
            painter.setPen(QPen(QColor("#444"), 1))
            painter.drawLine(100, y, self.width(), y)
            
    def draw_track_labels(self, painter):
        cell_height = self.playlist.cell_height
        
        for i in range(self.playlist.tracks):
            y = i * cell_height
            
            painter.fillRect(0, y, 100, cell_height, QColor("#2a2a2a"))
            painter.setPen(QColor("#ddd"))
            painter.setFont(QFont("Arial", 9))
            painter.drawText(10, y + cell_height // 2 + 4, f"Track {i+1}")
            
            painter.setPen(QColor("#444"))
            painter.drawLine(100, y + cell_height, self.width(), y + cell_height)
            
    def draw_patterns(self, painter):
        cell_width = self.playlist.cell_width
        cell_height = self.playlist.cell_height
        
        for pattern in self.playlist.patterns:
            for clip in pattern.clips:
                track = clip['track']
                start = clip['start']
                length = clip['length']
                
                x = start * cell_width + 100
                y = track * cell_height
                w = length * cell_width
                h = cell_height - 2
                
                color = QColor(pattern.color)
                painter.fillRect(int(x), int(y + 1), int(w), int(h), color)
                
                painter.setPen(QPen(color.darker(150), 1))
                painter.drawRect(int(x), int(y + 1), int(w), int(h))
                
                painter.setPen(QColor("#fff"))
                painter.setFont(QFont("Arial", 8, QFont.Bold))
                painter.drawText(int(x) + 5, int(y) + cell_height // 2 + 3, pattern.name)