
# Django Simple Worker


#### Installation
```shell
pip install django-simple-worker
```

Add to installed apps:
```python
INSTALLED_APPS = [
    'simpleworker',
]
```

Add to your urls (optional):
```python
path('simpleworker/', include(('simpleworker.urls', 'simpleworker'), namespace='simpleworker')),
```

#### Usage
TODO
