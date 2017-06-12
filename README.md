# LUKr
A simple LUKS encrypted virtual devices manager.

## Dependencies
* [cryptsetup](https://gitlab.com/cryptsetup/cryptsetup)
* [python-fire](https://github.com/google/python-fire)

## Quick guide
Create a new virtual device
```shell
lukr create path_to_file size_in_MB use_random(True/False)
```

Open virtual device
```shell
lukr open path_to_file path_to_mount_dir
```

Close virtual device
```shell
lukr close path_to_file path_to_mount_dir
```

## More information
Read docstrings or
```shell
lukr command --help
```
