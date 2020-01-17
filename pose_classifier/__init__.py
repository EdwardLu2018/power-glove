import pickle

OPEN = 0
FIST = 1
ONE = 2
TWO = 3
THREE = 4
FOUR = 5
MIDDLE = 6
OK = 7
ROCK =8
NEUTRAL = 9
CALI = 10
THUMB = 11
GUN = 12

L_PICKLE = 'left_glove_classifier.pkl'
R_PICKLE = 'rght_glove_classifier.pkl'

def classify_pose(data, right=False):
    flex_data = data.flex_data()
    if right:
        clf = pickle.load(open(R_PICKLE, 'rb'))
    else:
        clf = pickle.load(open(L_PICKLE, 'rb'))
    return clf.predict([flex_data])
