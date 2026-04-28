# portfolio-api

A unified Flask API powering [czvck.com](https://work.czvck.com) — 
self-hosted on a Raspberry Pi 400 and served via nginx.

## Overview

Currently handles contact form submissions, routing messages securely 
to my personal email via the Resend API. Built as the foundation for 
all backend services across my portfolio projects — additional endpoints 
will be added as the portfolio grows.

## Features

- **Rate limiting** — 200 requests/day, 50/hour globally, 
  with a tighter 5/hour limit on the contact endpoint
- **Honeypot bot protection** — invisible form field silently 
  filters automated submissions without revealing detection
- **Secure credential management** — API keys stored in 
  environment variables, never in source code
- **Reverse proxy** — served through nginx with HTTPS, 
  proxied from port 5051

## Tech Stack

- Python / Flask
- Resend API
- nginx
- systemd (process management)
- Raspberry Pi (self-hosted)

## Author Notes

This is intentionally designed as a unified API rather than 
a one-off script. The goal is a single backend that eventually 
serves all portfolio projects — network monitoring, MTG price 
tracking, and whatever comes next.
