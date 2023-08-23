# Patient Flow Simulator

The Patient Flow Simulator is a Python application designed to simulate patient flows using Camunda BPMN diagrams and the SpiffWorkflow library.

## Structure

- **runner.py**: Entry point for running the application, contains the number of patients to be put through.
- **playbook.py**: Defines procedures related to a patient visit including registration, triage, and visit areas.
- **simulation.py**: Handles the simulation of patient flows, including assigning triage levels and managing doctors' schedules. Contains the configuration for the number of doctors, nurses, etc. during the simulation.
- **generator.py**: Generates random data or scenarios for the simulation. (TO BE EXPANDED)

## Dependencies

0. **Python3.x**

1. **SpiffWorkflow**:
    - Handles BPMN workflows, Camunda parsing, and user tasks.

2. **Standard Python Libraries**:
    - `random`: For generating random values.
    - `threading`: For concurrent execution.
    - `os`: For OS-related tasks.
    - `time`: For time-based tasks.
    - `csv`: To work with CSV files.
    - `json`: For JSON data manipulation.
    - `string`: For common string operations.

## Setup and Execution

1. Ensure you have all dependencies installed.
2. Run `runner.py` to start the simulation.

## Notes

- The simulation uses BPMN diagrams (`Visit.bpmn` and `EDAsIs.bpmn`) for the patient flow logic.
- Adjust parameters in the respective Python files to modify the simulation's behavior.

## Citation Information
- The simulator has been publicized in the following paper. If you wish to use it for your own research, please cite the following paper (under publication as of 2023-08-23):
Zoltán Szabó, Dr. Emőke Adrienn Hompot, Dr. Vilmos Bilicki. "Patient Flow Analysis with a Custom Simulation Engine" Acta Cybernetica -- under publication --

- The ED model is based on the excellent work of Antonio Di Leva and Emilio Sulis:
Antionio Di Leva, and Emilio Sulis. "A business process methodology to investigate organization management: a hospital case study." WSEAS Transactions on business and economics (2017): 100-109.