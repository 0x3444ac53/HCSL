# Hand Coded Stringy lisp


## The Story

I was displeased with the way our culture pushes us towards large, complex templating engines that offer little to no arbitrary code execution, too many `%`'s and a frustrating amount of overhead. [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) has loops, ints, native python types, "functions", and (possibly, idk I didn't check) recursion (it probably does). All I want to do is replace one string with another string, and it shouldn't be that hard. [Bash seemed like the perfect tool](https://github.com/0x3444ac53/Not-Important), until you realise all the hoops one must jump through to have [recursive evaluation in a heredoc](https://github.com/0x3444ac53/Not-Important/blob/master/src/articles.html.sh#L21). Not to mention the difficulty of trying to [execute a python script](https://github.com/0x3444ac53/Not-Important/blob/master/main#L22) without having to create another file. 

I have taken it upon myself to solve this problem for all programmers that fell victim to the computer-science-drop-out-to-finance-bitch pipeline, and created a [Hand Coded Stringy Lisp](https://github.com/0x3444ac53/HCSL). 

## The Last Language you'll ever ~~want~~ need

All functions evaluate to a lisperal™, there are no variables, only functions that return lisperal™s. Functions are defined using the `func` builtin, which takes two arguments, a id and a lisperal™

```lisp
(func foo "{0} {1}")
(foo "hello" "world"); -> "hello world"
(func bar "hello")
(foo (bar) "world"); -> "hello world"
(func baz (foo (bar) "world")); -> "hello world"
```

There are no `ints`, `floats`, or any of those mathy things that made you hate linear algebra, just strings. 

I recognise that this may be a difficult transition for some (and we know all about those),  and that edge cases may arise that require something other than strings. So, I have graciously included some built-in functions to aid those that have not yet ascended to a higher plane:

```lisp
(exit "1")            ; -> exits with exitcode 1
                      ; not very useful in scripts, 
                      ; but handy in the repl

(execute "file name") ; will execute a file on your disk
(eval "bash_code")    ; if you must
(debug)               ; prints functions definitions
(map)                 ; see below
```

## map
There is one other built in, which is a map function, best explained by example
```lisp
; filename: map_exmaple.slisp
(func ul "<ul>{0}</ul>")
(func li "<li>{0}</li>")
(ul (map li (eval "cat map_exmaple.slisp")))
```
will print:
```
<ul><li>(func atag "<a href='{0}' class='{1}'>{2}</a>")</li>
<li>(func page (atag {0} "pages" {1}))</li>
<li>(func li "<li>{0}</li>")</li>
<li>(func ul "<ul>{0}</ul>")</li>
<li>(ul (map li (eval "cat test.slisp")))</li></ul>
```
syntax is `(map func_name expression [sep=\n] [joiner=\n])`. So you can specify how it splits the string it iterates on, and also specify what string is used to rejoin it. I would like to pretend this is robust and perfectly implented, but this Language only has strings, so it's application is fairly limited. 


# Acknowledgments

- [catgirl.sh](https://catgirl.sh) by [Camille](https://github.com/turquoise-hexagon) for inspiration
- Samie, who can create a pull request to link to herself if she so desires
- [Crafting Interpreters](https://craftinginterpreters.com/) by [Bob Nystrom](https://github.com/munificent) for introducing me to little languages
- My cat, [Ajax](https://www.instagram.com/p/CvT5ztQgaPs/), for reminding me to stretch
- My faithful companion, [Chester](https://www.instagram.com/p/CusjwW4AKO6/) for 13 wonderful years (so far)
- Erik Decker, for answering my calls more often than he should, and because he wanted to be acknowledged
- [evrimoztamur](https://news.ycombinator.com/user?id=evrimoztamur), for [an orange site comment](https://news.ycombinator.com/item?id=37223889) explaining that looping might actually be a good idea
