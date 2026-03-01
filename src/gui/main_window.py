"""PySide6 GUI for Paper Translator - macOS/Apple Style."""
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QLabel, QPushButton, QFileDialog, QMenuBar, QMenu,
    QStatusBar, QScrollArea, QFrame, QTextEdit, QSlider, QCheckBox,
    QComboBox, QGroupBox, QProgressBar, QToolBar, QDockWidget,
    QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem,
    QApplication, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, Signal, QMimeData
from PySide6.QtGui import QAction, QFont, QColor, QPalette, QDropEvent, QDragEnterEvent, QIcon, QKeySequence

from ..utils.config_loader import config


class AppleStyleSheet:
    """Apple-inspired stylesheet for the application."""
    
    @staticmethod
    def get_light_theme() -> str:
        return """
        QMainWindow {
            background-color: #F5F5F7;
        }
        QWidget {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
            font-size: 13px;
            color: #1D1D1F;
        }
        QPushButton {
            background-color: #007AFF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #0056CC;
        }
        QPushButton:pressed {
            background-color: #004499;
        }
        QPushButton:disabled {
            background-color: #C7C7CC;
            color: #8E8E93;
        }
        QTextEdit, QScrollArea {
            background-color: white;
            border: 1px solid #D2D2D7;
            border-radius: 8px;
        }
        QSplitter::handle {
            background-color: #D2D2D7;
            width: 1px;
        }
        QMenuBar {
            background-color: #F5F5F7;
            border-bottom: 1px solid #D2D2D7;
        }
        QMenuBar::item:selected {
            background-color: #E5E5EA;
        }
        QMenu {
            background-color: white;
            border: 1px solid #D2D2D7;
            border-radius: 8px;
        }
        QStatusBar {
            background-color: #F5F5F7;
            border-top: 1px solid #D2D2D7;
        }
        QLabel {
            color: #1D1D1F;
        }
        QProgressBar {
            border: none;
            background-color: #E5E5EA;
            border-radius: 4px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #007AFF;
            border-radius: 4px;
        }
        QComboBox {
            background-color: white;
            border: 1px solid #D2D2D7;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid #D2D2D7;
        }
        QCheckBox::indicator:checked {
            background-color: #007AFF;
            border-color: #007AFF;
        }
        """
    
    @staticmethod
    def get_dark_theme() -> str:
        return """
        QMainWindow {
            background-color: #1D1D1F;
        }
        QWidget {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
            font-size: 13px;
            color: #F5F5F7;
        }
        QPushButton {
            background-color: #0A84FF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #409CFF;
        }
        QTextEdit, QScrollArea {
            background-color: #2C2C2E;
            border: 1px solid #3A3A3C;
            border-radius: 8px;
            color: #F5F5F7;
        }
        QMenuBar {
            background-color: #1D1D1F;
            border-bottom: 1px solid #3A3A3C;
        }
        QStatusBar {
            background-color: #1D1D1F;
            border-top: 1px solid #3A3A3C;
        }
        """


class PDFDropZone(QFrame):
    """Drop zone for PDF files."""
    
    file_dropped = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.setAcceptDrops(True)
    
    def _setup_ui(self):
        self.setMinimumSize(400, 300)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Icon
        self.icon_label = QLabel("📄")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 48px;")
        
        # Text
        self.text_label = QLabel("拖拽 PDF 文件到这里\n或点击选择文件")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("color: #8E8E93; margin-top: 16px;")
        
        # Browse button
        self.browse_btn = QPushButton("浏览文件")
        self.browse_btn.clicked.connect(self._browse_file)
        self.browse_btn.setMaximumWidth(120)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addWidget(self.browse_btn)
        
        self._set_styles()
    
    def _set_styles(self):
        self.setStyleSheet("""
            PDFDropZone {
                background-color: #F5F5F7;
                border: 2px dashed #D2D2D7;
                border-radius: 16px;
                margin: 16px;
            }
            PDFDropZone:hover {
                border-color: #007AFF;
                background-color: #F0F0F7;
            }
        """)
    
    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择 PDF 文件", "", "PDF 文件 (*.pdf)"
        )
        if file_path:
            self.file_dropped.emit(file_path)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith('.pdf'):
                event.acceptProposedAction()
                self.setStyleSheet("""
                    PDFDropZone {
                        background-color: #E8F4FD;
                        border: 2px dashed #007AFF;
                        border-radius: 16px;
                        margin: 16px;
                    }
                """)
    
    def dragLeaveEvent(self, event):
        self._set_styles()
    
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].toLocalFile().lower().endswith('.pdf'):
            self.file_dropped.emit(urls[0].toLocalFile())
            self._set_styles()


class ReaderPane(QScrollArea):
    """A single reading pane (left or right)."""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.title = title
        self._setup_ui()
        self._sync_enabled = False
        self._other_pane: Optional['ReaderPane'] = None
        self._is_syncing = False
        
    def _setup_ui(self):
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Container widget
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(16, 16, 16, 16)
        
        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1D1D1F;
            margin-bottom: 12px;
        """)
        self.layout.addWidget(self.title_label)
        
        # Content area
        self.content = QTextEdit()
        self.content.setReadOnly(True)
        self.content.setLineWrapMode(QTextEdit.WidgetWidth)
        self.content.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: transparent;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        self.layout.addWidget(self.content)
        
        self.setWidget(self.container)
        
        # Connect scroll
        self.verticalScrollBar().valueChanged.connect(self._on_scroll)
    
    def _on_scroll(self, value):
        if self._sync_enabled and self._other_pane and not self._is_syncing:
            self._is_syncing = True
            other_bar = self._other_pane.verticalScrollBar()
            # Calculate ratio and sync
            ratio = value / max(1, self.verticalScrollBar().maximum())
            new_value = int(ratio * max(1, other_bar.maximum()))
            other_bar.setValue(new_value)
            self._is_syncing = False
    
    def set_other_pane(self, other: 'ReaderPane'):
        """Set the other pane for synchronized scrolling."""
        self._other_pane = other
    
    def set_content(self, text: str):
        """Set the content of this pane."""
        self.content.setPlainText(text)
    
    def append_content(self, text: str):
        """Append content to this pane."""
        self.content.append(text)
    
    def set_sync_enabled(self, enabled: bool):
        """Enable/disable synchronized scrolling."""
        self._sync_enabled = enabled


class BilingualReader(QFrame):
    """Main bilingual reader widget with two panes."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Splitter for resizing
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Left pane (original)
        self.left_pane = ReaderPane("原文 (English)")
        self.left_pane.setObjectName("original_pane")
        
        # Right pane (translated)
        self.right_pane = ReaderPane("译文 (中文)")
        self.right_pane.setObjectName("translated_pane")
        
        # Set up sync
        self.left_pane.set_other_pane(self.right_pane)
        self.right_pane.set_other_pane(self.left_pane)
        
        self.splitter.addWidget(self.left_pane)
        self.splitter.addWidget(self.right_pane)
        
        # Default 50:50 split
        self.splitter.setSizes([400, 400])
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        
        layout.addWidget(self.splitter)
        
        # Default sync enabled
        self.left_pane.set_sync_enabled(True)
        self.right_pane.set_sync_enabled(True)
    
    def set_original_content(self, text: str):
        self.left_pane.set_content(text)
    
    def set_translated_content(self, text: str):
        self.right_pane.set_content(text)
    
    def append_original(self, text: str):
        self.left_pane.append_content(text)
    
    def append_translated(self, text: str):
        self.right_pane.append_content(text)
    
    def set_sync_scroll(self, enabled: bool):
        self.left_pane.set_sync_enabled(enabled)
        self.right_pane.set_sync_enabled(enabled)


class SettingsPanel(QWidget):
    """Settings panel for translation options."""
    
    settings_changed = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Title
        title = QLabel("设置")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)
        
        # Theme selection
        theme_group = QGroupBox("外观")
        theme_layout = QHBoxLayout()
        
        theme_label = QLabel("主题:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["跟随系统", "浅色", "深色"])
        self.theme_combo.currentTextChanged.connect(self._on_settings_changed)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Translation settings
        trans_group = QGroupBox("翻译设置")
        trans_layout = QVBoxLayout()
        
        # Sync scroll
        self.sync_checkbox = QCheckBox("启用滚动同步")
        self.sync_checkbox.setChecked(True)
        self.sync_checkbox.stateChanged.connect(self._on_settings_changed)
        trans_layout.addWidget(self.sync_checkbox)
        
        # Font size
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("字体大小:"))
        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setMinimum(10)
        self.font_slider.setMaximum(24)
        self.font_slider.setValue(14)
        self.font_slider.valueChanged.connect(self._on_settings_changed)
        font_layout.addWidget(self.font_slider)
        font_layout.addWidget(QLabel("14"))
        trans_layout.addLayout(font_layout)
        
        trans_group.setLayout(trans_layout)
        layout.addWidget(trans_group)
        
        layout.addStretch()
    
    def _on_settings_changed(self):
        settings = {
            'theme': self.theme_combo.currentText(),
            'sync_scroll': self.sync_checkbox.isChecked(),
            'font_size': self.font_slider.value()
        }
        self.settings_changed.emit(settings)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.config = config
        self._setup_ui()
        self._apply_theme()
    
    def _setup_ui(self):
        self.setWindowTitle("Paper Translator - 论文翻译器")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Menu bar
        self._create_menu_bar()
        
        # Toolbar
        self._create_toolbar()
        
        # Stacked widget for different views
        self.stacked = QWidget()
        self.stacked_layout = QVBoxLayout(self.stacked)
        
        # Drop zone (initial view)
        self.drop_zone = PDFDropZone()
        self.drop_zone.file_dropped.connect(self._on_file_selected)
        
        # Reader (translation view)
        self.reader = BilingualReader()
        
        self.stacked_layout.addWidget(self.drop_zone)
        self.stacked_layout.addWidget(self.reader)
        self.reader.hide()
        
        self.main_layout.addWidget(self.stacked)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # Progress bar (hidden by default)
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(200)
        self.progress.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress)
        
        # Settings panel (dock)
        self._create_settings_panel()
    
    def _create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("文件")
        
        open_action = QAction("打开 PDF...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("视图")
        
        self.toggle_sync_action = QAction("滚动同步", self)
        self.toggle_sync_action.setCheckable(True)
        self.toggle_sync_action.setChecked(True)
        self.toggle_sync_action.triggered.connect(self._toggle_sync)
        view_menu.addAction(self.toggle_sync_action)
        
        view_menu.addSeparator()
        
        reset_layout_action = QAction("重置布局", self)
        reset_layout_action.triggered.connect(self._reset_layout)
        view_menu.addAction(reset_layout_action)
        
        # Help menu
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(toolbar)
        
        # Open button
        open_btn = QPushButton("📂 打开")
        open_btn.clicked.connect(self._open_file)
        toolbar.addWidget(open_btn)
        
        toolbar.addSeparator()
        
        # Back to drop zone
        self.back_btn = QPushButton("← Back")
        self.back_btn.clicked.connect(self._show_drop_zone)
        self.back_btn.setVisible(False)
        toolbar.addWidget(self.back_btn)
        
        # Spacer to push settings to right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolbar.addWidget(spacer)
        
        # Settings button
        settings_btn = QPushButton("⚙️ 设置")
        settings_btn.clicked.connect(self._toggle_settings)
        toolbar.addWidget(settings_btn)
    
    def _create_settings_panel(self):
        self.settings_dock = QDockWidget("设置", self)
        self.settings_panel = SettingsPanel()
        self.settings_panel.settings_changed.connect(self._apply_settings)
        self.settings_dock.setWidget(self.settings_panel)
        self.settings_dock.setVisible(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.settings_dock)
    
    def _apply_theme(self):
        theme = self.config.get('ui.theme', 'system')
        
        if theme == 'light':
            stylesheet = AppleStyleSheet.get_light_theme()
        elif theme == 'dark':
            stylesheet = AppleStyleSheet.get_dark_theme()
        else:
            # System theme detection (simplified)
            stylesheet = AppleStyleSheet.get_light_theme()
        
        self.setStyleSheet(stylesheet)
    
    def _on_file_selected(self, file_path: str):
        """Handle file selection."""
        self.current_file = file_path
        self._start_translation(file_path)
    
    def _open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择 PDF 文件", "", "PDF 文件 (*.pdf)"
        )
        if file_path:
            self.current_file = file_path
            self._start_translation(file_path)
    
    def _start_translation(self, file_path: str):
        """Start the translation process."""
        self.status_bar.showMessage(f"正在加载: {Path(file_path).name}")
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminate
        
        # Show reader
        self.drop_zone.hide()
        self.reader.show()
        self.back_btn.setVisible(True)
        
        # Load and translate (simulated for now)
        from ..core.pdf_parser import PDFParser
        from ..core.translator import translator
        
        try:
            parser = PDFParser(file_path, self.config)
            elements = parser.parse()
            
            # Get text content
            text_elements = parser.get_text_elements()
            original_text = "\n\n".join([e.content for e in text_elements])
            
            # Set original content
            self.reader.set_original_content(original_text)
            
            # Translate
            self.status_bar.showMessage("正在翻译...")
            translated = translator.translate(original_text)
            self.reader.set_translated_content(translated)
            
            self.status_bar.showMessage("翻译完成")
            
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")
        
        finally:
            self.progress.setVisible(False)
    
    def _show_drop_zone(self):
        """Show the drop zone."""
        self.drop_zone.show()
        self.reader.hide()
        self.back_btn.setVisible(False)
        self.status_bar.showMessage("就绪")
    
    def _toggle_sync(self, enabled: bool):
        """Toggle synchronized scrolling."""
        self.reader.set_sync_scroll(enabled)
    
    def _reset_layout(self):
        """Reset splitter layout."""
        self.reader.splitter.setSizes([400, 400])
    
    def _toggle_settings(self):
        """Toggle settings panel."""
        self.settings_dock.setVisible(not self.settings_dock.isVisible())
    
    def _apply_settings(self, settings: dict):
        """Apply new settings."""
        # Apply font size
        font_size = settings.get('font_size', 14)
        font = self.reader.left_pane.content.font()
        font.setPointSize(font_size)
        self.reader.left_pane.content.setFont(font)
        self.reader.right_pane.content.setFont(font)
        
        # Apply sync
        self.reader.set_sync_scroll(settings.get('sync_scroll', True))
        self.toggle_sync_action.setChecked(settings.get('sync_scroll', True))
        
        # Apply theme
        theme = settings.get('theme', '跟随系统')
        if theme == "浅色":
            self.setStyleSheet(AppleStyleSheet.get_light_theme())
        elif theme == "深色":
            self.setStyleSheet(AppleStyleSheet.get_dark_theme())
        else:
            self._apply_theme()
    
    def _show_about(self):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "关于 Paper Translator",
            "Paper Translator v0.1.0\n\n"
            "一款优雅的论文PDF双语对照阅读器\n"
            "支持 Gemini 和 Google Translate 翻译引擎\n\n"
            "© 2024"
        )


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Paper Translator")
    app.setOrganizationName("PaperTranslator")
    
    # Set app style
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()