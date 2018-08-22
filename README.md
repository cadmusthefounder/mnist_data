# Script to convert MNIST dataset into folders format.

``` bash
bash scripts/convert.sh data_type # Replace data_type with either mnist or fashion.
```

Returns 2 zip files in output folder, where the zip files have the following directory structure: 

 ``` bash
<label>/<img>.png
```
