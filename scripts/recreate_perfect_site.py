import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from core_app.models import Website, Page, Plugin, InstalledPlugin

def recreate_perfect_site():
    users = User.objects.all()
    print(f"Recreating the Master Sample Site for {len(users)} users...")
    
    for user in users:
        site_name = "Futura Digital Studio"
        site_slug = slugify(site_name)
        
        # Fresh delete/recreate
        Website.objects.filter(user=user, slug=site_slug).delete()
        
        site = Website.objects.create(
            user=user,
            name=site_name,
            slug=site_slug,
            description="Accelerating digital product development for the world's most innovative engineering teams.",
            primary_color="#6366f1",
            accent_color="#22d3ee",
            global_font="Plus Jakarta Sans",
            favicon_url="https://cdn-icons-png.flaticon.com/512/1000/1000947.png"
        )

        # ─── High-Fidelity Blocks ───
        blocks = [
            {
                "id": "nb-lux",
                "type": "navbar",
                "bg": "rgba(255,255,255,0.8)",
                "color": "#0f172a",
                "padding": "20px 40px",
                "brand": "FUTURA",
                "layout": "standard",
                "design": "glass",
                "links": ["Solutions", "Platform", "Community", "Pricing"]
            },
            {
                "id": "hero-lux",
                "type": "hero",
                "bg": "#4f46e5",
                "color": "#ffffff",
                "padding": "160px 40px",
                "align": "left",
                "title": "Engineer the Future of Web. Today.",
                "subtitle": "Futura is the world's first AI-native website builder for high-performance localized development and enterprise scaling.",
                "btnText": "Get Started Free",
                "bgImage": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "id": "feat-lux",
                "type": "cards",
                "bg": "#ffffff",
                "color": "#1e293b",
                "padding": "120px 40px",
                "title": "Built for Serious Engineering",
                "items": [
                    { "icon": "⚛️", "title": "Zero Latency", "desc": "Proprietary rendering engine optimized for 100ms response times globally." },
                    { "icon": "🛠️", "title": "Devtools First", "desc": "Direct access to raw HTML/CSS injection with real-time hot-reloading." },
                    { "icon": "🛰️", "title": "Localhost Native", "desc": "Fully sandboxed environment that syncs directly with Docker workflows." }
                ]
            },
            {
                "id": "pr-lux",
                "type": "pricing",
                "bg": "#f9fafb",
                "color": "#0f172a",
                "padding": "120px 40px",
                "title": "Scale With Confidence",
                "items": [
                    { "name": "Free Tier", "price": "$0", "features": ["1 Localhood Site", "Community Support", "Basic Elements"] },
                    { "name": "Pro Developer", "price": "$29", "features": ["Unlimited Sites", "Plugin Ecosystem", "Custom Domain", "Priority Discord"] },
                    { "name": "Enterprise", "price": "$499+", "features": ["SLA Guarantee", "On-Prem Deployment", "Custom Plugins", "Audit Logs"] }
                ]
            },
            {
                "id": "test-lux",
                "type": "testimonials",
                "bg": "#ffffff",
                "color": "#1e293b",
                "padding": "120px 40px",
                "title": "Voices of the Network",
                "items": [
                    { "name": "Marcus V. — CTO at Nexus", "avatar": "🏽", "text": "Futura completely removed the friction between our design system and production code." },
                    { "name": "Elena R. — Lead Engineer", "avatar": "🏼", "text": "The localized plugin mechanism is a game changer for building complex GDPR-compliant sites." }
                ]
            },
            {
                "id": "ct-lux",
                "type": "contact",
                "bg": "#f9fafb",
                "color": "#0f172a",
                "padding": "120px 40px",
                "title": "Let's Connect",
                "subtitle": "Ready to scale your next digital product? Our engineers are online and ready to chat."
            },
            {
                "id": "ft-lux",
                "type": "footer",
                "bg": "#020617",
                "color": "#cbd5e1",
                "padding": "80px 40px",
                "brand": "FUTURA",
                "text": "Innovating the next generation of web builders for high-performance localized environments.",
                "copyright": "© 2026 Futura Digital Inc. Proudly built on Localhost."
            }
        ]

        # ─── Home Page Creation ───
        Page.objects.create(
            website=site,
            title="Home",
            slug="home",
            is_home=True,
            content=blocks,
            seo_title="Futura Studio — Accelerate Your Digital Product",
            seo_description="Build, test, and deploy enterprise-grade websites instantly on localhost with the Futura engine.",
            og_title="Futura — The Next Gen WebPress",
            og_description="Check out my new high-fidelity website built on Localhost with Futura!",
            og_image="https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop"
        )

        # ─── Core Plugin Stack ───
        demo_plugins = ['dark-mode-toggle', 'live-chat-support', 'gdpr-cookie-consent', 'seo-optimizer', 'caching-pro', 'image-optimizer']
        for p_slug in demo_plugins:
            plugin = Plugin.objects.filter(slug=p_slug).first()
            if plugin:
                InstalledPlugin.objects.get_or_create(website=site, plugin=plugin, defaults={"is_active": True})

    print("Master Sample Site recreated for ALL users with high-fidelity blocks!")

if __name__ == "__main__":
    recreate_perfect_site()
