from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

#from nucleo.models.otp_codes import OtpActivationCode, OtpRestartPasswordCode
#from nucleo.tasks.enviar_mail import task_enviar_mail_activacion, task_enviar_mail_desactivacion
from nucleo.utilitarios.genericos import CleanCharField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    first_name = CleanCharField(_('first name'), max_length=200, blank=True)
    last_name = CleanCharField(_('last name'), max_length=200, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('es staff'),
        default=False,
        help_text=_('Indica si el usuario puede entrar al aplicativo para staff y usar el DjangoAdmin.'),
    )

    is_cliente = models.BooleanField(
        _('es cliente'),
        default=False,
        help_text=_('Indica si el usuario puede entrar al aplicativo para clientes.'),
    )
    is_active = models.BooleanField(
        _('esta activo'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_block = models.BooleanField(
        _('esta bloqueado'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    #otp_activation_code = models.ForeignKey(OtpActivationCode, null=True, blank=True)
    #otp_restart_password_code = models.ForeignKey(OtpRestartPasswordCode, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def inciar_activacion(self):
        pass
        #task_enviar_mail_activacion.delay(usuario_id=self.id)

    def iniciar_desactivacion(self):
        pass
        #if self.is_active:
            #self.is_active = False
            #self.save()
            #task_enviar_mail_desactivacion.delay(usuario_id=self.id)

    @transaction.atomic()
    def activar_cuenta(self, password):
        self.is_active = True
        self.set_password(password)
        self.save()
        #elf.otp_activation_code.esta_usado = True
        #self.otp_activation_code.save()

    @transaction.atomic()
    def bloquear_usuario(self):
        self.iniciar_desactivacion()
        self.is_block = True
        self.save()