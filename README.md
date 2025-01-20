# **MSProject**

## **Overview**

**MSProject** is a Python-based project designed to analyze MATLAB `.mat` files and extract  data for further analysis. This project provides modularized functions and tests to ensure functionality, supporting mixed data types and robust error handling.

---

## **Project Structure**

'.....'

## **Installation**

*Clone the Repository:*
'''bash
git clone <repository_url>
cd MSProject
'''

*Set Up a Virtual Environment:*
'''bash
pip install virtualenv
# create virtual environment (serve only this project):
python -m venv venv
# activate virtual environment
.\venv\Scripts\activate
# update venv's python package-installer (pip) to its latest version
python.exe -m pip install --upgrade pip
'''

*install projects packages*
pip install -e .
# install dev packages (Additional packages for linting, testing and other developer tools)
pip install -e .[dev]

## **Testing**

'''bash
pytest -v
'''
