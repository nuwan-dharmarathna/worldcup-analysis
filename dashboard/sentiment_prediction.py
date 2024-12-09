from joblib import load



def entity_sentiment_analysis(text, target_entity):
    
    sentiment_model = load("../models/sentiment_model.joblib")
    ner_model = load("../models/ner_model.joblib")
    
    # Extract entities
    entities = ner_model(text)
    entity_names = [e['word'] for e in entities]
    
    # Check if the target entity is in the text
    if target_entity not in entity_names:
        return f"No sentiment detected for {target_entity}"
    
    # Get sentiment
    sentiment = sentiment_model(text)[0]['label']
    
    # Interpret sentiment relative to the entity
    if target_entity in text:
        if sentiment == "POSITIVE":
            return f"Positive sentiment for {target_entity}"
        elif sentiment == "NEGATIVE":
            return f"Negative sentiment for {target_entity}"
    
    return f"Neutral sentiment for {target_entity}"