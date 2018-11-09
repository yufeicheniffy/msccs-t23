from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class searchForm(FlaskForm):
    PostID= StringField('Tweet PostID', validators=[DataRequired()])
    Category = StringField('Category', validators=[DataRequired()])
    Priority = StringField('Priority', validators=[DataRequired()])
    submit = SubmitField('Submit')