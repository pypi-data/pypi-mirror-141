from setuptools import setup

name = "types-cachetools"
description = "Typing stubs for cachetools"
long_description = '''
## Typing stubs for cachetools

This is a PEP 561 type stub package for the `cachetools` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `cachetools`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/cachetools. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `77e5a2d4680341f20b351bc7d5554a8fa31ec1b6`.
'''.lstrip()

setup(name=name,
      version="4.2.10",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/cachetools.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['cachetools-stubs'],
      package_data={'cachetools-stubs': ['__init__.pyi', 'cache.pyi', 'fifo.pyi', 'func.pyi', 'keys.pyi', 'lfu.pyi', 'lru.pyi', 'mru.pyi', 'rr.pyi', 'ttl.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
