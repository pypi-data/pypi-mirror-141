import sys,os,argparse
import textwrap,importlib
#script_path = os.path.dirname(__file__)
#sys.path.insert(1, script_path + '/..')

from DNBC4tools.tools.utils import _version, _pipelist

def pipeline_package(pipe):
    package = importlib.import_module(f"DNBC4tools.tools.{pipe}")
    return package

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''
        DNBC4_scRNA contain the following function:
        --------------------------------
        pipeline:
        DNBC4_scRNA data : Perform quality control and filtering on the raw fastq, 
                           use Star to align the cDNAData to the reference genome and annotate it with GTF file
        DNBC4_scRNA count : Determine the inflection point and judge the empty droplets, 
                            merge multiple beads in the same oil droplet, calculate the cell * gene expression matrix
        DNBC4_scRNA analysis : Perform quality control on the cell expression matrix,filter low-quality cells and genes,
                               perform cell clustering analysis and marker gene screening based on the expression matrix
        DNBC4_scRNA report : Data Aggregation and Visualization Web Report Generation,
                             need data,count,analysis output and result
        DNBC4_scRNA run : run data, count, analysis, report for a complete pipeline
        
        function:
        DNBC4_scRNA mkref : Create a genome reference directory
        DNBC4_scRNA clean : If you are satisfied with the result, delete the temp files, else change the parameters and rerun'''))
    parser.add_argument('-v', '--version', action='version', version=_version)
    subparsers = parser.add_subparsers(dest='parser_step')

    for _pipe in _pipelist:
        package= pipeline_package(_pipe)
        func = getattr(package, _pipe)
        func_opts = getattr(package, f"parse_{_pipe}")
        parser_step = subparsers.add_parser(_pipe, description='DNAC4scRNA %s'%_pipe,formatter_class=argparse.RawDescriptionHelpFormatter)
        func_opts(parser_step)
        parser_step.set_defaults(func=func)
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
