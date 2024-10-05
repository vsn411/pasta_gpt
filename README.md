
# PASTA Threat Modeling Tool

![PASTA Logo](./logo.png)  <!-- Example of how to include an image -->



[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/Pasta-Threat-Modeling-Tool)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/yourusername/Pasta-Threat-Modeling-Tool)

Welcome to the **PASTA Threat Modeling Tool** — a Python-based threat modeling tool designed to assist security professionals in implementing the **Process for Attack Simulation and Threat Analysis (PASTA)** methodology. PASTA provides an iterative, risk-centric approach for identifying and mitigating cybersecurity threats.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Comprehensive **PASTA threat modeling** capabilities.
- Attack surface analysis and vulnerability identification.
- Risk-based prioritization of threat scenarios.
- Customizable for various environments (on-prem, cloud, etc.) [future release]
- Visual representation of threat models and attack vectors.
- Exportable reports (PDF, CSV) [future release]

## Installation

### Requirements

- Python 3.8+
- Virtualenv (optional, but recommended)
- Dependencies listed in `requirements.txt`

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vsn411/pasta_gpt.git
   cd pasta_gpt
   ```

2. **Set up a virtual environment (optional):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the tool:**
   ```bash
   streamlit run pasta_gpt.py
   ```

## Usage
Use side-bar in threat modeling app further details. Note that you need to provide OpenAI or Mistral API key in order to get results.

## Contributing

We welcome contributions! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a Pull Request.

Please refer to our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Reference
This PASTA threat modeling tool is built on https://github.com/mrwadams/stride-gpt

---

**Happy threat modeling!** If you have any questions or run into issues, feel free to open an issue or reach out via [GitHub Discussions](https://github.com/vsn411/pasta_gpt/discussions).

---


