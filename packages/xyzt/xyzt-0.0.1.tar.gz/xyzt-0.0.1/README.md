# xyzt: compute and plot time cost scaling for functions with numpy array input

I often implement functions on atom positions in terms of `Nx3` numpy arrays,
and need to compare speed of different implementations.
This small library is a thin wrapper over `timeit` for that purpose.

```python
xyzt.timethem(functions_to_check, nmin=10, nmax=1e5, number=1e5) -> (n, times)
xyzt.plot(n, times, labels=None)
```

```python
for fi in functions:
    for n in valid_range:
        generate random n-dimensional input vector
        timeit fi(v_rand)
```

## example: `scipy.spatial.distance.cdist+min` versus `scipy.spatial.cKDTree`
