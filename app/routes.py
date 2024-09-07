from flask import flash, redirect, render_template, Blueprint, request, url_for
from flask_login import login_required, current_user
from app.database import get_session
from app.forms import CreateReviewForm
from app.models import Review

main = Blueprint("main", __name__)


@main.route("/home")
@login_required
def home():
    """Render homepage to present all reviews for a user"""
    session = get_session()

    # Return all reviews for admin
    if current_user.is_admin and "all_reviews" in request.args:
        employee_reviews = session.query(Review).all()
    else:
        # Return employee's reviews for regular user
        employee_reviews = (
            session.query(Review)
            .filter_by(employee_number=current_user.employee_number)
            .all()
        )

    return render_template("home.html", reviews=employee_reviews)


@main.route("/create-review", methods=["GET", "POST"])
def create_review():
    """Create a review and add to the Review table"""
    # Redirect if not authenticated
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    session = get_session()
    form = CreateReviewForm()

    if form.validate_on_submit():
        review = Review(
            employee_number=current_user.employee_number,
            review_date=form.review_date.data,
            reviewer_id=form.reviewer_id.data,
            overall_performance_rating=form.overall_performance_rating.data,
            goals=form.goals.data,
            reviewer_comments=form.reviewer_comments.data,
        )

        session.add(review)
        try:
            session.commit()
            flash("Your review has been successfully added.", "success")
            return redirect(url_for("main.home"))
        except Exception as e:
            session.rollback()
            flash(f"An error occurred while creating the review: {str(e)}", "danger")
            return redirect(url_for("main.create_review"))

    return render_template("create_review.html", form=form)


@main.route("/edit-review/<review_id>", methods=["GET", "POST"])
@login_required
def update_review(review_id):
    """Update review of review_id selected"""
    session = get_session()
    review = session.query(Review).get(review_id)

    # Populate form with data of review selected
    if request.method == "GET":
        form = CreateReviewForm(obj=review)
        return render_template("edit_review.html", form=form, review=review)

    form = CreateReviewForm()

    # Re-submit form including any changes
    if form.validate_on_submit():
        review.review_date = form.review_date.data
        review.reviewer_id = form.reviewer_id.data
        review.overall_performance_rating = form.overall_performance_rating.data
        review.goals = form.goals.data
        review.reviewer_comments = form.reviewer_comments.data

        try:
            session.commit()
            flash("Review updated successfully.", "success")
            return redirect(url_for("main.home"))
        except Exception as e:
            session.rollback()
            flash(f"An error occurred while updating the review: {str(e)}", "danger")

    return render_template("edit_review.html", form=form, review=review)


@main.route("/delete-review/<review_id>", methods=["POST"])
@login_required
def delete_review(review_id):
    """Delete review from Review table"""
    session = get_session()
    review = session.query(Review).get(review_id)

    # Ensure that only the admin can delete it
    if (
        review.employee_number != current_user.employee_number
        and not current_user.is_admin
    ):
        flash("You do not have permission to delete this review.", "danger")
        return redirect(url_for("main.home"))

    session.delete(review)
    try:
        session.commit()
        flash("Review deleted successfully.", "success")
    except Exception as e:
        session.rollback()
        flash(f"An error occurred while deleting the review: {str(e)}", "danger")

    return redirect(url_for("main.home"))
