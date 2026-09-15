from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Order


class OrderModelTests(TestCase):
    def test_order_belongs_to_user_and_defaults_to_shipped(self):
        user = get_user_model().objects.create_user(
            username="order-owner", password="A-safe-passphrase-923!"
        )

        order = Order.objects.create(
            user=user,
            sample_name="肠道样本 A01",
            sample_type="粪便",
            project_type=Order.ProjectType.AMPLICON,
        )

        self.assertEqual(order.user, user)
        self.assertEqual(order.status, Order.Status.SHIPPED)
        self.assertEqual(order.get_project_type_display(), "扩增子")
        self.assertEqual(order.get_status_display(), "已寄送")


class OrderSubmissionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="order-user", password="A-safe-passphrase-923!"
        )

    def test_order_page_requires_login(self):
        response = self.client.get(reverse("order-create"))

        self.assertRedirects(response, f"{reverse('login')}?next=/")

    def test_logged_in_user_sees_order_form_and_login_status(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("order-create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "提交新订单")
        self.assertContains(response, self.user.username)
        self.assertContains(response, reverse("order-history"))

    def test_project_type_prompt_is_localized(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("order-create"))

        self.assertContains(response, "请选择项目类型")
        self.assertNotContains(response, "- Select an option -")

    def test_valid_submission_creates_order_for_current_user(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("order-create"),
            {
                "sample_name": "肿瘤样本 T01",
                "sample_type": "组织",
                "project_type": Order.ProjectType.TRANSCRIPTOME,
                "status": Order.Status.COMPLETED,
                "user": get_user_model().objects.create_user(
                    username="other-user", password="A-safe-passphrase-923!"
                ).pk,
            },
        )

        self.assertRedirects(response, reverse("order-history"))
        order = Order.objects.get()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, Order.Status.SHIPPED)
        self.assertEqual(order.project_type, Order.ProjectType.TRANSCRIPTOME)

    def test_invalid_submission_does_not_create_order(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("order-create"),
            {"sample_name": "", "sample_type": "血液", "project_type": "invalid"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "请填写样本名称")
        self.assertFalse(Order.objects.exists())


class OrderHistoryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="history-user", password="A-safe-passphrase-923!"
        )
        self.other_user = get_user_model().objects.create_user(
            username="other-history-user", password="A-safe-passphrase-923!"
        )

    def test_history_requires_login(self):
        response = self.client.get(reverse("order-history"))

        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('order-history')}"
        )

    def test_history_only_shows_current_users_orders_newest_first(self):
        older = Order.objects.create(
            user=self.user,
            sample_name="我的旧样本",
            sample_type="血液",
            project_type=Order.ProjectType.AMPLICON,
        )
        newer = Order.objects.create(
            user=self.user,
            sample_name="我的新样本",
            sample_type="组织",
            project_type=Order.ProjectType.TRANSCRIPTOME,
            status=Order.Status.RECEIVED,
        )
        Order.objects.create(
            user=self.other_user,
            sample_name="其他用户样本",
            sample_type="唾液",
            project_type=Order.ProjectType.AMPLICON,
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("order-history"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["orders"], [newer, older])
        self.assertContains(response, "我的新样本")
        self.assertContains(response, "已接收")
        self.assertNotContains(response, "其他用户样本")

    def test_history_has_an_actionable_empty_state(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("order-history"))

        self.assertContains(response, "暂无历史订单")
        self.assertContains(response, reverse("order-create"))

    def test_history_is_paginated(self):
        Order.objects.bulk_create(
            [
                Order(
                    user=self.user,
                    sample_name=f"样本 {index:02d}",
                    sample_type="血液",
                    project_type=Order.ProjectType.AMPLICON,
                )
                for index in range(21)
            ]
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("order-history"))

        self.assertEqual(len(response.context["orders"]), 20)
        self.assertTrue(response.context["is_paginated"])
