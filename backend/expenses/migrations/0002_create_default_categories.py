from django.db import migrations


def create_default_categories(apps, schema_editor):
    Category = apps.get_model('expenses', 'Category')

    default_categories = [
        "Groceries",
        "Transport",
        "Entertainment",
        "Utilities",
        "Health",
        "Clothing",
        "Education",
        "Cafe & Restaurants",
        "Travel",
        "Savings",
    ]

    for name in default_categories:
        Category.objects.create(name=name, is_default=True, user=None)


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]