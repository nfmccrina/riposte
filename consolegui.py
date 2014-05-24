import ripper
import ripdata
import ripsettings

class ConsoleGui:
    def __init__(self):
        self.cd_info = None

    def main_loop(self):
        user_input = ''
        audio_ripper = ripper.Ripper()
        self.cd_info = ripdata.RipData()
        self.cd_info.initialize()

        settings = ripsettings.RipSettings()
        settings.initialize()

        print('Welcome to MusicRipper 0.1!')
        print('Press "h" for help, or "q" to quit')

        while user_input != 'q':
            user_input = raw_input("Enter command: ")

            if user_input == 'r':
                audio_ripper.set_data(self.cd_info)
                audio_ripper.set_settings(settings)
                audio_ripper.rip()
            elif user_input == 'h':
                print("MusicRipper help")
                print("e - edit CD info")
                print("h - display commands")
                print('p - print CD info')
                print("q - exit the program")
                print("r - rip the CD in the drive")
            elif user_input == 'e':
                self.get_cd_info()
            elif user_input == 'p':
                print('Album: {0}'.format(self.cd_info['album']))
                print('Disc: {0}'.format(self.cd_info['discnumber']))
                print('Artist: {0}'.format(self.cd_info['trackartists'][0] if not self.cd_info['variousartists'] else 'Various Artists'))
                print('Year: {0}'.format(self.cd_info['year']))
                print('Genre: {0}'.format(self.cd_info['genre']))
                for num in range(0, self.cd_info['totaltracks']):
                    print('Track {0}'.format(int(num + 1)))
                    print('    Title: {0}'.format(self.cd_info['tracknames'][num]))
                    if self.cd_info['variousartists']:
                        print('    Artist: {0}'.format(self.cd_info['trackartists'][num]))
                    

        print("Goodbye!")

    def get_cd_info(self):
        # collect album info from user

        usr_input = ''
        while usr_input != 'b':
            print('Edit Album Info (press \'h\' for help)')
            
            usr_input = raw_input('> ')
            
            if usr_input == 'h':
                print('a: edit album title')
                print('A: edit artist name')
                print('b: back to main menu')
                print('d: edit disc number')
                print('g: edit genre')
                print('i: edit individual track artists')
                print('t: edit track titles')
                print('T: edit individual track titles')
                print('y: edit year')
            elif usr_input == 'a':
                self.cd_info['album'] = raw_input('Enter album title: ')
            elif usr_input == 'A':
                artist = raw_input('Enter album artist (press return for various artists): ')
                for num in range(0, self.cd_info['totaltracks']):
                    if artist == '':
                        self.cd_info['trackartists'][num] = raw_input('Enter track {0} artist: '.format(int(num + 1)))
                    else:
                        self.cd_info['trackartists'][num] = artist
            elif usr_input == 'd':
                try:
                    self.cd_info['discnumber'] = int(raw_input('Enter disc #: '))
                except ValueError:
                    pass
            elif usr_input == 'g':
                self.cd_info['genre'] = raw_input('Enter genre: ')
            elif usr_input == 'i':
                try:
                    tracknum = int(raw_input('Enter track number to edit: '))
                    try:
                        self.cd_info['trackartists'][tracknum - 1] = raw_input('Enter track {0} artist: '.format(tracknum))
                    except IndexError:
                        print('Error: track {0} does not exist'.format(tracknum))
                except ValueError:
                    print('Invalid track number')
            elif usr_input == 't':
                for num in range(0, self.cd_info['totaltracks']):
                    title = raw_input('Enter track {0} title: '.format(int(num + 1)))
                    self.cd_info['tracknames'][num] = title
            elif usr_input == 'T':
                try:
                    tracknum = int(raw_input('Enter track number to edit: '))
                    try:
                        self.cd_info['tracknames'][tracknum - 1] = raw_input('Enter track {0} title: '.format(tracknum))
                    except IndexError:
                        print('Error: track {0} does not exist'.format(tracknum))
                except ValueError:
                    print('Invalid track number')
            elif usr_input == 'y':
                try:
                    self.cd_info['year'] = int(raw_input('Enter year: '))
                except ValueError:
                    pass
