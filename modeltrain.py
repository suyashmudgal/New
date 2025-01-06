import pandas as pd
import string
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
import pickle

# Load spaCy model (install if not already installed)
try:
    nlp = spacy.load('en_core_web_sm')
except:
    print("Please install spaCy and download 'en_core_web_sm' model.")
    exit()

# Load Dataset
try:
    df = pd.read_csv('fake.csv')  # Replace with your actual file name
    print("Dataset loaded successfully!")
except Exception as e:
    print("Error loading dataset:", e)
    exit()

# Inspect Dataset
print("Dataset Columns:", df.columns)
print("Sample Data:\n", df.head())

# Ensure required columns exist
required_columns = ['text', 'label']  # Replace with actual column names in your dataset
if not all(col in df.columns for col in required_columns):
    print("Required columns not found in dataset. Please check your dataset.")
    exit()

# Text Preprocessing function using spaCy
def clean_text(text):
    doc = nlp(text.lower())  # Convert text to lowercase
    # Remove punctuation and non-alphanumeric characters
    words = [token.lemma_ for token in doc if token.text not in string.punctuation and not token.is_stop]
    return ' '.join(words)

# Apply text cleaning
df['text'] = df['text'].apply(clean_text)

# Split data into features and target variable
X = df['text']
y = df['label']

# Convert labels to numeric if needed
if y.dtype == object:
    y = y.map({'Fake': 0, 'Real': 1})

# Train-test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature extraction using TF-IDF (unigrams only)
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Model: XGBoost
model = XGBClassifier(random_state=42)

# Train the model
model.fit(X_train_tfidf, y_train)

# Prediction
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.colorbar()
tick_marks = range(2)
plt.xticks(tick_marks, ['Fake', 'Real'], rotation=45)
plt.yticks(tick_marks, ['Fake', 'Real'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# Save the model and vectorizer using pickle
try:
    with open('fake_news_model_xgb.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    with open('tfidf_vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(tfidf_vectorizer, vectorizer_file)
    print("Model and vectorizer saved successfully!")
except Exception as e:
    print("Error saving model/vectorizer:", e)
