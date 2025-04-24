from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask_mysqldb import MySQL
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
from fine_tune_sentence_transformer import fine_tune_sentence_transformer

def optimize_weights(mysql):
    cur = mysql.connection.cursor()
    query = """
        SELECT exact_match_score, partial_match_score, cosine_similarity_score, 
               sentiment_score, enhanced_sentence_match_score, multinomial_naive_bayes_score,
               semantic_similarity_score, coherence_score, relevance_score, corrected_score
        FROM StudentAnswers
        WHERE corrected_score IS NOT NULL
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    if len(data) < 10:
        print("Insufficient data for weight optimization.")
        return None

    X = np.array([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]] for row in data])
    y = np.array([row[9] for row in data])

    model = LinearRegression()
    model.fit(X, y)
    optimized_weights = model.coef_ / np.sum(model.coef_)  # Normalize weights
    weights = optimized_weights.tolist()

    # Save optimized weights
    joblib.dump(weights, 'optimized_weights.pkl')
    print("Weights optimized and saved:", weights)
    return weights

def retrain_models(mysql):
    # Fine-tune SentenceTransformer
    fine_tune_success = fine_tune_sentence_transformer(mysql)
    
    # Optimize weights
    weights = optimize_weights(mysql)
    
    return {
        'fine_tune_success': fine_tune_success,
        'weights_updated': weights is not None
    }

def init_scheduler(app, mysql):
    scheduler = BackgroundScheduler()
    
    # Schedule retraining daily at midnight
    scheduler.add_job(
        func=retrain_models,
        trigger=CronTrigger(hour=0, minute=0),
        args=[mysql],
        id='retrain_models',
        name='Retrain models and optimize weights daily',
        replace_existing=True
    )
    
    scheduler.start()
    
    # Shutdown scheduler when Flask app exits
    import atexit
    atexit.register(lambda: scheduler.shutdown())
    
    return scheduler