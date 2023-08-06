import argparse
import os
import sys
from pathlib import Path
from typing import List
from rdfx import File, PersistenceSystem, prepare_files_list
from rdflib import Graph, util

RDF_FILE_ENDINGS = {
    "ttl": "turtle",
    "turtle": "turtle",
    "json": "json-ld",
    "json-ld": "json-ld",
    "jsonld": "json-ld",
    "owl": "xml",
    "xml": "xml",
    "rdf": "xml",
    "nt": "nt",
    "n3": "n3",
}

OUTPUT_FILE_ENDINGS = {
    "turtle": "ttl",
    "xml": "xml",
    "json-ld": "json-ld",
    "nt": "nt",
    "n3": "n3",
}


def get_input_format(file_path):
    input_format = util.guess_format(str(file_path))
    if input_format is None:
        str_path = str(file_path)
        if str_path.endswith("json-ld") or str_path.endswith("jsonld"):
            input_format = "json-ld"
        else:
            raise Exception(
                "ERROR: Cannot guess the RDF format of input file {}".format(file_path)
            )

    return input_format


def make_output_file_path(input_file_path, input_format, output_format, in_place):
    output_file_name = input_file_path.name.split(".")[:-1][0]

    if input_format == output_format and not in_place:
        output_file_name += ".new"

    output_file_name = output_file_name + "." + OUTPUT_FILE_ENDINGS.get(output_format)

    output_path = input_file_path.parent / output_file_name
    print("output file: {}".format(output_path))
    return output_path


def convert(
    input_file_path: Path,
    persistence_system,
    output_filename: str,
    output_format: str,
    comments: str = None,
):
    input_format = get_input_format(input_file_path)
    output_file_path = input_file_path.parent
    g = Graph().parse(str(input_file_path), format=input_format)
    persistence_system.write(g, output_filename, output_format, comments,output_file_path)


def merge(
    rdf_files: List[Path],
    persistence_system,
    output_format,
    output_filename,
    leading_comments=None,
):
    """
    Merges a given set of RDF files into one graph

    """
    for f in rdf_files:
        if not f.name.endswith(tuple(RDF_FILE_ENDINGS.keys())):
            raise ValueError(
                f"Files to be merged must have a known RDF suffix (one of {', '.join(RDF_FILE_ENDINGS)})"
            )

    g = Graph()
    for f in rdf_files:
        g.parse(f, format=RDF_FILE_ENDINGS[f.suffix.lstrip(".")])
    persistence_system.write(g, output_filename, output_format, leading_comments)


def persist_to(persistence_system: PersistenceSystem, g: Graph):
    if not issubclass(type(persistence_system), PersistenceSystem):
        return ValueError(
            f"You must select of the the subclasses of PersistenceSystem to use for the persistence_system argument"
        )
    else:
        persistence_system.write(g)


if __name__ == "__main__":
    if "-h" not in sys.argv and len(sys.argv) < 3:
        print(
            "ERROR: You must supply at a minimum the method (convert or merge), a file or files, and a target format"
        )
        exit()

    parser = argparse.ArgumentParser()

    parser.add_argument("method", choices=("convert", "merge"))

    parser.add_argument(
        "data",
        nargs="+",
        type=str,
        help="Path to the RDF file or directory of files for merging or conversion.",
    )

    parser.add_argument(
        "--format",
        "-f",
        type=str,
        help="The RDFlib token for the RDF format you want to convert the RDF file to.",
        choices=RDF_FILE_ENDINGS.keys(),
    )

    parser.add_argument(
        "-o",
        "--output",
        help="if set, the output location for merged or converted files, defaults to the current working directory",
        type=str,
    )

    parser.add_argument(
        "--comments", type=str, help="Comments to prepend to the RDF, turtle only."
    )

    args = parser.parse_args()

    if args.output:
        output_loc = Path(args.output)
    else:
        output_loc = Path(os.getcwd())

    if args.method == "merge":
        files_list = prepare_files_list(args.data)
        ps = File(directory=output_loc)
        merge(files_list, ps, args.format, "merged", args.comments)

    if args.method == "convert":
        ps = File(directory=output_loc)
        rdf_format = args.format
        leading_comments = args.comments
        files_list = prepare_files_list(args.data)
        for file in files_list:
            output_filename = Path(file).stem
            convert(file, ps, output_filename, rdf_format, leading_comments)
