%global with_python3 1

Name:           python-kitchen
Version:        1.2.1
Release:        4%{?dist}
Summary:        Small, useful pieces of code to make python coding easier
Summary(zh_CN.UTF-8): 使 Python 编程更容易的小巧实用的代码

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        LGPLv2+
URL:            https://pypi.python.org/pypi/kitchen/
Source0:        https://fedorahosted.org/releases/k/i/kitchen/kitchen-%{version}.tar.gz

# http://git.io/8KLw1Q
Patch0:         python-kitchen-expose-base64-py34.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-nose
# For the subprocess test
BuildRequires:  python-test

# sphinx needs to be more recent to build the html docs
BuildRequires: python-sphinx

# At present, chardet isn't present in epel but it's a soft dep
BuildRequires: python-chardet
Requires: python-chardet

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-test
BuildRequires:  python3-sphinx
BuildRequires:  python3-chardet
%endif

%description
kitchen includes functions to make gettext easier to use, handling unicode
text easier (conversion with bytes, outputting xml, and calculating how many
columns a string takes), and compatibility modules for writing code that uses
python-2.7 modules but needs to run on python-2.3.

%description -l zh_CN.UTF-8
使 Python 编程更容易的小巧实用的代码。

%package doc
Summary:        API documentation for the Kitchen python2 module
Summary(zh_CN.UTF-8): %{name} 的文档
# Currently discussing guidelines about doc subpackages Requiring the main package:
# https://lists.fedoraproject.org/pipermail/packaging/2013-June/009191.html
#Requires: %{name} = %{version}-%{release}
%description doc
kitchen includes functions to make gettext easier to use, handling unicode
text easier (conversion with bytes, outputting xml, and calculating how many
columns a string takes), and compatibility modules for writing code that uses
python-2.7 modules but needs to run on python-2.3.

This package contains the API documenation for programming with the
python-2 version of the kitchen library.

%description doc -l zh_CN.UTF-8
%{name} 的文档。


%if 0%{?with_python3}
%package -n python3-kitchen
Summary:    Small, useful pieces of code to make python 3 coding easier
Summary(zh_CN.UTF-8): 使 Python3 编程更容易的小巧实用的代码
Group:      Development/Languages
Group(zh_CN.UTF-8): 开发/语言

Requires:   python3
Requires:   python3-chardet

%description -n python3-kitchen
kitchen includes functions to make gettext easier to use, handling unicode
text easier (conversion with bytes, outputting xml, and calculating how many
columns a string takes).

This is the python3 version of the kitchen module.

%description -n python3-kitchen -l zh_CN.UTF-8
使 Python3 编程更容易的小巧实用的代码。

%package -n python3-kitchen-doc
Summary:    API documentation for the Kitchen python3 module
Summary(zh_CN.UTF-8): python3-kitchen 的文档
#Requires: %{name} = %{version}-%{release}
%description -n python3-kitchen-doc
kitchen includes functions to make gettext easier to use, handling unicode
text easier (conversion with bytes, outputting xml, and calculating how many
columns a string takes).

This package contains the API documenation for programming with the
python-3 version of the kitchen library.
%description -n python3-kitchen-doc -l zh_CN.UTF-8
python3-kitchen 的文档。
%endif


%prep
%setup -q -n kitchen-%{version}

%patch0 -p1

# Remove bundled egg info, if any.
rm -rf *.egg*

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

# Build docs
%if 0%{?fedora} || 0%{?rhel} >= 6

sphinx-build kitchen2/docs/ build/sphinx/html
cp -pr build/sphinx/html .
rm -rf html/.buildinfo

%if 0%{?with_python3}
pushd %{py3dir}
sphinx-build-3 kitchen3/docs/ build/sphinx/html
cp -pr build/sphinx/html .
rm -rf html/.buildinfo
popd
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif
magic_rpm_clean.sh

%check
# In current mock, the PATH isn't being reset.  This causes failures in some
# subprocess tests as a check tests /root/bin/PROGRAM and fails with Permission
# Denied instead of File Not Found.  reseting the PATH works around this.
PATH=/bin:/usr/bin
PYTHONPATH=.:kitchen2/ nosetests kitchen2/tests/

%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=.:kitchen3/ nosetests-%{python3_version} kitchen3/tests/
popd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.rst NEWS.rst COPYING COPYING.LESSER
%{python2_sitelib}/*

%files doc
%doc COPYING COPYING.LESSER kitchen2/docs/*
%if 0%{?fedora} || 0%{?rhel} >= 6
%doc html
%endif

%if 0%{?with_python3}
%files -n python3-kitchen
%defattr(-,root,root,-)
%doc README.rst NEWS.rst COPYING COPYING.LESSER
%{python3_sitelib}/*

%files -n python3-kitchen-doc
%doc COPYING COPYING.LESSER kitchen3/docs/*
%if 0%{?fedora} || 0%{?rhel} >= 6
%doc html
%endif
%endif

%changelog
* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 1.2.1-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 02 2014 Ralph Bean <rbean@redhat.com> - 1.2.1-2
- Include patch to get py34 tests working for rawhide.

* Tue Dec 02 2014 Ralph Bean <rbean@redhat.com> - 1.2.1-1
- Latest upstream, now with python3 support!
- Added python3 subpackages.
- Remove use of build_sphinx.
- Rename README and NEWS with new .rst extension.
- Modernized python2 macros.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-6
- Move the html docs to the docs package

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 25 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.1-4
- Move the api documentation into its own subpackage

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.1-1
- Bugfix for using easy_gettext_setup or get_translation_object with the
  default localedirs

* Thu Jan 12 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 final

* Thu Apr 14 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.0-1
- Upstream update to 1.0 final

* Sun Feb 20 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.4-1
- Upstream update 0.2.4
  - Changes i18n.easy_gettext_setup() to return lgettext functions when
    byte strings are requested.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 5 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.3-2
- Upstream respin of the tarball

* Wed Jan 5 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.3-1
- Upstream update to 0.2.3
- Fixes https://bugzilla.redhat.com/show_bug.cgi?id=667433

* Mon Jan 3 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.2-1
- Upstream update 0.2.2
  - Adds exception to message functions
- Build html docs

* Thu Sep 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.1-0.1.a1
- Update to upstream 0.2.1a1 release.
- Fixes build on python-2.7, adds iterutils module, optimizes some functions,
  increases documentation

* Thu Jul 29 2010 Dennis Gilmore <dennis@ausil.us> - 0.2-0.1.a2
- propoerlly version accrding to pre-release guidelines
- run tests
- update to 0.2a2
- include COPYING.LESSER and docs dir

* Thu Jul 29 2010 Dennis Gilmore <dennis@ausil.us> - 0.2a1-2
- rename to python-kitchen

* Thu Jul 29 2010 Dennis Gilmore <dennis@ausil.us> - 0.2a1-1
- update to 0.2a1

* Thu Jul 15 2010 Dennis Gilmore <dennis@ausil.us> - 0.1a3-3
- fix spelling mistake in description

* Thu Jul 15 2010 Dennis Gilmore <dennis@ausil.us> - 0.1a3-2
- add documentaion
- fix description

* Thu Jul 15 2010 Dennis Gilmore <dennis@ausil.us> - 0.1a3-1
- initial package
