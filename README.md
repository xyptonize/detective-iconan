# faviconfinder
## Usage
```bash
pip3 install -r requirements.txt
python3 faviconfinder.py -u <favicon-url1,favicon-url2,...> -s <platform>
```

## About Faviconfinder:

Faviconfinder is a tool designed to detect cloned phishing websites. It works by identifying websites that share the same favicon, which can be an indicator of potential cloning. The tool is particularly useful in uncovering cloned phishing sites. However, it may not be as effective against websites created from scratch by experienced blackhat hackers, as they tend to build sites from the ground up.

Faviconfinder utilizes data from various platforms such as Shodan, Censys, and Zoomeye to perform its analysis. If there is no relevant data available on these platforms, the tool may not yield any output.

While this tool may not be effective against veteran blackhat hackers who create websites from scratch, it can be a valuable asset in identifying and thwarting the efforts of script kiddies who simply clone and deploy websites for small-scale scamming activities.

## Planning to do
I am planning to make the filters more flexible that users can filter their specific filters and make it as a three in one platform for Shodan, Censys and Zoomeye.

