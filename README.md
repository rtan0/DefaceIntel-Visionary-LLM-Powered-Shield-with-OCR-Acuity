# DefaceIntel-Visionary


# Description
The purpose of this project is to develop a robust Web Defacement Detection tool that monitors websites for signs of defacement, an attack where the visual appearance of a website is altered by unauthorized users. the tool aims to promptly provide alert if a website content is manipulated, which is often a result of cyber attacks such as those carried out by hacktivists. The system utilizes two primary detection methods: a) analyzing drastic changes in webpage size and b) scanning for keywords and phrases associated with hacktivism, including those within images, using generative AI such as GPT that has been trained on large data including OSINT.


# Details
1. **Webpage Size Monitor**: This module keeps track of the size of webpages. It fetches the webpage at regular intervals, records the size, and compares it with the baseline size to detect any drastic changes. A significant change in size is considered an indicator of potential defacement.
2. **Generative AI and OCR**
- A generative AI model such as GPT4 generates a list of new and potential keywords based on news, threat intelligence content it has learned. This proactive approach helps the tool stay one step ahead in detecting hacktivist content.
-  Keywords Detection: Optical Character Recognition (OCR), this module scans the textual content of a webpage, including text embedded in images, for specific keywords and phrases that are often used by hacktivists.
<img width="1041" alt="DefaceIntel 2023-12-08 07_57_44" src="https://github.com/rtan0/DefaceIntel-Visionary-LLM-Powered-Shield-with-OCR-Acuity/assets/153265724/d7c5de0b-317b-4e98-883c-64cff519e722">
