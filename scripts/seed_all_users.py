import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from core_app.models import Website, Page, Plugin, InstalledPlugin

def seed_for_all_users():
    users = User.objects.all()
    print(f"Feeding {len(users)} users with the sample site...")
    
    for user in users:
        site_name = "Futura Digital Studio"
        site_slug = slugify(site_name)
        
        # Uniquify slug per user
        final_slug = site_slug
        
        # Create Website
        site, created = Website.objects.get_or_create(
            user=user,
            slug=final_slug,
            defaults={
                "name": site_name,
                "description": "A premium digital presence for modern creators.",
                "primary_color": "#6366f1",
                "accent_color": "#22d3ee",
                "global_font": "Plus Jakarta Sans"
            }
        )
        
        if created:
            print(f"Created for: {user.username}")
        else:
            print(f"Refreshed for: {user.username}")

        # Define Blocks (Same as before)
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
                { "name": "Solo", "price": "$0", "features": ["1 Project", "Basic Plugins"] },
                { "name": "Agency", "price": "$199", "features": ["White Label", "Priority Support", "Dedicated IP"] }
            ]},
            { "id": "tm1", "type": "testimonials", "bg": "#ffffff", "color": "#1e293b", "padding": "100px 20px", "title": "Trusted by Leaders", "items": [
                { "name": "Sarah Jenkins", "avatar": "👩", "text": "WebPress is the only tool that actually feels like a workspace, not just a builder." },
                { "name": "David Koh", "avatar": "👨", "text": "The SEO optimization plugins saved us hundreds of hours of manual work." }
            ]},
            { "id": "ct1", "type": "contact", "bg": "#f8fafc", "color": "#1e293b", "padding": "100px 20px", "title": "Start Your Project", "subtitle": "Our team responds in less than 24 hours. Let's build together." },
            { "id": "fr1", "type": "footer", "bg": "#0f172a", "color": "#ffffff", "padding": "60px 20px", "brand": "FUTURA", "text": "Evolving the web through high-fidelity engineering.", "copyright": "© 2026 Futura Studio. All rights reserved." }
        ]

        # Create/Update Home Page
        Page.objects.update_or_create(
            website=site,
            slug="home",
            defaults={
                "title": "Home",
                "is_home": True,
                "content": blocks,
                "seo_title": "Futura Studio — Premium Design & Scale",
                "seo_description": "Build your next big thing with Futura's high-fidelity website builder.",
                "og_title": "Futura — Scale Faster",
                "og_description": "Check out the Futura Studio website I built with WebPress!",
                "og_image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2426&auto=format&fit=crop"
            }
        )

        # Activate Plugins
        demo_plugin_slugs = ['dark-mode-toggle', 'live-chat-support', 'gdpr-cookie-consent', 'seo-optimizer']
        for p_slug in demo_plugin_slugs:
            plugin = Plugin.objects.filter(slug=p_slug).first()
            if plugin:
                InstalledPlugin.objects.get_or_create(website=site, plugin=plugin, defaults={"is_active": True})

    print("Sample site seeded successfully for ALL users!")

if __name__ == "__main__":
    seed_for_all_users()
