# {{ icon }} Baguette BI

## Business Intelligence as Code

Baguette BI is a code-first Business Intelligence framework. It allows data teams to
define their main deliverable with code, thus making it version-controlled, easily
reviewable, testable and reproducible.

For a set of problems that it tries to solve and what it does differently than other BI
tools, see {{ link("motivation.md", "Motivation") }}.

For a starter on all the moving parts and how they work together, take a look at
{{ link("concepts.md", "Concepts") }}.

For an non-exhaustive list of what that can be done in Baguette (because it's
insanely flexible), consult with {{ link("reference.md", "Reference") }}.

There's a set of examples
(loosely based on [Altair Examples](https://altair-viz.github.io/gallery/)) designed
to showcase what's possible in Baguette BI and how it's supposed to be used.

## Install and run it yourself

To run the docs on your local machine, first install Baguette with `pip`:

`$ pip install baguette_bi`

And then run the docs command:

`$ baguette docs`

## Acknowledgements

Baguette BI wouldn't exist without Artemiy [@s1yrat](https://github.com/s1yrat) and his
insightful feedback, ideas and, of course, code contributions.

The credit for the original idea that BI should look like a set of hyperlinked pages,
not dashboards, goes to Adam [@mcrascal](https://github.com/mcrascal). Check out his project,
[Evidence](https://www.evidence.dev/), which is similar, but also different, and has much
better design 😅.
