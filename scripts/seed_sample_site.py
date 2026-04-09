import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from core_app.models import Website, Page, Plugin, InstalledPlugin

def seed_complete_site():
    # 1. Get a user
    user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    if not user:
        print("No user found. Please create a user first.")
        return

    # 2. Create Website
    site_name = "Futura Digital Studio"
    site_slug = slugify(site_name)
    
    # Delete if exists to refresh
    Website.objects.filter(user=user, slug=site_slug).delete()
    
    site = Website.objects.create(
        user=user,
        name=site_name,
        slug=site_slug,
        description="A premium digital presence for modern creators.",
        primary_color="#6366f1",
        accent_color="#22d3ee",
        global_font="Plus Jakarta Sans"
    )

    # 3. Define Blocks
    blocks = [
        { "id": "nb1", "type": "navbar", "bg": "#ffffff", "color": "#1e293b", "padding": "18px 32px", "brand": "FUTURA", "layout": "classic", "design": "glass", "links": ["Home", "Solutions", "Pricing", "About"] },
        { "id": "hr1", "type": "hero", "bg": "#4f46e5", "color": "#ffffff", "padding": "120px 20px", "align": "center", "title": "Scale Your Vision Faster.", "subtitle": "The first all-in-one platform for rapid prototyping and enterprise scaling on localhost.", "btnText": "Get Started Free" },
        { "id": "ft1", "type": "cards", "bg": "#ffffff", "color": "#1e293b", "padding": "100px 20px", "title": "Engineered for Performance", "items": [
            { "icon": "🚀", "title": "Lightning Fast", "desc": "Zero latency rendering for all your visual assets." },
            { "icon": "🛡️", "title": "Bank-Grade Security", "desc": "End-to-end encryption across all your data nodes." },
            { "icon": "💎", "title": "Premium Design", "desc": "State of the art glassmorphism presets included." }
        ]},
        { "id": "pr1", "type": "pricing", "bg": "#f8fafc", "color": "#1e293b", "padding": "100px 20px", "title": "Transparent Plans", "items": [
            { "name": "Solo", "price": "$0", "features": ["1 Project", "Basic Plugins"] },
            { "name": "Studio", "price": "$49", "features": ["Unlimited Projects", "Custom HTML", "Advanced Analytics"] },
            { "name": "Agency", "price": "$199", "features": ["White Label", "Priority Support", "Dedicated IP"] }
        ]},
        { "id": "tm1", "type": "testimonials", "bg": "#ffffff", "color": "#1e293b", "padding": "100px 20px", "title": "Trusted by Leaders", "items": [
            { "name": "Sarah Jenkins", "avatar": "👩", "text": "WebPress is the only tool that actually feels like a workspace, not just a builder." },
            { "name": "David Koh", "avatar": "👨", "text": "The SEO optimization plugins saved us hundreds of hours of manual work." }
        ]},
        { "id": "ct1", "type": "contact", "bg": "#f8fafc", "color": "#1e293b", "padding": "100px 20px", "title": "Start Your Project", "subtitle": "Our team responds in less than 24 hours. Let's build together." },
        { "id": "fr1", "type": "footer", "bg": "#0f172a", "color": "#ffffff", "padding": "60px 20px", "brand": "FUTURA", "text": "Evolving the web through high-fidelity engineering.", "copyright": "© 2026 Futura Studio. All rights reserved." }
    ]

    # 4. Create Home Page
    page = Page.objects.create(
        website=site,
        title="Home",
        slug="home",
        is_home=True,
        content=blocks,
        seo_title="Futura Studio — Premium Design & Scale",
        seo_description="Build your next big thing with Futura's high-fidelity website builder.",
        og_title="Futura — Scale Faster",
        og_description="Check out the Futura Studio website I built with WebPress!",
        og_image="https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2426&auto=format&fit=crop"
    )

    # 5. Activate Plugins
    demo_plugin_slugs = ['dark-mode-toggle', 'live-chat-support', 'gdpr-cookie-consent', 'seo-optimizer']
    for p_slug in demo_plugin_slugs:
        plugin = Plugin.objects.filter(slug=p_slug).first()
        if plugin:
            InstalledPlugin.objects.get_or_create(website=site, plugin=plugin, defaults={"is_active": True})

    print(f"Sample Website '{site_name}' created successfully for user '{user.username}'!")
    print(f"Plugins activated: {', '.join(demo_plugin_slugs)}")

if __name__ == "__main__":
    seed_complete_site()
