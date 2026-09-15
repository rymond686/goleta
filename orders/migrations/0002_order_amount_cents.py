from django.db import migrations, models


def backfill_amounts(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    orders = Order.objects.using(schema_editor.connection.alias)
    for project_type, amount in (("amplicon", 15000), ("transcriptome", 20000)):
        orders.filter(project_type=project_type, amount_cents__isnull=True).update(
            amount_cents=amount
        )


class Migration(migrations.Migration):
    dependencies = [("orders", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="order",
            name="amount_cents",
            field=models.PositiveIntegerField(null=True, verbose_name="订单金额（人民币分）"),
        ),
        migrations.RunPython(backfill_amounts, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="order",
            name="amount_cents",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="留空按项目定价：扩增子 15000 分，转录组 20000 分。",
                verbose_name="订单金额（人民币分）",
            ),
        ),
    ]
