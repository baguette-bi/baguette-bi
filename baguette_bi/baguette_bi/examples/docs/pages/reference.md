# 🤔 Baguette BI Reference

This is a non-exhautive list of everything that can be done in Baguette BI. Before reading
this, make sure you're familiar with
[Markdown syntax](https://daringfireball.net/projects/markdown/)
and
[Jinja2 templating language](https://jinja.palletsprojects.com/).

[TOC]

## Markdown extensions

This is not supposed to be a full reference of Markdown syntax. For full documentation, see
[John Gruber's site](https://daringfireball.net/projects/markdown/).

At the same time, there are two Markdown extensions enabled by default, `toc` (table of
contents) and `fenced_code`.

### Table of Contents

To generate a table of contents for the document, just type:

```plaintext
[TOC]
```

Table of contents at the top of this page is generated this way.


### Fenced code block

By default, if you want to display a code block in Markdown, you have to indent the text
with 4 spaces or one `<tab>`. This is not optimal, so there's another way with `fenced_code`
extension.

Just type in triple backticks like this:

```plaintext
 ```
 your code
 ```
```

Syntax highlighting (courtesy of `highlight.js`) is available. By default, language is
auto-detected. If you'd like to specity a known programming language, you can specify it
after the first set of backticks, like this:

```plaintext
 ```python
 import os

 something = os.getenv("something")
 print(something, "else")  # comment
 ```
```

This will produce the following output:

```python
import os

something = os.getenv("something")
print(something, "else")  # comment
```

If you'd like to disable highligting, just specify `plaintext` as a language:

```plaintext
 ```plaintext
 import os

 something = os.getenv("something")
 print(something, "else")
 ```
```


## Markdown helpers

Somethimes, you want to embed a calculated value into a page, like this:

```plaintext
{{ '{{' }} df["column"].sum() {{ '}}' }}
```

At the same time, you might want to apply some formatting to it, for example, make the
text bold:

```plaintext
__{{ '{{' }} df["column"].sum() {{ '}}' }}__
```

This is ugly, so to avoid this, there's a set of filters designed to help you format
calculated values.

### strong, em, big, small

```plaintext
- {{ '{{' }} 'strong' | strong {{ '}}' }}
- {{ '{{' }} 'em' | em {{ '}}' }}
- {{ '{{' }} 'big' | big {{ '}}' }}
- {{ '{{' }} 'small' | small {{ '}}' }}
```

Outputs this:

- {{ 'text' | strong }}
- {{ 'text' | em }}
- {{ 'text' | big }}
- {{ 'text' | small }}

### Small and muted

```plaintext
{{ '{{' }} 'Small and muted' | small_muted {{ '}}' }}
```

{{ 'Small and muted' | small_muted }}

### Wrapping text in parentheses

You can wrap a value in parentheses with `paren` filter:

```plaintext
{{ '{{' }} 'in parentheses' | paren {{ '}}' }}
```

{{ 'in parentheses' | paren }}

### Combining helper filters

Helper filters (and others) can be combined in an arbitrary way:

```plaintext
- {{ '{{' }} 'big and strong' | big | strong {{ '}}' }}
- {{ '{{' }} 'small and em' | small | em {{ '}}' }}
```

- {{ 'big and strong' | big | strong }}
- {{ 'small and em' | small | em }}

For entirely awesome results, combine this with a header:

```plaintext
#### {{ '{{' }} 'This header isn\'t supposed to be in TOC' {{ '}}' }} {{ '{{' }} 'it\'s and example' | paren | small_muted {{ '}}' }}
```

#### {{ 'This header isn\'t supposed to be in TOC'  }} {{ 'it\'s an example' | paren | small_muted }}


## Locale-aware formatting numbers and time

Formatting filters are just a wrapper around the [Babel package](http://babel.pocoo.org).
So if you have time, make yourself familiar with it too (it's great!).

By default, locale is taken from `locale` setting, but you can override it at any
particular invocation of filter.

### Formatting dates
