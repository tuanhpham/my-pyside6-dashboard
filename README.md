# my-pyside6-dashboard

A custom dashboard application built using PySide6.

## Project Description

This project is a custom dashboard application that features a custom title bar, navigation content, and various pages. It uses PySide6 for the GUI and includes components such as a style manager, icon manager, and custom widgets.

## Setup

### Create Virtual Environment

```bash
python -m venv venv
```

# activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# install requirements
pip install -r requirements.txt

# to make local components available in virtual environment
pip install -e . 

# refresh new requirements.txt
pip freeze > requirements.txt
