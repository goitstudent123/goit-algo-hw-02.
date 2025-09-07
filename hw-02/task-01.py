#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field
from queue import Queue, Empty
from typing import Any
import itertools
import random
import time
import signal

@dataclass
class Request:
    """Represents a single request in the system."""
    id: int
    created_at: float = field(default_factory=time.time)
    payload: dict[str, Any] = field(default_factory=dict)


class RequestSystem:
    """Simple request processing system backed by a FIFO queue."""
    def __init__(self) -> None:
        self._queue: Queue[Request] = Queue()
        self._id_gen = itertools.count(1)
        self._running = True

    def generate_request(self) -> Request:
        """Create a new Request and enqueue it."""
        req = Request(
            id=next(self._id_gen),
            payload={"note": random.choice(["standard", "premium", "vip"])}
        )
        self._queue.put(req)
        print(f"[GEN ] -> queued request #{req.id} ({req.payload['note']})")
        return req

    def process_request(self) -> None:
        """Dequeue and process a single Request if available."""
        try:
            req = self._queue.get_nowait()
        except Empty:
            print("[PROC] <- queue is empty; nothing to process")
            return

        duration = random.uniform(0.1, 0.5)
        time.sleep(duration)
        latency_ms = int((time.time() - req.created_at) * 1000)
        print(f"[PROC] <- processed request #{req.id} in {duration:.2f}s (latency {latency_ms} ms)")
        self._queue.task_done()

    def run(self, *, max_iterations: int | None = None, tick: float = 0.3) -> None:
        """
        Run the main loop until interrupted (Ctrl+C) or until `max_iterations` reached.
        Each loop:
          - generate 0..N new requests
          - process exactly one request (if present)
        """
        iteration = 0
        while self._running and (max_iterations is None or iteration < max_iterations):
            for _ in range(random.randint(0, 3)):
                self.generate_request()

            self.process_request()

            iteration += 1
            time.sleep(tick)

        print("[INFO] stopping; draining remaining requests...")
        while not self._queue.empty():
            self.process_request()
        print("[INFO] done.")

    def stop(self) -> None:
        """Signal the loop to stop."""
        self._running = False


def main() -> None:
    system = RequestSystem()

    def _sigint_handler(_sig, _frm):
        print("\n[INFO] received interrupt; shutting down...")
        system.stop()
    signal.signal(signal.SIGINT, _sigint_handler)

    print("Press Ctrl+C to exit.\n\n")
    system.run(max_iterations=100)

if __name__ == "__main__":
    main()
