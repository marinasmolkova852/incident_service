import os
from flask import Flask, jsonify, request
from db import SessionLocal, engine
from models import Base, Incident, StatusEnum


app = Flask(__name__)
Base.metadata.create_all(bind=engine)


@app.route("/incidents", methods=["POST"])
def create_incident():
    data = request.json
    session = SessionLocal()

    try:
        incident = Incident(
            description=data.get("description"),
            source=data.get("source", "unknown")
        )
        session.add(incident)
        session.commit()
        return jsonify({
            "id": incident.id,
            "status": incident.status,
            "message": "Инцидент успешно добавлен"
        }), 201
    finally:
        session.close()


@app.route("/incidents", methods=["GET"])
def get_incidents():
    status_filter = request.args.get("status")
    session = SessionLocal()
    query = session.query(Incident)
    if status_filter:
        query = query.filter(Incident.status == status_filter)
    incidents = query.all()
    session.close()
    return jsonify([
        {
            "id": i.id,
            "description": i.description,
            "status": i.status,
            "source": i.source,
            "created_at": i.created_at.isoformat()
        } for i in incidents
    ])


@app.route("/incidents/<int:incident_id>", methods=["PATCH"])
def update_incident(incident_id):
    data = request.json
    session = SessionLocal()
    incident = session.query(Incident).get(incident_id)
    if not incident:
        session.close()
        return jsonify({"error": "Инцидент не найден"}), 404

    new_status = data.get("status")
    if new_status not in [s.value for s in StatusEnum]:
        session.close()
        return jsonify({"error": "Ошибка! Указан неверный статус"}), 400

    incident.status = new_status
    session.commit()
    session.close()
    return jsonify({"message": "Статус обновлён", "id": incident_id, "new_status": new_status})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

