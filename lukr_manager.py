import os
import subprocess
import getpass

class LukrManager():
    def __init__(self):
        pass

    def create(self, path, size, random = False):
        #Commands definition
        file_name = path.split('/')[-1]
        partition_command = ['cryptsetup',
                             '-y',
                             'luksFormat',
                             path]
        open_command = ['sudo',
                        'cryptsetup',
                        'luksOpen',
                        path,
                        file_name]
        format_command = ['sudo',
                          'mkfs.ext4',
                          '-j',
                          '/dev/mapper/' + file_name]
        close_command = ['sudo',
                         'cryptsetup',
                         'luksClose',
                         file_name]
        if random:
            allocator_command = ['dd',
                                 'if=/dev/urandom',
                                 'of='+path,
                                 'bs=1M',
                                 'count='+str(size)]
        else:
            allocator_command = ['dd',
                                 'if=/dev/zero',
                                 'of='+path,
                                 'bs=1M',
                                 'count='+str(size)]
        #Error control
        if os.path.exists(path):
            raise IOError('File already exists!')
        #Execute
        subprocess.run(allocator_command)            
        subprocess.run(partition_command)            
        subprocess.run(open_command)            
        subprocess.run(format_command)            
        subprocess.run(close_command)

    def open(self, path, mount_dir):
        #Commands definition
        file_name = path.split('/')[-1]
        open_command = ['sudo',
                        'cryptsetup',
                        'luksOpen',
                        path,
                        file_name]
        mount_command = ['sudo',
                         'mount',
                         '/dev/mapper/' + file_name,
                         mount_dir]
        chown_command = ['sudo',
                         'chown',
                         '-R',
                         getpass.getuser(),
                         mount_dir]
        #Error control
        if not os.path.exists(path):
            raise IOError('Path doesn\'t exist!')
        if not os.path.exists(mount_dir):
            raise IOError('Mount dir doesn\'t exist!')
        #Execute
        subprocess.run(open_command)
        subprocess.run(mount_command)
        subprocess.run(chown_command)
        

    def close(self, path, mount_dir):
        #Commands definition
        file_name = path.split('/')[-1]
        close_command = ['sudo',
                        'cryptsetup',
                        'luksClose',
                         file_name]
        umount_command = ['sudo',
                         'umount',
                         mount_dir]
        #Error control
        if not os.path.exists(path):
            raise IOError('Path doesn\'t exist!')
        if not os.path.exists(mount_dir):
            raise IOError('Mount dir doesn\'t exist!')
        #Execute
        subprocess.run(umount_command)
        subprocess.run(close_command)
