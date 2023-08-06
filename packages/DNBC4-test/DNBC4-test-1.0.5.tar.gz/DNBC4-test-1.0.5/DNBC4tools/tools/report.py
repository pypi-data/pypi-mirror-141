import os
from .utils import str_mkdir,start_print_cmd
from DNBC4tools.__init__ import _root_dir

class Report:
    def __init__(self,args):
        self.name = args.name
        self.species = args.species
        self.outdir = os.path.join(args.outdir,args.name)
    def run(self):
        str_mkdir('%s/04.report'%self.outdir)
        pre_cmd = 'python %s/rna/pre_process.py --outPath %s'\
            %(_root_dir,self.outdir)
        generate_cmd = 'python %s/rna/generate_report.py --outPath %s --htmlTemplate %s/template/template.html --name %s --species %s' \
            %(_root_dir,self.outdir,_root_dir,self.name,self.species)
        start_print_cmd(pre_cmd)
        start_print_cmd(generate_cmd)

def report(args):
    Report(args).run()

def parse_report(parser):
    parser.add_argument(
        '--name',
        required=True,
        help='Sample name'
    )
    parser.add_argument(
        '--species',
        type=str,
        default='NA',
        help='select species for cell annotation, only human and mouse can do auto annotation.'
    )
    parser.add_argument(
        '--outdir',
        help='output dir, default is current directory.',
        default=os.getcwd()
    )
    return parser