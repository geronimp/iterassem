#!/usr/bin/env python
###############################################################################
#
# iterassem.py
#
###############################################################################
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################
 
__author__ = "Joel Boyd"
__copyright__ = "Copyright 2016"
__credits__ = ["Joel Boyd"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Joel Boyd"
__email__ = "joel.boyd near uq.net.au"
__status__ = "Development"
 
###############################################################################
# System imports
import argparse
import logging
import os

# Local imports
from run import Run

###############################################################################

debug={1:logging.CRITICAL,
       2:logging.ERROR,
       3:logging.WARNING,
       4:logging.INFO,
       5:logging.DEBUG}

###############################################################################

def check_inputs(args):
    '''
    Make sure all the inputs are valid.
    
    Inputs
    ------
    args : argparse object

    Exceptions
    ----------
    Raises expetions
    
    '''
    # TODO
###############################################################################
################################ - Classes - ##################################
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''Assemble lots of data''')
    parser.add_argument('--forward', nargs = '+', required=True,
                        help='forward pair of metagenome reads')
    parser.add_argument('--reverse', nargs = '+', required=True,
                        help='reverse pair of metagenome reads')
    parser.add_argument('--single', nargs = '+',
                        help='unpaired reads to include in the assembly')
    parser.add_argument('--filter_contigs', 
                        help='contigs to pre-filter the assembly assembly for')
    parser.add_argument('--bams', nargs='+', 
                        help='bams to filter with')
    parser.add_argument('--assembler', choices = ['spades'],
                        help='unpaired reads to include in the assembly')
    parser.add_argument('--subset', type = float, required=True,
                        help='Split up metagenome into X size fragments')
    parser.add_argument('--cpus', default='5',
                        help='number of threads to use for mapping and \
assembly')
    parser.add_argument('--log',
                        help='output logging information to this file.')
    parser.add_argument('--verbosity', type = int, default = 4,
                        help='Level of verbosity (1 - 5 - default = 4) \
5 = Very verbose, 1 = Silent')
    parser.add_argument('--output', default = 'iterassem_output',
                        help='Output directory or file')

    args = parser.parse_args()
    
    check_inputs(args)

    if args.log:
        if os.path.isfile(args.log): 
            raise Exception("File %s exists" % args.log)
        logging.basicConfig(filename=args.log, level=debug[args.verbosity], 
                            format='%(asctime)s %(levelname)s: %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(level=debug[args.verbosity], 
                            format='%(asctime)s %(levelname)s: %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        
    Run().run(args.forward, args.reverse, args.single, args.filter_contigs, 
              args.bams, args.assembler, args.subset, args.cpus, args.output)
    