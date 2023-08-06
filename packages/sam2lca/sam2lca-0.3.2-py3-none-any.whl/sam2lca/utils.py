import os
import json
import rocksdb
from sam2lca.config import NCBI
import pandas as pd
import logging


def count_reads_taxid(read_taxid_dict):
    """Returns number of reads matching TAXID

    Args:
        read_taxid_dict (dict): {read_name(str): TAXID(int)}
    """
    taxid_cnt = {}
    taxid_reads = {}
    for r in read_taxid_dict:
        if read_taxid_dict[r] not in taxid_cnt:
            taxid_cnt[read_taxid_dict[r]] = 1
            taxid_reads[read_taxid_dict[r]] = [r]
            continue
        else:
            taxid_cnt[read_taxid_dict[r]] += 1
            taxid_reads[read_taxid_dict[r]].append(r)
    return taxid_cnt, taxid_reads


def output_file(sam_path):
    out = os.path.basename(sam_path).split(".")[:-1]
    out = {"sam2lca": ".".join(out) + ".sam2lca", "bam": ".".join(out) + ".bam"}

    return out


def check_extension(filename):
    """Check alignment file format to give correct open mode

    Args:
        filename (str): Path to alignment file

    Returns:
        str: opening mode

    Raises:
        Exception: Extension not supported
    """
    extension = filename.split(".")[-1]
    modes = {"bam": "rb", "sam": "r", "cram": "rc"}
    try:
        return modes[extension]
    except KeyError:
        raise Exception(f"{extension} file extension not supported")


def taxid_to_lineage(taxid_count_dict, output):
    res = {}
    for taxid in taxid_count_dict:
        read_count = taxid_count_dict[taxid]
        sciname = NCBI.get_taxid_translator([taxid])[taxid]
        rank = NCBI.get_rank([taxid])[taxid]
        taxid_lineage = NCBI.get_lineage(taxid)
        scinames = NCBI.get_taxid_translator(taxid_lineage)
        ranks = NCBI.get_rank(taxid_lineage)
        lineage = [{ranks[taxid]: scinames[taxid]} for taxid in taxid_lineage]
        res[taxid] = {
            "name": sciname,
            "rank": rank,
            "count": read_count,
            "lineage": lineage,
        }

        df = pd.DataFrame(res).transpose().sort_values("count", ascending=False)
        df["lineage"] = (
            df["lineage"]
            .astype(str)
            .str.replace("[\[\]\{\}]", "")
            .str.replace(", ", " - ")
        )
        df.to_csv(f"{output}.csv", index_label="TAXID")

    with open(f"{output}.json", "w") as write_file:
        json.dump(res, write_file)
    logging.info(
        f"Step 6/6: writing sam2lca results to:\n* {output}.json\n* {output}.csv"
    )

    return res


def get_db_connection(db_path):
    return rocksdb.DB(db_path, opts=rocksdb.Options(), read_only=True)
