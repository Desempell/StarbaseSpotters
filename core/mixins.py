from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author_id == self.request.user.id
