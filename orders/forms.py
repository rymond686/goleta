from django import forms

from .models import Order


class OrderSubmissionForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("sample_name", "sample_type", "project_type")
        error_messages = {
            "sample_name": {"required": "请填写样本名称"},
            "sample_type": {"required": "请填写样本类型"},
            "project_type": {"required": "请选择项目类型"},
        }
        widgets = {
            "sample_name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control order-control",
                    "placeholder": "例如：肠道样本 A01",
                }
            ),
            "sample_type": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control order-control",
                    "placeholder": "例如：血液、组织、粪便",
                }
            ),
            "project_type": forms.Select(
                attrs={"class": "form-select order-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_type = self.fields["project_type"]
        project_type.choices = [
            ("", "请选择项目类型"),
            *list(project_type.choices)[1:],
        ]
