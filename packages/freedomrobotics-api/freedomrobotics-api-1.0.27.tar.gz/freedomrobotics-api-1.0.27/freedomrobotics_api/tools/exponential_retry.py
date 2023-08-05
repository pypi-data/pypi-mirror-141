import functools


def retry(max_retries, logger=None, on_retry=None, on_fail=None):

    def _retry(fn):

        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            times_retried = 0
            while True:
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    times_retried += 1

                    if times_retried > max_retries:
                        # tried too many times, we should fail.
                        if logger:
                            logger.error(f"Execution of {fn.__name__} failed {max_retries} consecutively, giving up.")
                        if on_fail:
                            return on_fail()
                        else:
                            raise e
                    else:
                        # we should retry
                        if logger:
                            logger.error(f"Execution of {fn.__name__} failed, will retry. error: {e}\n", exc_info=True)
                        if on_retry:
                            on_retry()

        return wrapped

    return _retry
