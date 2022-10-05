### Wu-Manber multi-pattern string search algorithm

Restrictions:
<ol>
    <li>Patterns should have length >1</li>
    <li>The algorithm finds all substrings, not just the longest patterns</li>
</ol>


```
>>>from wu_manber import WuManber

>>>wm = WuManber(patterns=["honey", "funey", "fu", "list", "money"])
>>>wm.search("funeyneedmoney")
[('funey', 0), ('fu', 0), ('money', 9)]

```
