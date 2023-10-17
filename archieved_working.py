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

# Function to filter and clean URLs, and replace parameter values with "FUZZ"
def process_urls(input_filename, output_filename):
    cleaned_lines = set()

    with open(input_filename, "r") as file:
        lines = file.readlines()

    for line in lines:
        cleaned_line = line.rstrip("?").strip()
        if cleaned_line.startswith("http") and '=' in cleaned_line:
            cleaned_lines.add(replace_parameters_with_fuzz(cleaned_line))

    sorted_lines = sorted(cleaned_lines)  # Sort the cleaned URLs

    with open(output_filename, "w") as file:
        for line in sorted_lines:
            file.write(line + '\n')

# Function to replace parameter values with "FUZZ"
def replace_parameters_with_fuzz(url):
    parts = url.split('?')
    if len(parts) > 1:
        base_url, query_string = parts
        parameters = query_string.split('&')
        modified_parameters = []
        for parameter in parameters:
            key, value = parameter.split('=')
            modified_parameters.append(f'{key}=FUZZ')
        modified_query_string = '&'.join(modified_parameters)
        return f'{base_url}?{modified_query_string}'
    else:
        return url

# Function to delete a file
def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("[+] usage: python3 %s <json_file>" % sys.argv[0])
        sys.exit(-1)

    json_filename = sys.argv[1]
    extracted_url_filename = 'extracted_URL.txt'
    modified_url_filename = 'modified_URL.txt'

    # Step 1: Extract URLs from JSON
    extract_urls_from_json(json_filename, extracted_url_filename)
    print("[+] URLs have been extracted and saved to 'extracted_URL.txt'.")

    # Step 2: Filter and clean URLs, and replace parameter values with "FUZZ"
    process_urls(extracted_url_filename, modified_url_filename)
    print("[+] URLs have been filtered, cleaned, parameter values replaced with 'FUZZ', and sorted.")

    # Step 3: Delete the "extracted_URL.txt" file
    delete_file(extracted_url_filename)
    print("[+] 'extracted_URL.txt' has been deleted.")

    # Step 4: Nuclei!
    print("[+] The next step you can do is use Nuclei to run the scan against 'modified_URL.txt'!")
    print("\n[+] Example: nuclei -l modified_URL.txt -t '/opt/nuclei/fuzzing-templates' -rl 05")
