# Last updated for version 3.18.0
%define glib2_version                  2.38.0
%define gobject_introspection_version  1.39.0
%define python2_version                2.7

%global with_python3 1
%define python3_version                3.1

%global with_check 0

Name:           pygobject3
Version:	3.19.2
Release:	2%{?dist}
Summary:        Python bindings for GObject Introspection

License:        LGPLv2+ and MIT
URL:            https://live.gnome.org/PyGObject
Source0:        http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.18/pygobject-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires:  python2-devel >= %{python2_version}
%if 0%{?with_python3}
BuildRequires:  python3-devel >= %{python3_version}
BuildRequires:  python3-cairo-devel
%endif # if with_python3

BuildRequires:  cairo-gobject-devel
BuildRequires:  pycairo-devel

# Required by the upstream selftest suite:
%if %{with_check}
# Temporarily disabled pyflakes tests to avoid the build failing due to too new
# pyflakes 0.7.2 in F19
# https://bugzilla.gnome.org/show_bug.cgi?id=701009
#BuildRequires:  pyflakes
BuildRequires:  python-pep8
## for the Gdk and Gtk typelibs, used during the test suite:
BuildRequires:  gtk3
## for xvfb-run:
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  dejavu-sans-fonts
BuildRequires:  dejavu-sans-mono-fonts
BuildRequires:  dejavu-serif-fonts
## for dbus-launch, used by test_gdbus:
BuildRequires:  dbus-x11
%endif # with_check

%description
The %{name} package provides a convenient wrapper for the GObject library
for use in Python programs.

%package     -n python-gobject
Summary:        Python 2 bindings for GObject Introspection
Requires:       python-gobject-base%{?_isa} = %{version}-%{release}
# The cairo override module depends on this
Requires:       pycairo%{?_isa}

Obsoletes:      %{name} < 3.17.90-2
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}%{?_isa} = %{version}-%{release}

%description -n python-gobject
The python-gobject package provides a convenient wrapper for the GObject
library and and other libraries that are compatible with GObject Introspection,
for use in Python 2 programs.

%package     -n python-gobject-base
Summary:        Python 2 bindings for GObject Introspection base package
Requires:       gobject-introspection%{?_isa} >= %{gobject_introspection_version}

Obsoletes:      %{name}-base < 3.17.90-2
Provides:       %{name}-base = %{version}-%{release}
Provides:       %{name}-base%{?_isa} = %{version}-%{release}

%description -n python-gobject-base
This package provides the non-cairo specific bits of the GObject Introspection
library.

%if 0%{?with_python3}
%package     -n python3-gobject
Summary:        Python 3 bindings for GObject Introspection
Requires:       python3-gobject-base%{?_isa} = %{version}-%{release}
# The cairo override module depends on this
Requires:       python3-cairo%{?_isa}

%description -n python3-gobject
The python3-gobject package provides a convenient wrapper for the GObject 
library and and other libraries that are compatible with GObject Introspection, 
for use in Python 3 programs.

%package     -n python3-gobject-base
Summary:        Python 3 bindings for GObject Introspection base package
Requires:       gobject-introspection%{?_isa} >= %{gobject_introspection_version}

%description -n python3-gobject-base
This package provides the non-cairo specific bits of the GObject Introspection
library.

%endif # with_python3

%package        devel
Summary:        Development files for embedding PyGObject introspection support
Requires:       python-gobject%{?_isa} = %{version}-%{release}
Requires:       python3-gobject%{?_isa} = %{version}-%{release}
Requires:       gobject-introspection-devel%{?_isa}

%description    devel
This package contains files required to embed PyGObject

%prep
%setup -q -n pygobject-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
PYTHON=%{__python} 
export PYTHON
%configure
make %{?_smp_mflags} V=1

%if 0%{?with_python3}
pushd %{py3dir}
PYTHON=%{__python3}
export PYTHON
%configure
make %{?_smp_mflags} V=1
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
PYTHON=%{__python3}
export PYTHON
%make_install
popd

%endif # with_python3

%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete

# Don't include makefiles in the installed docs, in order to avoid creating
# multilib conflicts
rm -rf _docs
mkdir _docs
cp -a examples _docs
rm _docs/examples/Makefile*

%check
%if %{with_check}
# Run the selftests under a temporary xvfb X server (so that they can
# initialize Gdk etc):

# FIXME: disabled for python3
# Currently this fails with python3 with:
#  File "/builddir/build/BUILD/python3-pygobject3-3.3.4-4.fc19/gi/__init__.py", line 23, in <module>
#    from ._gi import _API, Repository
#ValueError: level must be >= 0
# Reported upstream as http://bugs.python.org/issue15610
%if 0
pushd %{py3dir}
PYTHON=%{__python3}
export PYTHON
xvfb-run make DESTDIR=$RPM_BUILD_ROOT check V=1
popd
%endif # with_python3

xvfb-run make DESTDIR=$RPM_BUILD_ROOT check V=1

%endif # with_check

%files -n python-gobject
%{python_sitearch}/gi/_gi_cairo.so

%files -n python-gobject-base
%license COPYING
%doc AUTHORS NEWS README
%dir %{python_sitearch}/gi
%{python_sitearch}/gi/*
%exclude %{python_sitearch}/gi/_gi_cairo.so
%{python_sitearch}/pygobject-*.egg-info
%{python_sitearch}/pygtkcompat/

%if 0%{?with_python3}
%files -n python3-gobject
%{python3_sitearch}/gi/_gi_cairo*.so

%files -n python3-gobject-base
%license COPYING
%doc AUTHORS NEWS README
%dir %{python3_sitearch}/gi
%{python3_sitearch}/gi/*
%exclude %{python3_sitearch}/gi/_gi_cairo*.so
%{python3_sitearch}/pygobject-*.egg-info
%{python3_sitearch}/pygtkcompat/
%endif # with_python3

%files devel
%doc _docs/*
%dir %{_includedir}/pygobject-3.0/
%{_includedir}/pygobject-3.0/pygobject.h
%{_libdir}/pkgconfig/pygobject-3.0.pc

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.19.2-2
- 更新到 3.19.2

* Tue Sep 29 2015 Liu Di <liudidi@gmail.com> - 3.18.0-1
- 更新到 3.18.0

* Fri Aug 14 2015 Liu Di <liudidi@gmail.com> - 3.17.1-1
- 更新到 3.17.1

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 3.11.90-3
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 3.11.90-2
- 为 Magic 3.0 重建

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Mon Nov 18 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug  9 2013 Daniel Drake <dsd@laptop.org> - 3.9.5-1
- Update to 3.9.5


