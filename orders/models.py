from django.conf import settings
from django.db import models


class Order(models.Model):
    class ProjectType(models.TextChoices):
        AMPLICON = "amplicon", "扩增子"
        TRANSCRIPTOME = "transcriptome", "转录组"

    class Status(models.TextChoices):
        SHIPPED = "shipped", "已寄送"
        RECEIVED = "received", "已接收"
        EXPERIMENT_STARTED = "experiment_started", "开始实验"
        COMPLETED = "completed", "已完成"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    sample_name = models.CharField("样本名称", max_length=120)
    sample_type = models.CharField("样本类型", max_length=80)
    project_type = models.CharField(
        "项目类型", max_length=20, choices=ProjectType.choices
    )
    status = models.CharField(
        "订单状态", max_length=24, choices=Status.choices, default=Status.SHIPPED
    )
    created_at = models.DateTimeField("提交时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        ordering = ("-created_at", "-pk")
        indexes = [models.Index(fields=("user", "-created_at"))]

    def __str__(self):
        return f"{self.sample_name} · {self.get_project_type_display()}"
