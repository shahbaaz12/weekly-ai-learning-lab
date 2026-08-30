# Week 7 - Scaling Databases

## Objective

Learn what actually makes a database slow, and how to choose the right fix -
from an index to a shard - by measuring first instead of guessing.

## What I built

**Dungeons and Databases: Split the Realm** - a lesson series that starts inside
a single database and works outward, so a scaling decision is only made once the
problem it solves is visible.

**https://shahbaaz12.github.io/dungeons-and-databases/**

## What it covers

1. Database internals - buffer pools, pages, and disk reads.
2. Indexing - what a B-tree is and when it stops helping.
3. Write-ahead logging - how a database survives a crash.
4. Replication - copying data to more than one machine.
5. Partitioning and sharding - splitting a table by rows.
6. Routing and consistency - finding the right shard, and what it costs.

## Where the code lives

This week is a hosted lesson series rather than a folder of scripts, so it lives
in its own repository. Open the link above to work through it.

## Key idea

Measure before splitting. Most slow queries are an indexing or access-pattern
problem, and sharding a database that was never diagnosed adds routing and
consistency work without removing the original bottleneck.
