import argparse
import csv
import json
import os
import re
import requests
from collections import Counter
from better_profanity import profanity
import matplotlib.pyplot as plt

# Load profanity words
profanity.load_censor_words()


api_key = "API_KEY"

def analyze_all_comments_with_gemini(all_comments, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    formatted_comments = [
        {"id": row["comment_id"], "text": row["comment_text"]} for row in all_comments
    ]

    prompt = (
        "You are an AI content moderator. Analyze the following list of comments.\n"
        "Return a JSON array where each element corresponds to a comment, in this format:\n"
        "{\n"
        "  \"id\": comment_id,\n"
        "  \"is_offensive\": true/false,\n"
        "  \"offense_type\": \"hate speech\"/\"toxicity\"/\"profanity\"/\"harassment\"/\"none\",\n"
        "  \"explanation\": \"short explanation\",\n"
        "  \"severity\": 1-5\n"
        "}\n\n"
        f"Comments:\n{json.dumps(formatted_comments, indent=2)}"
    )

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            output = response.json()
            response_text = output["candidates"][0]["content"]["parts"][0]["text"]
            match = re.search(r"\[.*\]", response_text, re.DOTALL)
            if match:
                return json.loads(match.group())
        else:
            print(f"Gemini API error: {response.status_code}")
    except Exception as e:
        print(f"Gemini API exception: {str(e)}")

   
    return [
        {
            "id": row["comment_id"],
            "is_offensive": False,
            "offense_type": "none",
            "explanation": "Error or fallback",
            "severity": 0
        }
        for row in all_comments
    ]

def visualize_offense_distribution(comments):
    offensive_comments = [row for row in comments if row["is_offensive"]]
    offense_types = [row["offense_type"] for row in offensive_comments]

    count = Counter(offense_types)
    labels = list(count.keys())
    values = list(count.values())

   
    plt.figure(figsize=(8, 4))
    plt.bar(labels, values, color="salmon")
    plt.title("Offense Type Distribution (Bar Chart)")
    plt.xlabel("Offense Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("offense_bar_chart.png")
    plt.show()

 
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Offense Type Distribution (Pie Chart)")
    plt.tight_layout()
    plt.savefig("offense_pie_chart.png")
    plt.show()

def print_summary(comments):
    offensive_comments = [row for row in comments if row["is_offensive"]]
    print(f"\nSummary: {len(comments)} total comments, {len(offensive_comments)} marked offensive")

    breakdown = Counter(row["offense_type"] for row in offensive_comments)
    print("\nOffense Type Breakdown:")
    for offense_type, count in breakdown.items():
        print(f" - {offense_type}: {count}")

    top_offensive = sorted(offensive_comments, key=lambda x: -int(x.get("severity", 0)))[:5]
    print("\nTop 5 Most Offensive Comments:")
    for row in top_offensive:
        print(f"ID: {row['comment_id']}, Severity: {row['severity']}, Type: {row['offense_type']}")
        print(f"Text: {row['comment_text']}")
        print(f"Explanation: {row['explanation']}\n")

def process_all_at_once(input_file, output_file, api_key):
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        comments = [row for row in reader]

   
    for row in comments:
        if profanity.contains_profanity(row["comment_text"]):
            row["comment_text"] += "\nNote: Detected profanity."

    print(f"Total comments loaded: {len(comments)}")

    results = analyze_all_comments_with_gemini(comments, api_key)

  
    for row in comments:
        result = next((r for r in results if str(r["id"]) == str(row["comment_id"])), None)
        if result:
            row.update({
                "is_offensive": result.get("is_offensive", False),
                "offense_type": result.get("offense_type", "none"),
                "explanation": result.get("explanation", ""),
                "severity": result.get("severity", 0)
            })

   
    fieldnames = list(comments[0].keys())
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comments)

   
    print_summary(comments)


    visualize_offense_distribution(comments)

def main():
    parser = argparse.ArgumentParser(description="Moderate entire comment dataset at once with charts.")
    parser.add_argument("input", help="Input CSV file path")
    parser.add_argument("output", help="Output CSV file path")
    args = parser.parse_args()

    process_all_at_once(args.input, args.output, api_key)

if __name__ == "__main__":
    main()
