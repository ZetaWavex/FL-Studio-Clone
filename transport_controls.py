from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpinBox
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

class TransportControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.is_playing = False
        self.is_recording = False
        self.current_time = "00:00:00"
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border-bottom: 1px solid #444;
            }
        """)
        
        play_btn = QPushButton("▶")
        play_btn.setFixedSize(40, 30)
        play_btn.setStyleSheet(self.get_button_style("#00cc66"))
        play_btn.clicked.connect(self.toggle_play)
        layout.addWidget(play_btn)
        
        stop_btn = QPushButton("■")
        stop_btn.setFixedSize(40, 30)
        stop_btn.setStyleSheet(self.get_button_style("#ff3333"))
        stop_btn.clicked.connect(self.stop)
        layout.addWidget(stop_btn)
        
        record_btn = QPushButton("●")
        record_btn.setFixedSize(40, 30)
        record_btn.setStyleSheet(self.get_button_style("#ff0000"))
        record_btn.setCheckable(True)
        record_btn.clicked.connect(self.toggle_record)
        layout.addWidget(record_btn)
        
        layout.addSpacing(20)
        
        bpm_label = QLabel("BPM:")
        bpm_label.setStyleSheet("color: #ddd; font-weight: bold;")
        layout.addWidget(bpm_label)
        
        self.bpm_spin = QSpinBox()
        self.bpm_spin.setRange(20, 999)
        self.bpm_spin.setValue(140)
        self.bpm_spin.setFixedWidth(70)
        self.bpm_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3a3a3a;
                color: #ff6600;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 3px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.bpm_spin.valueChanged.connect(self.on_bpm_changed)
        layout.addWidget(self.bpm_spin)
        
        layout.addSpacing(20)
        
        self.time_label = QLabel("00:00:00")
        self.time_label.setStyleSheet("""
            QLabel {
                color: #ff6600;
                font-size: 16px;
                font-weight: bold;
                font-family: monospace;
            }
        """)
        layout.addWidget(self.time_label)
        
        layout.addStretch()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        
    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: #3a3a3a;
                color: {color};
                border: 1px solid #555;
                border-radius: 3px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #4a4a4a;
            }}
            QPushButton:pressed {{
                background-color: {color};
                color: #000;
            }}
        """
        
    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.timer.start(1000)
        else:
            self.timer.stop()
        self.update_status()
        
    def stop(self):
        self.is_playing = False
        self.timer.stop()
        self.current_time = "00:00:00"
        self.time_label.setText(self.current_time)
        self.update_status()
        
    def toggle_record(self):
        self.is_recording = not self.is_recording
        
    def update_time(self):
        parts = self.current_time.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        
        seconds += 1
        if seconds >= 60:
            seconds = 0
            minutes += 1
        if minutes >= 60:
            minutes = 0
            hours += 1
            
        self.current_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_label.setText(self.current_time)
        
    def on_bpm_changed(self, value):
        if self.parent_window:
            self.parent_window.bpm = value
            self.parent_window.update_statusbar()
            
    def update_status(self):
        if self.parent_window:
            self.parent_window.is_playing = self.is_playing
            self.parent_window.update_statusbar()