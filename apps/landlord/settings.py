from .models import Setting


def set_setting(key, value, tenant):
    try:
        setting = Setting.objects.get(key=key, tenant=tenant)
        setting.value = value
        setting.save()
    except:
        setting = Setting(key=key, value=value, tenant=tenant)
        setting.save()


def get_setting(key, tenant):
    try:
        setting = Setting.objects.get(key=key, tenant=tenant)
        return setting.value
    except:
        return None
