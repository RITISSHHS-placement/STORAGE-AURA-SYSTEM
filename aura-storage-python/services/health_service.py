import random
import math
from datetime import date, timedelta


class HealthService:
    def generate_health_data(self, scenario: str) -> dict:
        failing = scenario == "failing"
        progress = random.uniform(0.5, 1.0) if failing else random.uniform(0.0, 0.2)

        ecc = (1 + progress**3 * 120 + random.uniform(-5, 5)) if failing else random.uniform(1, 5)
        bad_blocks = int(progress * 3) if failing else 0
        latency = (2.5 + progress**2 * 6 + random.uniform(-0.2, 0.2)) if failing else (2.5 + random.uniform(-0.2, 0.2))
        pe_cycles = int(1000 + progress**2 * 800) if failing else random.randint(1000, 1200)
        temperature = (45 + progress * 20 + random.uniform(-2, 2)) if failing else (45 + random.uniform(-3, 3))
        voltage = (0.02 + progress**2 * 0.1) if failing else (0.02 + random.uniform(-0.005, 0.005))

        failure_risk = random.uniform(0.75, 0.95) if failing else random.uniform(0.02, 0.12)
        status = "CRITICAL" if failure_risk > 0.7 else ("WARNING" if failure_risk > 0.3 else "HEALTHY")

        return {
            "scenario": scenario,
            "day": 14,
            "eccRate": round(ecc, 2),
            "badBlockCount": bad_blocks,
            "readLatencyMs": round(latency, 2),
            "peCycles": pe_cycles,
            "temperatureC": round(temperature, 1),
            "voltageVariation": round(voltage, 4),
            "failureRisk": round(failure_risk, 3),
            "healthStatus": status,
            "timeSeries": self._generate_series(scenario, 14),
        }

    def predict_failure(self, scenario: str, days: int) -> dict:
        failing = scenario == "failing"
        predictions = []
        today = date.today()

        for i in range(1, days + 1):
            progress = i / days
            if failing:
                risk = min(0.99, progress**2 * 0.9 + random.uniform(-0.03, 0.03))
            else:
                risk = max(0.01, 0.08 + random.uniform(-0.03, 0.03))
            predictions.append({
                "day": i,
                "date": (today - timedelta(days=days - i)).strftime("%b %d"),
                "risk": round(risk, 3),
            })

        final_risk = predictions[-1]["risk"]
        return {
            "predictions": predictions,
            "finalRisk": final_risk,
            "recommendation": "REPLACE_IMMEDIATELY" if final_risk > 0.7 else "MONITOR",
            "accuracy": 89.3,
        }

    def _generate_series(self, scenario: str, days: int) -> list:
        failing = scenario == "failing"
        series = []
        today = date.today()

        for i in range(days):
            progress = i / days
            series.append({
                "date": (today - timedelta(days=days - i - 1)).strftime("%b %d"),
                "eccRate": round(1 + progress**3 * 120 + random.uniform(-3, 3), 1) if failing else round(random.uniform(1, 5), 1),
                "badBlocks": int(progress * 3) if failing else 0,
                "latency": round(2.5 + progress**2 * 6 + random.uniform(-0.1, 0.1), 2) if failing else round(2.5 + random.uniform(-0.2, 0.2), 2),
                "temperature": round(45 + progress * 20 + random.uniform(-1, 1), 1) if failing else round(45 + random.uniform(-3, 3), 1),
                "voltageVariation": round(0.02 + progress**2 * 0.1, 4) if failing else round(0.02 + random.uniform(-0.003, 0.003), 4),
            })
        return series
