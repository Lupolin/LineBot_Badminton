from logging import StreamHandler


def get_stream_handler(handler_name: str | None = None) -> StreamHandler:
    console_handler = StreamHandler()
    console_handler.set_name(handler_name if handler_name else __name__)
    return console_handler
