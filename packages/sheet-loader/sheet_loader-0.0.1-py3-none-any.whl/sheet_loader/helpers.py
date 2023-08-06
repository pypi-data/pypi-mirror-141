# coding=utf-8


def frame_chunker(frame, chunk_size):
    for i in range(0, len(frame), chunk_size):
        yield frame.iloc[i : (i + chunk_size)]
