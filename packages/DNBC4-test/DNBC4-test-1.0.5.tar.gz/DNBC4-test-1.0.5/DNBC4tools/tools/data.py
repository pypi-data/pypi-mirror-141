import os
from threading import Thread
from .utils import str_mkdir,start_print_cmd
from DNBC4tools.__init__ import _root_dir

class Data:
    def __init__(self, args):
        self.cDNAr1 = args.cDNAfastq1
        self.cDNAr2 = args.cDNAfastq2
        self.oligor1 = args.oligofastq1
        self.oligor2 = args.oligofastq2
        self.thread = args.thread
        self.name = args.name
        self.lowqual = args.lowqual
        self.cDNAconfig = args.cDNAconfig
        self.oligoconfig = args.oligoconfig
        self.outdir = os.path.join(args.outdir,args.name)
        self.starindex = args.starIndexDir
        self.gtf = args.gtf
        self.include_introns = args.include_introns
        self.no_bgifilter = args.no_bgifilter
    
    def run(self):
        str_mkdir('%s/01.data'%self.outdir)
        scRNA_parse_cmd = ['%s/soft/scRNA_parse'%_root_dir,'-t', str(self.thread),'-q', str(self.lowqual)]
        if  not self.no_bgifilter:
            scRNA_parse_cmd += ['-f','-dropN']

        scRNA_parse_cDNA_cmd = scRNA_parse_cmd + [
            '-config',self.cDNAconfig,
            '-cbdis','%s/01.data/%s.cDNA_barcode_counts_raw.txt'%(self.outdir,self.name),
            '-1','%s/01.data/%s.cDNA_reads.fq'%(self.outdir,self.name),
            '-report','%s/01.data/cDNA_sequencing_report.csv'%self.outdir,
            self.cDNAr1,self.cDNAr2
        ]
        scRNA_parse_oligo_cmd = scRNA_parse_cmd + [
            '-config',self.oligoconfig,
            '-cbdis','%s/01.data/%s.Index_barcode_counts_raw.txt'%(self.outdir,self.name),
            '-1','%s/01.data/%s.Index_reads.fq'%(self.outdir,self.name),
            '-report','%s/01.data/Index_sequencing_report.csv'%self.outdir,
            self.oligor1,self.oligor2
        ]
        star_cmd = '%s/soft/STAR --limitOutSJcollapsed 4000000 --outStd SAM --outSAMunmapped Within --runThreadN %s --genomeDir %s --readFilesIn %s/01.data/%s.cDNA_reads.fq --outFileNamePrefix  %s/01.data/ 1> %s/01.data/aln.sam'\
            %(_root_dir,self.thread,self.starindex,self.outdir,self.name,self.outdir,self.outdir)
        PISA_sam2bam_cmd = '%s/soft/PISA sam2bam -adjust-mapq -gtf %s -o %s/01.data/aln.bam -report %s/01.data/alignment_report.csv %s/01.data/aln.sam'\
            %(_root_dir,self.gtf,self.outdir,self.outdir,self.outdir)
        PISA_anno_cmd = ['%s/soft/PISA anno -gtf %s -o %s/01.data/anno.bam -report %s/01.data/anno_report.csv %s/01.data/aln.bam'
            %(_root_dir,self.gtf,self.outdir,self.outdir,self.outdir)]
        if self.include_introns:
            PISA_anno_cmd += ['-intron']
        PISA_corr_cmd = '%s/soft/PISA corr -tag UR -new-tag UB -tags-block CB,GN -@ %s -o %s/01.data/%s.final.bam %s/01.data/anno.bam'\
            %(_root_dir,self.thread,self.outdir,self.name,self.outdir)

        scRNA_parse_cDNA_cmd = ' '.join(scRNA_parse_cDNA_cmd)
        scRNA_parse_oligo_cmd = ' '.join(scRNA_parse_oligo_cmd)
        threads = []
        threads.append(Thread(target=start_print_cmd(scRNA_parse_cDNA_cmd)))
        threads.append(Thread(target=start_print_cmd(scRNA_parse_oligo_cmd)))
        for t in threads:
            t.start()
        start_print_cmd(star_cmd)
        start_print_cmd(PISA_sam2bam_cmd)
        PISA_anno_cmd = ' '.join(PISA_anno_cmd)
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
        default='%s/config/DNBelabC4_scRNA_oligo_readStructure.json'%_root_dir
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
        '--no_bgifilter',
        action='store_true',
        help='No process bgiseq filter.'
        )
    parser.add_argument(
        '--lowqual',
        help='Drop reads if average sequencing quality below this value.',
        type=int,
        default=4
        )
    parser.add_argument(
        '--include_introns', 
        action='store_true',
        help='Include intronic reads in count.'
        )
    return parser
