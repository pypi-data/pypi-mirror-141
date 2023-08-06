import os,subprocess
from scRNA.utils import _root_dir,str_mkdir,change_env

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

        PISA_attrcnt_cmd = '%s/lib/software/PISA attrcnt -cb CB -tags UB,GN \
            -@ %s -dedup -o %s/02.count/beads_stat.txt -list %s \
            %s/01.data/final.bam'%(_root_dir,self.thread,self.outdir,self.cDNAbarcodeCount,self.outdir)
        cellCalling_cmd = [
            'Rscript %s/lib/R/cell_calling.R'%_root_dir,'-i',
            '%s/02.count/beads_stat.txt'%self.outdir,
            '-o %s/02.count/'%self.outdir
        ]
        if self.expectNum:
            cellCalling_cmd += ['-f %s'%self.expectnum]
        cellCalling_cmd= ' '.join(cellCalling_cmd)
        mergeBarcodes_cmd = '%s/lib/software/mergeBarcodes -b \
            %s/02.count/beads_barcode_all.txt -f %s -n %s -o \
            %s/02.count/'%(_root_dir,self.outdir,self.Indexreads,self.name,self.outdir)
        similiarBeads_cmd = '%s/lib/software/s1.get.similarityOfBeads -n %s \
            %s %s/02.count/%s_CB_UB_count.txt \
            %s/02.count/beads_barcodes.txt %s \
            %s/02.count/Similarity.all.csv \
            %s/02.count/Similarity.droplet.csv \
            %s/02.count/Similarity.droplet.filtered.csv'\
            %(_root_dir,self.thread,self.name,self.outdir,self.name,self.outdir,self.oligotype,self.outdir,self.outdir,self.outdir)
        combineBeads_cmd = 'python %s/lib/python/combinedListOfBeads.py \
            %s/02.count/Similarity.droplet.filtered.csv \
            %s/02.count/%s_combined_list.txt'\
            %(_root_dir,self.outdir,self.outdir,self.name)
        CellMerge_cmd = 'python %s/lib/python/cellMerge.py --indir \
            %s/02.count --name %s'%(_root_dir,self.outdir,self.name)
        tagAdd_cmd = '%s/software/tagAdd -n %s -bam %s \
            -file %s/02.count/%s_barcodeTranslate.txt \
            -out %s/02.count/anno_decon.bam -tag_check CB:Z: -tag_add DB:Z: \
            '%(_root_dir,self.thread,self.bam,self.outdir,self.name,self.outdir)
        
        print(PISA_attrcnt_cmd)
        subprocess.check_call(PISA_attrcnt_cmd, shell=True)
        print(cellCalling_cmd)
        subprocess.check_call(cellCalling_cmd, shell=True)
        subprocess.check_call("cat %s | awk '{print $1}'> %s/02.count/beads_barcode_all.txt"\
            %(self.cDNAbarcodeCount,self.outdir), shell=True)
        print(mergeBarcodes_cmd)
        subprocess.check_call(mergeBarcodes_cmd, shell=True)
        print(similiarBeads_cmd)
        subprocess.check_call(similiarBeads_cmd, shell=True)
        print(combineBeads_cmd)
        subprocess.check_call(combineBeads_cmd, shell=True)
        print(CellMerge_cmd)
        subprocess.check_call(CellMerge_cmd, shell=True)
        print(tagAdd_cmd)
        subprocess.check_call(tagAdd_cmd, shell=True)

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