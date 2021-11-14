import pickle

def most_common():
    str_l = pickle.loads(open(r'./shapecolour.p','rb').read())
    dict_max = max(str_l,key=str_l.count)
    dict_result = {'Colour':dict_max['colour'],'Shape':dict_max['shape']}
    return dict_result