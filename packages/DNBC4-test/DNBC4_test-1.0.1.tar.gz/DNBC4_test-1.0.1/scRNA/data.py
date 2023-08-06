import os,subprocess
from scRNA.utils import _root_dir,str_mkdir,change_env,start_print_cmd

class Data:
    def __init__(self, args):
        self.cDNAr1 = args.cDNAfastq1
        self.cDNAr2 = args.cDNAfastq2
        self.oligor1 = args.oligofastq1
        self.oligor2 = args.oligofastq2
        self.thread = args.thread
        self.name = args.name
        self.lowqual = args.lowqual
        self.bgifilter = args.bgifilter
        self.dropN = args.dropN
        self.cDNAconfig = args.cDNAconfig
        self.oligoconfig = args.oligoconfig
        self.outdir = args.outdir
        self.starindex = args.starIndexDir
        self.gtf = args.gtf
    
    def run(self):
        str_mkdir('%s/01.data'%self.outdir)
        change_env()
        scRNA_parse_cmd = ['%s/lib/software/scRNA_parse'%_root_dir,'-t', str(self.thread),'-q', str(self.lowqual)]
        if self.bgifilter:
            scRNA_parse_cmd += ['-f']
        if self.dropN:
            scRNA_parse_cmd += ['-dropN']

        scRNA_parse_cDNA_cmd = scRNA_parse_cmd + [
            '-config',self.cDNAconfig,
            '-cbdis','%s/01.data/%s.cDNA_barcode_counts_raw.txt'%(self.outdir,self.name),
            '-1','%s/01.data/%s.cDNA_reads.fq'%(self.outdir,self.name),
            '-report','%s/01.data/%s.cDNA_sequencing_report.csv'%(self.outdir,self.name),
            self.cDNAr1,self.cDNAr2
        ]
        scRNA_parse_oligo_cmd = scRNA_parse_cmd + [
            '-config',self.oligoconfig,
            '-cbdis','%s/01.data/%s.Index_barcode_counts_raw.txt'%(self.outdir,self.name),
            '-1','%s/01.data/%s.Index_reads.fq'%(self.outdir,self.name),
            '-report','%s/01.data/%s.Index_sequencing_report.csv'%(self.outdir,self.name),
            self.oligor1,self.oligor2
        ]
        star_cmd = '%s/lib/software/STAR --limitOutSJcollapsed 4000000 --outStd SAM\
            --outSAMunmapped Within --runThreadN %s --genomeDir %s\
            --readFilesIn %s/01.data/%s.cDNA_reads.fq --outFileNamePrefix  \
            %s/01.data/ 1> %s/01.data/aln.sam'%(_root_dir,self.thread,self.starindex,self.outdir,self.name,self.outdir,self.outdir)
        PISA_sam2bam_cmd = '%s/lib/software/PISA sam2bam -adjust-mapq -gtf %s \
            -o %s/01.data/aln.bam -report %s/01.data/alignment_report.csv \
            %s/01.data/aln.sam'%(_root_dir,self.gtf,self.outdir,self.outdir,self.outdir)
        PISA_anno_cmd = '%s/lib/software/PISA anno -gtf %s \
            -o %s/01.data/anno.bam -report %s/01.data/anno_report.csv \
            %s/01.data/aln.bam'%(_root_dir,self.gtf,self.outdir,self.outdir,self.outdir)
        PISA_corr_cmd = '%s/lib/software/PISA corr -tag UR -new-tag UB \
            -tags-block CB,GN -@ %s -o %s/01.data/final.bam \
            %s/01.data/anno.bam'%(_root_dir,self.thread,self.outdir,self.outdir)

        scRNA_parse_cDNA_cmd = ' '.join(scRNA_parse_cDNA_cmd)
        scRNA_parse_oligo_cmd = ' '.join(scRNA_parse_oligo_cmd)
        start_print_cmd(scRNA_parse_cDNA_cmd)
        start_print_cmd(scRNA_parse_oligo_cmd)
        start_print_cmd(star_cmd)
        start_print_cmd(PISA_sam2bam_cmd)
        start_print_cmd(PISA_anno_cmd)
        start_print_cmd(PISA_corr_cmd)

def data(args):
    Data(args).run()

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
        help='whitelist file in JSON format for cDNA fastq,The value of cell barcode is an array in the JSON, \
        consist of one or more segments in one or both reads.',
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
        help='whitelist file in JSON format for oligo fastq',
        default='%s/config/DNBelabC4_scRNA_beads_readStructure.json'%_root_dir
        )
    parser.add_argument(
        '--thread',
        type=int, 
        default=4,
        help='Analysis threads.'
        )
    parser.add_argument(
        '--starIndexDir',
        type=str, 
        help='star index dir'
        )
    parser.add_argument(
        '--gtf',
        type=str, 
        help='gtf file'
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
        action='store_true'
        )
    return parser
