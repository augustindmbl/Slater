# Atomic Physics Calculation Toolkit

This toolkit provides a set of Python scripts and utilities for performing atomic physics calculations. The interface is powered by [Streamlit](https://streamlit.io/), allowing for a simple and interactive use of the code.

## 📦 Installation Guide (from scratch)

### 1. Install Python (version 3.9 or higher)

If Python is not installed yet:

- **Windows**: Download the installer from [python.org](https://www.python.org/downloads/windows/) and make sure to check **"Add Python to PATH"** during installation. -> Verify path in cmd
- **macOS**: Use [Homebrew](https://brew.sh/):  
  ```bashCom
  brew install python
  ```
- **Linux (Debian/Ubuntu)**:  
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```


python --version

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install required packages

In the project folder, install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt -> Bien se mettre dans le repertory de Slater
```

If no `requirements.txt` exists yet, a minimal setup might include:

```bash
pip install streamlit numpy scipy matplotlib
```

### 5. Verify the installation

To ensure everything is set up correctly, run the following tests:

```bash
python -c "import streamlit; import numpy; import scipy; import matplotlib.pyplot as plt; print('All imports successful!')"
```

You should see:  
```bash
All imports successful!
```

### 6. Launch the application (if applicable)

If your code uses a Streamlit interface, you can start it with:

```bash
streamlit run main.py
```
Ils demandent un mail, on s'en branle on tape sur enter
Accepter les réseaux privés accessibles par python. 

Replace `main.py` with the appropriate script filename.
