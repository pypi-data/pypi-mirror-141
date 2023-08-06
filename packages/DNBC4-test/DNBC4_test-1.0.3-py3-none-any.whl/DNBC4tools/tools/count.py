import os,subprocess
from .utils import _root_dir,str_mkdir,change_env,start_print_cmd

class Count:
    def __init__(self,args):
        self.name = args.name
        self.bam = args.bam
        self.cDNAbarcodeCount = args.cDNAbarcodeCount
        self.Indexreads = args.Indexreads
        self.oligobarcodeCount = args.oligobarcodeCount
        self.thread = args.thread
        self.oligotype = args.oligotype
        self.outdir = args.outdir
        self.expectNum = args.expectNum
    
    def run(self):
        str_mkdir('%s/02.count'%self.outdir)
        change_env()

        PISA_attrcnt_cmd = '%s/soft/PISA attrcnt -cb CB -tags UB,GN \
            -@ %s -dedup -o %s/02.count/beads_stat.txt -list %s \
            %s/01.data/final.bam'%(_root_dir,self.thread,self.outdir,self.cDNAbarcodeCount,self.outdir)
        cellCalling_cmd = [
            'Rscript %s/rna/cell_calling.R'%_root_dir,'-i',
            '%s/02.count/beads_stat.txt'%self.outdir,
            '-o %s/02.count/'%self.outdir
        ]
        if self.expectNum:
            cellCalling_cmd += ['-f %s'%self.expectnum]
        cellCalling_cmd= ' '.join(cellCalling_cmd)
        mergeBarcodes_cmd = '%s/soft/mergeBarcodes -b \
            %s/02.count/beads_barcode_all.txt -f %s -n %s -o \
            %s/02.count/'%(_root_dir,self.outdir,self.Indexreads,self.name,self.outdir)
        similiarBeads_cmd = '%s/soft/s1.get.similarityOfBeads -n %s \
            %s %s/02.count/%s_CB_UB_count.txt \
            %s/02.count/beads_barcodes.txt %s \
            %s/02.count/Similarity.all.csv \
            %s/02.count/Similarity.droplet.csv \
            %s/02.count/Similarity.droplet.filtered.csv'\
            %(_root_dir,self.thread,self.name,self.outdir,self.name,self.outdir,self.oligotype,self.outdir,self.outdir,self.outdir)
        combineBeads_cmd = 'python %s/rna/combinedListOfBeads.py \
            %s/02.count/Similarity.droplet.filtered.csv \
            %s/02.count/%s_combined_list.txt'\
            %(_root_dir,self.outdir,self.outdir,self.name)
        CellMerge_cmd = 'python %s/rna/cellMerge.py --indir \
            %s/02.count --name %s'%(_root_dir,self.outdir,self.name)
        tagAdd_cmd = '%s/soft/tagAdd -n %s -bam %s \
            -file %s/02.count/%s_barcodeTranslate.txt \
            -out %s/02.count/anno_decon.bam -tag_check CB:Z: -tag_add DB:Z: \
            '%(_root_dir,self.thread,self.bam,self.outdir,self.name,self.outdir)
        PISA_count_cmd = '%s/soft/PISA count -@ %s -tag DB -anno-tag GN \
            -umi UB -outdir %s/02.count/matrix %s/02.count/anno_decon.bam\
            '%(_root_dir,self.thread,self.outdir,self.outdir)

        start_print_cmd(PISA_attrcnt_cmd)
        start_print_cmd(cellCalling_cmd)
        subprocess.check_call("cat %s | awk '{print $1}'> %s/02.count/beads_barcode_all.txt"\
            %(self.cDNAbarcodeCount,self.outdir), shell=True)
        start_print_cmd(mergeBarcodes_cmd)
        start_print_cmd(similiarBeads_cmd)
        start_print_cmd(combineBeads_cmd)
        start_print_cmd(CellMerge_cmd)
        start_print_cmd(tagAdd_cmd)
        str_mkdir('%s/02.count/matrix'%self.outdir)
        start_print_cmd(PISA_count_cmd)


def count(args):
    Count(args).run()

def parse_count(parser):
    parser.add_argument(
        '--name',
        help='sample name'
    )
    parser.add_argument(
        '--bam',
        help='Bam file after star and anno, ./1_data/final.bam'
    )
    parser.add_argument(
        '--cDNAbarcodeCount',
        help='Read count per cell barcode for cDNA, ./1_data/cDNA_barcode_counts_raw.txt.',
    )
    parser.add_argument(
        '--Indexreads',
        help='Barcode reads generate by scRNAparse, ./1_data/Index_reads.fq.'
    )
    parser.add_argument(
        '--oligobarcodeCount',
        help='Read count per cell barcode for oligo, ./1_data/Index_barcode_counts_raw.txt.'
    )
    parser.add_argument(
        '--oligotype',
        help='Whitelist for oligo, default is %s/config/oligo_type8.txt'%_root_dir,
        default='%s/config/oligo_type8.txt'%_root_dir
    )
    parser.add_argument(
        '--thread',
        help='Analysis threads. default is 4.',
        type=int,
        default=4
    )
    parser.add_argument(
        '--outdir',
        help='output dir, default is current directory.',
        default=os.getcwd()
    )
    parser.add_argument(
        '--expectNum',
        help='expectNum.',
    )
    return parser