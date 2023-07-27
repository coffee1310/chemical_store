
class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs

        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context