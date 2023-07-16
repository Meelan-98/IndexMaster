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

def get_action(index_choice):
    
    if (index_choice==0):
        index_name = "passport_number_1"
    elif (index_choice==1):
        index_name = "email_1"
    elif (index_choice==2):
        index_name = "first_name_1_last_name_1"
    elif (index_choice==3):
        index_name = "job_title_1_company_1"
    elif (index_choice==4):
        index_name = "first_name_1"
    elif (index_choice==5):
        index_name = "last_name_1"
    elif (index_choice==6):
        index_name = "job_title_1"
    elif (index_choice==7):
        index_name = "company_1"
    elif (index_choice==8):
        index_name = "title_1"

    return(index_name)

# print(initial_state_function("workloads/test_workload_2.json"))
