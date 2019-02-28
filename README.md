* Each item flows between processors is a instance that subclass the `FlowItemWrapperBase`

* `call_path` is in the format of `((index, step_uid), ...)`

* use `call_path` to build a trie tree, the extrected result is saved at the leaf of the trie tree

```
  P1 will be called with call_path [(0,0)]

       +
       |
       |
       v
       P1
       |   -----> P1 outputs two doms to one child,
       |          the P2 will be called twice with call_path
       |          [(0,0),(0,1)] and [(0,0),(1,1)]
       |
       |
 +---+ P2 +---+
 |            | ----> P2 output 2 element for each call and
 |            |       send them to two children, each call to children
 +            +       will cause step_uid increase by 1
P3            P4
                      For P2's first input, P3 will be called with [(0,0),(0,1),(0,2)]
                                                                   [(0,0),(0,1),(1,2)]
                                            P4 will be called with [(0,0),(0,1),(0,3)]
                                                                   [(0,0),(0,1),(1,3)]
                      For P2's 2nd   input, P3 will be called with [(0,0),(1,1),(0,4)]
                                                                   [(0,0),(1,1),(1,4)]
                                            P4 will be called with [(0,0),(1,1),(0,5)]
                                                                   [(0,0),(1,1),(1,5)]


```


```

(0,0)--+-(0,1)--+-(0,2)   {k1: v1, k2: v2}     <meta fields_group_name = foo>
       |        |
       |        +-(1,2)   {k1: v3, k2: v4}     <meta fields_group_name = baz>
       |        |
       |        +-(0,3)   {k3: v5, k4: v6}     <meta fields_group_name = bar>
       |        |
       |        +-(1,3)   {k3: v7, k4: v8}     <meta fields_group_name = baz>
       |
       +-(1,1)--+-(0,4)   {k1: v9, k2: v10}    <Also has some meta data>
                |
                +-(1,4)   {k1: v11, k2: v12}   <Also has some meta data>
                |
                +-(0,5)   {k3: v13, k4: v14}   <Also has some meta data>
                |
                +-(1,5)   {k3: v15, k4: v16}   <Also has some meta data>

```

```
First, reach the leaf node, get:
(0,2)   {k1: v1, k2: v2}
(1,2)   {k1: v3, k2: v4}
(0,3)   {k3: v5, k4: v6}
(1,3)   {k3: v7, k4: v8}

Sort, get:
(0,2)   {k1: v1, k2: v2}
(0,3)   {k3: v5, k4: v6}
(1,2)   {k1: v3, k2: v4}
(1,3)   {k3: v7, k4: v8}
```

Group the sorted items by `idx` key, for each group, we will have a `buf`, the `buf` is an empty dict at first, and we will data in this group into the `buf`.

Because each item has a `meta` object, we will do some additional process with different config inthe `meta`. The most important one for now is called `fields_group_name`

suppose neither of the following two items have `fields_group_name`, then, they will be merged into the buf directly:
```
(0,2)   {k1: v1, k2: v2}
(0,3)   {k3: v5, k4: v6}

will be merged into 

{k1: v1, k2: v2, k3: v5, k4: v6}
```

suppose two items each has `fields_group_name` `foo` and `bar`, then, they will be merged into the following format:

```
(0,2)   {k1: v1, k2: v2}
(0,3)   {k3: v5, k4: v6}

will be merged into 

{
    foo: {k1: v1, k2: v2},
    bar: {k3: v5, k4: v6}
}
```


suppose two items both have `fields_group_name` `baz` , then, they will be merged into the following format:

```
(0,2)   {k1: v1, k2: v2}
(0,3)   {k3: v5, k4: v6}

will be merged into 
{
    baz: {k1: v1, k2: v2, k3: v5, k4: v6}
}
```

Note that all of the above three result is a dict result.
Now, suppose the first group and the second group were merged into 

```
{
    foo: {k1: v1, k2: v2},
    bar: {k3: v5, k4: v6}
}

And

{
    baz: {k1: v1, k2: v2, k3: v5, k4: v6}
}
```

Now we have to merge them into the finally one, it also a dict of list, so we get:

```
{
    foo: [{k1: v1, k2: v2}],
    bar: [{k3: v5, k4: v6}],
    baz: [{k1: v1, k2: v2, k3: v5, k4: v6}]
}
```

Before we get the finally merge result, we also have another meta option `force_list`, if it is flase, then the list with only one item will be moved out of the list. suppose `force_list` is False, then the above result will become:

```
{
    foo: {k1: v1, k2: v2},
    bar: {k3: v5, k4: v6},
    baz: {k1: v1, k2: v2, k3: v5, k4: v6}
}
```



```
So, after first Merge, we get:

(0,0)--+-(0,1)  {
       |            foo: [{k1: v1, k2: v2}],
       |            bar: [{k3: v5, k4: v6}],
       |            baz: [{k1: v1, k2: v2, k3: v5, k4: v6}]
       |        }
       |      
       +-(1,1)  {
                    k1: [v9, v11],
                    k2: [v10, v12],
                    k3: [v13, v15],
                    k4: [v14, v16]
                }
```

Now we can perform the next level merge.


Next, let's look more closer into the merge process.

suppose we have the following state, in stractor, the data in the trie tree have a flag to indicate that whether it's a merged result. a merged result is the result of a previous merge, it a leaf node created by replacing a sub-tree, an unmerged result is the leaf node of the origin trie tree:
```

(0,0)--+-(0,1)  {                               // a merged result
       |            foo: v1, 
                    bar: v2,
                    baz: v3
       |        }
       |      
       +-(0,2)  {                               // an unmerged result
       |            foo: [{k1: v11, k2: v21}]               
       |        }
       |
       +-(0,3)  {                               // an unmerged result
       |            bar: "baz"               
       |        }
       |
       +-(0,4)  {                               // an unmerged result
                    baz: {k3:v31}            
                }
```

Stractor will first merge the unmerged items, and then merge the merged item into the new merged one. this order is important.

When merge the above group, first, a new empty `buf` will be created, and the two unmerged result will be merged, so the `buf` will look like this:

```
{
    foo: [{k1: v11, k2: v21}],
    bar: "baz",
    baz: {k3:v31}
}
```

then, we will merge the previous merged results into the `buf`, if a key in the previous merged result is already in the `buf`, then, it's up to the `merge_conflict` meta option. for example, if use the default 'recursive' policy, a sub-dict with the same name will be created, if it is a list, then the previous ,erged result will be appended to the list, else, the previous merged result will replace the new merged one. so, the final merged result is:
```
{
    foo: [{k1: v11, k2: v21},v1],
    bar: v2,
    baz: {k3:v31, baz: v3}
}
```