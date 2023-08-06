from django import template
from django.utils.safestring import mark_safe
from django_atomics.components import Row
from django_hookup import core as hookup

register = template.Library()


@register.inclusion_tag(takes_context=True, filename="admin/admin_menu.html")
def render_admin_menu(context, classnames=None):
    request = context["request"]
    menus = [func(request) for func in hookup.get_hooks("REGISTER_ADMIN_MENU")]
    # lambda x: x["order"]
    return {"classnames": classnames, "menus": sorted(menus)}


@register.simple_tag(takes_context=True)
def render_app_sections(context, app_label, classnames=None):
    request = context["request"]
    hookname = "REGISTER_ADMIN_APP_SECTION"
    sections = ""
    for func in hookup.get_hooks(hookname):
        app, component = func(request)
        if app == app_label:
            sections += component

    return mark_safe(sections)


@register.simple_tag(takes_context=True)
def render_header_chips(context, app_label):
    request = context["request"]
    hook_name = "REGISTER_ADMIN_%s_HEADER_CHIPS" % app_label.upper()
    chips = [func(request) for func in hookup.get_hooks(hook_name)]
    component = Row(childs=chips)
    component.render(context={"request": context["request"]})
    return mark_safe(component.render(context={"request": context["request"]}))


@register.simple_tag(takes_context=True)
def get_app_list(context, app_label=None):
    from django.contrib.admin import site

    request = context["request"]
    app_dict = site.get_app_list(request)
    return app_dict
