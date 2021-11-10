from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.template import engines, TemplateSyntaxError


def validate_string_template(value):
    try:
        tpl = engines['django'].from_string(value)
        tpl.render()
    except TemplateSyntaxError as e:
        raise ValidationError(
            _('%(value)s is not a valid string format'),
            params={'value': e.message},
        )
