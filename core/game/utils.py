import json

def find_paragraph_by_index(index):
    '''
    returns json object
    '''
    with open("static/game-data.json") as json_data:
        print(index)
        data_load = json.load(json_data)
        data_state = [paragraph for paragraph in data_load if paragraph['id']==index][0]
        return json.dumps(data_state)

