from robot.libraries.BuiltIn import BuiltIn


class Authentication:

    # TEST CASE, TEST SUITE ou GLOBAL
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @property
    def _s2l(self):
        return BuiltIn().get_library_instance('Selenium2Library')

    def connexion(self, login_input_locator, login_value, password_input_locator, password_value, login_button_locator):
        self._s2l.input_text(login_input_locator, login_value)
        self._s2l.input_text(password_input_locator, password_value)
        self._s2l.click_element(login_button_locator)
    
    def rechercher(self, input_locator, input_value):
        self._s2l.input_text(input_locator, input_value)
