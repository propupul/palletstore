# palletstore
Store: Pick a product(sku), and program will tell you which location to store it at. 

Retrieve: Chose a product(sku) and the program will tell you which location to get it from, the program choses the oldest item of the product you selected by date.

This program uses Flask. One file contains the program `app.py

Requirements:
Python 3

How to run locally:
1. Clone repo to your computer
2. Create virtualenv `python3 -m venv /path/to/new/virtual/envname`
    - Activate environment `source envname/bin/activate `
3. Install the requirements  from the `requirements.txt`.
    - `$ pip install -r requirements.txt`
4. Run the program `flask run`
5. Open up a browser and sign-in with
    - username: warehouse
    - password: Warehouse_Pass1
    
Note: I've included in the repo a preconfigured database with 2 tables. The relevant is `store_retrieve` it is prefilled with data. In there you have 3 columns: location, sku, and date.
