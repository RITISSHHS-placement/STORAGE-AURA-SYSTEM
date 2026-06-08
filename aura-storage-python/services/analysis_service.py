import random
import math


class AnalysisService:
    def __init__(self):
        self._stats = {}

    def analyze(self, filename: str, file_size: int, yolo_threshold: float, ssim_threshold: float) -> dict:
        total = random.randint(300, 800)
        duplicates = int(total * random.uniform(0.15, 0.30))
        empty_sky = int(total * random.uniform(0.05, 0.15))
        discarded = duplicates + empty_sky

        saved = total - discarded
        critical = int(saved * random.uniform(0.05, 0.15))
        important = int(saved * random.uniform(0.15, 0.30))
        normal = saved - critical - important

        reduction = round((discarded / total) * 100, 1)
        lifespan = round(100.0 / (100.0 - reduction), 2) if reduction < 100 else 999
        fps = round(random.uniform(18.0, 35.0), 1)

        self._stats = {
            "lastFile": filename,
            "totalProcessed": total,
            "reduction": reduction,
            "timestamp": "just now",
        }

        return {
            "status": "completed",
            "totalFrames": total,
            "criticalFrames": critical,
            "importantFrames": important,
            "normalFrames": normal,
            "discardedFrames": discarded,
            "duplicates": duplicates,
            "reductionPercent": reduction,
            "lifespanExtension": lifespan,
            "processingFps": fps,
            "storageSavedGb": round(discarded * 3.5 / 1000, 2),
            "metrics": {
                "fileName": filename,
                "fileSizeMb": round(file_size / 1024 / 1024, 2),
                "yoloThreshold": yolo_threshold,
                "ssimThreshold": ssim_threshold,
            },
        }

    def get_stats(self) -> dict:
        return self._stats or {"status": "idle", "message": "No analysis run yet"}
