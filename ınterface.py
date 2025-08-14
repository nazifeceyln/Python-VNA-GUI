#Yazar: Nazife CEYLAN

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMenu, QMenuBar, QStatusBar, QToolBar, QAction, 
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QComboBox
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices


class SOLTCalibrationApp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SOLT Calibration")
        self.setGeometry(100, 100, 800, 400)

        # Ana widget ve layout
        layout = QVBoxLayout(self)

        # Başlık
        title = QLabel("SOLT CALIBRATION")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px;")
        layout.addWidget(title)

        # Kalibrasyon Tablosu
        self.table = QTableWidget(7, 3)
        self.table.setHorizontalHeaderLabels(["Step", "Description", "Status"])
        self.populate_table()
        layout.addWidget(self.table)

        # Apply Butonu
        apply_button = QPushButton("Apply Calibration")
        apply_button.setStyleSheet("background-color: lightblue; font-size: 14px;")
        apply_button.clicked.connect(self.apply_calibration)
        layout.addWidget(apply_button)

    def populate_table(self):
        """Kalibrasyon tablosunu doldurur."""
        steps = [
            ("Port 1 Short", "Short Standard connected to port 1, port 2 open"),
            ("Port 1 Open", "Open Standard connected to port 1, port 2 open"),
            ("Port 1 Load", "Load Standard connected to port 1, port 2 open"),
            ("Port 2 Short", "Port 1 Open, short standard connected to port 2"),
            ("Port 2 Open", "Port 1 Open, open standard connected to port 2"),
            ("Port 2 Load", "Port 1 Open, load standard connected to port 2"),
            ("Through", "Port 1 connected to port 2 via through standard"),
        ]

        for row, (step, description) in enumerate(steps):
            self.table.setItem(row, 0, QTableWidgetItem(step))
            self.table.setItem(row, 1, QTableWidgetItem(description))

            # Measure butonu
            measure_button = QPushButton("Measure")
            measure_button.clicked.connect(self.create_measure_callback(row))
            self.table.setCellWidget(row, 2, measure_button)

    def create_measure_callback(self, row):
        """Her satıra özel bir measure callback oluşturur."""
        def measure():
            self.measure_action(row)
        return measure

    def measure_action(self, row):
        """Measure butonuna tıklandığında çalışır.""" 
        step_name = self.table.item(row, 0).text()

        # Örnek: Kalibrasyon simülasyonu veya cihazla iletişim
        success = self.simulate_measurement(step_name)

        if success:
            self.table.setItem(row, 2, QTableWidgetItem("Completed"))
            self.table.item(row, 2).setTextAlignment(Qt.AlignCenter)
            self.table.item(row, 2).setForeground(Qt.green)
        else:
            QMessageBox.warning(self, "Error", f"Measurement failed for {step_name}!")

    def simulate_measurement(self, step_name):
        """
        Örnek bir ölçüm simülasyonu. Burada cihaz API'sine bağlanarak gerçek bir ölçüm
        işlemi yapılabilir.
        """
        print(f"Simulating measurement for {step_name}...")
        return True  # Simülasyon başarılı

    def apply_calibration(self):
        """Apply Calibration butonuna tıklandığında çalışır."""
        completed_steps = []
        for row in range(self.table.rowCount()):
            status_item = self.table.item(row, 2)
            if status_item and status_item.text() == "Completed":
                completed_steps.append(self.table.item(row, 0).text())

        if len(completed_steps) == self.table.rowCount():
            QMessageBox.information(self, "Calibration", "All calibration steps completed successfully!")
        else:
            QMessageBox.warning(self, "Calibration", "Some calibration steps are incomplete!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("LibreVNA-GUI")
        self.setGeometry(100, 100, 800, 600)
        
        # Add logo next to window title (logo olmalı)
        self.setWindowIcon(QIcon(r"C:\Users\EXCALIBUR\OneDrive\Desktop\Tübitak_2209a\akdeniz-universitesi-logo.png"))


        # Create menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Create file menu
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        # Add actions to file menu
        save_setup_action = QAction("Save Setup", self)
        save_setup_action.triggered.connect(self.save_setup)
        file_menu.addAction(save_setup_action)

        load_setup_action = QAction("Load Setup", self)
        load_setup_action.triggered.connect(self.load_setup)
        file_menu.addAction(load_setup_action)

        save_image_action = QAction("Save Image", self)
        save_image_action.triggered.connect(self.save_image)
        file_menu.addAction(save_image_action)

        save_graph_action = QAction("Save Graph", self)
        save_graph_action.triggered.connect(self.save_graph)
        file_menu.addAction(save_graph_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create device menu
        device_menu = QMenu("Device", self)
        menu_bar.addMenu(device_menu)
        
        # Add actions to device menu
        device_info_menu = QMenu("Device Information", self)
        device_menu.addMenu(device_info_menu)
        
        basic_info_action = QAction("Basic Information", self)
        basic_info_action.triggered.connect(self.show_basic_info)
        device_info_menu.addAction(basic_info_action)
        
        user_manual_action = QAction("User Manual Access", self)
        user_manual_action.triggered.connect(self.open_user_manual)
        device_info_menu.addAction(user_manual_action)

        calibration_menu = QMenu("Calibration", self)
        device_menu.addMenu(calibration_menu)
        
        solt_action = QAction("SOLT", self)
        solt_action.triggered.connect(self.open_solt_calibration)
        calibration_menu.addAction(solt_action)
        
        calibration_measurements_action = QAction("Calibration Measurements", self)
        calibration_menu.addAction(calibration_measurements_action)
        
        edit_calibration_kit_action = QAction("Edit Calibration Kit", self)
        calibration_menu.addAction(edit_calibration_kit_action)

        # Create tools menu
        tools_menu = QMenu("Tools", self)
        menu_bar.addMenu(tools_menu)
        deembedding_action = QAction("De-embedding", self)
        tools_menu.addAction(deembedding_action)

        # Create help menu
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        # Create status bar
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Create toolbar
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Add a button to the toolbar
        connect_action = QAction("Connect Device", self)
        connect_action.triggered.connect(self.connect_device)
        toolbar.addAction(connect_action)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a plot widget (placeholder)
        self.plot_widget = QWidget(central_widget)
        self.plot_widget.setMinimumSize(400, 300)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.plot_widget)

        # Create a horizontal layout for the frequency controls
        frequency_layout = QHBoxLayout()

        # Start frequency input
        self.start_freq_input = QLineEdit(self)
        self.start_freq_input.setPlaceholderText("Start Frequency")
        frequency_layout.addWidget(self.start_freq_input)

        # Frequency unit selection
        self.unit_combo = QComboBox(self)
        self.unit_combo.addItems(["kHz", "MHz", "GHz"])
        frequency_layout.addWidget(self.unit_combo)

        # Stop frequency input
        self.stop_freq_input = QLineEdit(self)
        self.stop_freq_input.setPlaceholderText("Stop Frequency")
        frequency_layout.addWidget(self.stop_freq_input)

        # Frequency unit selection
        self.unit_combo = QComboBox(self)
        self.unit_combo.addItems(["kHz", "MHz", "GHz"])
        frequency_layout.addWidget(self.unit_combo)

        # Add frequency controls to the top layout
        layout.addLayout(frequency_layout)

        # Create top buttons layout
        top_left_layout = QHBoxLayout()

        # Create RUN and Dielectric Measurements buttons
        run_button = QPushButton("RUN")
        run_button.setStyleSheet("background-color: green; font-size: 14px;")
        run_button.clicked.connect(self.run_action)
        top_left_layout.addWidget(run_button)

        shielding_button = QPushButton("Electromagnetic Shielding Effectiveness")
        shielding_button.setStyleSheet("background-color: lightgrey; font-size: 14px;")
        shielding_button.clicked.connect(self.electromagnetic_shielding_effectiveness_action)
        top_left_layout.addWidget(shielding_button)

        dielectric_button = QPushButton("Dielectric Measurements")
        dielectric_button.setStyleSheet("background-color: lightgrey; font-size: 14px;")
        dielectric_button.clicked.connect(self.dielectric_measurements_action)
        top_left_layout.addWidget(dielectric_button)

        # Add the layout for the top-left buttons to the central widget layout
        layout.addLayout(top_left_layout)

        # Create bottom buttons layout
        bottom_layout = QHBoxLayout()

        # Add Clear, Quit, and Save to File buttons
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_action)
        bottom_layout.addWidget(clear_button)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.quit_action)
        bottom_layout.addWidget(quit_button)

        save_button = QPushButton("Save to File")
        save_button.clicked.connect(self.save_to_file)
        bottom_layout.addWidget(save_button)

        # Add the bottom layout to the central widget
        layout.addLayout(bottom_layout)

    def run_action(self):
        """RUN button action"""
        start_freq = self.start_freq_input.text()
        stop_freq = self.stop_freq_input.text()
        unit = self.unit_combo.currentText()
        QMessageBox.information(self, "Run", f"Running from {start_freq} {unit} to {stop_freq} {unit}")

    def dielectric_measurements_action(self):
        """Dielectric Measurements button action"""
        QMessageBox.information(self, "Dielectric Measurements", "Dielectric Measurements action initiated.")

    def electromagnetic_shielding_effectiveness_action(self):
        """Electromagnetic Shielding Effectiveness button action"""
        QMessageBox.information(self, "Electromagnetic Shielding Effectiveness", "Electromagnetic Shielding Effectiveness action initiated.")    

    def save_setup(self):
        """Save setup functionality"""
        print("Saving setup...")

    def load_setup(self):
        """Load setup functionality"""
        print("Loading setup...")

    def save_image(self):
        """Save image functionality"""
        print("Saving image...")

    def save_graph(self):
        """Save graph functionality"""
        print("Saving graph...")

    def show_basic_info(self):
        # Show basic device information
        info_window = QDialog(self)
        info_window.setWindowTitle("Device Information")
        info_window.setFixedSize(300, 200)  # Set fixed size

        layout = QVBoxLayout()
        info_window.setLayout(layout)

        # Add device information labels
        model_label = QLabel("Model: LibreVNA-123")
        layout.addWidget(model_label)

        serial_label = QLabel("Serial Number: 123456789")
        layout.addWidget(serial_label)

        firmware_label = QLabel("Firmware Version: v1.0")
        layout.addWidget(firmware_label)

        start_freq_label = QLabel("Start Frequency: 100 kHz")
        layout.addWidget(start_freq_label)

        stop_freq_label = QLabel("Stop Frequency: 6 GHz")
        layout.addWidget(stop_freq_label)

        info_window.exec_()

    def open_user_manual(self):
        # Open the user manual PDF file
        user_manual_url = "https://github.com/jankae/LibreVNA/blob/master/Documentation/UserManual/manual.pdf"  # Replace this with the actual path
        QDesktopServices.openUrl(QUrl(user_manual_url))
    

    def open_solt_calibration(self):
        """Open SOLT calibration window"""
        self.solt_calibration_dialog = SOLTCalibrationApp(self)
        self.solt_calibration_dialog.exec_()

    def connect_device(self):
        """Device connection functionality"""
        print("Connecting to device...")

    def clear_action(self):
        """Clear action"""
        print("Clearing data...")

    def quit_action(self):
        """Quit action"""
        self.close()

    def save_to_file(self):
        """Save to file functionality"""
        print("Saving to file...")

    def closeEvent(self, event):
        """Handle closing event"""
        event.accept()


# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

