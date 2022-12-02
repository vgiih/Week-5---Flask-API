from Week5 import app
from flask import render_template, request
import pandas as pd
import pickle
from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired

model = pickle.load(open('model.pkl', 'rb'))


class FormPrevisao(FlaskForm):
    tv = FloatField('TV', validators=[DataRequired()])
    radio = FloatField('Radio', validators=[DataRequired()])
    jornal = FloatField('News', validators=[DataRequired()])
    button_submit = SubmitField("Predict")


dictionary = {'TV': 0, 'Radio': 0, 'Jornal': 0}

output = 0


@app.route('/', methods=["GET", "POST"])
def index():
    global output
    form_prev = FormPrevisao()

    if form_prev.validate_on_submit() or "button_submit" in request.form:
        if (type(form_prev.tv.data) == float or type(form_prev.tv.data) == int) \
                and (type(form_prev.radio.data) == float or type(form_prev.radio.data) == int)\
                and (type(form_prev.jornal.data) == float or type(form_prev.jornal.data) == int):
            dictionary['Tv'] = form_prev.tv.data
            dictionary['Radio'] = form_prev.radio.data
            dictionary['Jornal'] = form_prev.jornal.data

            x_values = pd.DataFrame(dictionary, index=[0])

            data = pd.read_csv("vendas.csv")
            columns = list(data.columns)[1:-1]

            x_values = x_values[columns]

            pred = model.predict(x_values)

            output = round(pred[0], 2)
            return render_template('index.html', form_prev=form_prev,
                                   prediction_text='The income should be $ {}'.format(output))
        else:
            return render_template('index.html', form_prev=form_prev, error_text='All fields should be numeric')
    return render_template('index.html', form_prev=form_prev)
