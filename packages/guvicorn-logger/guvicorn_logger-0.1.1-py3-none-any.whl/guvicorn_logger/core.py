import logging
from copy import copy

import click
from uvicorn.logging import AccessFormatter as _AF
from uvicorn.logging import ColourizedFormatter as _CF
from uvicorn.logging import DefaultFormatter as _DF


class BaseFormatter(_CF):
    def color_default(self, asctime: str, level_no: int) -> str:
        def default(asctime: str) -> str:
            return str(asctime)

        func = self.level_name_colors.get(level_no, default)
        return func(asctime)

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        asctime = recordcopy.asctime
        process = recordcopy.process

        seperator = " " * (8 - len(recordcopy.levelname))
        if self.use_colors:
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            asctime = self.color_default(asctime, recordcopy.levelno)
            _temp = "PID: " + str(process)
            process = self.color_default(_temp, recordcopy.levelno)
            if "color_message" in recordcopy.__dict__:
                recordcopy.msg = recordcopy.__dict__["color_message"]
                recordcopy.__dict__["message"] = recordcopy.getMessage()
        recordcopy.__dict__["levelprefix"] = levelname + ":" + seperator
        recordcopy.asctime = asctime
        recordcopy.__dict__["pid"] = process
        return super().formatMessage(recordcopy)


class AccessFormatter(BaseFormatter, _AF):
    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        ) = recordcopy.args
        status_code = self.get_status_code(int(status_code))
        request_line = "%s %s HTTP/%s" % (method, full_path, http_version)
        if self.use_colors:
            request_line = click.style(request_line, bold=True)
        recordcopy.__dict__.update(
            {
                "client_addr": client_addr,
                "request_line": request_line,
                "status_code": status_code,
            }
        )
        return super().formatMessage(recordcopy)


class DefaultFormatter(BaseFormatter, _DF):
    ...
