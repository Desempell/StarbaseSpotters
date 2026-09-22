import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at'], 'verbose_name': 'review', 'verbose_name_plural': 'reviews'},
        ),
        migrations.AlterModelOptions(
            name='spot',
            options={'ordering': ['-created_at'], 'verbose_name': 'viewing spot', 'verbose_name_plural': 'viewing spots'},
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating'),
        ),
        migrations.AlterField(
            model_name='review',
            name='spot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='spots.spot', verbose_name='spot'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(max_length=2000, verbose_name='review'),
        ),
        migrations.AlterField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spots', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='crowd',
            field=models.CharField(choices=[('low', 'Almost empty'), ('medium', 'Moderate'), ('high', 'Crowded')], default='medium', max_length=10, verbose_name='crowd'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='distance_km',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='distance to launch pad, km'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='has_cell_signal',
            field=models.BooleanField(default=False, verbose_name='cell signal available'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='has_parking',
            field=models.BooleanField(default=False, verbose_name='parking available'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='longitude'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='site',
            field=models.CharField(choices=[('starbase', 'Starbase, Texas'), ('ksc', 'Kennedy Space Center, Florida')], default='starbase', max_length=20, verbose_name='launch site'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='title',
            field=models.CharField(max_length=120, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='visibility',
            field=models.PositiveSmallIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='visibility (1–5)'),
        ),
    ]
