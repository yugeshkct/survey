from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import Survey
from services.survey_service import create_survey
from utils.logger import logger

survey_bp = Blueprint("survey_bp", __name__)

@survey_bp.route("/create-survey", methods=["POST"])
def create_survey_route():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body found"}), 400

    db = SessionLocal()
    try:
        result = create_survey(data, db)
        return jsonify(result), 201
    except Exception as e:
        db.rollback()
        logger.error("Survey creation failed: %s", str(e))
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@survey_bp.route("/surveys", methods=["GET"])
def get_all_surveys():
    db = SessionLocal()
    try:
        surveys = db.query(Survey).all()
        response = []
        for survey in surveys:
            response.append({
                "id": survey.id,
                "survey_name": survey.survey_name,
                "page_name": survey.page_name,
                "survey_monkey_id": survey.survey_monkey_id,
                "survey_link": survey.survey_link,
                "created_at": survey.created_at.isoformat()
            })
        return jsonify(response), 200
    finally:
        db.close()


@survey_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200