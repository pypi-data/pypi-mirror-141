=========
 Changes
=========

1.1.0 (2022-03-03)
==================

- Fix handling the case where the project name is a namespace
  (``icrs.releaser``), but the source directory on disk doesn't
  include the namespace (``src/releaser``). This is a legacy case,
  supported for projects that are transitioning to a standard layout.


1.0.1 (2022-02-25)
==================

- Add the 'recommended' extra for installing the same things that
  ``zest.releaser[recommended]`` does.


1.0.0 (2022-02-25)
==================

- Initial PyPI release.
