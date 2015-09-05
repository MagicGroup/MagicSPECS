%global with_python3 1

# -doc package generation
# EL6: python-sphinx is not new enough
%global with_docpkg 1

%global srcname feedparser
%global tag     %{nil}

Name:           python-feedparser
Version:	5.2.1
Release:	1%{?dist}
Summary:        Parse RSS and Atom feeds in Python
Summary(zh_CN.UTF-8): 在 Python 中解析 RSS 和 Atom 种子

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        BSD
URL:            https://github.com/kurtmckee/feedparser
Source0:        https://pypi.python.org/packages/source/f/%{srcname}/%{srcname}-%{version}%{tag}.tar.bz2
# only for EPEL5
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

# optional import at run-time, but is likely installed because other
# python module packages depend on it, too
# no failing tests on 2013-03-09 with python-chardet-2.0.1
BuildRequires: python-chardet
Requires: python-chardet

## TODO: Decide on these, also with regard to explicit "Requires".
## Optional imports at run-time and influence the test-suite, too,
## and causes additional tests to fail.
#
#BuildRequires:  python-BeautifulSoup
#  usage removed in > 5.1.3
#
## the preferred XML parser
#BuildRequires:  libxml2-python

## TODO: python3-chardet BR and Req
# fixes included in > 5.1.3

%description
Universal Feed Parser is a Python module for downloading and parsing 
syndicated feeds. It can handle RSS 0.90, Netscape RSS 0.91, 
Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94, RSS 1.0, RSS 2.0, 
Atom 0.3, Atom 1.0, and CDF feeds. It also parses several popular extension 
modules, including Dublin Core and Apple's iTunes extensions.

%description -l zh_CN.UTF-8
在 Python 中解析 RSS 和 Atom 种子。

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Parse RSS and Atom feeds in Python
Summary(zh_CN.UTF-8): 在 Python 中解析 RSS 和 Atom 种子
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%description -n python3-%{srcname}
Universal Feed Parser is a Python module for downloading and parsing 
syndicated feeds. It can handle RSS 0.90, Netscape RSS 0.91, 
Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94, RSS 1.0, RSS 2.0, 
Atom 0.3, Atom 1.0, and CDF feeds. It also parses several popular extension 
modules, including Dublin Core and Apple's iTunes extensions.
%description -n python3-%{srcname} -l zh_CN.UTF-8
在 Python 中解析 RSS 和 Atom 种子。
%endif

%if 0%{?with_docpkg}
%package doc
BuildRequires: python-sphinx
BuildArch: noarch
Summary: Documentation for the Python feedparser
Summary(zh_CN.UTF-8): %{name} 的文档

%description doc
This documentation describes the behavior of Universal Feed Parser %{version}. 

The documentation is also included i source form (Sphinx ReST).

%description doc -l zh_CN.UTF-8
%{name} 的文档。
%endif


%prep
%setup -q -n %{srcname}-%{version}
%if 0%{?with_python3}
cp -a . %{py3dir}
%endif

find -type f -exec sed -i 's/\r//' {} ';'
find -type f -exec chmod 0644 {} ';'


%build
%{__python2} setup.py build

%if 0%{?with_docpkg}
# build documentation
rm -rf __tmp_docs ; mkdir __tmp_docs
sphinx-build -b html -d __tmp_docs/ docs/ __tmp_docs/html/
%endif

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
# only for EPEL5
rm -rf %{buildroot}

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif
magic_rpm_clean.sh

%check
pushd feedparser
PYTHONPATH=%{buildroot}%{python2_sitelib} %{__python2} feedparsertest.py || :
popd
%if 0%{?with_python3}
pushd %{py3dir}/feedparser
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} feedparsertest.py || :
popd
%endif


# only for EPEL5
%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.rst NEWS
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc LICENSE README.rst NEWS
%{python3_sitelib}/*
%endif

%if 0%{?with_docpkg}
%files doc
%doc LICENSE __tmp_docs/html/
# the original Sphinx ReST tree
%doc docs
%endif

%changelog
* Thu Sep 03 2015 Liu Di <liudidi@gmail.com> - 5.2.1-1
- 更新到 5.2.1

* Mon Jun 29 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 5.2.0-1
- Upstream 5.2.0
- Cleanup spec

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 5.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.3-4
- Conditionalize the -doc package, because python-sphinx is not new
  enough for EL6.

* Sun May 26 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.3-3
- BR python-sphinx and build pregenerated HTML documentation to be
  included in a python-feedparser-doc package together with the sources
  for the documentation

* Sat Mar  9 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.3-2
- Add BuildRequires/Requires python-chardet because if it's installed
  as a dependency of other Python module packages, it would be imported
  and used anyway, and it doesn't make any tests fail.

* Sat Mar  9 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.3-1
- Update to 5.1.3 (50k diff).
- Patch test-suite minimally for python3 to show that it fails early.
- Fix file permissions and line delimiters at end of %%prep section.
- Fix python3 sitelib path in %%check section.

* Fri Mar  8 2013 Michael Schwendt <mschwendt@fedoraproject.org>
- Update URL to new location at Google code (#880138).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 5.1.2-5
- remove rhel logic from with_python3 conditional (RHBZ #902896)

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 5.1.2-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.2-2
- Also package NEWS files as documentation.
- 5.1.2 fixes CVE-2012-2921
  (DoS via memory consumption processing ENTITY declarations).

* Tue May 22 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 5.1.2-1
- Update to 5.1.2 and its security fix (#787401).
- Ignore testsuite results for now (#787401).
- Set PYTHONPATH in %%check section to include files in %%buildroot.
- Drop CFLAGS usage from spec file, because this is Python.

* Sat Feb  4 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 5.1-1
- upstream 5.1 (#787401)
- spec cleanup
- tests disabled
- python3 support

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 05 2011 Luke Macken <lmacken@redhat.com> - 5.0.1-1
- Latest upstream release
- Remove feedparser_utf8_decoding.patch
- Remove democracynow_feedparser_fix.patch
- Run the test suite

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Dec 14 2009 Haïkel Guémar <karlthered@gmail.com> - 4.1-11
- rebuild for Fedora 13

* Fri Aug 07 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-10
- Apply patch for title munging issue (#491373)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 04 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-8
- Fix source URL (moved to googlecode).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 27 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-6
- Patch for a utf8 decoding issue (#477024)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.1-5
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.1-4
- fix license tag

* Thu Jun 28 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-3
- Ghostbusting (#205413).
- Remove manual python-abi Requires.
- Appease rpmlint.

* Sat Dec 23 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 4.1-2
- Rebuild for new Python.

* Wed Jan 11 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.1-1
- Version 4.1

* Sat Jan 07 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.0.2-2
- Set sane permissions on doc files.

* Wed Jan 04 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 4.0.2-1
- Initial build.
