from flask import request, render_template, jsonify, url_for, redirect, g
from .models import User
from index import app, db
from sqlalchemy.exc import IntegrityError
from .utils.auth import generate_token, requires_auth, verify_token
from sklearn.ensemble import RandomForestClassifier as rf
import pandas as pd
from sklearn.externals import joblib
import json


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')


@app.route("/api/tester", methods=["GET"])
def get_test():
    print('inside /api/tester')
    response = jsonify({'death': 'cancer'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# # inputs
# training_data = './static/public/train.csv'
# include = ['Age', 'Sex', 'Embarked', 'Survived']
# dependent_variable = include[-1]

# model_directory = 'model'
# model_file_name = '%s/model.pkl' % model_directory
# model_columns_file_name = '%s/model_columns.pkl' % model_directory

# # These will be populated at training time
# model_columns = None
# clf = None


@app.route('/testdeath', methods=['GET'])
def testdeath():
    print("inside test death")
    import pandas as pd
    from sklearn.externals import joblib
    clf = joblib.load('./static/public/model')
    if clf:
        print('successfully loaded -- ready to test')
        try:

            '''
            load data - would use user input
            '''
            x_test = joblib.load('./static/public/x_test')
            y_test = joblib.load('./static/public/y_test')


            prediction = clf.predict(x_test)
            print('Prediction')
            print(prediction)
            d = map(lambda x: float(x), prediction)
            treeScore = clf.score(x_test, y_test)
            print('treeScore', treeScore)
            response = jsonify({'test': 'sucess'})
            # response = jsonify({
            #     'treeScore': treeScore,
            #     'prediction': list(d)
            # })

            response.headers.add('Access-Control-Allow-Origin', '*')
            return response


        except Exception as e:
            print(e)
            response = jsonify({'error': str(e)})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    else:
        print('train first')
        response = jsonify({'test': 'need to train'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/traindeath', methods=['GET'])
def traindeath():
    import pandas as pd
    import numpy as np
    import re
    import csv
    import random


    column_names = ['resident_status', 'education_2003_revision', 'education_reporting_flag',
                    'month_of_death', 'sex', 'detail_age_type', 'detail_age',
                    'place_of_death_and_decedents_status', 'marital_status',
                    'day_of_week_of_death', 'current_data_year',
                    'injury_at_work', 'manner_of_death', 'activity_code',
                    'place_of_injury_for_causes_w00_y34_except_y06_and_y07_',
                    '39_cause_recode', 'race']

    # test if data is already loaded
    try:
        clf = joblib.load('./static/public/model')
        print(clf)
        if clf is not None:
            print('model clf already exists')
            response = jsonify({'test': 'already created'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except Exception:
        print('model not yet created')


    #IMPORT DATA
    data = pd.read_csv('./static/public/intermediate_clean_2015_deaths.csv')

    print('read data from csv') # this is quick

    #SET GENDER TO BINARY
    data['sex'] = data['sex'].map({'F':0, 'M': 1}).astype(int)

    #MAP MARITAL STATUS AND INJURY AT WORK TO INTEGERS
    title_mapping = {"M": 1, "W": 2, "S": 3, "D": 4}
    data['marital_status'] = data['marital_status'].map(title_mapping)

    title_mapping = {"U": 1, "N": 0}
    data['injury_at_work'] = data['injury_at_work'].map(title_mapping)

    #FILL ALL BLANK CELLS
    for each in column_names:
        data[each] = data[each].fillna(0)

    one_hot = ['resident_status', 'education_2003_revision', 'education_reporting_flag',
                     'sex', 'detail_age_type',
                    'place_of_death_and_decedents_status', 'marital_status',
                    'day_of_week_of_death',
                    'injury_at_work', 'manner_of_death', 'activity_code',
                    'place_of_injury_for_causes_w00_y34_except_y06_and_y07_', 'race']

    #ONE HOT ENCODING
    data = pd.get_dummies(data, columns=one_hot)
    print('one hot encoded') # this is quick

    #CREATE TEST AND TRAIN DATA
    from sklearn.model_selection import train_test_split
    n_train = data.drop(['39_cause_recode'], axis=1)
    z_test = data
    x_train, x_test, y_train, y_test = train_test_split(n_train, z_test['39_cause_recode'].ravel(), test_size=0.4, random_state=5)

    print('split data') # quick

    #EXAMPLE IMPLEMENTATION WITH SKLEARN

    from sklearn import tree
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_train,y_train)

    print('fit data clf') # slow


    joblib.dump(clf, './static/public/model')
    print('dumped') # 

    '''
    dump test data for testing -- use user input actually
    '''
    joblib.dump(x_test, './static/public/x_test')
    joblib.dump(y_test, './static/public/y_test')

    # clf.predict(x_test)

    # treeScore = clf.score(x_test, y_test)
    # print("tree score:", treeScore)
    response = jsonify({'trained': 'success'})
    # response = jsonify(result=list(d))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




