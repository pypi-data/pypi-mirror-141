Simple python package to sort Json from files, strings, or dictionaries

Usage:
`sorted_jsn = json_sort.sorter.sort_from_dict(jsn)`
`sorted_jsn = json_sort.sorter.sort_from_file(jsn)`
`sorted_jsn = json_sort.sorter.sort_from_string(jsn)`

One can use a custom sort method by providing a predicate to the methods as in `...predicate={method_name_here}`:
