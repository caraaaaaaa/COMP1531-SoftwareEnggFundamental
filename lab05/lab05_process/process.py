import json
import operator
import pickle

def process():
    str_l = pickle.loads(open(r'./shapecolour.p','rb').read())
    dict_max = max(str_l,key=str_l.count)
    dict_result = {"mostCommon" :{'colour':dict_max['colour'],'shape':dict_max['shape']},
                  "rawData" : str_l}

    result = json.dumps(dict_result)
    
    with open('processed.json', 'w') as f:
        f.write(result)
