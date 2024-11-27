#!/bin/bash

# Train the model
python3 train_model.py

# Create Sqlite3 DB
python3 database.py

# Run program
python3 main.py