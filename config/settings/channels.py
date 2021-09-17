from .env_reader import env

ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": env.list(
                "DJANGO_CHANNEL_HOSTS",
                default=[
                    ("127.0.0.1", 6379),  # default localhost @ 6379
                ],
            ),
        },
    },
}
