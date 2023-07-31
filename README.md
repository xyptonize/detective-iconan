# faviconfinder
## Usage
```bash
pip3 install requirements.txt
python3 faviconfinder.py -u <favicon-url1,favicon-url2,...> -s <platform>
```

## About
Faviconfinder is just a poor tool which detects cloned phishing websites. In order to find benign websites the cloned website must contain same favicon.
I think this tool has no practical usage since Veteran blackhats don't clone websites they make it by themselves so it won't work against that. But it can be used against script kiddies who just clones and deployes it for a little scam money. 

This tool leverages Shodan, Censys, Zoomeye to work so if there is no data in these platform there will be no output.

## Planning to do
I am planning to make the filters more flexible that users can filter their specific filters and make it as a three in one platform for Shodan, Censys and Zoomeye.

