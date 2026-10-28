
from fastapi.testclient import TestClient
import pandas as pd
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction():
    df = pd.read_csv("StudentPerformanceFactors.csv")
    student = df.drop(columns=["Exam_Score"]).iloc[0].to_dict()

    response = client.post("/predict", json=student)

    assert response.status_code == 200
    assert "predicted_exam_score" in response.json()
    assert isinstance(response.json()["predicted_exam_score"], (int, float))
