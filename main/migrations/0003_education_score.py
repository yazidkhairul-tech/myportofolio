from django.db import migrations, models
 
 
class Migration(migrations.Migration):
 
    dependencies = [
        ('main', '0002_education'),
    ]
 
    operations = [
        migrations.AddField(
            model_name='education',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
 
