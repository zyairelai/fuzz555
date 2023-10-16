import os
import sys
import json

if len(sys.argv) != 2:
    print("[+] usage: python3 %s <json_file>" % sys.argv[0])
    sys.exit(-1)

# Read the JSON data from uwu.json
with open(sys.argv[0], 'r') as file:
    data = json.load(file)

# Create or open a file for writing the extracted URLs
with open('extracted_URL.txt', 'w') as output_file:
    # Iterate through the entries
    for entry in data:
        request = entry.get('Request')

        if request:
            url = request.get('URL')
            if request.get('Body') != "":
                url += "?" + request.get('Body')
            output_file.write(url + '\n')

print("[+] URLs have been extracted and saved to 'extracted_URL.txt'.")

# Define the filename of the input file
input_filename = 'extracted_URL.txt'

# Define the filename for the output file
output_filename = 'modified_URL.txt'

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

# Read the input file and process the URLs
with open(input_filename, 'r') as input_file:
    urls = input_file.readlines()

# Process and replace parameter values with "FUZZ"
modified_urls = [replace_parameters_with_fuzz(url.strip()) for url in urls]

# Write the modified URLs to the output file
with open(output_filename, 'w') as output_file:
    output_file.writelines('\n'.join(modified_urls))

print("[+] Parameter values have been replaced with 'FUZZ' and saved to 'modified_URL.txt'.")

# Delete the "extracted_URL.txt"
if os.path.exists("extracted_URL.txt"):
    os.remove("extracted_URL.txt")
    print("[+] 'extracted_URL.txt' has been deleted.")

print("[+] The next step you can do is use Nuclei to run the scan against 'modified_URL.txt'!")
print("\n[+] Example: nuclei -l modified_URL.txt -t '/opt/nuclei/fuzzing-templates' -rl 05")
