import uuid

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth import password_validation
# from django.utils.text import slugify


class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
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


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(_('email address'), null=False, unique=True)
    intro = models.TextField(blank=True, null=True)
    profile = models.ImageField(upload_to='profile/', null=True, blank=True)
    header = models.ImageField(upload_to='header/', null=True, blank=True)
    direct_link = models.URLField(max_length=255, null=True, blank=True)
    is_direct = models.BooleanField(default=False)
    username = models.CharField(
        max_length=150,
        unique=False,
        help_text=_('150 characters or fewer.'),
        blank=False, null=False,
    )
    # adminサイトへのアクセス権をユーザーが持っているか判断するメソッド
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether this user can log into this admin site.'),
    )
    # ユーザーがアクティブかどうか判断するメソッド
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active.'
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    # 上からメールドレスフィールド、ユーザー名として使うフィールド、スーパーユーザーを作る際に必ず入力するべきフィールドを指定している。
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # メールの送信に関するメソッド
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        # self.slug = self.slug or slugify(self.username)
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def toggle_direct(self):
        if self.is_direct:
            self.is_direct = False
        else:
            self.is_direct = True
        self.save()

    def set_direct_link(self, link):
        self.direct_link = link.link
        self.save()


class Links(models.Model):
    MEDIA_CHOICES = [
        ('TWT', 'Twitter'),
        ('INS', 'Instagram'),
        ('TIK', 'TikTok'),
        ('FBK', 'Facebook'),
        ('YTB', 'Youtube'),
        ('LNE', 'LINE'),
        ('MIS', 'Other'),
    ]

    account_id = models.CharField(blank=True, max_length=150)

    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE)

    media_choice = models.CharField(
        max_length=3,
        choices=MEDIA_CHOICES,
        default='MIS',
    )

    link = models.URLField(max_length=255)

    order_num = models.PositiveIntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return self.get_media_choice_display()
