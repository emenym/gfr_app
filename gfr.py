import os
from flask import Flask, redirect, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import DecimalField, Form, IntegerField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap
import math

app = Flask(__name__)
app.secret_key = 'development key'
Bootstrap(app)


class GfrForm(FlaskForm):
    scr = DecimalField("Serum Creatinine", validators=[DataRequired("Please enter a valid SCR")])
    # age = IntegerField("", validators=[DataRequired(),
    #                                    NumberRange(0, 120)])
    age = IntegerField("Age", validators=[DataRequired("Please enter a valid age"), NumberRange(min=1)])
    sex = SelectField('Sex', coerce=int, choices=[(1, 'Female'), (0, 'Male')])
    black = RadioField('Race', choices=[('0', 'Other '), ('1', 'Black')], default=0)
    submit = SubmitField('Estimate')


@app.route('/gfr', methods=('GET', 'POST'))
def submit():
    form = GfrForm(request.form)
    if form.validate_on_submit():
        if request.method == 'POST':
            scr = float(request.form['scr'])
            age = int(request.form['age'])
            sex = int(request.form['sex'])
            black = int(request.form['black'])
            gfr = calc_gfr(float(scr), age, sex, black)
            return render_template('gfr_result.html',
                                   egfr=gfr)
            # return "egfr : " + str(gfr)
        else:
            scr = request.args.get('scr')
            gfr = calc_gfr(float(scr), 68, True, True)
            return "egfr : " + str(gfr)
        # return redirect('/gfr_result')
    return render_template('gfr.html', form=form)


@app.route("/gfr_result", methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        scr = request.form['scr']
        gfr = calc_gfr(float(scr), 68, True, True)
        return render_template('gfr_result.html',
                               egfr=gfr)
        # return "egfr : " + str(gfr)
        # return redirect(url_for('success', name=user))
    else:
        scr = request.args.get('scr')
        # return redirect(url_for('success', name=user))
        gfr = calc_gfr(float(scr), 68, True, True)
        return "egfr : " + str(gfr)


def calc_gfr(scr, age, female, black):
    gfr = 175 * math.pow(scr, -1.154) * math.pow(age, -0.203)
    if female:
        gfr = gfr * 0.742
    if black:
        gfr = gfr * 1.212
    return round(gfr, 1)
    # GFR (mL/min/1.73 m2) = 175 × (Scr)-1.154 × (Age)-0.203 × (0.742 if female) × (1.212 if African American)


@app.route('/gfr2', methods=('GET', 'POST'))
def submit2():
    form = GfrForm(request.form)
    if form.is_submitted():
        print("submitted")
    if form.validate():
        print("valid")
    if form.validate_on_submit():
        print("1")
        print(form.errors)
        return redirect('/success')
    print("2")
    print(form.errors)
    return render_template('gfr2.html', form=form)

@app.route('/gfr3', methods=('GET', 'POST'))
def submit3():
    form = GfrForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('gfr3.html', form=form)
        else:
            return render_template('success.html')
    elif request.method == 'GET':
        return render_template('gfr3.html', form=form)


# @app.route("/gfr")
# def gfr():
#     return render_template("gfr.html")



if __name__ == "__main__":
    port = os.environ.get('PORT', 80)
    if port == '8080':
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.run(host='0.0.0.0', port=port, debug=True)