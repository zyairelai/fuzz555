import os
import sys
import json

# Function to extract URLs from a JSON file
def extract_urls_from_json(json_filename, output_filename):
    with open(json_filename, 'r') as file:
        data = json.load(file)

    with open(output_filename, 'w') as output_file:
        for entry in data:
            request = entry.get('Request')
            if request:
                url = request.get('URL')
                if request.get('Body') != "":
                    url += "?" + request.get('Body')
                output_file.write(url + '\n')

def filter_urls(input_file, output_file):
    filtered_urls = []
    with open(input_file, 'r') as infile:
        for line in infile:
            if '?' in line and line.startswith('http'):
                filtered_urls.append(line)

    filtered_urls.sort()  # Sort the filtered URLs

    with open(output_file, 'w') as outfile:
        for url in filtered_urls:
            outfile.write(url)

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
    print("[+] URLs have been filtered, cleaned, parameter values replaced with 'FUZZ', and sorted.")

    # Step 3: Delete the "extracted_URL.txt" file
    delete_file(extracted_URL)
    print("[+] 'extracted_URL.txt' has been deleted.")

    # Step 4: Nuclei!
    print("[+] The next step you can do is use Nuclei to run the scan against 'filtered_URL.txt'!")
    print("\n[+] Example: nuclei -l filtered_URL.txt -t '/opt/nuclei/fuzzing-templates' -rl 05")
