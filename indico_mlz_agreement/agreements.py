from sqlalchemy.orm import joinedload

from indico.modules.events.agreements.base import AgreementDefinitionBase, AgreementPersonInfo
from indico.modules.events.registration.models.forms import RegistrationForm

from indico_mlz_extension import _


class MLZPersonInfo(AgreementPersonInfo):
    @property
    def identifier(self):
        prefix = '{}-{}'.format(self.email.lower() if self.email else 'NOEMAIL', self.data['type'])
        return '{}:{}'.format(prefix, self.data['person_id'])

class MLZPhotReleaseAgreement(AgreementDefinitionBase):
    name = 'mlz-photo-release'
    title = _('MLZ Photo Release')
    description = _('For photos to be all participants should agree.')
    form_template_name = 'agreement_form.html'
    disabled_reason = _('There are no agreements to sign. This means that either no recording request has been '
                        'done/accepted or there are no speakers assigned to the contributions in question.')

    @classmethod
    def can_access_api(cls, user, event):
        return super(MLZPhotReleaseAgreement, cls).can_access_api(user, event)

    @classmethod
    def is_active(cls, event):
        return True

    @classmethod
    def iter_people(cls, event):
        query = (RegistrationForm.query.with_parent(event)
                 .options(joinedload('registrations').joinedload('data').joinedload('field_data')))
        for regform in query:
            for registration in regform.active_registrations:

                yield MLZPersonInfo(registration.full_name, registration.email or None,
                                    data={'type':'registrant', 'person_id': str(registration.id)})
