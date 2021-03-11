# AFS - Agnostic File Storage

## Goals and motivations

The purpose of this module is to offer an agnostic, easy-to-use module 
for different file systems (At present time, just local and SMB/CIFS). 
The initial use of this module was provide an easy path to translate 
local file systems operations to a network samba server.

## Example of use

So, you can translate code like this:

    if os.path.isdir('/tmp/token.txt'):
        if not os.path.isdir('/tmp/results'):
            os.mkdir('/tmp/results')
        with open('/tmp/results/data.txt', 'wb') as f:
            f.write('This is an example\n')

To something like this (which must work identical):

    with afs.connect('temp') as fs:
        if not fs.isdir('results'):
            fs.mkdir('results')
        fs.cd('results')
        fs.save('data.txt', 'This is an example\n')

Usually you need to iterate a list of directories checking
for the existence of the dir, create if needed, and then changing
to the dir, for every directory::

    dirs = ['media', 'public', '2016', 'sep', '14']
    with afs.connect('static') as fs:
        for dir in dirs:
            if not fs.is_dir(dir):
                fs.mkdir(dir)
            fs.cd(dir)
        # You can save the file now

Using the `set_path` method make all this steps with one single call::

    with afs.connect('static') as fs:
        fs.set_path('media', 'public', '2016', 'sep', '14')
        # You can save the file now


The entry `temp` is defined in a configuration file, using
a format similar to windows .INI files, like this:

    [temp]
    kind: local
    base: /tmp

We can now switch to another directory by just replacing the 
`temp` base entry to the desired base path, for example. More 
interesting, you can change to a network SMB Server, modifying the 
configuration file to:

    [temp]
    kind: smb
    username: samba_user
    password: samba_password
    host: nas
    domain: mycompany.com
    service: test$

## Things to do

 * Add more storage file systems: NFS, Amazon S3, SFTP

 * Improve security, nobody likes password stored as plain text
   in configuration files.

 * More tests
