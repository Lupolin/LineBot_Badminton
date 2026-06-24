import socket

from opentelemetry.sdk.resources import HOST_NAME, SERVICE_INSTANCE_ID, SERVICE_NAME, Resource


def create_resource(service_name: str) -> Resource:
    return Resource.create(
        {
            SERVICE_NAME: service_name,
            SERVICE_INSTANCE_ID: socket.gethostname(),
            HOST_NAME: socket.gethostname(),
        }
    )
