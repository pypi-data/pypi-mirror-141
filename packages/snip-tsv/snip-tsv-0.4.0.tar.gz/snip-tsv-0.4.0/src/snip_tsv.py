from __future__ import annotations

import argparse
import ast
import csv
import difflib
import re
from io import TextIOWrapper
from typing import Any
from typing import cast
from typing import NamedTuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


__version__ = "0.4.0"


COL_DTYPE = {"int": int, "float": float, "str": str}
CROP_END_REGEX = re.compile(r":(\+|-)?\d+(\.\d+)?$")


class Defaults:
    IN_FILE = "-"
    DELIMITER = "\t"
    HAS_HEADER = False
    PLOT_X = "0"
    PLOT_Y = "1"
    CROP_COL = "0"
    OUT_FILE = "-"


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    if hasattr(args, "handler"):
        return args.handler(args)

    parser.print_help()
    return 1


def create_parser(
    parser: argparse.ArgumentParser | None = None,
) -> argparse.ArgumentParser:
    _parser = parser or argparse.ArgumentParser()

    _parser.add_argument(
        "in_file",
        type=argparse.FileType("r"),
        default=Defaults.IN_FILE,
        help="Input data file. (default: %(default)s)",
    )

    _parser.add_argument("-v", "--version", action="version", version=__version__)
    _parser.add_argument(
        "-H",
        "--header",
        default=Defaults.HAS_HEADER,
        action="store_true",
        help="When set assume the first row to be a header row. By default, "
        "no header row is assumed.",
    )
    _parser.add_argument(
        "-d",
        "--delimiter",
        default=Defaults.DELIMITER,
        help="The delimiter used in the input data file. (default: %(default)r)",
    )
    _parser.add_argument(
        "-x",
        "--plot-x",
        default=Defaults.PLOT_X,
        help="Column to use on the x-axis. A 0-indexed integer or a column "
        "heading string. (default: %(default)s)",
    )
    _parser.add_argument(
        "-y",
        "--plot-y",
        default=Defaults.PLOT_Y,
        help="Column to use on the y-axis. A 0-indexed integer or a column "
        "heading string. (default: %(default)s)",
    )
    _parser.add_argument(
        "-c",
        "--crop-col",
        default=Defaults.CROP_COL,
        help="Column to search in for --crop-start/--crop-end values. A "
        "0-indexed integer or a column heading string. (default: %(default)s)",
    )
    _parser.add_argument(
        "-s",
        "--crop-start",
        help="Start value to use for cropping (inclusive). If the column is "
        "numeric then the row with column entry closest to the given value is used.",
    )
    _parser.add_argument(
        "-e",
        "--crop-end",
        help="End value to use for cropping (exclusive). If the column is "
        "numeric then the row with column entry closest to the given value "
        "is used. To specify a numeric value relative to --crop-start use "
        "the syntax ':<number>'. Omit this flag to crop from --crop-start to "
        "the end of the file.",
    )
    _parser.add_argument(
        "-o",
        "--out-file",
        type=argparse.FileType("w"),
        default=Defaults.OUT_FILE,
        help="File to write the results to (either an image or TSV file. If "
        "not provided a matplotlib plot is shown when plotting, and data is "
        "written to stdout when cropping. (default: %(default)s)",
    )

    _parser.set_defaults(handler=handler)

    return _parser


def handler(args: argparse.Namespace) -> int:
    in_file: TextIOWrapper = args.in_file
    has_header: bool = args.header
    delimiter: str = args.delimiter
    data = read_file(in_file, delimiter, has_header)

    popts = PlotOptions.from_namespace(args, data.header)
    copts = CropOptions.from_namespace(args, data.header)
    out_file: TextIOWrapper = args.out_file

    if copts.start is not None:
        cropped_data = crop(data, copts)
        return write_records(cropped_data, out_file, delimiter)
    else:
        fig, ax = plot(data, popts)
        return write_figure(fig, ax, out_file)


class Data(NamedTuple):
    records: list[list[Any]]
    header: list[str] | None = None
    filename: str | None = None
    is_numeric: list[bool] | None = None


def read_file(
    file: TextIOWrapper,
    delimiter: str = Defaults.DELIMITER,
    has_header: bool = Defaults.HAS_HEADER,
) -> Data:
    reader = csv.reader(file, delimiter=delimiter)
    header = next(reader) if has_header else None
    try:
        records = [[coerce(c) for c in row] for row in reader]
    except ValueError as e:
        msg = f"Failed to parse file {file.name!r}. Did you forget the --header flag?"
        raise ValueError(msg) from e
    is_numeric = _determine_numeric_columns(records)
    return Data(records, header, file.name, is_numeric)


def coerce(s: str | None) -> Any:
    if s is None:
        return s
    try:
        return ast.literal_eval(s)
    except SyntaxError:
        return ast.literal_eval(f"'{s}'")
    except ValueError:
        if s.lower() == "nan":
            return float(s)
        raise


def _determine_numeric_columns(records: list[list[Any]]) -> list[bool]:
    numeric = [True for _ in records[0]]
    for record in records:
        numeric = [n and isinstance(e, (int, float)) for n, e in zip(numeric, record)]
    return numeric


class CropOptions(NamedTuple):
    col: int
    start: Any
    end: Any

    @classmethod
    def from_namespace(cls, args: argparse.Namespace, header: list[str] | None = None):
        col = _get_column_index(args.crop_col, header)
        start = coerce(args.crop_start)
        end = cls._parse_endpoint(start, args.crop_end)
        return cls(col, start, end)

    @staticmethod
    def _parse_endpoint(start: int | float | None, end: Any):
        if end is None:
            return end
        if re.match(CROP_END_REGEX, end):
            if not isinstance(start, (int, float)):
                msg = f"Cannot specify relative crop end [{end=}] "
                msg += f"with non-numeric crop start [{start=}]"
                raise ValueError(msg)
            return start + coerce(end[1:])
        else:
            return coerce(end)


class PlotOptions(NamedTuple):
    x: int = int(Defaults.PLOT_X)
    y: int = int(Defaults.PLOT_Y)

    @classmethod
    def from_namespace(cls, args: argparse.Namespace, header: list[str] | None = None):
        plot_x = _get_column_index(args.plot_x, header)
        plot_y = _get_column_index(args.plot_y, header)
        return cls(plot_x, plot_y)


def _get_column_index(col: str, headings: list[str] | None = None) -> int:
    _heading_map = {h: i for i, h in enumerate(headings)} if headings else {}
    if col.isnumeric():
        return int(col)
    elif col not in _heading_map:
        msg = f"Column {col!r} is unknown."
        matches = difflib.get_close_matches(str(col), _heading_map.keys())
        if matches:
            matches_s = ", ".join(matches)
            msg += f" Did you mean one of: {matches_s}"
        raise ValueError(msg)
    else:
        return _heading_map[col]


def crop(data: Data, opts: CropOptions) -> Data:
    start_idx: int | None = None
    end_idx: int | None = None

    if data.is_numeric and data.is_numeric[opts.col]:
        start_idx, end_idx = find_endpoints_closest(data, opts)
    else:
        start_idx, end_idx = find_endpoints_exact(data, opts)

    return Data(data.records[start_idx:end_idx], data.header, data.filename)


def find_endpoints_exact(
    data: Data,
    opts: CropOptions,
) -> tuple[int | None, int | None]:
    start_idx: int | None = None
    end_idx: int | None = None
    for i, record in enumerate(data.records):
        if record[opts.col] == opts.start and start_idx is None:
            start_idx = i
        if opts.end is not None and record[opts.col] == opts.end and end_idx is None:
            end_idx = i

    return start_idx, end_idx


def find_endpoints_closest(
    data: Data,
    opts: CropOptions,
) -> tuple[int | None, int | None]:
    start_idx = _argmin(
        [abs(cast(float, r[opts.col] - opts.start)) for r in data.records],
    )
    end_idx = None
    if opts.end is not None:
        end_idx = start_idx + _argmin(
            [
                abs(cast(float, r[opts.col] - opts.end))
                for r in data.records[start_idx:]
            ],
        )
    return start_idx, end_idx


def _argmin(values: list[int | float]) -> int:
    pair = min((v, i) for i, v in enumerate(values))
    return pair[1]


def write_records(
    data: Data,
    out_file: TextIOWrapper,
    delimiter: str = Defaults.DELIMITER,
) -> int:
    writer = csv.writer(out_file, delimiter=delimiter)
    if data.header is not None:
        writer.writerow(data.header)
    writer.writerows(data.records)

    return 0


def plot(data: Data, opts: PlotOptions) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots()
    x = [r[opts.x] for r in data.records]
    y = [r[opts.y] for r in data.records]
    ax.plot(x, y)

    return fig, ax


def write_figure(fig: Figure, ax: Axes, out_file: TextIOWrapper) -> int:
    if out_file.name in ("<stdout>", "<stderr>"):
        plt.show()
    else:
        fig.savefig(out_file.name, dpi=200)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
