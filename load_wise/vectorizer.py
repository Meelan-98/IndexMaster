import json

def create_binary_vector(larger_list, smaller_list):
    binary_vector = []
    smaller_set = set(smaller_list)

    for name in larger_list:
        if name in smaller_set:
            binary_vector.append(1)
        else:
            binary_vector.append(0)

    return binary_vector

def load_and_iterate_json(file_path,attributes):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    vectorz = []
    count =[]

    for query in data:
        vector = create_binary_vector(attributes,list(query.keys()))
        if vector not in vectorz:
            count.append(1)
            vectorz.append(vector)
        else:
            index = vectorz.index(vector)
            count[index] = count[index] + 1
    
    print(count)
    return(vectorz)


fields = ['first_name','last_name','title','address','phone_number','job_title','company','email','passport_number','suffix']
file_path = 'tData.json'
vector_representation = load_and_iterate_json(file_path,fields)

print(vector_representation)
