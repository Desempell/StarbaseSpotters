import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='название')),
                ('site', models.CharField(choices=[('starbase', 'Starbase, Техас'), ('ksc', 'Космический центр Кеннеди, Флорида')], default='starbase', max_length=20, verbose_name='космодром')),
                ('launch_date', models.DateTimeField(verbose_name='плановое время старта (UTC)')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('status', models.CharField(choices=[('planned', 'Запланирован'), ('completed', 'Состоялся'), ('scrubbed', 'Отменён')], default='planned', max_length=10, verbose_name='статус')),
                ('booster_caught', models.BooleanField(blank=True, null=True, verbose_name='бустер пойман башней')),
                ('ship_splashdown', models.BooleanField(blank=True, null=True, verbose_name='корабль приводнился')),
                ('actual_launch_time', models.DateTimeField(blank=True, null=True, verbose_name='фактическое время старта (UTC)')),
            ],
            options={
                'verbose_name': 'полёт',
                'verbose_name_plural': 'полёты',
                'ordering': ['-launch_date'],
            },
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booster_caught', models.BooleanField(verbose_name='бустер поймают башней?')),
                ('ship_splashdown', models.BooleanField(verbose_name='корабль успешно приводнится?')),
                ('predicted_launch_time', models.DateTimeField(verbose_name='во сколько реально стартуют (UTC)?')),
                ('comment', models.TextField(blank=True, max_length=500, verbose_name='комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменено')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='flights.flight', verbose_name='полёт')),
            ],
            options={
                'verbose_name': 'прогноз',
                'verbose_name_plural': 'прогнозы',
                'ordering': ['-created_at'],
                'constraints': [models.UniqueConstraint(fields=('flight', 'author'), name='one_prediction_per_user_per_flight')],
            },
        ),
    ]
