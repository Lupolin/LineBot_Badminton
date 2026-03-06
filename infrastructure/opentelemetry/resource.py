import socket

from opentelemetry.sdk.resources import HOST_NAME, SERVICE_INSTANCE_ID, SERVICE_NAME, Resource

from infrastructure.setting import config

resource: Resource = Resource.create(
    {
        SERVICE_NAME: config.SERVICE_NAME,
        SERVICE_INSTANCE_ID: socket.gethostname(),
        HOST_NAME: socket.gethostname(),
    }
)
