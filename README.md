# **MSProject**

## **Purpose**

This project aims to replicate the figures from the paper *The effect of microsaccades in the primary visual cortex: a two-phase modulation in the absence of visual stimulation*.
Link to the article : <https://www.biorxiv.org/content/10.1101/2024.08.12.607606v1>

## **Overview**

**MSProject** is a Python-based project designed to analyze MATLAB `.mat` files and extract  data for further analysis. This project provides modularized functions and tests to ensure functionality, supporting mixed data types and robust error handling.

---

## **Project Structure**

```bash
MSproject/
│── src/
│   ├── my_project/                   
│   │   ├── inspect_data/              
│   │   │   ├── __init__.py
│   │   │   ├── analysis_functions1.py
│   │   │   ├── analysis_functions2.py
│   │   │   ├── preprocessing.py       
│   │   │
│   │   ├── plotting_figures/          
│   │   │   ├── __init__.py
│   │   │   ├── analysis1.py
│   │   │   ├── analysis2_for_each_monkey.py
│   │   │   ├── check_preprocessing.py  

│   │   │   ├── preprocessing_data.py
│   │   │
│   │   ├── config.py                  
│── test/                              
│   ├── __init__.py
│   ├── gandalf_100718a_msMats.mat     
│   ├── test_extract_data_matlab.py     
│── venv/                               
│── .gitignore                           
│── MSProject.code-workspace             
│── pyproject.toml                       
│── README.md                            
```

## **Files in the project

1. inspect_data
    - preprocessing _functions: functions for preprocessing data before strating the analysis
    - analysis_functions1 : functions and plotting for Figure 1 in the article
    - analysis_functions2 : functions and plotting for Figure 2 in the article
2. plotting_figures
    - preprocessing _data : first step in the project to get the right analysis + to handle matlab files.
    - check_preprocessing : this function is for you Validation of the preprocessing part.
    - analysis1 : analysis and plotting for figure 1.
    - analysis2_for_each_monkey : analysis and plotting for figure 2 , for each monkey separately.
3. config : in this file you can change the data directory.
4.test
    -test-extract_data_matlab : testing file for main function in analysis1_functions.

## **Installation**

*Clone the Repository:*

```bash
git clone <repository_url>
cd MSProject
```

*Set Up a Virtual Environment:*

```bash
pip install virtualenv
# create virtual environment (serve only this project):
python -m venv venv
# activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
# update venv's python package-installer (pip) to its latest version
python.exe -m pip install --upgrade pip
```

# Install required packages

pip install -r requirements.txt

# (Optional) Install additional development dependencies for linting and testing

pip install -r requirements-dev.txt

# Dependencies

This project requires `tkinter`, which is pre-installed with most Python distributions but may be missing in some environments.  
On Windows (usually pre-installed, but if missing, reinstall Python with "Tcl/Tk" enabled)

If you encounter issues, install it manually:

```bash
# On Ubuntu/Debian:
sudo apt-get install python3-tk
# On Mac:
brew install python-tk
```

## **Testing**

The project includes unit tests to validate data processing, file handling, and visualization.
To run all tests:

```bash
pytest -v
```
