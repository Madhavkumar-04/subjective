from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data
for pkg in ["punkt", "wordnet"]:
    nltk.download(pkg)

def preprocess_text(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return lemmatized_tokens

def create_naive_bayes_model():
    # Manually defined training data for "What is photosynthesis?"
    training_data = [
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis is how plants use sunlight to make food from carbon dioxide and water, producing oxygen.", 9),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s the process where plants make glucose using light, water, and CO2, releasing oxygen.", 10),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Plants use sunlight to convert water and carbon dioxide into sugar.", 8),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis is when plants make their own food.", 6),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s how plants grow using sunlight.", 4),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Plants take in sunlight and make oxygen.", 5),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis uses chlorophyll to make energy.", 6),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s a process that makes glucose in plants with light.", 7),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Plants use carbon dioxide and water to make food in sunlight, giving off oxygen.", 9),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis is the process of plants making food with sunlight, water, and air.", 8),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s when plants use sunlight to make sugar and oxygen from CO2 and water.", 10),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Plants make energy from sunlight.", 5),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis is how plants breathe and make food.", 4),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s a chemical reaction in plants using sunlight.", 6)
    ]

    # Prepare data
    texts = [expected_answer for expected_answer, _, _ in training_data] + [student_answer for _, student_answer, _ in training_data]
    labels = [1 if score >= 7 else 0 for _, _, score in training_data] * 2  # Binary labels: 1 for good answers (score >= 7), 0 for poor

    # Create vectorizer and model
    vectorizer = CountVectorizer(tokenizer=preprocess_text)
    X = vectorizer.fit_transform(texts)
    clf = MultinomialNB()
    clf.fit(X, labels)

    # Save model and vectorizer
    joblib.dump(clf, 'naive_bayes_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("Naive Bayes model and vectorizer saved successfully.")

if __name__ == '__main__':
    create_naive_bayes_model()