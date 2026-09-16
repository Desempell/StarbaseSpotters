import django.core.validators
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
            name='Spot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='название')),
                ('site', models.CharField(choices=[('starbase', 'Starbase, Техас'), ('ksc', 'Космический центр Кеннеди, Флорида')], default='starbase', max_length=20, verbose_name='космодром')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='широта')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='долгота')),
                ('distance_km', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='до стартового стола, км')),
                ('visibility', models.PositiveSmallIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='обзор (1–5)')),
                ('crowd', models.CharField(choices=[('low', 'Почти никого'), ('medium', 'Умеренно'), ('high', 'Толпа')], default='medium', max_length=10, verbose_name='людей')),
                ('has_parking', models.BooleanField(default=False, verbose_name='есть парковка')),
                ('has_cell_signal', models.BooleanField(default=False, verbose_name='есть мобильная связь')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменено')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spots', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'точка наблюдения',
                'verbose_name_plural': 'точки наблюдения',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='оценка')),
                ('text', models.TextField(max_length=2000, verbose_name='отзыв')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменено')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='spots.spot', verbose_name='точка')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='spot',
            constraint=models.CheckConstraint(condition=models.Q(('visibility__gte', 1), ('visibility__lte', 5)), name='spot_visibility_between_1_and_5'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('spot', 'author'), name='one_review_per_user_per_spot'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(condition=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='review_rating_between_1_and_5'),
        ),
    ]
