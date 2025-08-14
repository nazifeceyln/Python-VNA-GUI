# Python-VNA-GUI
A Python-based GUI for controlling a Vector Network Analyzer and Measurements of Permittivity and Electromagnetic Shielding Effectiveness

# Python-VNA-GUI

A Python-based Graphical User Interface (GUI) for controlling a Vector Network Analyzer (VNA) and performing measurements of electromagnetic properties such as permittivity, loss tangent, reflection loss, absorption loss, and total shielding effectiveness.

#Features
- **SCPI Protocol Support**: Full communication with VNA via Standard Commands for Programmable Instruments (SCPI)
- **Waveguide Calibration**: WR229 waveguide calibration support for 3.3 – 4.9 GHz band
- **Real-Time Plotting**: Displays S-parameters and shielding effectiveness simultaneously
- **Material Property Computation**: Calculates permittivity, loss tangent, reflection loss, absorption loss
- **User-Friendly Interface**: Developed with PyQt5

#Requirements
- Python 3.8+
- PyQt5
- NumPy
- Matplotlib
- pyVISA

Install dependencies:
```bash
pip install -r requirements.txt
