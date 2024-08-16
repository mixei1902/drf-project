from rest_framework.serializers import ValidationError

forbidden_words = ["ставки", "крипта", "продам", "гараж"]


def validete_forbidden_words(value):
    if value.lower() in forbidden_words:
        raise ValidationError("Использованы запрещённые слова")
