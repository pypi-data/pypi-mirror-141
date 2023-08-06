# jsw-nx
> Next toolkit for python.

## installation
```shell
pip install jsw-nx -U
```

## usage
```python
import jsw_nx as nx

## common methods
nx.includes([1,2,3], 2) # => True
nx.includes([1,2,3], 5) # => False
```

## next core methods
- base/filter
- base/find
- base/find_index
- base/foreach
- base/forin
- base/get
- base/includes
- base/index
- base/map
- base/reduce
- base/set
- base/type

## ruby style
- rubify/times
- rubify/to_a
- rubify/to_b
- rubify/to_f
- rubify/to_i
- rubify/to_n
- rubify/to_s

## next packages
- days
- deep_each
- is_process_alive
- param
- parse_cookie
- qs
- replace_dict_all
- [tmpl](https://js.work/posts/34ef06b7870ec)
- uniq

## next classes
+ date
  - format 
  - now 
  - create
+ fileutils
  - mkdir_p
  - cd
  - pwd
  - ls
  - mv
  - rmdir
  - touch
  - cp_r
  - isfile
  - isdir
  - exists
  - gbk_to_utf8
+ tar
  - gz
  - xz
+ [JSON](https://js.work/posts/3dc24683e53c4)
  - parse
  - stringify