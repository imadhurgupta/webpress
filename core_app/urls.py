from django.urls import path
from .views import platform, builder, management
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ─── Platform / Auth ───────────────────────────────────────────────────────
    path('', platform.overview, name='overview'),
    path('login/', platform.login_view, name='login'),
    path('logout/', platform.logout_view, name='logout'),
    path('signup/', platform.signup_view, name='signup'),
    path('verify-otp/', platform.verify_otp_view, name='verify_otp'),
    path('dashboard/', platform.dashboard, name='dashboard'),
    path('profile/', platform.profile_view, name='profile'),
    path('profile/change-password/', platform.change_password_view, name='change_password'),
    path('password-reset/', platform.CustomPasswordResetView.as_view(), name='password_reset'),
    
    # ─── Site Builder & Management ─────────────────────────────────────────────
    path('my-websites/', builder.my_websites, name='my_websites'),
    path('my-websites/create/', builder.create_website, name='create_website'),
    path('my-websites/<int:site_id>/delete/', builder.delete_website, name='delete_website'),
    path('builder/<int:site_id>/page/<int:page_id>/', builder.builder, name='builder'),
    path('builder/<int:site_id>/page/<int:page_id>/save/', builder.save_page, name='save_page'),
    path('builder/upload-image/', builder.upload_image, name='upload_image'),
    path('builder/<int:site_id>/toggle-plugin/', builder.toggle_plugin_builder, name='toggle_plugin_builder'),
    path('builder/<int:site_id>/save-plugin-settings/', builder.save_plugin_settings, name='save_plugin_settings'),
    path('builder/<int:site_id>/save-settings/', builder.save_site_settings, name='save_site_settings'),
    path('builder/<int:site_id>/page/<int:page_id>/preview/', builder.preview_site, name='preview_site'),
    path('builder/<int:site_id>/preview/<str:page_slug>/', builder.preview_site_by_slug, name='preview_site_by_slug'),
    path('builder/<int:site_id>/publish/', builder.toggle_publish_site, name='toggle_publish_site'),
    path('builder/<int:site_id>/page/create/', builder.create_page, name='builder_create_page'),
    path('builder/<int:site_id>/page/<int:page_id>/delete/', builder.delete_page, name='builder_delete_page'),
    path('builder/<int:site_id>/page/<int:page_id>/set-home/', builder.set_home_page, name='builder_set_home_page'),
    
    # ─── Administrative & Leads ────────────────────────────────────────────────
    path('dashboard/plugins/', builder.plugins, name='plugins'),
    path('dashboard/plugins/<int:plugin_id>/install/', builder.install_plugin, name='install_plugin'),
    path('dashboard/plugins/<int:installed_plugin_id>/toggle/', builder.toggle_plugin, name='toggle_plugin'),
    path('dashboard/admin/', management.management_portal, name='management_portal'),
    path('dashboard/admin/plugins/', management.manage_plugins, name='manage_plugins'),
    path('dashboard/admin/themes/', management.manage_themes, name='manage_themes'),
    path('dashboard/admin/users/', management.manage_users, name='manage_users'),
    path('dashboard/admin/domains/', management.manage_domains, name='manage_domains'),
    path('dashboard/leads/', builder.leads_dashboard, name='leads_dashboard'),
    path('api/submit-form/<int:site_id>/', builder.submit_form, name='submit_form'),
    
    # ─── Deployment & Public Serving ───────────────────────────────────────────
    path('builder/<int:site_id>/export-docker/', builder.export_site_docker, name='export_site_docker'),
    path('sites/<slug:user_slug>/<slug:site_slug>/', builder.serve_public_page, name='serve_public_site'),
    path('sites/<slug:user_slug>/<slug:site_slug>/<slug:page_slug>/', builder.serve_public_page, name='serve_public_page'),

    # ─── Auth View Completions ────────────────────────────────────────────────
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core_app/platform/auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core_app/platform/auth/password_reset_confirm.html',
        success_url='/password-reset-complete/'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core_app/platform/auth/password_reset_complete.html'
    ), name='password_reset_complete'),
]
