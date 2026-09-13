import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QMenuBar, QMenu, QAction, QToolBar, QStatusBar, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont

from channel_rack import ChannelRack
from piano_roll import PianoRoll
from playlist import Playlist
from mixer import Mixer
from browser import Browser
from transport_controls import TransportControls
from audio_processor import AudioProcessor
from project_manager import ProjectManager

class FLStudioClone(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FL Studio Clone")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)
        
        self.bpm = 140
        self.is_playing = False
        self.current_position = 0
        
        self.audio_processor = AudioProcessor()
        self.project_manager = ProjectManager()
        self.project_manager.create_new_project()
        
        self.init_ui()
        self.init_menu()
        self.init_toolbar()
        self.init_statusbar()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.transport_controls = TransportControls(self)
        main_layout.addWidget(self.transport_controls)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #333; }
            QTabBar::tab {
                background: #2a2a2a;
                color: #ddd;
                padding: 8px 16px;
                margin-right: 2px;
                border: 1px solid #444;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #3a3a3a;
                border-bottom: 2px solid #ff6600;
            }
            QTabBar::tab:hover {
                background: #333;
            }
        """)
        
        self.channel_rack = ChannelRack(self)
        self.piano_roll = PianoRoll(self)
        self.playlist = Playlist(self)
        self.mixer = Mixer(self)
        self.browser = Browser(self)
        
        self.tab_widget.addTab(self.channel_rack, "Channel Rack")
        self.tab_widget.addTab(self.piano_roll, "Piano Roll")
        self.tab_widget.addTab(self.playlist, "Playlist")
        self.tab_widget.addTab(self.mixer, "Mixer")
        self.tab_widget.addTab(self.browser, "Browser")
        
        main_layout.addWidget(self.tab_widget)
        
    def init_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2a2a2a;
                color: #ddd;
                padding: 2px;
            }
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
            }
            QMenuBar::item:selected {
                background: #3a3a3a;
            }
            QMenu {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
            }
            QMenu::item {
                padding: 5px 30px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #ff6600;
            }
        """)
        
        file_menu = menubar.addMenu("File")
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_wav_action = QAction("Export as WAV", self)
        export_wav_action.setShortcut("Ctrl+E")
        export_wav_action.triggered.connect(self.export_wav)
        file_menu.addAction(export_wav_action)
        
        export_mp3_action = QAction("Export as MP3", self)
        export_mp3_action.setShortcut("Ctrl+Shift+E")
        file_menu.addAction(export_mp3_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        edit_menu = menubar.addMenu("Edit")
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)
        
        tools_menu = menubar.addMenu("Tools")
        channel_rack_action = QAction("Channel Rack", self)
        channel_rack_action.setShortcut("F5")
        channel_rack_action.triggered.connect(lambda: self.tab_widget.setCurrentWidget(self.channel_rack))
        tools_menu.addAction(channel_rack_action)
        
        piano_roll_action = QAction("Piano Roll", self)
        piano_roll_action.setShortcut("F7")
        piano_roll_action.triggered.connect(lambda: self.tab_widget.setCurrentWidget(self.piano_roll))
        tools_menu.addAction(piano_roll_action)
        
        playlist_action = QAction("Playlist", self)
        playlist_action.setShortcut("F6")
        playlist_action.triggered.connect(lambda: self.tab_widget.setCurrentWidget(self.playlist))
        tools_menu.addAction(playlist_action)
        
        mixer_action = QAction("Mixer", self)
        mixer_action.setShortcut("F9")
        mixer_action.triggered.connect(lambda: self.tab_widget.setCurrentWidget(self.mixer))
        tools_menu.addAction(mixer_action)
        
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def init_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2a2a2a;
                border: none;
                padding: 5px;
                spacing: 5px;
            }
            QToolButton {
                background-color: #3a3a3a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px 10px;
            }
            QToolButton:hover {
                background-color: #4a4a4a;
            }
            QToolButton:pressed {
                background-color: #ff6600;
            }
        """)
        self.addToolBar(toolbar)
        
    def init_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.setStyleSheet("""
            QStatusBar {
                background-color: #2a2a2a;
                color: #ddd;
                border-top: 1px solid #444;
            }
        """)
        self.update_statusbar()
        
    def update_statusbar(self):
        self.statusbar.showMessage(f"BPM: {self.bpm} | Position: {self.current_position} | Status: {'Playing' if self.is_playing else 'Stopped'}")
        
    def new_project(self):
        reply = QMessageBox.question(self, "New Project", "Create a new project? Unsaved changes will be lost.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.channel_rack.clear_all()
            self.playlist.clear_all()
            self.mixer.reset_all()
            self.current_position = 0
            self.bpm = 140
            self.project_manager.create_new_project()
            self.update_statusbar()
    
    def open_project(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "FL Studio Project (*.flp);;All Files (*)")
        if filepath:
            try:
                project_data = self.project_manager.load_project(filepath)
                self.bpm = project_data.get('bpm', 140)
                self.update_statusbar()
                self.statusbar.showMessage(f"Opened: {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open project: {str(e)}")
    
    def save_project(self):
        if self.project_manager.project_path:
            project_data = self.collect_project_data()
            self.project_manager.save_project(project_data)
            self.statusbar.showMessage(f"Saved: {self.project_manager.project_path}")
        else:
            self.save_project_as()
    
    def save_project_as(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "FL Studio Project (*.flp);;All Files (*)")
        if filepath:
            project_data = self.collect_project_data()
            self.project_manager.save_project(project_data, filepath)
            self.project_manager.add_to_recent(filepath)
            self.statusbar.showMessage(f"Saved: {filepath}")
    
    def export_wav(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Export as WAV", "", "WAV Audio (*.wav);;All Files (*)")
        if filepath:
            try:
                channel_data = self.channel_rack.get_channel_data()
                audio = self.audio_processor.process_channel_rack(channel_data)
                self.audio_processor.export_to_wav(audio, filepath)
                self.statusbar.showMessage(f"Exported WAV: {filepath}")
                QMessageBox.information(self, "Export Complete", f"Successfully exported to:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def export_mp3(self):
        QMessageBox.information(self, "Export MP3", "MP3 export requires additional libraries (lameenc).\nPlease install with: pip install lameenc")
    
    def collect_project_data(self):
        return {
            'version': '1.0.0',
            'bpm': self.bpm,
            'time_signature': '4/4',
            'channels': self.channel_rack.get_channel_data(),
            'patterns': [],
            'playlist': [],
            'mixer_tracks': [{'name': t.name, 'volume': t.volume, 'muted': t.muted, 'solo': t.solo} for t in self.mixer.tracks],
            'metadata': {
                'name': os.path.basename(self.project_manager.project_path or 'Untitled'),
                'author': '',
                'description': ''
            }
        }
            
    def show_about(self):
        QMessageBox.about(self, "About FL Studio Clone",
                         "FL Studio Clone\nVersion 1.0.0\n\nA digital audio workstation (DAW) built with Python, C++, and C#.\n\nFeatures:\n- Channel Rack\n- Piano Roll\n- Playlist\n- Mixer\n- Browser\n- Audio Processing\n- MIDI Support")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e1e;
        }
    """)
    window = FLStudioClone()
    window.show()
    sys.exit(app.exec_())