#!/usr/bin/python3

import os
import sys
import json

# Function to extract URLs from a JSON file
def extract_urls_from_json(json_filename, output_filename):
    with open(json_filename, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)

    with open(output_filename, 'w') as output_file:
        for entry in data:
            request = entry.get('Request')
            if request:
                url = request.get('URL')
                if request.get('Body') != "":
                    url += "?" + request.get('Body')
                output_file.write(url + '\n')

# Filter the URL starts with "http" and contains '?'
def filter_urls(input_file, output_file):
    filtered_urls = []
    with open(input_file, 'r') as infile:
        for line in infile:
            if '?' in line and line.startswith('http'):
                filtered_urls.append(line)

    with open(output_file, 'w') as outfile:
        for url in filtered_urls:
            outfile.write(url)

# Replace Parameter value with 'FUZZ'
def replace_parameter_values(filename):
    updated_urls = []

    with open(filename, 'r') as file:
        for url in file:
            parts = url.strip().split('&')
            updated_parts = []

            for part in parts:
                param_split = part.split('=')

                if len(param_split) == 2:
                    param_key, param_value = param_split
                    param_value = 'FUZZ'
                    updated_param = f"{param_key}={param_value}"
                else:
                    # If there's no '=', keep the part as it is
                    updated_param = part

                updated_parts.append(updated_param)

            updated_url = '&'.join(updated_parts)
            updated_urls.append(updated_url)

    with open(filename, 'w') as file:
        file.writelines("\n".join(updated_urls))

# Remove URL without FUZZ and sort them
def process_filtered_urls(input_file):
    # Read lines from the input file and filter out empty and non-'FUZZ' lines
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file.readlines() if 'FUZZ' in line]

    # Remove duplicates and sort the lines
    unique_sorted_lines = sorted(set(lines))

    # Write the unique, sorted lines back to the input file (overwriting it)
    with open(input_file, 'w') as file:
        file.write('\n'.join(unique_sorted_lines))

# Function to delete a file
def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("[+] usage: python3 %s <json_file>" % sys.argv[0])
        sys.exit(-1)

    json_filename = sys.argv[1]
    extracted_URL = 'extracted_URL.txt'
    filtered_URL = 'filtered_URL.txt'
    modified_URL = 'modified_URL.txt'

    # Step 1: Extract URLs from JSON
    extract_urls_from_json(json_filename, extracted_URL)
    print("[+] URLs have been extracted and saved to 'extracted_URL.txt'.")

    # Step 2: Filter and clean URLs, and replace parameter values with "FUZZ"
    filter_urls(extracted_URL, filtered_URL)
    replace_parameter_values(filtered_URL)
    process_filtered_urls(filtered_URL)
    print("[+] URLs have been filtered, cleaned, parameter values replaced with 'FUZZ', and sorted.")

    # Step 3: Delete the "extracted_URL.txt" file
    delete_file(extracted_URL)
    print("[+] 'extracted_URL.txt' has been deleted.")

    # Step 4: Nuclei!
    print("[+] The next step you can do is use Nuclei to run the scan against 'filtered_URL.txt'!")
    print("\n[+] Example: nuclei -l filtered_URL.txt -t '/opt/nuclei/fuzzing-templates' -rl 05")
