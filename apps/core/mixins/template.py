class TemplateListMixin:
    template_name: str | None = None
    partial_template_name: str | None = None

    def get_template_name(self, model_name: str, app_label: str):
        if getattr(self, "template_name", None) and isinstance(self.template_name, str):
            return self.template_name

        return f"apps/{app_label}/{model_name}/list.html"

    def get_partial_template_name(self, model_name: str, app_label: str) -> str:
        if getattr(self, "partial_template_name", None) and isinstance(self.partial_template_name, str):
            return self.partial_template_name

        return f"cotton/{app_label}/{model_name}/partial_list.html"
