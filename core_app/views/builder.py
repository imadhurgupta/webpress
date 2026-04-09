from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from ..models import Website, Page, Plugin, Lead, InstalledPlugin, Template
import json, zipfile, io
from .templates_data import TEMPLATE_CONTENTS

# ─── Website Builder Views ─────────────────────────────────────────────────────

@login_required(login_url='login')
def my_websites(request):
    websites = Website.objects.filter(user=request.user)
    templates = Template.objects.all()
    return render(request, 'core_app/builder/my_websites.html', {
        'websites': websites, 
        'templates': templates,
        'user': request.user
    })

@login_required(login_url='login')
def create_website(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'My New Website').strip()
        template_id = request.POST.get('template', 'blank')
        
        base_slug = slugify(name); slug = base_slug; counter = 1
        while Website.objects.filter(user=request.user, slug=slug).exists():
            slug = f"{base_slug}-{counter}"; counter += 1
            
        site = Website.objects.create(user=request.user, name=name, slug=slug)
        
        # Auto-install Standard Plugins (SEO, Analytics, Dark Mode)
        standard_slugs = ['seo-optimizer', 'analytics-pro', 'dark-mode-toggle', 'gdpr-cookie-consent']
        for s_slug in standard_slugs:
            p_obj = Plugin.objects.filter(slug=s_slug).first()
            if p_obj:
                InstalledPlugin.objects.get_or_create(website=site, plugin=p_obj, is_active=True)
        
        # Auto-install Category Plugins
        cat = request.POST.get('category', '').lower()
        cat_plugins = {
            'ecommerce': ['e-commerce-engine', 'product-image-zoom', 'wishlist-engine'],
            'business': ['appointment-scheduler', 'client-portal'],
            'portfolio': ['instagram-feed-pro', 'behance-integration', 'slider-revolution'],
            'blog': ['reading-time-indicator', 'related-posts-engine', 'comments-manager'],
            'educational': ['lms-academy', 'interactive-quiz-engine', 'student-course-progress'],
            'media': ['breaking-news-ticker', 'trending-articles-sidebar', 'author-bio-box'],
            'directory': ['interactive-map-search', 'advanced-filter-sidebar'],
            'social': ['user-activity-stream', 'private-messaging', 'community-forums']
        }
        if cat in cat_plugins:
            for cp_slug in cat_plugins[cat]:
                p_obj = Plugin.objects.filter(slug=cp_slug).first()
                if p_obj:
                    InstalledPlugin.objects.get_or_create(website=site, plugin=p_obj, is_active=True)
        
        # Check database for custom template first
        db_template = Template.objects.filter(key=template_id).first()
        if db_template:
            initial_content = db_template.initial_content
        else:
            initial_content = TEMPLATE_CONTENTS.get(template_id, [])
        page = Page.objects.create(website=site, title='Home', slug='home', is_home=True, content=initial_content)
        return redirect('builder', site_id=site.id, page_id=page.id)
    return redirect('my_websites')

@login_required(login_url='login')
@require_POST
def delete_website(request, site_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    site.delete(); messages.success(request, f"Website '{site.name}' deleted.")
    return redirect('my_websites')

@login_required(login_url='login')
def builder(request, site_id, page_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    page = get_object_or_404(Page, id=page_id, website=site)
    all_plugins = list(Plugin.objects.all())
    print(f"DEBUG: Builder View - Plugin Count: {len(all_plugins)}")
    installed_plugins = site.installed_plugins.all().select_related('plugin')
    
    # Map installed plugins for easier JS access
    installed_map = {ip.plugin_id: {'active': ip.is_active, 'settings': ip.settings} for ip in installed_plugins}
    
    return render(request, 'core_app/builder/builder.html', {
        'site': site, 
        'page': page, 
        'pages': site.pages.all(), 
        'market_plugins': all_plugins,
        'installed_plugins_json': json.dumps(installed_map),
        'content_json': json.dumps(page.get_content()), 
        'user': request.user
    })

@login_required(login_url='login')
@require_POST
def save_page(request, site_id, page_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    page = get_object_or_404(Page, id=page_id, website=site)
    data = json.loads(request.body)
    if 'content' in data: page.content = data['content']
    if 'seo' in data:
        seo = data['seo']; page.seo_title = seo.get('title', page.seo_title); page.seo_description = seo.get('description', page.seo_description)
    page.save(); return JsonResponse({'status': 'ok'})

@csrf_exempt
@login_required(login_url='login')
@require_POST
def upload_image(request):
    if 'image' not in request.FILES: return JsonResponse({'status': 'error'}, status=400)
    fs = FileSystemStorage(); filename = fs.save(request.FILES['image'].name, request.FILES['image'])
    return JsonResponse({'status': 'ok', 'url': fs.url(filename)})

@login_required(login_url='login')
@require_POST
def toggle_plugin_builder(request, site_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    data = json.loads(request.body); plugin = get_object_or_404(Plugin, id=data.get('plugin_id'))
    inst, created = InstalledPlugin.objects.get_or_create(website=site, plugin=plugin)
    if not created: inst.is_active = not inst.is_active; inst.save()
    
    # Auto-provision if turning ON auth-manager
    if inst.is_active and plugin.slug == 'auth-manager':
        if not Page.objects.filter(website=site, slug='login').exists():
            Page.objects.create(website=site, title='Login', slug='login', content=[{'id': 'tp1', 'type': 'login', 'title': 'Welcome Back'}])
        if not Page.objects.filter(website=site, slug='signup').exists():
            Page.objects.create(website=site, title='Sign Up', slug='signup', content=[{'id': 'tp2', 'type': 'signup', 'title': 'Create an Account'}])
            
    return JsonResponse({'success': True, 'is_active': inst.is_active})

@login_required(login_url='login')
@require_POST
def save_site_settings(request, site_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    data = json.loads(request.body)
    for k in ['name', 'logo_url', 'favicon_url', 'primary_color', 'accent_color', 'global_font', 'custom_css']:
        if k in data: setattr(site, k, data[k])
    site.save(); return JsonResponse({'status': 'ok'})

@login_required(login_url='login')
@require_POST
def save_plugin_settings(request, site_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    data = json.loads(request.body)
    plugin_slug = data.get('slug')
    plugin_settings = data.get('settings', {})
    
    inst = InstalledPlugin.objects.filter(website=site, plugin__slug=plugin_slug).first()
    if not inst:
        return JsonResponse({'status': 'error', 'message': 'Plugin not installed'}, status=400)
    
    inst.settings = plugin_settings
    inst.save()
    return JsonResponse({'status': 'ok'})

@login_required(login_url='login')
@never_cache
def preview_site(request, site_id, page_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    page = get_object_or_404(Page, id=page_id, website=site)
    
    installed_plugins = site.installed_plugins.filter(is_active=True).select_related('plugin')
    installed_map = {ip.plugin.id: {'active': ip.is_active, 'settings': ip.settings} for ip in installed_plugins}
    
    head_scripts = "\n".join(p.plugin.head_script for p in installed_plugins if p.plugin.head_script)
    body_scripts = "\n".join(p.plugin.body_script for p in installed_plugins if p.plugin.body_script)
    
    return render(request, 'core_app/builder/preview.html', {
        'site': site, 
        'page': page, 
        'blocks': page.get_content(), 
        'baseUrl': f"/builder/{site.id}/preview/", 
        'head_scripts': head_scripts, 
        'body_scripts': body_scripts,
        'installed_plugins_json': json.dumps(installed_map)
    })

@login_required(login_url='login')
@never_cache
def preview_site_by_slug(request, site_id, page_slug):
    site = get_object_or_404(Website, id=site_id, user=request.user); page = get_object_or_404(Page, website=site, slug=page_slug)
    return preview_site(request, site_id, page.id)

@login_required(login_url='login')
@require_POST
def toggle_publish_site(request, site_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    site.published = not site.published; site.save()
    return JsonResponse({'status': 'ok', 'published': site.published})

@login_required(login_url='login')
def create_page(request, site_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    title = request.POST.get('title', 'New Page').strip()
    slug = slugify(title)
    
    # Ensure slug uniqueness
    original_slug = slug
    counter = 1
    while Page.objects.filter(website=site, slug=slug).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
        
    page = Page.objects.create(website=site, title=title, slug=slug, content=[])
    return redirect('builder', site_id=site.id, page_id=page.id)

@login_required(login_url='login')
@require_POST
def delete_page(request, site_id, page_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    if site.pages.count() > 1: get_object_or_404(Page, id=page_id, website=site).delete()
    return redirect('builder', site_id=site.id, page_id=site.pages.first().id)

@login_required(login_url='login')
@require_POST
def set_home_page(request, site_id, page_id):
    site = get_object_or_404(Website, id=site_id, user=request.user)
    Page.objects.filter(website=site).update(is_home=False)
    Page.objects.filter(id=page_id).update(is_home=True)
    return redirect('builder', site_id=site.id, page_id=page_id)

# ── Plugins & Administrative ───────────────────────────────────────────────────

@login_required(login_url='login')
def plugins(request):
    installed_plugins = InstalledPlugin.objects.filter(website__user=request.user).select_related('plugin', 'website')
    installed_map = {ip.id: {'active': ip.is_active, 'settings': ip.settings, 'slug': ip.plugin.slug, 'site_id': ip.website.id} for ip in installed_plugins}
    
    return render(request, 'core_app/builder/plugins.html', {
        'plugins': Plugin.objects.all(), 
        'websites': request.user.websites.all(), 
        'installed_plugins': installed_plugins,
        'installed_plugins_json': json.dumps(installed_map)
    })

@login_required(login_url='login')
@require_POST
def install_plugin(request, plugin_id):
    site = get_object_or_404(Website, id=request.POST.get('website_id'), user=request.user)
    plugin = get_object_or_404(Plugin, id=plugin_id)
    inst, created = InstalledPlugin.objects.get_or_create(website=site, plugin=plugin)
    
    # Auto-provision pages for specific plugins
    if plugin.slug == 'auth-manager':
        # Create Login Page if not exists
        if not Page.objects.filter(website=site, slug='login').exists():
            Page.objects.create(
                website=site, 
                title='Login', 
                slug='login', 
                content=[{'id': 'p1', 'type': 'login', 'title': 'Welcome Back', 'layout': 'centered'}]
            )
        # Create Signup Page if not exists
        if not Page.objects.filter(website=site, slug='signup').exists():
            Page.objects.create(
                website=site, 
                title='Sign Up', 
                slug='signup', 
                content=[{'id': 'p2', 'type': 'signup', 'title': 'Create an Account'}]
            )
            
    return redirect('plugins')

@login_required(login_url='login')
@require_POST
def toggle_plugin(request, installed_plugin_id):
    inst = get_object_or_404(InstalledPlugin, id=installed_plugin_id, website__user=request.user)
    inst.is_active = not inst.is_active; inst.save(); return redirect('plugins')

@staff_member_required
def admin_plugins(request):
    return render(request, 'core_app/builder/admin_plugins.html', {'plugins': Plugin.objects.all()})

@staff_member_required
def admin_plugin_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Plugin.objects.create(name=name, slug=slugify(name), description=request.POST.get('description'), icon_svg=request.POST.get('icon_svg'))
        return redirect('admin_plugins')
    return render(request, 'core_app/builder/admin_plugin_create.html')

@login_required(login_url='login')
def leads_dashboard(request):
    return render(request, 'core_app/builder/leads.html', {'leads': Lead.objects.filter(website__user=request.user)})

@csrf_exempt
def submit_form(request, site_id):
    site = get_object_or_404(Website, id=site_id)
    data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    
    Lead.objects.create(
        website=site,
        name=data.get('name', 'Anonymous'),
        email=data.get('email', ''),
        message=data.get('message', ''),
        source_url=data.get('source_url', request.META.get('HTTP_REFERER', ''))
    )
    return JsonResponse({'status': 'ok'})

@login_required(login_url='login')
def export_site_docker(request, site_id):
    site = get_object_or_404(Website, id=site_id, user=request.user); buf = io.BytesIO()
    active_plugins = InstalledPlugin.objects.filter(website=site, is_active=True).select_related('plugin')
    installed_map = {ip.plugin.id: {'active': ip.is_active, 'settings': ip.settings} for ip in active_plugins}
    head_scripts = "\n".join(p.plugin.head_script for p in active_plugins if p.plugin.head_script)
    body_scripts = "\n".join(p.plugin.body_script for p in active_plugins if p.plugin.body_script)
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in site.pages.all():
            z.writestr('index.html' if p.is_home else f"{p.slug}.html", render_to_string('core_app/builder/preview.html', {
                'site': site, 
                'page': p, 
                'blocks': p.get_content(), 
                'is_public': True, 
                'baseUrl': '/', 
                'head_scripts': head_scripts, 
                'body_scripts': body_scripts,
                'installed_plugins_json': json.dumps(installed_map)
            }))
        z.writestr('Dockerfile', "FROM nginx:alpine\nCOPY . /usr/share/nginx/html\n")
    res = HttpResponse(buf.getvalue(), content_type='application/zip'); res['Content-Disposition'] = f'attachment; filename=site.zip'; return res

def serve_public_page(request, user_slug, site_slug, page_slug=None):
    site = get_object_or_404(Website, slug=site_slug, user__username=user_slug)
    page = get_object_or_404(Page, website=site, slug=page_slug) if page_slug else site.pages.filter(is_home=True).first()
    active_plugins = InstalledPlugin.objects.filter(website=site, is_active=True).select_related('plugin')
    installed_map = {ip.plugin.id: {'active': ip.is_active, 'settings': ip.settings} for ip in active_plugins}
    head_scripts = "\n".join(p.plugin.head_script for p in active_plugins if p.plugin.head_script)
    body_scripts = "\n".join(p.plugin.body_script for p in active_plugins if p.plugin.body_script)
    return render(request, 'core_app/builder/preview.html', {
        'site': site, 
        'page': page, 
        'blocks': page.get_content(), 
        'is_public': True, 
        'baseUrl': f"/sites/{user_slug}/{site_slug}/", 
        'head_scripts': head_scripts, 
        'body_scripts': body_scripts,
        'installed_plugins_json': json.dumps(installed_map)
    })
