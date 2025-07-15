#!/usr/bin/env python3

import sys
import os
import time
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit, QFileDialog, QProgressBar,
    QGroupBox, QCheckBox, QSpinBox, QLineEdit, QMessageBox
)
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QFont
import organize_videos
import logging

class VideoOrganizerThread(QThread):
    """Thread for running video organization in background"""
    progress_signal = Signal(str)
    finished_signal = Signal(bool, str)
    
    def __init__(self, source_dir, config):
        super().__init__()
        self.source_dir = source_dir
        self.config = config
        self.is_running = False
        
    def run(self):
        try:
            self.is_running = True
            self.progress_signal.emit("Starting video organization...")
            
            # Redirect logging to our signal
            original_logger = organize_videos.logger
            
            class SignalLogger:
                def __init__(self, signal):
                    self.signal = signal
                    self.level = logging.INFO
                
                def info(self, msg):
                    self.signal.emit(f"INFO: {msg}")
                
                def error(self, msg):
                    self.signal.emit(f"ERROR: {msg}")
                
                def debug(self, msg):
                    # Only show debug messages if level is DEBUG
                    if self.level <= logging.DEBUG:
                        self.signal.emit(f"DEBUG: {msg}")
                
                def warning(self, msg):
                    self.signal.emit(f"WARNING: {msg}")
                
                def setLevel(self, level):
                    self.level = level
                
                def getEffectiveLevel(self):
                    return self.level
            
            # Create and configure the signal logger
            signal_logger = SignalLogger(self.progress_signal)
            signal_logger.setLevel(logging.INFO)
            
            # Replace the original logger
            organize_videos.logger = signal_logger
            
            # Also configure the root logger to INFO level
            logging.getLogger().setLevel(logging.INFO)
            
            # Update configuration
            organize_videos.SOURCE_DIR = self.source_dir
            organize_videos.VIDEO_EXTENSIONS = set(self.config['extensions'])
            organize_videos.JUMP_TIME_THRESHOLD = organize_videos.timedelta(minutes=self.config['jump_threshold'])
            organize_videos.PRESERVE_NAMES = self.config['preserve_names']
            
            # Run the organization
            organize_videos.organize_videos()
            
            self.progress_signal.emit("Video organization completed successfully!")
            self.finished_signal.emit(True, "Organization completed successfully!")
            
        except Exception as e:
            self.progress_signal.emit(f"Error during organization: {str(e)}")
            self.finished_signal.emit(False, f"Error: {str(e)}")
        finally:
            self.is_running = False
            organize_videos.logger = original_logger

class VideoOrganizerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.organizer_thread = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Skydiving Video Organizer")
        self.setGeometry(100, 100, 900, 700)
        
        # Apply sophisticated dark theme inspired by modern mobile apps
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
                color: #ffffff;
            }
            
            QTabWidget::pane {
                border: none;
                background-color: #1e1e2e;
            }
            
            QTabBar::tab {
                background-color: #2a2a3e;
                color: #a0a0a0;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                font-weight: 500;
                font-size: 14px;
            }
            
            QTabBar::tab:selected {
                background-color: #3a3a4e;
                color: #ffffff;
            }
            
            QTabBar::tab:hover {
                background-color: #323246;
                color: #ffffff;
            }
            
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                color: #ffffff;
                border: none;
                border-radius: 16px;
                margin-top: 16px;
                padding: 20px;
                background-color: #2a2a3e;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                top: 12px;
                padding: 0 12px 0 12px;
                background-color: #2a2a3e;
                color: #ffffff;
            }
            
            QLineEdit {
                background-color: #3a3a4e;
                border: 1px solid #4a4a5e;
                border-radius: 12px;
                padding: 12px 16px;
                color: #ffffff;
                font-size: 14px;
                selection-background-color: #6c5ce7;
            }
            
            QLineEdit:focus {
                border: 1px solid #6c5ce7;
                background-color: #3a3a4e;
            }
            
            QPushButton {
                background-color: #6c5ce7;
                border: none;
                border-radius: 12px;
                color: #ffffff;
                padding: 14px 24px;
                font-weight: 600;
                font-size: 15px;
                min-height: 24px;
            }
            
            QPushButton:hover {
                background-color: #5a4fd8;
            }
            
            QPushButton:pressed {
                background-color: #4a3fc8;
            }
            
            QPushButton:disabled {
                background-color: #3a3a4e;
                color: #6a6a7a;
            }
            
            QSpinBox {
                background-color: #3a3a4e;
                border: 1px solid #4a4a5e;
                border-radius: 12px;
                padding: 10px 16px;
                color: #ffffff;
                font-size: 14px;
            }
            
            QSpinBox:focus {
                border: 1px solid #6c5ce7;
            }
            
            QCheckBox {
                color: #ffffff;
                font-size: 14px;
                spacing: 12px;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #4a4a5e;
                border-radius: 6px;
                background-color: #3a3a4e;
            }
            
            QCheckBox::indicator:checked {
                background-color: #6c5ce7;
                border: 2px solid #6c5ce7;
            }
            
            QCheckBox::indicator:hover {
                border: 2px solid #6c5ce7;
            }
            
            QTextEdit {
                background-color: #3a3a4e;
                border: 1px solid #4a4a5e;
                border-radius: 16px;
                color: #ffffff;
                font-family: 'Monaco', 'Menlo', 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                padding: 16px;
                selection-background-color: #6c5ce7;
                line-height: 1.4;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: 400;
            }
            
            QTableWidget {
                background-color: #3a3a4e;
                border: 1px solid #4a4a5e;
                border-radius: 16px;
                color: #ffffff;
                gridline-color: #2a2a3e;
                selection-background-color: #6c5ce7;
            }
            
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #2a2a3e;
            }
            
            QTableWidget::item:selected {
                background-color: #6c5ce7;
                color: #ffffff;
            }
            
            QHeaderView::section {
                background-color: #2a2a3e;
                color: #ffffff;
                padding: 12px;
                border: none;
                font-weight: 600;
                font-size: 14px;
            }
            
            QProgressBar {
                border: none;
                border-radius: 8px;
                text-align: center;
                background-color: #3a3a4e;
                color: #ffffff;
                font-weight: 500;
            }
            
            QProgressBar::chunk {
                background-color: #6c5ce7;
                border-radius: 8px;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Source directory selection
        source_group = QGroupBox("Source Directory")
        source_layout = QHBoxLayout(source_group)
        
        self.source_path_edit = QLineEdit("No directory selected")
        self.source_path_edit.setReadOnly(True)
        source_layout.addWidget(self.source_path_edit, 1)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_source_directory)
        source_layout.addWidget(browse_btn)
        
        main_layout.addWidget(source_group)
        
        # Configuration group
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout(config_group)
        
        # Video extensions
        ext_layout = QHBoxLayout()
        ext_layout.addWidget(QLabel("Video Extensions:"))
        self.extensions_edit = QLineEdit(".mp4, .mov, .MP4, .MOV")
        ext_layout.addWidget(self.extensions_edit)
        config_layout.addLayout(ext_layout)
        
        # Jump threshold
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Jump Time Threshold (minutes):"))
        self.jump_threshold_spin = QSpinBox()
        self.jump_threshold_spin.setRange(1, 60)
        self.jump_threshold_spin.setValue(20)
        threshold_layout.addWidget(self.jump_threshold_spin)
        threshold_layout.addStretch()
        config_layout.addLayout(threshold_layout)
        
        # Preserve video names option
        preserve_layout = QHBoxLayout()
        self.preserve_names_checkbox = QCheckBox("Preserve original video names in parentheses")
        self.preserve_names_checkbox.setChecked(True)  # Default to enabled
        preserve_layout.addWidget(self.preserve_names_checkbox)
        preserve_layout.addStretch()
        config_layout.addLayout(preserve_layout)
        
        main_layout.addWidget(config_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.organize_btn = QPushButton("Organize Videos")
        self.organize_btn.clicked.connect(self.start_organization)
        button_layout.addWidget(self.organize_btn)
        

        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Log output
        log_group = QGroupBox("Log Output")
        log_layout = QVBoxLayout(log_group)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)
        
        # Clear log button
        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(self.log_output.clear)
        log_layout.addWidget(clear_log_btn)
        
        main_layout.addWidget(log_group)
        
        # Set default source directory (empty - user must select)
        self.source_directory = ""
        self.source_path_edit.setText("No directory selected")
            
        # Add some initial log messages
        self.log_output.append("Skydiving Video Organizer started")
        self.log_output.append("Please select a source directory and configure settings")
        
    def browse_source_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if directory:
            self.source_directory = directory
            self.source_path_edit.setText(directory)
            self.log_output.append(f"Source directory set to: {directory}")
            
    def start_organization(self):
        if not self.source_directory:
            QMessageBox.warning(self, "Warning", "Please select a source directory first.")
            return
            
        if self.organizer_thread and self.organizer_thread.is_running:
            QMessageBox.information(self, "Info", "Organization is already running.")
            return
            
        # Get configuration
        extensions = [ext.strip() for ext in self.extensions_edit.text().split(',')]
        config = {
            'extensions': extensions,
            'jump_threshold': self.jump_threshold_spin.value(),
            'preserve_names': self.preserve_names_checkbox.isChecked()
        }
        
        # Start organization thread
        self.organizer_thread = VideoOrganizerThread(self.source_directory, config)
        self.organizer_thread.progress_signal.connect(self.update_log)
        self.organizer_thread.finished_signal.connect(self.organization_finished)
        
        # Update UI
        self.organize_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        self.organizer_thread.start()
        
    def organization_finished(self, success, message):
        self.organize_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
            

            
    def update_log(self, message):
        self.log_output.append(f"{datetime.now().strftime('%H:%M:%S')} - {message}")
        # Auto-scroll to bottom
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )
        


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = VideoOrganizerGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 