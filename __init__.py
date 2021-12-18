from pathlib import Path
from typing import Optional, Tuple, Iterable, Dict, Any, List
import multiprocessing as mp
from multiprocessing.connection import Connection as mpConn
from multiprocessing.shared_memory import SharedMemory, ShareableList
from contextlib import contextmanager
import numpy as np

def get_raw_data(file):
    return map(str.strip, Path(file).parent.joinpath("input.txt").read_text().splitlines())


# custom exception classes to help with error handling
class MultiProcessContextError(Exception):
    pass


class MPCCloseError(MultiProcessContextError):
    pass


class MPCOpenError(MultiProcessContextError):
    pass


# global vars
dtype_map = {
    0: np.uint8,
    1: np.uint16,
    2: np.uint32,
    3: np.int32,
    4: np.uint64,
    5: np.int64,
    6: np.float32,
    7: np.float64,
}
[dtype_map.setdefault(v.__name__, k) for k, v in tuple(dtype_map.items())]


##
# The custom context managers

@contextmanager
def npsm_create_context(sm_name, data: np.ndarray) -> np.ndarray:
    """Create a context manager to wrap the sm_context and produce
    a numpy array using the shared memory buffer. This context manager
    ensures the shared memory is release on error conditions."""
    with sm_context(sm_name, True, data.nbytes) as sm:
        sl = ShareableList([*data.shape] + [dtype_map[str(data.dtype)]], name=f"{sm_name}_shape")
        wrapper = np.ndarray(data.shape, data.dtype, buffer=sm.buf)
        wrapper[:] = data[:]
        try:
            yield wrapper
        finally:
            data[:] = wrapper[:]
            sl.shm.unlink()
            sl.shm.close()


@contextmanager
def npsm_use_context(sm_name, offsets: Tuple[slice] = None) -> np.ndarray:
    """Using the sm_name argument we access the shared memory buffer and
    wrap it in a numpy array. This context ensures the memory is properly
    released on error conditions."""
    with sm_context(sm_name) as sm:
        sl = ShareableList(None, name=f"{sm_name}_shape")
        shape = [sl[i] for i in range(len(sl) - 1)]
        dtype = dtype_map[sl[len(sl) - 1]]
        wrapper = np.ndarray(shape, dtype, buffer=sm.buf)
        if offsets:
            if not isinstance(offsets,slice):
                offsets = list(offsets)
                for i in range(len(offsets)):
                    if offsets[i] is None:
                        offsets[i] = slice(None, None, None)
                    elif isinstance(offsets[i], int):
                        offsets[i] = slice(None, None, None)
                    elif isinstance(offsets[i], tuple):
                        offsets[i] = slice(*offsets[i])
            else:
                offsets = offsets,
            wrapper = wrapper[tuple(offsets)]
        try:
            yield wrapper
        finally:
            sm.close()


@contextmanager
def sm_context(sm_name, create: bool = False, size: int = None) -> SharedMemory:
    """The most simple of the custom context managers. This ensures that whoever
    creates the shared memory, also unlinks and closes that memory upon exit.

    This may not always be the appropriate use for shared memory, as there can be instances
    where some cron-job allocates resources and starts a process on them then abandons the
    original pointer to those resources assuming the new process will manage them."""
    sm = SharedMemory(sm_name, create, size) if size is not None else SharedMemory(sm_name, create)
    try:
        yield sm
    finally:
        if create:
            sm.unlink()
        sm.close()


@contextmanager
def multiproc_nested_contexts(num_procs: int,
                              pipes_is_duplex: bool,
                              callable_target,
                              split_args: bool,
                              target_args: Optional[Iterable] = None,
                              target_kwargs: Optional[Dict[str, Any]] = None,
                              is_daemon: bool = True) -> list:
    """creates as many child processes as is specified by num_procs.

    Each child process is also assigned its own pair of read/write pipes for communicating with the parent.

    Note: Only the contexts are nested! The child process created in each context layer is still a direct child of the
    process which initially called this function; i.e., all resulting child processes are siblings

    :param num_procs:
    :type num_procs:
    :return:
    :rtype:
    """
    @contextmanager
    def recursable_inner(nprocs: int, procs: List[mp.Process], pipes: List[mpConn]) -> List[mpConn]:
        try:
            nprocs -= 1
            pread, pwrite = mp.Pipe(duplex=pipes_is_duplex)
            with pread:
                with pwrite:
                    if split_args:
                        kwargs = {k: v for k, v in target_kwargs.get(nprocs, {}).items()}
                        kwargs['pwrite'] = pwrite
                        args = target_args[nprocs]
                    else:
                        kwargs = {k: v for k, v in target_kwargs.items()}
                        kwargs['pwrite'] = pwrite
                        args = target_args
                    proc = mp.Process(target=callable_target, args=args, kwargs=kwargs, daemon=is_daemon)
                    procs.append(proc)
                    pipes.append(pread)
                    if nprocs:
                        with recursable_inner(nprocs, procs, pipes) as pips:
                            yield pips
                    else:
                        try:
                            for _proc in procs:
                                _proc.start()
                            yield pipes
                        finally:
                            try:
                                try:
                                    proc.join()
                                except AssertionError:
                                    # if something happens and we have an exception that prevents the final context
                                    # layer from starting the accumulated processes, a call to proc.join() will raise
                                    # an assertion error as you can't join a process that was never started.
                                    pass
                                proc.close()
                            except BaseException as be:
                                raise MPCCloseError(
                                    f"An exception was encountered while trying to close process in layer {num_procs - nprocs}") from be
        except MPCCloseError:
            raise
        except BaseException as be:
            raise MPCOpenError(
                f"An exception was encountered while setting up context layer {num_procs - nprocs}") from be

    assert num_procs > 0, "calling multiproc_nested_contexts with an initial num_procs<1 is illogical :P caller must specify at least 1 process"
    if target_kwargs is None:
        target_kwargs = {}
    try:
        with recursable_inner(num_procs, [], []) as pipes:
            yield pipes
    except (MPCCloseError, MPCOpenError) as e:
        raise e
    except BaseException as be:
        err = MultiProcessContextError("Encountered an unexpected error")
        raise err from be
    finally:
        pass

