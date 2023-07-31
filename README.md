# faviconfinder
## Usage
```bash
pip3 install -r requirements.txt
python3 faviconfinder.py -u <favicon-url1,favicon-url2,...> -s <platform> -mail <yes/no>
```

## About Faviconfinder:

Faviconfinder is a tool designed to detect cloned phishing websites. It works by identifying websites that share the same favicon, which can be an indicator of potential cloning. The tool is particularly useful in uncovering cloned phishing sites. However, it may not be as effective against websites created from scratch by experienced blackhat hackers, as they tend to build sites from the ground up.

Faviconfinder utilizes data from various platforms such as Shodan, Censys, and Zoomeye to perform its analysis. If there is no relevant data available on these platforms, the tool may not yield any output.

While this tool may not be effective against veteran blackhat hackers who create websites from scratch, it can be a valuable asset in identifying and thwarting the efforts of script kiddies who simply clone and deploy websites for small-scale scamming activities.

## Planning to do

I plan to enhance the tool's flexibility by making the filters more customizable. This improvement will empower users to specify their own specific filters, allowing for a more tailored and precise search not just for cloned phishing websites. The goal is to make Faviconfinder a versatile three-in-one platform, effectively integrating the capabilities of Shodan, Censys, and Zoomeye to offer comprehensive website analysis.

Additionally, I intend to transform Faviconfinder into a fully-fledged service. This means users can access the tool via an online platform where they can start a search and receive email alerts once the process is complete. This feature will enable users to conveniently monitor potential threats and stay informed about their online presence without the need for manual checks.

## Extra
I know the code so messy. I'm not a programmer or a coder so don't mind it plez xD