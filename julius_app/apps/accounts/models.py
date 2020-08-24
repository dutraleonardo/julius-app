import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_id(self, pk):
        return self.get(pk=pk)


class User(AbstractBaseUser, PermissionsMixin):
    COMPANY = 'company'
    PERSON = 'person'
    ACCOUNT_TYPES = (
        (COMPANY, _('company')),
        (PERSON, _('person'))
    )
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False, null=True)
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    phone_number = models.CharField(_('phone_number'), max_length=100, blank=True, null=True)
    cpf_or_cnpj = models.CharField(_('cpf_or_cnpj'), max_length=14, blank=False, null=True)
    account_type = models.CharField(_('account_type'), max_length=124, choices=ACCOUNT_TYPES, blank=False, null=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        return self.email


class Card(models.Model):
    user = models.OneToOneField('accounts.User', verbose_name=_('user'), related_name='card',
                                on_delete=models.CASCADE)
    points = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('card')
        verbose_name_plural = _('cards')


class Transaction(models.Model):
    ADD = 'add'
    REMOVE = 'remove'
    TRANSACTION_TYPES = (
        (ADD, _('add')),
        (REMOVE, _('remove'))
    )
    user = models.ForeignKey('accounts.User', verbose_name=_('user'), related_name='transactions',
                             on_delete=models.CASCADE)
    card = models.ForeignKey('accounts.Card', verbose_name=_('card'), related_name='transactions',
                             on_delete=models.CASCADE)
    value = models.IntegerField(blank=True, null=True)
    transaction_type = models.CharField(_('transaction_type'), max_length=124, choices=TRANSACTION_TYPES, blank=True,
                                        null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('business_info')
        verbose_name_plural = _('business_infos')


class Product(models.Model):
    user = models.ForeignKey('accounts.User', verbose_name=_('user'), related_name='product',
                             on_delete=models.CASCADE)
    product_name = models.CharField(_('product_name'), max_length=30, blank=True, null=True)
    description = models.CharField(_('description'), max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)


class Campaign(models.Model):
    user = models.ForeignKey('accounts.User', verbose_name=_('user'), related_name='campaign',
                             on_delete=models.CASCADE)
    product = models.ForeignKey('accounts.Product', verbose_name=_('product'), related_name='campaign',
                                on_delete=models.CASCADE)
    campaign_name = models.CharField(_('campaign_name'), max_length=30, blank=True, null=True)
    description = models.CharField(_('description'), max_length=120, blank=True, null=True)
    points_qty = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
