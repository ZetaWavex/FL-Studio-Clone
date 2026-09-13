from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QSlider, QFrame, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette

class Channel:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.volume = 75
        self.pan = 0
        self.muted = False
        self.steps = [False] * 16
        
class ChannelRack(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.channels = []
        self.step_count = 16
        self.init_ui()
        self.add_default_channels()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        header_layout = QHBoxLayout()
        title_label = QLabel("Channel Rack")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #ff6600;")
        header_layout.addWidget(title_label)
        
        add_channel_btn = QPushButton("+ Add Channel")
        add_channel_btn.setStyleSheet("""
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
        add_channel_btn.clicked.connect(self.add_channel)
        header_layout.addWidget(add_channel_btn)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444;
                background-color: #1e1e1e;
            }
            QScrollBar:vertical {
                background-color: #2a2a2a;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                border-radius: 6px;
            }
        """)
        
        self.channels_widget = QWidget()
        self.channels_layout = QVBoxLayout(self.channels_widget)
        self.channels_layout.setContentsMargins(0, 0, 0, 0)
        self.channels_layout.setSpacing(2)
        
        scroll_area.setWidget(self.channels_widget)
        main_layout.addWidget(scroll_area)
        
    def add_default_channels(self):
        colors = ["#ff6600", "#00ccff", "#ff0066", "#66ff00", "#cc66ff", "#ffcc00"]
        default_names = ["Kick", "Snare", "HiHat", "Clap", "Bass", "Lead"]
        
        for name, color in zip(default_names, colors):
            self.add_channel(name, color)
            
    def add_channel(self, name=None, color="#ff6600"):
        if not name:
            name = f"Channel {len(self.channels) + 1}"
            
        channel = Channel(name, color)
        self.channels.append(channel)
        
        channel_widget = self.create_channel_widget(channel)
        self.channels_layout.addWidget(channel_widget)
        
    def create_channel_widget(self, channel):
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-left: 3px solid {channel.color};
                border-radius: 3px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(5, 3, 5, 3)
        layout.setSpacing(8)
        
        name_label = QLabel(channel.name)
        name_label.setStyleSheet("color: #ddd; font-weight: bold;")
        name_label.setFixedWidth(80)
        layout.addWidget(name_label)
        
        mute_btn = QPushButton("M")
        mute_btn.setFixedSize(25, 25)
        mute_btn.setCheckable(True)
        mute_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #ff3333;
                color: white;
            }
        """)
        mute_btn.clicked.connect(lambda checked, ch=channel: self.toggle_mute(ch, checked))
        layout.addWidget(mute_btn)
        
        volume_slider = QSlider(Qt.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(channel.volume)
        volume_slider.setFixedWidth(80)
        volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 8px;
                background: #3a3a3a;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ff6600;
                width: 14px;
                margin: -3px 0;
                border-radius: 7px;
            }
        """)
        volume_slider.valueChanged.connect(lambda value, ch=channel: setattr(ch, 'volume', value))
        layout.addWidget(volume_slider)
        
        steps_layout = QHBoxLayout()
        steps_layout.setSpacing(2)
        
        for i in range(self.step_count):
            step_btn = QPushButton()
            step_btn.setFixedSize(25, 30)
            step_btn.setCheckable(True)
            
            is_group = (i // 4) % 2 == 0
            bg_color = "#3a3a3a" if is_group else "#2a2a2a"
            
            step_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    border: 1px solid #555;
                    border-radius: 2px;
                }}
                QPushButton:checked {{
                    background-color: {channel.color};
                    border: 1px solid {channel.color};
                }}
                QPushButton:hover {{
                    border: 1px solid #777;
                }}
            """)
            
            step_btn.clicked.connect(lambda checked, idx=i, ch=channel: self.toggle_step(ch, idx, checked))
            steps_layout.addWidget(step_btn)
            
        layout.addLayout(steps_layout)
        
        return frame
        
    def toggle_step(self, channel, step_index, checked):
        channel.steps[step_index] = checked
        
    def toggle_mute(self, channel, muted):
        channel.muted = muted
        
    def clear_all(self):
        self.channels.clear()
        while self.channels_layout.count():
            child = self.channels_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def get_channel_data(self):
        return [{
            'name': ch.name,
            'color': ch.color,
            'volume': ch.volume,
            'muted': ch.muted,
            'steps': ch.steps[:]
        } for ch in self.channels]