### Wu-Manber multi-pattern string search algorithm

```
>>>from wu_manber import WuManber

>>>wm = WuManber(patterns=["honey", "funey", "fu", "list", "money"])
>>>wm.search("funeyneedmoney")
[('funey', 0), ('fu', 0), ('money', 9)]

```
