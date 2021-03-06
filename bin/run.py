#!/usr/bin/env python
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
__copyright__ = "Copyright 2015"
__credits__ = ["Joel Boyd"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Joel Boyd"
__email__ = "joel.boyd near uq.net.au"
__status__ = "Development"
 
from filter_contigs import FilterContigs

import logging
import tempfile
import os


class Run:
    
    def run(self, forward, reverse, single, filter_contigs, bams, assembler, 
            subset, cpus, output):
        '''
        '''
        fc = FilterContigs()
        ar = AssembleReads()

        logging.info('Creating working directory')
        try:
            os.mkdir(output)
        except:
            raise Exception('Directory %s already exists' % (output))
        
        # Pre-filter by bins, if provided
        if(bams or filter_contigs):
            logging.info('Pre-filtering reads before assembly')
            output_directory = os.path.join(output, 'filtering')
            os.mkdir(output_directory)
            forward, reverse, single \
                        = fc.filter(filter_contigs, bams, forward, reverse, 
                                    single, cpus, output_directory)
        
        # Run assembler
        if assembler:
            logging.info('Beginning iterassem pathway')
        
        

        

