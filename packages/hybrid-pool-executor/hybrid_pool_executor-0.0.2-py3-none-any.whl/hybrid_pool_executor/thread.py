import weakref
from dataclasses import dataclass
from queue import Empty, SimpleQueue
from threading import Condition, Thread
from time import monotonic
from typing import Any, Hashable, Optional
from hybrid_pool_executor.typing import (
    ActionFlag,
    ACT_DONE,
    ACT_EXCEPTION,
    ACT_NONE,
    ACT_CLOSE,
    ACT_CMD_WORKER_STOP_FLAGS,
    ACT_RESET,
    ACT_RESTART,
    WorkerMode,
    WORKER_MODE_THREAD,
)
from hybrid_pool_executor.base import (
    BaseAction,
    BaseAsyncFutureInterface,
    BaseFuture,
    BaseOrder,
    BaseWorkerSpec,
    BaseWorker,
    CancelledError,
)


@dataclass
class ThreadWorkerSpec(BaseWorkerSpec):
    pass


@dataclass
class ThreadAction(BaseAction):
    worker_mode: WorkerMode = WORKER_MODE_THREAD


@dataclass
class ThreadOrder(BaseOrder):
    worker_mode: WorkerMode = WORKER_MODE_THREAD


class ThreadAsyncFutureInterface(BaseAsyncFutureInterface):
    pass


class ThreadFuture(BaseFuture):
    def __init__(self):
        self._condition = Condition()
        self._result = None
        self._exception = None


class ThreadWorker(BaseWorker):
    def __init__(self, spec: ThreadWorkerSpec):
        self.name = spec.name
        self.spec = spec

        self._running: bool = False
        self._idle: bool = True
        self._braking: bool = True
        self._thread: Optional[Thread] = None
        self._task_id: Optional[Hashable] = None

    def _get_response(
        self,
        flag: ActionFlag = ACT_NONE,
        result: Optional[Any] = None,
        exception: Optional[BaseException] = None,
    ):
        return ThreadAction(
            flag=flag,
            task_id=self._task_id,
            worker_id=self.name,
            result=result,
            exception=exception,
        )

    def start(self):
        if not self._braking:
            raise RuntimeError(
                f"{self.__class__.__qualname__} {self.name} is already started"
            )
        self._thread = Thread(target=self.run, daemon=self.spec.daemon)
        self._thread.start()

        # Block method until self.run actually starts to avoid creating multiple
        # workers when in high concurrency situation.
        while self._braking:
            pass

    def run(self):
        self._braking = False
        self._running = True

        spec = self.spec
        get_response = self._get_response
        task_bus: SimpleQueue = spec.task_bus
        request_bus: SimpleQueue = spec.request_bus
        response_bus: SimpleQueue = spec.response_bus
        max_task_count: int = spec.max_task_count
        max_err_count: int = spec.max_err_count
        max_cons_err_count: int = spec.max_cons_err_count
        idle_timeout: float = spec.idle_timeout
        wait_interval: float = spec.wait_interval

        task_count: int = 0
        err_count: int = 0
        cons_err_count: int = 0

        response: Optional[ThreadAction] = None

        idle_tick = monotonic()
        while True:
            if monotonic() - idle_tick > idle_timeout:
                response = get_response(ACT_CLOSE)
                break
            while not request_bus.empty():
                request: ThreadAction = request_bus.get()
                if request.match(ACT_RESET):
                    task_count = 0
                    err_count = 0
                    cons_err_count = 0
                if request.match(ACT_CMD_WORKER_STOP_FLAGS):
                    response = get_response(request.flag)
                    self._braking = True
                    break
                if self._braking:
                    break

                try:
                    order: ThreadOrder = task_bus.get(timeout=wait_interval)
                except Empty:
                    continue
                result = None
                try:
                    self._idle = False
                    self._task_id = order.name

                    # check if order is cancelled
                    if order.cancelled:
                        raise CancelledError(
                            f'Future "{order.name}" has been cancelled'
                        )

                    result = order.func(*order.args, **order.kwargs)
                except Exception as exc:
                    err_count += 1
                    cons_err_count += 1
                    response = get_response(
                        flag=ACT_EXCEPTION,
                        result=result,
                        exception=exc,
                    )
                else:
                    cons_err_count = 0
                    response = get_response(flag=ACT_DONE, result=result)
                finally:
                    task_count += 1

                    self._task_id = None
                    self._idle = True

                    idle_tick = monotonic()
                    if (
                        0 <= max_task_count <= task_count
                        or 0 <= max_err_count <= err_count
                        or 0 <= max_cons_err_count <= cons_err_count
                    ):
                        response.add_flag(ACT_RESTART)
                        break
                    response_bus.put(response)
                    response = None

            if response is not None and response.flag != ACT_NONE:
                response_bus.put(response)
            self._running = False
            self._braking = True

    def stop(self):
        self._braking = True
        if self._thread and self._thread.is_alive():
            self._thread.join()
        self._running = False
        self._thread = None

    def idle(self) -> bool:
        return self._idle
