import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core_app.models import Plugin, Template

plugins_data = [
    {
        'slug': 'google-analytics',
        'name': 'Google Analytics',
        'description': 'Track website traffic and user engagement using Google Analytics.',
        'icon_svg': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>',
        'is_pro': False,
        'head_script': '<!-- Google Analytics Script Placeholder -->\n<script>console.log("GA Init");</script>',
        'body_script': '',
    },
    {
        'slug': 'live-chat',
        'name': 'AI Live Chat',
        'description': 'Add an AI powered live chat widget to converse with your visitors 24/7.',
        'icon_svg': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
        'is_pro': True,
        'price': '9.99',
        'head_script': '',
        'body_script': '<div id="live-chat-btn" style="position:fixed;bottom:20px;right:20px;background:#6366f1;color:#fff;padding:15px;border-radius:50%;box-shadow:0 4px 10px rgba(0,0,0,0.2);cursor:pointer;z-index:9999;"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></div><script>document.getElementById("live-chat-btn").onclick=()=>alert("Live chat feature coming soon!");</script>',
    },
    {
        'slug': 'fb-pixel',
        'name': 'Facebook Pixel',
        'description': 'Integrate Facebook Pixel to track ad conversions and optimize your ads.',
        'icon_svg': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>',
        'is_pro': False,
        'head_script': '<!-- Facebook Pixel Placeholder -->\n<script>console.log("FB Pixel Init");</script>',
        'body_script': '',
    },
    {
        'slug': 'seo-optimizer',
        'name': 'SEO Optimizer Pro',
        'description': 'Automatically generate meta tags and structure data to boost your search rankings.',
        'icon_svg': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
        'is_pro': True,
        'price': '4.99',
        'head_script': '<meta name="generator" content="Octopyder Builder">',
        'body_script': '',
    }
]

for p in plugins_data:
    price = p.pop('price', 0.00)
    Plugin.objects.update_or_create(
        slug=p['slug'],
        defaults={
            'name': p['name'],
            'description': p['description'],
            'icon_svg': p['icon_svg'],
            'is_pro': p.get('is_pro', False),
            'price': price,
            'head_script': p.get('head_script', ''),
            'body_script': p.get('body_script', ''),
        }
    )

print("Plugins seeded.")

templates_data = [
    {
        'key': 'portfolio-modern',
        'name': 'Modern Portfolio',
        'description': 'A sleek, dark-themed portfolio suitable for designers and developers.',
        'category': 'Portfolio',
        'thumbnail_url': 'https://images.unsplash.com/photo-1547658719-da2b51169166?auto=format&fit=crop&q=80&w=400',
        'is_premium': False,
    },
    {
        'key': 'saas-landing',
        'name': 'SaaS Startup',
        'description': 'High-converting landing page optimized for SaaS products.',
        'category': 'Landing Page',
        'thumbnail_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=400',
        'is_premium': True,
    },
    {
        'key': 'ecommerce-store',
        'name': 'Boutique Store',
        'description': 'Beautiful grid-based layout for selling physical and digital goods.',
        'category': 'E-Commerce',
        'thumbnail_url': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&q=80&w=400',
        'is_premium': True,
    },
    {
        'key': 'agency-creative',
        'name': 'Creative Agency',
        'description': 'Bold and colorful layout perfect for creative agencies.',
        'category': 'Business',
        'thumbnail_url': 'https://images.unsplash.com/photo-1497215848143-bc000216694e?auto=format&fit=crop&q=80&w=400',
        'is_premium': False,
    },
    {
        'key': 'personal-blog',
        'name': 'Minimalist Blog',
        'description': 'Focus on reading experience with this distraction-free template.',
        'category': 'Blog',
        'thumbnail_url': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&q=80&w=400',
        'is_premium': False,
    }
]

for t in templates_data:
    Template.objects.update_or_create(
        key=t['key'],
        defaults={
            'name': t['name'],
            'description': t['description'],
            'category': t['category'],
            'thumbnail_url': t.get('thumbnail_url', ''),
            'is_premium': t.get('is_premium', False),
        }
    )

print("Templates seeded.")
