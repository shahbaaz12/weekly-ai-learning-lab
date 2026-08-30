# Week 6 - System Design and Scaling

## Objective

Learn how a web application grows from one server into a distributed system, and
what each new layer in front of it actually solves.

## What I built

**Silicon Lanes** - an interactive lesson series that follows one request as the
architecture around it grows, with Docker containers standing in for the real
infrastructure at every step.

**https://shahbaaz12.github.io/silicon-lanes/**

## What it covers

1. Reverse proxies - putting something in front of the application server.
2. Load balancing - spreading traffic at L4 and at L7.
3. API gateways - one entry point for many services.
4. CDN and edge caching - serving a response closer to the user.
5. DNS, anycast, and BGP - how a request finds a machine at all.
6. High availability and failover - staying up when a machine does not.

## Where the code lives

This week is a hosted lesson series rather than a folder of scripts, so it lives
in its own repository. Open the link above to work through it.

## Key idea

Every layer is added to solve one specific problem. Reading the request path from
the browser inward is the fastest way to see which problem each one solves, and
which ones a small system does not need yet.
