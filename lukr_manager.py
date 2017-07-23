import os
import subprocess
from subprocess import Popen, PIPE
import getpass
import exceptions

class LukrManager():
    """Encrypted virtual device manager
    """
    
    def __init__(self):
        pass

    def create(self, path, size, password, random = False):
        """Create encrypted virtual device
        
        Keyword arguments:
        path -- Path to the new virtual device.
        size -- Size in MBytes of the new virtual device.
        random -- Use of random data generator to overwrite
        old data.(Default False)
        """
        
        #Commands definition
        password = str(password)
        file_name = path.split('/')[-1]
        partition_command = ['cryptsetup',
                             '-y',
                             'luksFormat',
                             path]
        open_command = ['pkexec',
                        'cryptsetup',
                        'luksOpen',
                        path,
                        file_name]
        format_command = ['pkexec',
                          'mkfs.ext4',
                          '-j',
                          '/dev/mapper/' + file_name]
        close_command = ['pkexec',
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
        cmd = Popen(partition_command, stdin=PIPE, universal_newlines=True)
        cmd.communicate(password + '\n')
        cmd.wait()
        cmd = Popen(open_command, stdin=PIPE, universal_newlines=True)
        cmd.communicate(password + '\n')
        cmd.wait()
        subprocess.run(format_command)            
        subprocess.run(close_command)

    def open(self, path, mount_dir, password):
        """Open encrypted virtual device
        
        Keyword arguments:
        path -- Path to the virtual device file.
        mount_dir -- Directory where you want it to mount.
        """
        
        #Commands definition
        password = str(password)
        file_name = path.split('/')[-1]
        open_command = ['pkexec',
                        'cryptsetup',
                        'luksOpen',
                        path,
                        file_name]
        mount_command = ['pkexec',
                         'mount',
                         '/dev/mapper/' + file_name,
                         mount_dir]
        chown_command = ['pkexec',
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
        cmd = Popen(open_command, stdin=PIPE, universal_newlines=True)
        cmd.communicate(password + '\n')
        cmd.wait()
        if cmd.returncode == 2:
            raise exceptions.WrongPassword
        subprocess.run(mount_command)
        subprocess.run(chown_command)
        

    def close(self, path, mount_dir):
        """Close an open encrypted virtual device
        
        Keyword arguments:
        path -- Path to the virtual device file.
        mount_dir -- Directory where it is mounted.
        """
        
        #Commands definition
        file_name = path.split('/')[-1]
        close_command = ['pkexec',
                        'cryptsetup',
                        'luksClose',
                         file_name]
        umount_command = ['pkexec',
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
