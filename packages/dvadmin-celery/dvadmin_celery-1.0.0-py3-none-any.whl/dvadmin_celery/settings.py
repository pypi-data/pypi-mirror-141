from django.conf import settings
if not hasattr(settings,'CACHES'):
    settings.CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f'{settings.REDIS_URL}/1',
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }

# 注册app
apps = ['django_celery_beat', 'django_celery_results', 'plugins.dvadmin_celery_backend']

# 租户celery
if getattr(settings, 'PLUGINS_LIST', {}).get('dvadmin_tenant_backend', None):
    apps.append('tenant_schemas_celery')
    settings.CACHES['default']['KEY_FUNCTION'] = 'django_tenants.cache.make_key'
    settings.CACHES['default']['REVERSE_KEY_FUNCTION'] = 'django_tenants.cache.reverse_key'

for app in apps:
    if app not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += [app]

SHARED_APPS = getattr(settings, 'SHARED_APPS', [])
SHARED_APPS += apps

if not hasattr(settings, 'REDIS_URL'):
    raise Exception("请配置redis地址，否则celery无法使用！")

# celery 配置
if not hasattr(settings,'BROKER_URL'):
    BROKER_URL = f'{settings.REDIS_URL}/2'
CELERY_TIMEZONE = 'Asia/Shanghai'  # celery 时区问题
DJANGO_CELERY_BEAT_TZ_AWARE = False
if not hasattr(settings,'CELERY_RESULT_BACKEND'):
    CELERY_RESULT_BACKEND = 'django-db'
    CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'  # Backend数据库