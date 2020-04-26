from django.core import mail
from django.contrib.auth.models import User
from logs.tests.testing_lib import RegularTest


class SignUpTests(RegularTest):

    def _load_page(self):
        """
        Check that user can go to the page and see the form
        return the response and form for further testing
        """
        response = self.assert_page_loading("/sign_up")
        form = response.forms["sign-up-form"]
        return response, form


    def _fill_form_with_correct_information(self, form):
        form['username'] = "dinosaur"
        form['email'] = "mrbladers@yandex.ru"
        form['password'] = "1Why?Q)duck?"
        form['g-recaptcha-response'] = 'PASSED'
        return form

    def test_sign_up_page(self):
        response, form = self._load_page()
        self.assertContains(response, "Sign up")
        self.assertNotContains(response, "Welcome, check your e-mail")

    def test_sign_up_required_fields(self):
        response, form = self._load_page()

        response = form.submit()

        self.assertContains(response, 'Please enter your name')
        self.assertContains(response, 'Please enter your e-mail')
        self.assertContains(response, 'Please enter your password')

    def test_sign_up_ok_new_user_created(self):
        response, form = self._load_page()

        form = self._fill_form_with_correct_information(form)
        form.submit().follow()

        self.assertEquals(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEquals(user.email, "mrbladers@yandex.ru")

    def test_sign_up_ok_email_sent(self):
        # from constance import config
        # config.CONTACT_FROM_EMAIL = 'Anton Vinokurov <anton.vinokurov.w@gmail.com>'

        response, form = self._load_page()

        form = self._fill_form_with_correct_information(form)
        response = form.submit().follow()

        self.assertEquals(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEquals(email.from_email, "mrbladers@yandex.ru")
        self.assertEquals(email.body, u"Hi Dinosaur!")
        self.assertEquals(email.to, ["Anton Vinokurov <anton.vinokurov.w@gmail.com>"])

        self.assertContains(response, "Welcome to PreciousWeb.")
        
class SignInTests(RegularTest):

    def _load_page(self):
        """
        Check that user can go to the page and see the form
        return the response and form for further testing
        """
        response = self.assert_page_loading("/sign_in")
        form = response.forms["sign-in-form"]
        return response, form


    def _fill_form_with_correct_information(self, form):
        form['email'] = "mrbladers@yandex.ru"
        form['password'] = "1Why?Q)duck?"
        return form

    def test_sign_in_page(self):
        response, form = self._load_page()
        self.assertContains(response, "Sign in")
        self.assertNotContains(response, "Welcome back")

    def test_sign_in_required_fields(self):
        response, form = self._load_page()

        response = form.submit()

        self.assertContains(response, 'Please enter your e-mail')
        self.assertContains(response, 'Please enter your password')

    def test_sign_in_ok_user_authenticated(self):
        response, form = self._load_page()

        form = self._fill_form_with_correct_information(form)
        form.submit().follow()

        # TODO check authenticated
        # self.assertEquals(User.objects.count(), 1)
        # user = User.objects.first()
        # self.assertEquals(user.email, "mrbladers@yandex.ru")