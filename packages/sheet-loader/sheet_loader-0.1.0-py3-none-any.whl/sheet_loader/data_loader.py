# coding=utf-8
import csv
import logging
from contextlib import contextmanager
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import Union, Tuple

import pandas as pd
from chardet import UniversalDetector

from .constants import DEFAULT_CHUNK_SIZE
from .helpers import frame_chunker

GeneralPath = Union[Path, SpooledTemporaryFile]
try:
    from s3path import S3Path

    S3PATH_EXISTS = True
    GeneralPath = Union[GeneralPath, S3Path]
except ImportError:
    S3PATH_EXISTS = False
    S3Path = None
try:
    from fastapi import UploadFile

    FASTAPI_EXISTS = True
    GeneralPathOrUpload = Union[GeneralPath, UploadFile]
except ImportError:
    FASTAPI_EXISTS = False
    UploadFile = None
    GeneralPathOrUpload = GeneralPath

logger = logging.getLogger(__name__)
csv_sniff = csv.Sniffer()
csv_sniff.preferred = ["|", ",", "\t"]


def sheet_loader(file: GeneralPath, **pd_kwargs):
    if file.suffix.lower().startswith(".xls"):
        return load_xlsx(file, **pd_kwargs)
    return load_csv(file, **pd_kwargs)


@contextmanager
def lazy_open(file, *args, **kwargs):
    if hasattr(file, "read"):
        file.seek(0)
        try:
            yield file
        finally:
            file.seek(0)
    elif hasattr(file, "open"):
        with file.open(*args, **kwargs) as fh:
            yield fh
    else:
        with open(file, *args, **kwargs) as fh:
            yield fh


def detect_encoding(file: GeneralPath, return_size=1024 * 1024) -> Tuple[str, str]:
    detector = UniversalDetector()
    buffer = b""
    with lazy_open(file, "rb") as fh:
        while chunk := fh.read(4096):
            detector.feed(chunk)
            buffer += chunk
            if detector.done or len(buffer) >= return_size:
                break
    if detector.done:
        encoding: str = detector.result["encoding"]
    else:
        res = detector.close()
        if res["encoding"] is None or res["encoding"].lower() in ("utf-8", "ascii"):
            encoding = "utf-8"
        else:
            encoding: str = res["encoding"]

    logger.debug("Encoding: %s", encoding)
    return encoding, buffer.decode(encoding)


@contextmanager
def load_xlsx(file: GeneralPath, **pd_kwargs):
    if hasattr(file, "as_uri"):
        yield pd.read_excel(file.as_uri(), dtype="string", **pd_kwargs)
    else:
        yield pd.read_excel(file, dtype="string", **pd_kwargs)
    # df = wr.s3.read_excel(
    #     file.as_uri(),
    #     dtype="string",
    #     parse_dates=DTYPE_DATES,
    # )
    # return df


@contextmanager
def load_csv(file: GeneralPath, **pd_kwargs):
    encoding, buffer = detect_encoding(file)
    try:
        dialect = csv_sniff.sniff(buffer)
        logger.debug(
            "Dialect: %s",
            {k: v for k, v in dialect.__dict__.items() if not k.startswith("_")},
        )
        # header_line = next(
        #     csv.reader(io.StringIO(buffer, newline=None), dialect=dialect)
        # )
        # dtypes = {k: v for k, v in DTYPE_MAP.items() if k in header_line}
        # date_dtypes = [v for v in DTYPE_DATES if v in header_line]
        with lazy_open(file) as fh:
            df = pd.read_csv(
                fh,
                dialect=dialect,
                encoding=encoding,
                on_bad_lines="warn",
                dtype="string",
                header=0,
                **pd_kwargs,
            )
            yield df
    except:
        logger.exception(buffer, stack_info=True)
        raise


@contextmanager
def load_xlsx_chunked(file: GeneralPath, chunksize, **pd_kwargs):
    with load_xlsx(file, **pd_kwargs) as data:
        yield frame_chunker(data, chunk_size=chunksize)


@contextmanager
def generic_load_sheet(file: GeneralPathOrUpload, chunk_size=DEFAULT_CHUNK_SIZE):
    if FASTAPI_EXISTS and isinstance(file, UploadFile):
        our_file = file.file
        if (
            file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            or file.filename.lower().endswith("xlsx")
            or file.filename.lower().endswith("xls")
        ):
            loader = load_xlsx_chunked
        else:
            loader = load_csv
    else:
        our_file = file
        if file.suffix.lower()[1:].startswith("xls"):
            loader = load_xlsx_chunked
        else:
            loader = load_csv
    with loader(our_file, chunksize=chunk_size) as loaded_file:
        yield loaded_file
