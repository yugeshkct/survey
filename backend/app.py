# from flask import Flask
# from flask_cors import CORS
# from config import Config
# from db import Base, engine
# from routes.survey_routes import survey_bp

# def create_app():
#     app = Flask(__name__)
#     CORS(app, origins=[Config.FRONTEND_URL, "http://localhost:3000"])

#     Base.metadata.create_all(bind=engine)

#     app.register_blueprint(survey_bp, url_prefix="/api")
#     return app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, jsonify
from flask_cors import CORS
from db import Base, engine
from routes.survey_routes import survey_bp

def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=False
    )

    Base.metadata.create_all(bind=engine)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"message": "Backend is running"}), 200

    app.register_blueprint(survey_bp, url_prefix="/api")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)