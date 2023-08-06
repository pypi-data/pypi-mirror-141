===================
Django Web Analysis
===================

Django analytics is an app that can help you with a little analysis like who viewed what, when.

Quick start
-----------

1. Add "analyse" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'analyse',
    ]


2. Import the "ObjectViewedMixin" class like this::

    from analyse.mixins import ObjectViewedMixin



3. Then add the imported class any class based detail view like this::

    class BlogDetail(DetailView, ObjectViewedMixin):
        ...

You can view the data from your admin panel and you can also pull and use information from your code base.