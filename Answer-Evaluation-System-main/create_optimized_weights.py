import joblib

def create_optimized_weights():
    # Default weights (same as fallback in evaluate)
    weights = [0.15, 0.1, 0.1, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1]
    
    # Optionally, you can optimize weights here using a dataset and optimization algorithm
    # For now, we use the default weights
    joblib.dump(weights, 'optimized_weights.pkl')
    print("Optimized weights saved to optimized_weights.pkl")

if __name__ == '__main__':
    create_optimized_weights()