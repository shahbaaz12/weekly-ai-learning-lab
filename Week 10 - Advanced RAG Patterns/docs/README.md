# Week 10 documents

The sample data every project in this week reads from. It is all made up:
the fables are public-domain retellings, and Nexa is not a real company.

## Structure

```text
docs/
├── smallStories/                        one PDF per fable            -> 01 - Conversational RAG
├── products/                            one PDF per Nexa product     -> 02 - Hybrid RAG
│   └── combined/combinedDoc.pdf         the same ten guides in one file
├── products2/
│   ├── Hierarchical_Product_Catalog.json   the catalog                -> 03 - Hierarchical RAG
│   ├── Hierarchical_Product_Catalog.pdf    the same catalog as a PDF
│   └── Hierarchical_RAG_Validation_Questions.json   78 test questions
├── Classic_Fables_Collection.pdf        all ten fables in one file
├── Product_Knowledge_Base.pdf           all ten Nexa guides in one file
└── Pro_Series_Product_Guide.pdf         six Nexa Pro products, a separate line
```

Each project's index script reads only its own folder, and only that folder's
top level. The combined and collection PDFs are there for reading, not
indexing. Indexing them alongside the single files would store every chunk
twice.

## smallStories

Ten one-page fables, each as its own PDF. Each fable has a clear cast, so
follow-up questions like "is *he* lazy?" have a definite answer once the
conversation says which story is being discussed.

## products

Ten one-page support guides, `NEX-1001` to `NEX-1010`, for a line of Nexa
smart-home devices: a hub, an air sensor, a bulb, a doorbell camera, a coffee
maker, a power strip, a thermostat, a robot vacuum, a lock, and a leak sensor.
Every guide has the same sections, and every guide has its own error codes such
as `E922`. Those codes are the reason the hybrid project exists: they are rare
exact tokens that vector search alone misses.

## products2

`Hierarchical_Product_Catalog.json` holds twenty products with this shape:

```text
Category                        4
└── Subcategory                 10
    └── Product                 20   id, name, manufacturer, price, description,
        │                            specifications, quick start, usage, error codes
        └── Variant             26   id, name, price, description
```

Every product carries `category` and `subcategory`, and every variant lives
inside its product, so the hierarchy is already in the data. The project turns
each level into its own documents rather than flattening the whole thing.

`Hierarchical_RAG_Validation_Questions.json` is a test set for that project.
Each of the 78 entries has a question, an expected answer, the product or
subcategory the answer should come from, and a test type:

| Test type | Count | What it checks |
|---|---|---|
| Local product lookup | 20 | One product's own fields |
| Leaf / error-code lookup | 20 | One error code on one product |
| Variant lookup | 13 | One variant, below the product level |
| Subcategory aggregation | 10 | Everything under one subcategory |
| Missing-child test | 7 | A variant or code that does not exist |
| Category aggregation | 4 | Everything under one top-level category |
| Cross-category, global, ambiguity, negative | 4 | One each |

The first three types should route to DETAIL and the aggregation types to
SUMMARY, which makes the file a ready-made check for the router.

## Pro_Series_Product_Guide

Six professional-line products, `NEX-P2001` to `NEX-P2006`, in one PDF. None
of the three projects index it. It is a separate product line, useful for
testing what a retriever does with a question about a product it has never
seen.
