from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea, QSpinBox
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
import math

class PianoRoll(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.notes = []
        self.grid_width = 16
        self.grid_height = 128
        self.cell_width = 40
        self.cell_height = 12
        self.scroll_offset_x = 0
        self.scroll_offset_y = 0
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        header_layout = QHBoxLayout()
        title_label = QLabel("Piano Roll")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #ff6600;")
        header_layout.addWidget(title_label)
        
        snap_label = QLabel("Snap:")
        snap_label.setStyleSheet("color: #ddd;")
        header_layout.addWidget(snap_label)
        
        self.snap_spin = QSpinBox()
        self.snap_spin.setRange(1, 8)
        self.snap_spin.setValue(1)
        self.snap_spin.setFixedWidth(60)
        self.snap_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3a3a3a;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 3px;
            }
        """)
        header_layout.addWidget(self.snap_spin)
        
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet("""
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
        clear_btn.clicked.connect(self.clear_notes)
        header_layout.addWidget(clear_btn)
        
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        self.piano_roll_view = PianoRollView(self)
        main_layout.addWidget(self.piano_roll_view)
        
    def add_note(self, note, start_step, length, velocity=100):
        self.notes.append({
            'note': note,
            'start': start_step,
            'length': length,
            'velocity': velocity
        })
        
    def clear_notes(self):
        self.notes.clear()
        self.piano_roll_view.update()
        
    def get_note_color(self, note):
        note_in_octave = note % 12
        colors = [
            "#ff6600", "#ff8833", "#ffaa66", "#ffcc99",
            "#00ccff", "#33ddff", "#66eeff", "#99ffff",
            "#ff0066", "#ff3388", "#ff66aa", "#ff99cc"
        ]
        return colors[note_in_octave]
        
    def is_black_key(self, note):
        note_in_octave = note % 12
        return note_in_octave in [1, 3, 6, 8, 10]

class PianoRollView(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.piano_roll = parent
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border: 1px solid #444;
            }
        """)
        self.setMinimumHeight(400)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.fillRect(self.rect(), QColor("#1e1e1e"))
        
        self.draw_grid(painter)
        self.draw_piano_keys(painter)
        self.draw_notes(painter)
        
    def draw_grid(self, painter):
        cell_width = self.piano_roll.cell_width
        cell_height = self.piano_roll.cell_height
        offset_x = self.piano_roll.scroll_offset_x
        offset_y = self.piano_roll.scroll_offset_y
        
        for i in range(self.piano_roll.grid_width + 1):
            x = i * cell_width - offset_x + 50
            if x < 50 or x > self.width():
                continue
                
            is_beat = i % 4 == 0
            color = QColor("#444") if is_beat else QColor("#333")
            pen = QPen(color, 1 if is_beat else 0.5)
            painter.setPen(pen)
            painter.drawLine(x, 0, x, self.height())
            
        for i in range(self.piano_roll.grid_height + 1):
            y = i * cell_height - offset_y
            if y < 0 or y > self.height():
                continue
                
            note = self.piano_roll.grid_height - 1 - i
            is_black = self.piano_roll.is_black_key(note)
            is_c = note % 12 == 0
            
            if is_c:
                color = QColor("#555")
            elif is_black:
                color = QColor("#2a2a2a")
            else:
                color = QColor("#333")
                
            painter.setPen(QPen(color, 1 if is_c else 0.5))
            painter.drawLine(50, y, self.width(), y)
            
    def draw_piano_keys(self, painter):
        cell_height = self.piano_roll.cell_height
        offset_y = self.piano_roll.scroll_offset_y
        
        for i in range(self.piano_roll.grid_height):
            y = i * cell_height - offset_y
            if y < 0 or y > self.height():
                continue
                
            note = self.piano_roll.grid_height - 1 - i
            is_black = self.piano_roll.is_black_key(note)
            
            if is_black:
                painter.fillRect(0, y, 50, cell_height, QColor("#1a1a1a"))
            else:
                painter.fillRect(0, y, 50, cell_height, QColor("#2a2a2a"))
                
            if note % 12 == 0:
                octave = note // 12
                painter.setPen(QColor("#ddd"))
                painter.setFont(QFont("Arial", 8))
                painter.drawText(5, y + cell_height - 2, f"C{octave}")
                
            painter.setPen(QColor("#444"))
            painter.drawLine(50, y, self.width(), y)
            
    def draw_notes(self, painter):
        cell_width = self.piano_roll.cell_width
        cell_height = self.piano_roll.cell_height
        offset_x = self.piano_roll.scroll_offset_x
        offset_y = self.piano_roll.scroll_offset_y
        
        for note_data in self.piano_roll.notes:
            note = note_data['note']
            start = note_data['start']
            length = note_data['length']
            
            x = start * cell_width - offset_x + 50
            y = (self.piano_roll.grid_height - 1 - note) * cell_height - offset_y
            w = length * cell_width
            h = cell_height - 1
            
            if x + w < 50 or x > self.width() or y + h < 0 or y > self.height():
                continue
                
            color = QColor(self.piano_roll.get_note_color(note))
            painter.fillRect(int(x), int(y), int(w), int(h), color)
            
            painter.setPen(QPen(color.darker(150), 1))
            painter.drawRect(int(x), int(y), int(w), int(h))