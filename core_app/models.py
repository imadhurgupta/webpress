from django.db import models
from django.contrib.auth.models import User
import json


class Website(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='websites')
    name        = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    slug        = models.SlugField(max_length=120)
    published   = models.BooleanField(default=False)
    custom_domain = models.CharField(max_length=255, blank=True, null=True, unique=True, help_text="Custom domain mapping (e.g., example.com)")
    
    # Global Settings / Branding
    logo_url      = models.URLField(blank=True)
    favicon_url   = models.URLField(blank=True)
    primary_color = models.CharField(max_length=10, default='#6366f1')
    accent_color  = models.CharField(max_length=10, default='#22d3ee')
    global_font   = models.CharField(max_length=60, default='Outfit')
    custom_css    = models.TextField(blank=True)
    
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'slug')
        ordering        = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} / {self.name}"


class Page(models.Model):
    TYPE_CHOICES = [
        ('page', 'Static Page'),
        ('post', 'Chronological Post'),
    ]
    
    website    = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='pages')
    title      = models.CharField(max_length=120, default='Home')
    content    = models.JSONField(default=list)   # stores list of block dicts
    is_home    = models.BooleanField(default=False)
    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='page')
    
    # Post Specific Data
    categories      = models.JSONField(default=list, blank=True)
    tags            = models.JSONField(default=list, blank=True)
    featured_image  = models.URLField(blank=True, null=True)
    
    # Page SEO & Social Media
    seo_title        = models.CharField(max_length=150, blank=True)
    seo_description  = models.TextField(blank=True)
    slug             = models.SlugField(max_length=120, default='home')
    favicon          = models.CharField(max_length=255, blank=True)
    keywords         = models.CharField(max_length=255, blank=True)
    canonical_url    = models.URLField(blank=True)
    robots_meta      = models.CharField(max_length=100, default='index, follow')
    
    # Open Graph (Social Sharing)
    og_title        = models.CharField(max_length=150, blank=True)
    og_description  = models.TextField(blank=True)
    og_image        = models.URLField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('website', 'slug')
        ordering        = ['-updated_at']

    def __str__(self):
        return f"[{self.content_type.upper()}] {self.website.name} / {self.title}"

    def get_content(self):
        return self.content if isinstance(self.content, list) else json.loads(self.content)


class Plugin(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon_svg = models.TextField(blank=True, help_text="Paste an SVG for the icon")
    description = models.TextField()
    is_pro = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    # Features or scripts to inject
    head_script = models.TextField(blank=True, help_text="HTML to inject in <head>")
    body_script = models.TextField(blank=True, help_text="HTML to inject near </body>")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class InstalledPlugin(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='installed_plugins')
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    # Store dynamic user configurations (e.g. Google Analytics ID)
    settings = models.JSONField(default=dict, blank=True)
    installed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('website', 'plugin')

    def __str__(self):
        return f"{self.plugin.name} -> {self.website.name}"


class Template(models.Model):
    key = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    initial_content = models.JSONField(default=list)
    category = models.CharField(max_length=60, default='General')
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"


class Lead(models.Model):
    website    = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='leads')
    name       = models.CharField(max_length=120)
    email      = models.EmailField()
    message    = models.TextField()
    source_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Lead from {self.website.name} - {self.email}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website_url = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


# ─── Signals ───────────────────────────────────────────────────
from django.contrib.auth.signals import user_logged_in
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Avoid recursion if this is called during the initial creation
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)


@receiver(user_logged_in)
def send_login_alert(sender, user, request, **kwargs):
    """Sends a security alert email every time a user logs in."""
    try:
        # Check if the user is completely created/saved, just to be safe
        if not user.is_active or not getattr(user, 'email', None):
            return
            
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
        login_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        html_msg = render_to_string('core_app/platform/emails/email_login_alert.html', {
            'name': user.first_name or user.username or 'User',
            'login_time': login_time,
            'user_agent': user_agent
        })
        text_msg = strip_tags(html_msg)
        
        msg = EmailMultiAlternatives(
            'Security Alert: New Login via WebPress',
            text_msg,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        msg.attach_alternative(html_msg, "text/html")
        msg.send(fail_silently=True)
    except Exception:
        pass

@receiver(user_signed_up)
def send_welcome_email_allauth(sender, request, user, **kwargs):
    """Sends a welcome email when a user registers via Google initially."""
    try:
        html_msg = render_to_string('core_app/platform/emails/email_welcome.html', {
            'name': user.first_name or user.username or 'User',
            'login_url': request.build_absolute_uri(reverse('login'))
        })
        text_msg = strip_tags(html_msg)
        msg = EmailMultiAlternatives(
            'Welcome to WebPress! 🚀',
            text_msg,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        msg.attach_alternative(html_msg, "text/html")
        msg.send(fail_silently=True)
    except Exception:
        pass
