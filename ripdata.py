import subprocess
import re

class RipData(dict):
    def __init__(self):
        self['variousartists'] = False
        self['album'] = ''
        self['discnumber'] = 1
        self['genre'] = ''
        self['year'] = 0
        self['totaltracks'] = 0
        self['tracknames'] = []
        self['trackartists'] = []

    def initialize(self):
        self['totaltracks'] = self.get_number_of_tracks()
        
        for num in range(0, self['totaltracks']):
            self['tracknames'].extend(' ')
            self['trackartists'].extend(' ')

    def get_number_of_tracks(self):
        '''Use cdparanoia to find out how many tracks are on the CD'''

        try:
            track_info = subprocess.check_output(['cdparanoia', '-Q'], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            return 0

        regex_result = re.findall('^\s+\d+', track_info, re.MULTILINE)
        tracknumbers = [int(x.lstrip()) for x in regex_result]
        return max(tracknumbers)
