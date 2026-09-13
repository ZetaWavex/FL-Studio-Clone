from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSlider, QScrollArea, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QFont

class MixerTrack:
    def __init__(self, name):
        self.name = name
        self.volume = 75
        self.pan = 0
        self.muted = False
        self.solo = False
        self.fader_level = 0.0
        self.effects = []

class Mixer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.tracks = []
        self.track_count = 12
        self.init_ui()
        self.add_default_tracks()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        header_layout = QHBoxLayout()
        title_label = QLabel("Mixer")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #ff6600;")
        header_layout.addWidget(title_label)
        
        add_track_btn = QPushButton("+ Add Track")
        add_track_btn.setStyleSheet("""
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
        add_track_btn.clicked.connect(self.add_track)
        header_layout.addWidget(add_track_btn)
        
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444;
                background-color: #1e1e1e;
            }
            QScrollBar:horizontal {
                background-color: #2a2a2a;
                height: 12px;
            }
            QScrollBar::handle:horizontal {
                background-color: #555;
                border-radius: 6px;
            }
        """)
        
        self.tracks_widget = QWidget()
        self.tracks_layout = QHBoxLayout(self.tracks_widget)
        self.tracks_layout.setContentsMargins(5, 5, 5, 5)
        self.tracks_layout.setSpacing(5)
        self.tracks_layout.setAlignment(Qt.AlignLeft)
        
        scroll_area.setWidget(self.tracks_widget)
        main_layout.addWidget(scroll_area)
        
    def add_default_tracks(self):
        default_names = ["Master", "Kick", "Snare", "HiHat", "Bass", "Lead", "Pad", "FX", "Vocals", "Guitar", "Piano", "Drums"]
        for name in default_names:
            self.add_track(name)
            
    def add_track(self, name=None):
        if not name:
            name = f"Track {len(self.tracks) + 1}"
            
        track = MixerTrack(name)
        self.tracks.append(track)
        
        track_widget = self.create_track_widget(track)
        self.tracks_layout.addWidget(track_widget)
        
    def create_track_widget(self, track):
        frame = QFrame()
        frame.setFixedWidth(100)
        frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 4px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        name_label = QLabel(track.name)
        name_label.setStyleSheet("color: #ddd; font-weight: bold; font-size: 10px;")
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        
        meter = LevelMeter(track)
        meter.setFixedHeight(150)
        layout.addWidget(meter)
        
        fader = QSlider(Qt.Vertical)
        fader.setRange(0, 100)
        fader.setValue(track.volume)
        fader.setFixedHeight(120)
        fader.setStyleSheet("""
            QSlider::groove:vertical {
                border: 1px solid #555;
                width: 8px;
                background: #3a3a3a;
                border-radius: 4px;
            }
            QSlider::handle:vertical {
                background: #ff6600;
                height: 14px;
                margin: -3px 0;
                border-radius: 7px;
            }
        """)
        fader.valueChanged.connect(lambda value, tr=track: setattr(tr, 'volume', value))
        layout.addWidget(fader)
        
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(3)
        
        mute_btn = QPushButton("M")
        mute_btn.setFixedSize(25, 20)
        mute_btn.setCheckable(True)
        mute_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                font-size: 9px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #ff3333;
                color: white;
            }
        """)
        mute_btn.clicked.connect(lambda checked, tr=track: setattr(tr, 'muted', checked))
        controls_layout.addWidget(mute_btn)
        
        solo_btn = QPushButton("S")
        solo_btn.setFixedSize(25, 20)
        solo_btn.setCheckable(True)
        solo_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                font-size: 9px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #ffcc00;
                color: black;
            }
        """)
        solo_btn.clicked.connect(lambda checked, tr=track: setattr(tr, 'solo', checked))
        controls_layout.addWidget(solo_btn)
        
        layout.addLayout(controls_layout)
        
        volume_label = QLabel(f"{track.volume}%")
        volume_label.setStyleSheet("color: #aaa; font-size: 9px;")
        volume_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(volume_label)
        
        return frame
        
    def reset_all(self):
        self.tracks.clear()
        while self.tracks_layout.count():
            child = self.tracks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class LevelMeter(QFrame):
    def __init__(self, track):
        super().__init__()
        self.track = track
        self.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 3px;")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.fillRect(self.rect(), QColor("#1e1e1e"))
        
        meter_width = self.width() - 10
        meter_height = self.height() - 10
        fill_height = (self.track.volume / 100) * meter_height
        
        x = 5
        y = self.height() - 5 - fill_height
        
        if self.track.volume > 80:
            color = QColor("#ff3333")
        elif self.track.volume > 60:
            color = QColor("#ffcc00")
        else:
            color = QColor("#00ff00")
            
        painter.fillRect(int(x), int(y), int(meter_width), int(fill_height), color)
        
        painter.setPen(QPen(QColor("#444"), 1))
        painter.drawRect(5, 5, meter_width, meter_height)