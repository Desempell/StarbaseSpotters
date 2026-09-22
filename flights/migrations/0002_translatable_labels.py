import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flight',
            options={'ordering': ['-launch_date'], 'verbose_name': 'flight', 'verbose_name_plural': 'flights'},
        ),
        migrations.AlterModelOptions(
            name='prediction',
            options={'ordering': ['-created_at'], 'verbose_name': 'prediction', 'verbose_name_plural': 'predictions'},
        ),
        migrations.AlterField(
            model_name='flight',
            name='actual_launch_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='actual launch time (UTC)'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='booster_caught',
            field=models.BooleanField(blank=True, null=True, verbose_name='booster caught by tower'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='launch_date',
            field=models.DateTimeField(verbose_name='planned launch time (UTC)'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='name',
            field=models.CharField(max_length=80, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='ship_splashdown',
            field=models.BooleanField(blank=True, null=True, verbose_name='ship splashed down'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='site',
            field=models.CharField(choices=[('starbase', 'Starbase, Texas'), ('ksc', 'Kennedy Space Center, Florida')], default='starbase', max_length=20, verbose_name='launch site'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='status',
            field=models.CharField(choices=[('planned', 'Planned'), ('completed', 'Completed'), ('scrubbed', 'Scrubbed')], default='planned', max_length=10, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='booster_caught',
            field=models.BooleanField(verbose_name='will the tower catch the booster?'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='comment',
            field=models.TextField(blank=True, max_length=500, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='flight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='flights.flight', verbose_name='flight'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='predicted_launch_time',
            field=models.DateTimeField(verbose_name='when will it actually launch (UTC)?'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='ship_splashdown',
            field=models.BooleanField(verbose_name='will the ship splash down successfully?'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated'),
        ),
    ]
