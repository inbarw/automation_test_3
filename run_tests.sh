#!/bin/bash

# Remove old results
rm -rf ./test_results/allure-results/*
rm -rf ./test_results/allure-report/*

# Create directories if they don't exist
mkdir -p ./test_results/allure-results
mkdir -p ./test_results/allure-report

# Run tests with Allure results output directory specified
pytest tests --alluredir=./test_results/allure-results

# Generate Allure report
allure generate ./test_results/allure-results -o ./test_results/allure-report

# Open the report
allure open ./test_results/allure-report