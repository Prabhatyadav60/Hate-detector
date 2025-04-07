# 🛡️ Offensive Comment Analyzer

This project is a Python-based tool that detects and categorizes offensive content from user comments using the **Google Gemini API** and **profanity filtering**. It helps in moderating user-generated content by flagging hate speech, toxicity, profanity, and harassment, along with visual summaries.

---

## 🚀 Features

- 🔍 Detects whether a comment is offensive or not  
- 🏷️ Categorizes offense type: `hate speech`, `toxicity`, `profanity`, `harassment`, or `none`  
- 🎯 Assigns severity on a scale of 1–5  
- 🧠 Uses Google Gemini API for AI-powered analysis  
- 🧹 Uses `better_profanity` for keyword-based filtering  
- 📊 Visualizes offense type distribution (Bar + Pie charts)  
- 📄 Outputs a detailed CSV report and summary  

---
## Demo ->

## 📂 Input

CSV file with the following columns:

csv
comment_id,comment_text
📤 Output
A new CSV file with added columns:

is_offensive

offense_type

explanation

severity

Bar chart: offense_bar_chart.png

Pie chart: offense_pie_chart.png

Console output summary

## ⚙️ Installation
Install required libraries using:


pip install requests matplotlib better_profanity
🔑 API Key
Replace this line in the script:

api_key = "API_KEY"
with your actual API key from Google AI Studio.

## ▶️ How to Run

python script.py input.csv output.csv
Example:

python detect_offensive_comments.py comments.csv results.csv
Make sure input.csv exists in the correct format.

## 🧪 What It Does
Loads all comments from the input CSV

Checks for basic profanity using better_profanity

Sends the comments to Gemini API for detailed analysis

Updates each comment with analysis results

Saves results in a new CSV

Displays a summary and charts showing offense breakdown
