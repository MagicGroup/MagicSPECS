%if 0%{?fedora} || 0%{?rhel} > 6
%global with_python3 1
%endif

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:          python-urwid
Version:       1.0.0
Release:       5%{?dist}
Summary:       Console user interface library

Group:         Development/Libraries
License:       LGPLv2+
URL:           http://excess.org/urwid/
Source0:       http://excess.org/urwid/urwid-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)
BuildRequires: python2-devel
BuildRequires: python-setuptools-devel
BuildRequires: python-twisted-core
BuildRequires: pygobject2

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: /usr/bin/2to3
%endif # if with_python3

%description
Urwid is a Python library for making text console applications.  It has
many features including fluid interface resizing, support for UTF-8 and
CJK encodings, standard and custom text layout modes, simple markup for
setting text attributes, and a powerful, dynamic list box that handles a
mix of widget types.  It is flexible, modular, and leaves the developer in
control.

%if 0%{?with_python3}
%package -n python3-urwid
Summary: Urwid console user interface library for Python 3
Group: Development/Languages

%description -n python3-urwid
Urwid is a Python library for making text console applications.  It has
many features including fluid interface resizing, support for UTF-8 and
CJK encodings, standard and custom text layout modes, simple markup for
setting text attributes, and a powerful, dynamic list box that handles a
mix of widget types.  It is flexible, modular, and leaves the developer in
control.

This package contains the mako module built for use with python3.
%endif # with_python3

%prep
%setup -q -n urwid-%{version}
find urwid -type f -name "*.py" -exec sed -i -e '/^#!\//, 1d' {} \;
find urwid -type f -name "*.py" -exec chmod 644 {} \;

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
#2to3 --no-diffs -w mako test
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python} setup.py install --skip-build --no-compile --root %{buildroot}
rm -f tmpl_tutorial.html
mkdir examples
cp -p *.py examples/
rm -f examples/test_urwid.py examples/docgen_*.py

%check
python setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG *.html examples
%{python_sitearch}/urwid
%{python_sitearch}/urwid-%{version}*.egg-info

%if 0%{?with_python3}
%files -n python3-urwid
%defattr(-,root,root,-)
%doc CHANGELOG *.html examples
%{python3_sitearch}/urwid
%{python3_sitearch}/urwid-%{version}*.egg-info
%endif

%changelog
* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1.0.0-5
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0.0-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Luke Macken <lmacken@redhat.com> - 1.0.0-2
- Add a python3-urwid subpackage (#746627)

* Wed Oct 19 2011 Luke Macken <lmacken@redhat.com> - 1.0.0
- Update to version 1.0.0
- Add python-setuptools-devel to the BuildRequires
- Run the test suite using the setup.py

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed May 19 2010 David Cantrell <dcantrell@redhat.com> - 0.9.9.1-1
- Initial package
