from flask import Flask, redirect, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap
import os
import math

app = Flask(__name__)
app.secret_key = os.urandom(16)
Bootstrap(app)

DEBUG = os.environ.get("DEBUG", False)


class GfrForm(FlaskForm):
    scr = DecimalField("Serum Creatinine", validators=[DataRequired("Please enter a valid SCR")])
    age = IntegerField("Age", validators=[DataRequired("Please enter a valid age"), NumberRange(min=1)])
    sex = SelectField('Sex', coerce=int, choices=[(1, 'Female'), (0, 'Male')])
    black = RadioField('Race', choices=[('0', 'Other '), ('1', 'Black')], default=0)
    submit = SubmitField('Estimate')


def debug_print(debug_str):
    if DEBUG:
        print(debug_str)


@app.route('/gfr', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))
def gfr():
    debug_print("Enter gfr")
    form = GfrForm(request.form)
    if form.validate_on_submit():
        if request.method == 'POST':
            debug_print("Method = POST")
            scr = float(request.form['scr'])
            age = int(request.form['age'])
            sex = int(request.form['sex'])
            black = int(request.form['black'])
            gfr = calc_gfr(float(scr), age, sex, black)
            debug_print("Rendering POST gfr_result")
            return render_template('gfr_result.html',
                                   egfr=gfr)
        else:
            debug_print("Method = GET")
            scr = request.args.get('scr')
            gfr = calc_gfr(float(scr), 68, True, True)
            debug_print("Rendering GET gfr_result")
            return "egfr : " + str(gfr)
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                debug_print(err + ' ' + errorMessages)
    debug_print("Rendering gfr")
    return render_template('gfr.html', form=form)


@app.route("/gfr_result", methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        scr = request.form['scr']
        gfr = calc_gfr(float(scr), 68, True, True)
        return render_template('gfr_result.html',
                               egfr=gfr)
    else:
        scr = request.args.get('scr')
        gfr = calc_gfr(float(scr), 68, True, True)
        return "egfr : " + str(gfr)


def calc_gfr(scr, age, female, black):
    gfr = 175 * math.pow(scr, -1.154) * math.pow(age, -0.203)
    if female:
        gfr = gfr * 0.742
    if black:
        gfr = gfr * 1.212
    debug_print("GFR Calculated: " + str(gfr))
    return round(gfr, 1)
    # GFR (mL/min/1.73 m2) = 175 × (Scr)-1.154 × (Age)-0.203 × (0.742 if female) × (1.212 if African American)


if __name__ == "__main__":
    port = os.environ.get('PORT', 80)
    if port == '8080':
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.run(host='0.0.0.0', port=port, debug=False)
