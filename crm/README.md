# CRM Celery and Celery Beat Setup

This document explains how to set up and run the Celery task for generating weekly CRM reports, scheduled with Celery Beat.

---

## Prerequisites

- Redis server installed and running on `redis://localhost:6379/0`
- Python dependencies installed (`celery`, `django-celery-beat`, etc.)

---

## Installation and Setup

1. **Install Redis**

On Ubuntu:

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
