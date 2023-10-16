# fuzz555
Reading JSON from Burp Logger++ and make it ready for Nuclei Fuzzing!

# GRAB THE SCRIPT
```
wget https://raw.githubusercontent.com/zyairelai/fuzz555/main/fuzz555.py
```

# Tutorial / Usage
### 1. Export all requests from Burp Logger++ Extension as JSON
![image](https://github.com/zyairelai/fuzz555/assets/49854907/124f0568-67cc-478c-9273-49432f0d91e9)

### 2. Run the script with the Logger++ JSON as input
```
python3 fuzz555.py LoggerPlusPlus.json
```

### 3. The output will be compatible for Nuclei Fuzzing Template!
```
$ cat modified_URL.txt
http://192.168.183.159/phpMyAdmin/index.php?token=FUZZ
http://192.168.183.159/phpMyAdmin/index.php?phpMyAdmin=FUZZ&phpMyAdmin=FUZZ&pma_username=FUZZ&pma_password=FUZZ&server=FUZZ&phpMyAdmin=FUZZ&lang=FUZZ&convcharset=FUZZ&token=FUZZ
```

### 4. Happy Nuclei for quick win!
```
nuclei -l modified_URL.txt -t '/opt/nuclei/fuzzing-templates'
```
