from codecs import open
import os

from setuptools import setup, find_packages


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*path.split('/'))
    return [req]


def _reqs(*f):
    return [
        _pip_requirement(r) for r in (
            strip_comments(l) for l in open(
            os.path.join(os.getcwd(), *f)).readlines()
        ) if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]


def get_requirements(*requirements_file):
    """Get the contents of a file listing the requirements"""
    lines = open(os.path.join(os.getcwd(), *requirements_file)).readlines()
    dependencies = []
    for line in lines:
        maybe_dep = line.strip()
        if maybe_dep.startswith('#'):
            # Skip pure comment lines
            continue
        if maybe_dep.startswith('git+'):
            # VCS reference for dev purposes, expect a trailing comment
            # with the normal requirement
            __, __, maybe_dep = maybe_dep.rpartition('#')
        else:
            # Ignore any trailing comment
            maybe_dep, __, __ = maybe_dep.partition('#')
        # Remove any whitespace and assume non-empty results are dependencies
        maybe_dep = maybe_dep.strip()
        if maybe_dep:
            dependencies.append(maybe_dep)
    return dependencies

setup(name='google_search_results_async',
      version='2.4.1b0',
      description='Scrape and search localized results from Google, Bing, Baidu, Yahoo, Yandex, Ebay, Homedepot, youtube at scale using SerpApi.com',
      url='https://github.com/serpapi/google-search-results-python',
      author='Matteo Senardi',
      author_email='pualien@gmail.com',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Natural Language :: English',
          'Topic :: Utilities',
      ],
      python_requires='>=3.5',
      zip_safe=False,
      include_package_data=True,
      license="MIT",
      packages=find_packages(exclude=['tests']),
      install_requires=get_requirements('requirements.txt'),
      keywords='scrape,serp,api,json,search,localized,rank,google,bing,baidu,yandex,yahoo,ebay,scale,datamining,training,machine,ml,youtube,naver,walmart,apple,store,app',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      )
