import json

def multiply_list_by_value(lst, value):
    multiplied_list = [item * value for item in lst]
    return multiplied_list


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

    final_vector = []

    for query in data:
        vector = create_binary_vector(attributes,list(query.keys()))
        if vector not in vectorz:
            count.append(1)
            vectorz.append(vector)
        else:
            index = vectorz.index(vector)
            count[index] = count[index] + 1

    for v in range(len(vectorz)):
        final_vector.append(multiply_list_by_value(vectorz[v], count[v]))
    
    return(final_vector)

def flatten_2d_list(nested_list):
    flattened_list = [item for sublist in nested_list for item in sublist]
    return flattened_list


def export_load_vector(file_path):

    fields = ['first_name','last_name','title','address','phone_number','job_title','company','email','passport_number','suffix']
    vector_representation = load_and_iterate_json(file_path,fields)

    vector_representation.append([1,0,1])

    return(flatten_2d_list(vector_representation))


def state_change(current_state,index_choices):
    current_state[-3:] = index_choices[:3]
    return(current_state)

# print(export_load_vector('tData.json'))