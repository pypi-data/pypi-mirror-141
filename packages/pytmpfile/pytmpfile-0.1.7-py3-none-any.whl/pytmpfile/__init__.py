from memory_tempfile import MemoryTempfile
import contextlib
from typing import Optional
import tempfile
import os

__all__ = ['get_tmp_path', 'tempdir']
__version__ = '0.1.7'

SCRATCH_TMP = os.path.join('/scratch', 'tmp', os.environ['SLURM_JOB_ID'])
PREF_PATH = [SCRATCH_TMP] if os.path.exists(SCRATCH_TMP) else []

# Credits: https://pypi.org/project/memory-tempfile/
tempfile = MemoryTempfile(preferred_paths=PREF_PATH + ['/run/user/{uid}'],
                          filesystem_types=['tmpfs', 'ramfs', 'xfs'], fallback=True)

if not tempfile.found_mem_tempdir():
    raise RuntimeError('No tmp directory found')


def tempdir():
    return tempfile.gettempdir()


@contextlib.contextmanager
def get_tmp_path(content: Optional[str] = None, suffix: Optional[str] = None, delete=True) -> str:
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=delete, mode='w+') as ntf:
        if content:
            ntf.write(content)
            ntf.flush()
        yield ntf.name
