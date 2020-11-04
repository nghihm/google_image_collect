# Introduction
This directory contains download image from url code and js_console.js from pyimagesearch https://www.pyimagesearch.com/2017/12/04/how-to-create-a-deep-learning-dataset-using-google-images/

# Requirements
Python 3.6 or later with all lib in requirement.txt

# Install
pip install -r requirement.txt

# Use
1. Install/update Chrome: https://www.google.com/chrome/
2. Download chromedriver: https://chromedriver.chromium.org/
3. Run
```bash 
python google_images_collects.py -m ALL -s searchtext -o image_folder -d file_urls.txt -g chromedriver
```