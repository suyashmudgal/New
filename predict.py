import spacy
import string
import pickle

def predictNews(news_text):
    # Load spaCy model
    try:
        nlp = spacy.load('en_core_web_sm')
    except Exception as e:
        return {"error": f"spaCy model not found. Please run 'python -m spacy download en_core_web_sm'. Error: {e}"}
    
    # Load the saved model and TF-IDF vectorizer
    try:
        with open('fake_news_model_xgb.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
    except FileNotFoundError as e:
        return {"error": "Model or vectorizer file not found. Please ensure they are saved."}
    
    # Preprocess the input news text using spaCy
    try:
        doc = nlp(news_text.lower())  # Convert text to lowercase
        clean_words = [token.lemma_ for token in doc if token.text not in string.punctuation and not token.is_stop]
        clean_text = ' '.join(clean_words)
    except Exception as e:
        return {"error": f"Error in preprocessing: {e}"}
    
    # Transform the cleaned text using the TF-IDF vectorizer
    try:
        tfidf_features = vectorizer.transform([clean_text])
    except Exception as e:
        return {"error": f"Error in vectorization: {e}"}
    
    # Predict the label and get probabilities
    try:
        prediction = model.predict(tfidf_features)[0]
        probabilities = model.predict_proba(tfidf_features)[0]
        confidence = max(probabilities) * 100  # Get the highest confidence score
    except Exception as e:
        return {"error": f"Error during prediction: {e}"}
    
    # Map numeric prediction to label
    label = "Real" if prediction == 1 else "Fake"
    
    return [label, f"{confidence:.2f}"]