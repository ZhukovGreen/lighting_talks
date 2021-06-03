import logging
import sys
import warnings
from concurrent import futures
from contextlib import contextmanager
from logging import handlers
from multiprocessing import Process, Queue

import pytest

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


logger = logging.getLogger(__name__)


class ActorContext:
    def __init__(self):
        self.log = logger

    def run(self):
        warnings.warn("some warning", DeprecationWarning)
        self.log.debug("Some msg")


@pytest.fixture()
def caplog_workaround():
    @contextmanager
    def ctx():
        logger_queue = Queue()
        logger = logging.getLogger()
        logger.addHandler(handlers.QueueHandler(logger_queue))
        yield
        while not logger_queue.empty():
            log_record: logging.LogRecord = logger_queue.get()
            logger._log(
                level=log_record.levelno,
                msg=log_record.message,
                args=log_record.args,
                exc_info=log_record.exc_info,
            )

    return ctx


def worker():
    current_actor_context = ActorContext()
    current_actor_context.run()


def test_caplog_fails(caplog, caplog_workaround):
    with caplog.at_level(logging.DEBUG, logger="leapp.actors.quagga_report"):
        with caplog_workaround():
            with futures.ProcessPoolExecutor(max_workers=1) as pool:
                fut = pool.submit(worker)
                futures.wait((fut,))
    assert "Some msg" in caplog.text


def test_caplog_passes(caplog, capsys):
    current_actor_context = ActorContext()
    with caplog.at_level(logging.DEBUG, logger="leapp.actors.quagga_report"):
        current_actor_context.run()
    assert "Some msg" in caplog.text
