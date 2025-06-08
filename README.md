```
uv venv && | uv pip install --no-cache-dir -e .
```

```
podman build -t search-subbrands .
podman run --rm -p 8000:8000 --env-file=.env search-subbrands
```