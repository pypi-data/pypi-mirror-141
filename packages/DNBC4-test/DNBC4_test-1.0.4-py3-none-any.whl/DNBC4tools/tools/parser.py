import os
from scRNA.__init__ import _root_dir

def parse_data(parser):
    parser.add_argument(
        '--name',
        help='sample name', 
        type=str
        )
    parser.add_argument(
        '--outdir',
        help='output dir, default is current directory', 
        default=os.getcwd()
        )
    parser.add_argument(
        '--cDNAfastq1',
        help='cDNAR1 fastq file, Multiple files are separated by comma.', 
        required=True
        )
    parser.add_argument(
        '--cDNAfastq2',
        help='cDNAR2 fastq file, Multiple files are separated by comma.', 
        required=True
        )
    parser.add_argument(
        '--cDNAconfig',
        help="""whitelist file in JSON format for cDNA fastq,The value of cell barcode is an array in the JSON, 
        consist of one or more segments in one or both reads.""",
        default='%s/config/DNBelabC4_scRNA_beads_readStructure.json'%_root_dir
        )
    parser.add_argument(
        '--oligofastq1',
        help='oligoR1 fastq file, Multiple files are separated by comma.',
        required=True
        )
    parser.add_argument(
        '--oligofastq2',
        help='oligoR2 fastq file, Multiple files are separated by comma.',
        required=True
        )
    parser.add_argument(
        '--oligoconfig',
        help="""whitelist file in JSON format for oligo fastq""",
        default='%s/config/DNBelabC4_scRNA_beads_readStructure.json'%_root_dir
        )
    parser.add_argument(
        '--thread',
        type=int, 
        default=4,
        help='Analysis threads.'
        )
    parser.add_argument(
        '--bgifilter',
        action='store_true',
        help='Process bgiseq filter.'
        )
    parser.add_argument(
        '--lowqual',
        help='Drop reads if average sequencing quality below this value.',
        type=int,
        default=4
        )
    parser.add_argument(
        '--dropN',
        help='Drop reads if N base in sequence or barcode.',
        action='store_true',
        )
    return parser