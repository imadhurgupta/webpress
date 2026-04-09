from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from ..models import Plugin, Template, Website
import json

@staff_member_required
def management_portal(request):
    stats = {
        'total_users': User.objects.count(),
        'total_websites': Website.objects.count(),
        'total_plugins': Plugin.objects.count(),
        'total_themes': Template.objects.count(),
        'active_domains': Website.objects.exclude(custom_domain__isnull=True).exclude(custom_domain='').count()
    }
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_websites = Website.objects.order_by('-created_at')[:5]
    
    return render(request, 'core_app/management/portal.html', {
        'stats': stats,
        'recent_users': recent_users,
        'recent_websites': recent_websites
    })

@staff_member_required
def manage_plugins(request):
    if request.method == 'POST':
        # Simple create logic for demonstration
        name = request.POST.get('name')
        if name:
            from django.utils.text import slugify
            
            # Use provided slug or create one from name
            base_slug = slugify(name)
            slug = base_slug
            counter = 1
            while Plugin.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            Plugin.objects.create(
                name=name,
                slug=slug,
                description=request.POST.get('description', ''),
                icon_svg=request.POST.get('icon_svg', ''),
                is_pro=request.POST.get('is_pro') == 'on',
                head_script=request.POST.get('head_script', ''),
                body_script=request.POST.get('body_script', '')
            )
            messages.success(request, "Plugin created successfully.")
            return redirect('manage_plugins')
            
    plugins = Plugin.objects.all().order_by('-created_at')
    return render(request, 'core_app/management/manage_plugins.html', {'plugins': plugins})

@staff_member_required
def manage_themes(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category', 'General')
        description = request.POST.get('description', '')
        thumb = request.POST.get('thumbnail_url', '')
        content_json = request.POST.get('content_json', '[]')
        
        from django.utils.text import slugify
        key = slugify(name)
        
        # In a real scenario, we might save the JSON to a file or database field
        # For this version, we will save to Template model but also we'd need to
        # update the builder to check this.
        
        Template.objects.create(
            name=name,
            key=key,
            category=category,
            description=description,
            thumbnail_url=thumb,
            initial_content=json.loads(content_json)
        )
        
        # Note: In a full implementation, we'd store the blocks JSON in a 
        # separate model linked to Template, or a JSON field in Template.
        # Since Template model doesn't have a content field yet, let's add it.
        
        messages.success(request, f"Theme '{name}' registered successfully.")
        return redirect('manage_themes')
        
    themes = Template.objects.all()
    return render(request, 'core_app/management/manage_themes.html', {'themes': themes})

@staff_member_required
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'core_app/management/manage_users.html', {'users': users})

@staff_member_required
def manage_domains(request):
    websites_with_domains = Website.objects.exclude(custom_domain__isnull=True).exclude(custom_domain='').order_by('-updated_at')
    return render(request, 'core_app/management/manage_domains.html', {'websites': websites_with_domains})
