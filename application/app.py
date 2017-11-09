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


@app.route("/api/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)

@app.route("/api/tester", methods=["GET"])
def get_test():
    response = jsonify({'death': 'cancer'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# inputs
training_data = './static/public/train.csv'
include = ['Age', 'Sex', 'Embarked', 'Survived']
dependent_variable = include[-1]

model_directory = 'model'
model_file_name = '%s/model.pkl' % model_directory
model_columns_file_name = '%s/model_columns.pkl' % model_directory

# These will be populated at training time
model_columns = None
clf = None


@app.route('/predict', methods=['POST'])
def predict():
    print("inside predict")
    import pandas as pd
    from sklearn.externals import joblib
    if clf:
        try:
            json_ = [
                {'Age': 85, 'Sex': 'male', 'Embarked': 'S'},
                {'Age': 24, 'Sex': 'female', 'Embarked': 'C'},
                {'Age': 3, 'Sex': 'male', 'Embarked': 'C'},
                {'Age': 21, 'Sex': 'male', 'Embarked': 'S'}
            ]
            # json_ = request.json
            query = pd.get_dummies(pd.DataFrame(json_))

            # https://github.com/amirziai/sklearnflask/issues/3
            # Thanks to @lorenzori
            query = query.reindex(columns=model_columns, fill_value=0)

            prediction = list(clf.predict(query))
            print(prediction)
            # response = jsonify({'prediction':'predict'})
            # response.headers.add('Access-Control-Allow-Origin', '*')
            # return response
            return prediction


        except Exception:
            print('exception')
            # response = jsonify({'prediction': 'error'})
            # response.headers.add('Access-Control-Allow-Origin', '*')
            # return response
            # return jsonify({'error': str(e), 'trace': traceback.format_exc()})
    else:
        print('train first')
        # response = jsonify({'prediction': 'else'})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        # return response

@app.route('/train', methods=['GET'])
def train():
    # using random forest as an example
    # can do the training separately and just update the pickles

    df = pd.read_csv(training_data)
    df_ = df[include]

    categoricals = []  # going to one-hot encode categorical variables

    for col, col_type in df_.dtypes.iteritems():
        if col_type == 'O':
            categoricals.append(col)
        else:
            df_[col].fillna(0, inplace=True)  # fill NA's with 0 for ints/floats, too generic

    # get_dummies effectively creates one-hot encoded variables
    df_ohe = pd.get_dummies(df_, columns=categoricals, dummy_na=True)

    x = df_ohe[df_ohe.columns.difference([dependent_variable])]
    y = df_ohe[dependent_variable]

    # capture a list of columns that will be used for prediction
    global model_columns
    model_columns = list(x.columns)
    # joblib.dump(model_columns, model_columns_file_name)

    global clf
    clf = rf()
    # start = time.time()
    clf.fit(x, y)
    # print('Trained in %.1f seconds' % (time.time() - start))
    # print('Model training score: %s' % clf.score(x, y))

    # joblib.dump(clf, model_file_name)

    print('Predict')
    prediction = predict()
    # convert to ints
    d = map(lambda x: int(x), prediction)

    # response = jsonify({'train':'Success'})
    response = jsonify({'prediction': list(d)})
    # response = jsonify(result=list(d))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route("/api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        email=incoming["email"],
        password=incoming["password"]
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )


@app.route("/api/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@app.route("/api/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403

