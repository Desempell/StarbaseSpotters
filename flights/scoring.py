from dataclasses import dataclass

from .models import MAX_SCORE, Prediction


@dataclass
class PredictorStats:
    user: object
    predictions: int = 0
    points: int = 0

    @property
    def accuracy(self):
        if not self.predictions:
            return 0
        return round(100 * self.points / (self.predictions * MAX_SCORE))


def _collect(predictions):
    stats = {}
    for prediction in predictions:
        row = stats.setdefault(prediction.author_id, PredictorStats(user=prediction.author))
        row.predictions += 1
        row.points += prediction.score()
    return stats


def leaderboard(limit=None):
    predictions = Prediction.objects.resolved().select_related("flight", "author")
    rows = sorted(
        _collect(predictions).values(),
        key=lambda row: (-row.points, -row.accuracy, row.user.username),
    )
    return rows[:limit] if limit else rows


def user_stats(user):
    predictions = Prediction.objects.resolved().filter(author=user).select_related("flight", "author")
    return _collect(predictions).get(user.pk, PredictorStats(user=user))
