import re
import pandas as pd

# Step 1: Prepare the index of words with scores
# WORDS NEED TO BE WRITTEN IN ALL SMALL LETTERS
word_scores = {
    'gaming': 10,
    'mus': 5,
    'dator': 2,
    'skärm': 6,
    'tangentbord': 5,
    'kalsonger': 20
}

# Step 2: Preprocess the input
def preprocess_input(text):
    # Normalize (lowercase)
    text = text.lower()
    # Tokenize (split into words) using regex to handle punctuation
    words = re.findall(r'\b\w+\b', text)
    return words

# Step 3: Calculate the score for each input
def calculate_score(input_text, word_scores):
    # Gets words from the input_text
    words = preprocess_input(input_text)
    # Sets all the scores to 0
    score = 0
    
    for word in words:
        if word in word_scores:
            score += word_scores[word]
    return score

# Read data from the CSV file
def read_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    # Assuming the CSV has columns 'Title' and 'Price'
    titles = df['Title'].tolist()
    
    def parse_price(price_str):
        # Remove non-digit characters
        cleaned_price = re.sub(r'\D', "", price_str)
        # Return 0 if the cleaned price is empty, otherwise convert to integer
        return int(cleaned_price) if cleaned_price else 0

    prices = df['Price'].apply(parse_price).tolist()
    return df, titles, prices

# Calculate scores and add them to the DataFrame
def score_inputs(df, titles, prices, word_scores):
    scores = []
    for title, price in zip(titles, prices):
        score = calculate_score(title, word_scores)
        if price < 1000:
            score += 1  # Increment score if cost is less than 1000 kr
        scores.append(score)
    
    df['Score'] = scores
    return df

# Example usage
file_path = 'facebook_data.csv'
df, input_texts, input_costs = read_data_from_csv(file_path)

# Calculate scores and update the DataFrame
df = score_inputs(df, input_texts, input_costs, word_scores)

# Sort the DataFrame by the score in descending order
df = df.sort_values(by='Score', ascending=False)

# Write the sorted DataFrame back to the CSV file
df.to_csv('sorted_scraped_data.csv', index=False, encoding='utf-8')

print("Data has been scored and saved to sorted_scraped_data.csv")
