import logging
import sys
from copy import copy

from py import process
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
    ...


class DefaultFormatter(BaseFormatter, _DF):
    ...
