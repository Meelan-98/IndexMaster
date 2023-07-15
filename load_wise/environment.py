import json

def initial_state_function(workload_path):

    with open(workload_path, 'r') as json_file:
        data = json.load(json_file)

    fields = ['first_name','last_name','title','address','phone_number','job_title','company','email','passport_number','suffix']

    state = []

    for i in range (0,len(fields)):
        state.append(0)

    first_query = data[0]

    for field in first_query.keys():
        location = fields.index(field)
        state[location] = 1

    return([state,len(data)])

def state_change(path, tot_queries, rem_queries):

    fields = ['first_name','last_name','title','address','phone_number','job_title','company','email','passport_number','suffix']

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    which_query = tot_queries - rem_queries

    existence_map = [0]*len(fields)

    query = data[which_query]

    for field in query.keys():
        location = fields.index(field)
        existence_map[location] = 1

    return(existence_map)

# print(initial_state_function("workloads/test_workload_2.json"))
