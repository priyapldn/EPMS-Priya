from flask import flash, redirect, render_template, Blueprint, url_for
from flask_login import login_required, current_user
from app.database import get_session
from app.forms import CreateReviewForm
from app.models import Review

main = Blueprint('main', __name__)

@main.route("/home")
@login_required
def home():
    session = get_session()

    employee_reviews = session.query(Review).filter_by(employee_number=current_user.employee_number).all()

    return render_template('home.html', reviews=employee_reviews)

@main.route("/create-review", methods=["GET", "POST"])
def create_review():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    session = get_session()
    form = CreateReviewForm()

    if form.validate_on_submit():

        review_date = form.review_date.data
        reviewer_id = form.reviewer_id.data
        overall_performance_rating = form.overall_performance_rating.data
        goals = form.goals.data
        reviewer_comments = form.reviewer_comments.data
        
        review = Review(
            employee_number = current_user.employee_number,
            review_date = review_date,
            reviewer_id = reviewer_id,
            overall_performance_rating = overall_performance_rating,
            goals = goals,
            reviewer_comments = reviewer_comments
        )
        
        session.add(review)
        try:
            session.commit()
            flash('Your review has been successfully added.', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            session.rollback()
            flash(f'An error occurred while creating your account: {str(e)}', 'danger')
            return redirect(url_for('main.create_review'))

    return render_template('create_review.html', form=form)

@main.route('/delete-review/<review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    session = get_session()
    # Ensure that only the owner of the review or an admin can delete it
    review = session.query(Review).get(review_id)
    
    if review.employee_number != current_user.employee_number and not current_user.is_admin:
        flash('You do not have permission to delete this review.', 'danger')
        return redirect(url_for('main.home'))

    session.delete(review)
    try:
        session.commit()
        flash('Review deleted successfully.', 'success')
    except Exception as e:
        session.rollback()
        flash(f'An error occurred while deleting the review: {str(e)}', 'danger')
    
    return redirect(url_for('main.home'))