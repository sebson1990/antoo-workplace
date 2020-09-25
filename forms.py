from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddReviewForm(FlaskForm):
    review_title = StringField('Review Title', validators=[DataRequired()])
    review_content = StringField('Review Content', validators=[DataRequired()])
