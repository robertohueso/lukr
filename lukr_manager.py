import os
import subprocess
import getpass

class LukrManager():
    def __init__(self):
        pass

    def create(self, path, size, random = False):
        file_name = path.split('/')[-1]
        if not os.path.exists(path):
            if random:
                allocator_command = ['dd',
                                     'if=/dev/random',
                                     'of='+path,
                                     'bs=1M',
                                     'count='+str(size)]
            else:
                allocator_command = ['dd',
                                     'if=/dev/zero',
                                     'of='+path,
                                     'bs=1M',
                                     'count='+str(size)]
            subprocess.run(allocator_command)
            partition_command = ['cryptsetup',
                                 '-y',
                                 'luksFormat',
                                 path]
            subprocess.run(partition_command)
            open_command = ['sudo',
                            'cryptsetup',
                            'luksOpen',
                            path,
                            file_name]
            subprocess.run(open_command)
            format_command = ['sudo',
                              'mkfs.ext4',
                              '-j',
                              '/dev/mapper/' + file_name]
            subprocess.run(format_command)
            close_command = ['sudo',
                             'cryptsetup',
                             'luksClose',
                             file_name]
            subprocess.run(close_command)

    def open(self, path, mount_dir):
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
        subprocess.run(open_command)
        subprocess.run(mount_command)
        subprocess.run(chown_command)
        

    def close(self, path, mount_dir):
        file_name = path.split('/')[-1]
        close_command = ['sudo',
                        'cryptsetup',
                        'luksClose',
                         file_name]
        umount_command = ['sudo',
                         'umount',
                         mount_dir]
        subprocess.run(umount_command)
        subprocess.run(close_command)
