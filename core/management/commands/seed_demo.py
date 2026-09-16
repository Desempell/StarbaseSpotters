from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.choices import LaunchSite
from flights.models import Flight, Prediction
from spots.models import Review, Spot

DEMO_PASSWORD = "starship-demo-2026"
DEMO_USERS = ["mechazilla_fan", "boca_local", "raptor_counter"]

DEMO_SPOTS = [
    {
        "title": "Пляж Бока-Чика",
        "site": LaunchSite.STARBASE,
        "description": "Ближе всего к стартовому столу. В день запуска дорогу перекрывают, "
        "но во время прожигов и перевозки бустеров отсюда отличный вид.",
        "latitude": Decimal("25.996000"),
        "longitude": Decimal("-97.150000"),
        "distance_km": Decimal("2.5"),
        "visibility": 5,
        "crowd": Spot.Crowd.HIGH,
        "has_parking": False,
        "has_cell_signal": False,
        "author": "boca_local",
    },
    {
        "title": "Isla Blanca Park, Саут-Падре",
        "site": LaunchSite.STARBASE,
        "description": "Классическое место для запусков: башня видна через пролив. "
        "Приезжайте за 4–5 часов, парковка забивается.",
        "latitude": Decimal("26.071000"),
        "longitude": Decimal("-97.157000"),
        "distance_km": Decimal("9.0"),
        "visibility": 5,
        "crowd": Spot.Crowd.HIGH,
        "has_parking": True,
        "has_cell_signal": True,
        "author": "mechazilla_fan",
    },
    {
        "title": "Маяк Порт-Изабел",
        "site": LaunchSite.STARBASE,
        "description": "Дальше, зато спокойно, есть кафе и туалеты. Звук доходит секунд через 40.",
        "latitude": Decimal("26.077000"),
        "longitude": Decimal("-97.207000"),
        "distance_km": Decimal("12.5"),
        "visibility": 3,
        "crowd": Spot.Crowd.MEDIUM,
        "has_parking": True,
        "has_cell_signal": True,
        "author": "raptor_counter",
    },
    {
        "title": "Playalinda Beach",
        "site": LaunchSite.KSC,
        "description": "Пляж рядом с будущими площадками Starship во Флориде. Вход платный.",
        "latitude": Decimal("28.655000"),
        "longitude": Decimal("-80.633000"),
        "distance_km": Decimal("6.0"),
        "visibility": 4,
        "crowd": Spot.Crowd.MEDIUM,
        "has_parking": True,
        "has_cell_signal": False,
        "author": "mechazilla_fan",
    },
    {
        "title": "Space View Park, Титусвилл",
        "site": LaunchSite.KSC,
        "description": "Парк с видом через реку Индиан-Ривер, играет трансляция запуска.",
        "latitude": Decimal("28.614000"),
        "longitude": Decimal("-80.807000"),
        "distance_km": Decimal("20.0"),
        "visibility": 3,
        "crowd": Spot.Crowd.HIGH,
        "has_parking": True,
        "has_cell_signal": True,
        "author": "boca_local",
    },
]

DEMO_REVIEWS = [
    ("Isla Blanca Park, Саут-Падре", "boca_local", 5, "Лучший вид на поимку бустера, слышно всё."),
    ("Isla Blanca Park, Саут-Падре", "raptor_counter", 4, "Круто, но очень много людей и пробки после старта."),
    ("Пляж Бока-Чика", "mechazilla_fan", 4, "Для прожигов идеально, в день старта не пустят."),
    ("Маяк Порт-Изабел", "mechazilla_fan", 3, "Далековато, зато с детьми удобно."),
    ("Playalinda Beach", "raptor_counter", 5, "Тихо и близко, берите воду и репеллент."),
]


class Command(BaseCommand):
    help = "Создаёт демо-пользователей, точки наблюдения, отзывы, полёты и прогнозы."

    @transaction.atomic
    def handle(self, *args, **options):
        users = {username: self._user(username) for username in DEMO_USERS}

        spots = {}
        for data in DEMO_SPOTS:
            data = {**data, "author": users[data["author"]]}
            spot, _ = Spot.objects.get_or_create(title=data.pop("title"), defaults=data)
            spots[spot.title] = spot

        for spot_title, username, rating, text in DEMO_REVIEWS:
            Review.objects.get_or_create(
                spot=spots[spot_title],
                author=users[username],
                defaults={"rating": rating, "text": text},
            )

        now = timezone.now().replace(second=0, microsecond=0)
        flight_1 = self._flight(
            "Демо-полёт 1",
            launch_date=now - timedelta(days=40),
            status=Flight.Status.COMPLETED,
            booster_caught=True,
            ship_splashdown=True,
            actual_launch_time=now - timedelta(days=40) + timedelta(minutes=18),
            description="Бустер пойман башней, корабль приводнился в Индийском океане.",
        )
        flight_2 = self._flight(
            "Демо-полёт 2",
            launch_date=now - timedelta(days=12),
            status=Flight.Status.COMPLETED,
            booster_caught=False,
            ship_splashdown=True,
            actual_launch_time=now - timedelta(days=12) + timedelta(hours=1, minutes=5),
            description="Бустер ушёл на мягкую посадку в залив, старт задержали на час.",
        )
        flight_3 = self._flight(
            "Демо-полёт 3",
            launch_date=now + timedelta(days=9),
            description="Следующий тестовый полёт. Прогнозы открыты!",
        )

        predictions = [
            (flight_1, "mechazilla_fan", True, True, timedelta(minutes=15)),
            (flight_1, "boca_local", True, False, timedelta(0)),
            (flight_1, "raptor_counter", False, True, timedelta(hours=2)),
            (flight_2, "mechazilla_fan", True, True, timedelta(minutes=50)),
            (flight_2, "boca_local", False, True, timedelta(hours=1)),
            (flight_2, "raptor_counter", False, False, timedelta(minutes=10)),
            (flight_3, "boca_local", True, True, timedelta(minutes=30)),
        ]
        for flight, username, booster, ship, shift in predictions:
            Prediction.objects.get_or_create(
                flight=flight,
                author=users[username],
                defaults={
                    "booster_caught": booster,
                    "ship_splashdown": ship,
                    "predicted_launch_time": flight.launch_date + shift,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Демо-данные готовы. Пользователи: {', '.join(DEMO_USERS)}; пароль: {DEMO_PASSWORD}"
            )
        )

    def _user(self, username):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
        return user

    def _flight(self, name, **fields):
        flight, _ = Flight.objects.get_or_create(name=name, defaults=fields)
        return flight
