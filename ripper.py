import os
import re
import subprocess
import ripdata
import ripsettings
import shutil

class Ripper:
    def __init__(self):
        self.data = None
        self.settings = None

    def set_data(self, data_obj):
        self.data = data_obj

    def set_settings(self, settings_obj):
        self.settings = settings_obj

    def rip(self):
        # rip audio (cdparanoia)
        # convert to format (flac, mp3, etc.)
        # set metadata
        # move to desired location

        if os.path.exists(self.settings['tmpdir']):
            shutil.rmtree(self.settings['tmpdir'])
            os.mkdir(self.settings['tmpdir'])
        else:
            os.mkdir(self.settings['tmpdir'])

        self.rip_audio()
        self.convert_audio()
        self.set_metadata()
        self.move_files()

    def rip_audio(self):
        # Calls cdparanoia to rip CD audio into temporary working directory

        current_dir = os.getcwd()
        os.chdir(self.settings['tmpdir'])
        subprocess.call(["cdparanoia", "-B"])
        
        if os.path.exists(self.settings['tmpdir'] + "/track00.cdda.wav"):
            os.remove(self.settings['tmpdir'] + "/track00.cdda.wav")

        os.chdir(current_dir)
    
    def convert_audio(self):
        # Calls the appropriate encoder (currently only FLAC) to convert
        # from wav format. Deletes the wav files

        current_dir = os.getcwd()
        os.chdir(self.settings['tmpdir'])

        re_obj = re.compile(".*wav$")
        for f in os.listdir(self.settings['tmpdir']):
            if not re_obj.match(f):
                continue
            else:
                if self.settings['audioformat'] == "flac":
                    command = ["flac"]
                    command.extend(self.settings['flacoptions'])
                    command.extend([f])
                    subprocess.call(command)

        for f in os.listdir(self.settings['tmpdir']):
            if re_obj.match(f):
                os.remove(self.settings['tmpdir'] + "/" + f)

        os.chdir(current_dir)

    def set_metadata(self):
        current_dir = os.getcwd()
        os.chdir(self.settings['tmpdir'])

        if self.settings['audioformat'] == 'flac':
            for num in range(0, self.data['totaltracks']):
                subprocess.call(['metaflac', '--set-tag=TITLE={0}'.format(self.data['tracknames'][num]), '--set-tag=ALBUM={0}'.format(self.data['album']), '--set-tag=DISCNUMBER={0}'.format(self.data['discnumber']), '--set-tag=TRACKNUMBER={0}'.format(int(num + 1)), '--set-tag=GENRE={0}'.format(self.data['genre']), '--set-tag=YEAR={0}'.format(self.data['year']), '--set-tag=ARTIST={0}'.format(self.data['trackartists'][num]), 'track{:02d}.cdda.flac'.format(int(num + 1))])
        
        os.chdir(current_dir)

    def move_files(self):
        current_dir = os.getcwd()
        os.chdir(self.settings['tmpdir'])

        
        for num in range(0, self.data['totaltracks']):
            # for each track, determine artist and album and move into
            # appropriate folder structure

            shutil.move('track{:02d}.cdda.flac'.format(int(num + 1)), self.generate_pathname(num))

        os.chdir(current_dir)

    def generate_pathname(self, tracknum):
        # Create the folder structure where songs will be ripped to

        if not os.path.exists(self.settings['riplocation']):
            os.mkdir(self.settings['riplocation'])

        substitutions = {'%a': self.data['trackartists'][tracknum], '%A': self.data['album'], '%d': self.data['discnumber'], '%g': self.data['genre'], '%n': int(tracknum + 1), '%t': self.data['tracknames'][tracknum], '%y': self.data['year']}

        name = self.settings['filenameformat']
        name = name.split('/')
        path = self.settings['riplocation']
        
        for num in range(0, len(name)):
            folder = name[num]                
            if num != len(name) - 1:
                for wildcard in substitutions.keys():
                    folder = folder.replace(wildcard, str(substitutions[wildcard]))
                path = path + '/' + folder
                if not os.path.exists(path):
                    os.mkdir(path)
            else:
                for wildcard in substitutions.keys():
                    folder = folder.replace(wildcard, str(substitutions[wildcard]))
                path = path + '/' + folder

        if self.settings['audioformat'] == 'flac':
            path = path + '.flac'

        return path
