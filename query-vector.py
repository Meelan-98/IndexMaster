from sklearn.feature_extraction import FeatureHasher

def convert_query_to_vector(query):
    # Convert query to vector representation using feature hashing
    hasher = FeatureHasher(n_features=5, input_type='string')
    vector = hasher.transform([query]).toarray()
    
    return vector.flatten()

# Example queries
query1 = {'name': 'query_name', 'job_title': 'query_job_title'}
query2 = {'address': 'query_address', 'company': 'query_company'}
query3 = {'name': 'query_name', 'job_title': 'query_job_title', 'company': 'query_company'}

# Convert queries to vector representation
vector1 = convert_query_to_vector(query1)
vector2 = convert_query_to_vector(query2)
vector3 = convert_query_to_vector(query3)

# Print the vector representations
print("Vector representation for query1:", vector1)
print("Vector representation for query2:", vector2)
print("Vector representation for query3:", vector3)
