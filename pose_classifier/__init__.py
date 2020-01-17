import pickle

class PoseClassifier(object):
    def __init__(self):
        self.OPEN = 0
        self.FIST = 1
        self.ONE = 2
        self.TWO = 3
        self.THREE = 4
        self.FOUR = 5
        self.MIDDLE = 6
        self.OK = 7
        self.ROCK = 8
        self.NEUTRAL = 9
        self.CALI = 10
        self.THUMB = 11
        self.GUN = 12

        self.L_PICKLE = 'left_glove_classifier.pkl'
        self.R_PICKLE = 'rght_glove_classifier.pkl'

    def classify_pose(self, data, right=False):
        flex_data = data.flex_data()
        if right:
            clf = pickle.load(open(self.R_PICKLE, 'rb'))
        else:
            clf = pickle.load(open(self.L_PICKLE, 'rb'))
        return clf.predict([flex_data])[0]
