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
__copyright__ = "Copyright 2016"
__credits__ = ["Joel Boyd"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Joel Boyd"
__email__ = "joel.boyd near uq.net.au"
__status__ = "Development"
 
###############################################################################

import logging
import os
import subprocess
import tempfile

from itertools import chain, izip

class FilterContigs:
    
    BAM_SUFFIX = '.bam'
    
    def extract(self, bams, forward, reverse, single, output): 
        '''
        '''
        def extract_batch(list, read_names, output):
            filtered_file_list = []
            for file in list:
                file_split = os.path.splitext(file)
                filtered_file = os.path.join(output,
                                             "%s.filtered%s" % (file_split[0],
                                                                 file_split[1]))
                cmd = 'fxtract -vXHF %s %s > %s' % (read_names, file, 
                                                    filtered_file)
                subprocess.call(cmd, shell=True)
                filtered_file_list.append(filtered_file)
            return filtered_file_list
            
        with tempfile.NamedTemporaryFile(suffix='.txt') as read_names:
            for bam in bams:
                cmd = "samtools view %s | awk '{print $1}' | sort | uniq > %s" \
                                                    % (bam, read_names.name) 
                subprocess.call(cmd, shell=True)
        
            filtered_forward = extract_batch(forward, read_names.name, output)
            filtered_reverse = extract_batch(reverse, read_names.name, output)
            if single:
                filtered_single = extract_batch(single, 
                                                read_names.name, 
                                                output)
            else:
                filtered_single = None
            return filtered_forward, filtered_reverse, filtered_single
        
        return filtered_forward, filtered_reverse, filtered_single
            
    
    def map(self, filter_contigs, forward, reverse, single, cpus, output):
        '''
        '''
        # Create mapping database and map reads
        paired_reads = list(chain.from_iterable(izip(forward, reverse)))
        
        cmd = 'bamm make -o %s -t %s -d %s -c %s' % (output, cpus, 
                                                     filter_contigs, 
                                                     paired_reads)
        if single:
            cmd += ' -s %s ' % (single)
        
        logging.debug("Running command: %s" % cmd)
        subprocess.call(cmd, shell=True)
        
        bams = [file for file in os.listdir(output) if 
                file.endswith(self.BAM_SUFFIX)]
        
        return bams

    def filter(self, filter_contigs, bams, forward, reverse, single, cpus, 
               output):
        '''
        '''
        if not bams:
            output_mapping = os.path.join(output, 'mapping')
            os.mkdir(output_mapping)
            bams = self.map(filter_contigs, forward, reverse, single, cpus, 
                            output_mapping)
            
        filtered_forward, filtered_reverse, filtered_single \
                            = self.extract(bams, forward, reverse, single,
                                           output_mapping)
        
        return filtered_forward, filtered_reverse, filtered_single
            