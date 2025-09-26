

**_Flagbit_** is an _open source_ feature flag library for Python with a simple goal: 
make it easy to turn features **on** and **off**, everywhere.

It’s inspired by [Django Admin](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/), simple to set up, batteries included,
and designed to give you a central place to manage things that otherwise get messy.

With **_Flagbit_** you get:

* a clean Python API for backend usage,
* an HTTP API so your frontend (or any service) can fetch flag states,
* and a flexible logic layer that keeps everything consistent across your stack.

Instead of scattering `if some_feature_enabled`: checks throughout your code,
you define flags once and consume them anywhere.

Key ideas:

* 🗄 Database agnostic: use any database you like for flag storage.
* 🎛 Centralized overrides: frontend or backend can override behavior safely.
* 🌍 API everywhere: expose flags over HTTP so any codebase, not just Python, can use them.
* 🔮 Future-ready: the API design paves the way for SDKs in other languages, so your whole system can share the same flag infrastructure.

The goal is a _full-stack feature flagging solution_ that feels natural in Python,
is easy to adopt today, and grows with you tomorrow.