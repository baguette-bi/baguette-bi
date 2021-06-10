{{ link("index.md", "👈 Index") }}

# 🤔 Baguette BI concepts

[TOC]

## 🪐 Project

A project in Baguette BI is what your team will work on. It's a set of files defining
what you want to put on your server. You give Baguette your project, and it will run
the web server where users can view what you made. If you want to make changes to your
project, you change the code and then run the server again.

A project is a Python package. Here's an example of such a structure.

```plaintext
my_project
├── __init__.py
├── charts
│   └── __init__.py
├── connections.py
├── datasets.py
└── pages
    └── index.md
```

You can create this simple scaffold by running `baguette new my_project` command.

There's also a special `pages` directory that contains a set of Markdown files templated
with Jinja2.

## 📑 Pages

At the first glance, Baguette BI looks like a wiki. In some sense, it is. Pages are what
your users will interact with. You build pages with Markdown, templated with Jinja2.

## Connections and Datasets

### Metrics

## Charts

### Tags

## Users and Permissions
