## Introduction

### Requirements


### Usage
#### Basics
##### img_to_cbz
> Creating one CBZ archive from a directory containing images, using the default ("directory") naming scheme
```bash
# Source directory layout:
# -> source_dir/Awesome Comic/The first adventure - T1/
# +-> img1.jpg
# +-> [ ... ]
# +-> imgX.png

./img_to_cbz.py "source_dir/Awesome Comic/The first adventure - T1" "dst_dir/Awesome Comic"

# Output:
# -> dst_dir/Awesome Comic/
# +-> The first adventure - T1.cbz

```

> Creating several CBZ archives from images, in multiple directories (1 comic / directory), using the "context" naming scheme
```bash
# Source directory layout:
# -> source_dir/Awesome Comic/
# +-> The first adventure - T1/
# ++-> img1.jpg
# ++-> [ ... ]
# ++-> imgX.jpg
# +-> Another Adventure - T2/
# ++-> img1.png
# ++-> [ ... ]
# ++-> imgX.png

./img_to_cbz.py --naming-method context --naming-format 'Awesome Comic - {dir}.cbz' "source_dir/Awesome Comic" "dst_dir/Awesome Comic"

# Output:
# -> dst_dir/Awesome Comic/
# +-> Awesome Comic - The first adventure - T1.cbz
# +-> Awesome Comic - Another Adventure - T2.cbz

```

##### arc_repack
> 
```bash

```

#### Renaming target files / directory

### Examples
**img_to_cbz**:
```bash

```

**arc_repack**:
```bash

```
