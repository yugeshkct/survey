import requests
from config import Config
from models import Survey, Question, Choice
from utils.logger import logger

HEADERS = {
    "Authorization": f"Bearer {Config.SM_TOKEN}",
    "Content-Type": "application/json"
}

def create_survey(data, db):
    survey_name = list(data.keys())[0]
    page_name = list(data[survey_name].keys())[0]
    questions_dict = data[survey_name][page_name]

    logger.info("Creating survey: %s", survey_name)

    survey_response = requests.post(
        f"{Config.BASE_URL}/surveys",
        headers=HEADERS,
        json={"title": survey_name},
        timeout=30
    )
    survey_response.raise_for_status()
    survey_monkey_id = survey_response.json()["id"]

    page_response = requests.post(
        f"{Config.BASE_URL}/surveys/{survey_monkey_id}/pages",
        headers=HEADERS,
        json={"title": page_name},
        timeout=30
    )
    page_response.raise_for_status()
    page_id = page_response.json()["id"]

    survey_record = Survey(
        survey_name=survey_name,
        page_name=page_name,
        survey_monkey_id=survey_monkey_id
    )
    db.add(survey_record)
    db.flush()

    for question_title, question_data in questions_dict.items():
        payload = {
            "family": "single_choice",
            "subtype": "vertical",
            "headings": [{"heading": question_data["Description"]}],
            "answers": {
                "choices": [{"text": answer} for answer in question_data["Answers"]]
            }
        }

        question_response = requests.post(
            f"{Config.BASE_URL}/surveys/{survey_monkey_id}/pages/{page_id}/questions",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        question_response.raise_for_status()

        question_record = Question(
            survey_id=survey_record.id,
            question_title=question_title,
            description=question_data["Description"]
        )
        db.add(question_record)
        db.flush()

        for answer in question_data["Answers"]:
            db.add(
                Choice(
                    question_id=question_record.id,
                    choice_text=answer
                )
            )

    collector_response = requests.post(
        f"{Config.BASE_URL}/surveys/{survey_monkey_id}/collectors",
        headers=HEADERS,
        json={"type": "weblink"},
        timeout=30
    )
    collector_response.raise_for_status()

    survey_url = collector_response.json().get("url")
    survey_record.survey_link = survey_url

    db.commit()

    return {
        "message": "Survey created successfully",
        "survey_link": survey_url,
        "survey_id": survey_record.id
    }