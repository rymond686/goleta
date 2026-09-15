from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class OrderAmountMigrationTests(TransactionTestCase):
    def test_existing_orders_receive_project_prices(self):
        executor = MigrationExecutor(connection)
        latest = executor.loader.graph.leaf_nodes()
        self.addCleanup(lambda: MigrationExecutor(connection).migrate(latest))
        previous = [("orders", "0001_initial")]
        executor.migrate(previous)
        old_apps = executor.loader.project_state(previous).apps
        user = old_apps.get_model("auth", "User").objects.create(username="legacy-owner")
        Order = old_apps.get_model("orders", "Order")
        ids = {}
        for project_type in ("amplicon", "transcriptome"):
            order = Order.objects.create(
                user_id=user.pk, sample_name=project_type, sample_type="组织",
                project_type=project_type, status="received",
            )
            ids[project_type] = order.pk

        executor = MigrationExecutor(connection)
        target = [("orders", "0002_order_amount_cents")]
        executor.migrate(target)
        Order = executor.loader.project_state(target).apps.get_model("orders", "Order")

        self.assertEqual(Order.objects.count(), 2)
        for project_type, amount in (("amplicon", 15000), ("transcriptome", 20000)):
            order = Order.objects.get(pk=ids[project_type])
            self.assertEqual(order.amount_cents, amount)
            self.assertEqual(order.user_id, user.pk)
            self.assertEqual(order.status, "received")
