%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%if 0%{?rhel} == 5
%global with_python26 1
%endif

%if 0%{?with_python26}
%global __python26 %{_bindir}/python2.6
%global py26dir %{_builddir}/python26-%{name}-%{version}-%{release}
%{!?python26_sitelib: %global python26_sitelib %(%{__python26} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
# Update rpm byte compilation script so that we get the modules compiled by the
# correct inerpreter
%global __os_install_post %__multiple_python_os_install_post
%endif


%global upstream_name Pygments

Name:           python-pygments
Version:        1.4
Release:        8%{?dist}
Summary:        Syntax highlighting engine written in Python

Group:          Development/Libraries
License:        BSD
URL:            http://pygments.org/
Source0:        http://pypi.python.org/packages/source/P/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel >= 2.4, python-setuptools, python-nose
%if 0%{?with_python3}
BuildRequires:  python3-devel, python3-setuptools
%if 0%{?fedora} >= 15
BuildRequires: python3-nose
%endif
%endif # if with_python3
Requires:       python-setuptools, python-imaging
%if 0%{?with_python26}
BuildRequires:  python26-devel, python26-distribute
%endif


%description
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!

%if 0%{?with_python3}
%package -n python3-pygments
Summary:        Syntax highlighting engine written in Python 3
Group:          Development/Libraries
Requires:       python3-setuptools

%description -n python3-pygments
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!
%endif # if with_python3

%if 0%{?with_python26}
%package -n python26-pygments
Summary:        A syntax highlighting engine written in Python 2.6
Group:          Development/Libraries
Requires:       python26-distribute
Requires:       python26-imaging
Requires:       python(abi) = 2.6

%description -n python26-pygments
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:
%endif #end of python2.6


%prep
%setup -q -n Pygments-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%if 0%{?with_python26}
rm -rf %{py26dir}
cp -a . %{py26dir}
find %{py26dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python26}|'
%endif # with_python26


%build
%{__python} setup.py build
%{__sed} -i 's/\r//' LICENSE

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%if 0%{?with_python26}
pushd %{py26dir}
%{__python26} setup.py build
popd
%endif # with_python26


%install
rm -rf $RPM_BUILD_ROOT

# Run the Python 3 build first so that the Python 2 version of
# /usr/bin/pygmentize "wins":
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

# Run the Python 2.6 build first so that the Python 2 version of
# /usr/bin/pygmentize "wins":
%if 0%{?with_python26}
pushd %{py26dir}
%{__python26} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python26

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
pushd docs
install -d %{buildroot}%{_mandir}/man1
mv pygmentize.1 $RPM_BUILD_ROOT%{_mandir}/man1/pygmentize.1
mv build html
mv src reST
popd
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%check
make test

%if 0%{?with_python26}
pushd %{py26dir}
# There's currently no python26-nose
#make test
popd
%endif # with_python26

# python3-nose is available from f15 on
%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?fedora} >= 15
make test
%endif
popd
%endif # with_python3

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES docs/html docs/reST LICENSE TODO
# For noarch packages: sitelib
%{python_sitelib}/*
%{_bindir}/pygmentize
%lang(en) %{_mandir}/man1/pygmentize.1.gz

%if 0%{?with_python3}
%files -n python3-pygments
%defattr(-,root,root,-)
%doc AUTHORS CHANGES docs/html docs/reST LICENSE TODO
%{python3_sitelib}/*
%endif # with_python3

%if 0%{?with_python26}
%files -n python26-pygments
%defattr(-,root,root,-)
%doc AUTHORS CHANGES docs/ LICENSE TODO
%{python26_sitelib}/*
%endif # with_python26


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.4-8
- 为 Magic 3.0 重建

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.4-7
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 1.4-6
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-3
- Really enable the python3 unittests.
- Fix python26 byte compilation (thanks to Jeffrey Ness)

* Sat Sep 10 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-2
- Fix python main package having dependencies for the python2.6 subpackage
- Fix places that used the default python instead of python26
- Attempt to make byte compilation more robust in case we add python3 to EPEL5
- Run unittests on python3 in F15+

* Fri Jun 24 2011 Steve Milner <smilner@fedoraproject.org> - 1.4-1
- update for upstream release
- Add python2.6 support done by Steve Traylen <steve.traylen@cern.ch>. BZ#662755.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-7
- update to most recent python guidelines
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu May  6 2010 Gareth Armstrong <gareth.armstrong@hp.com> - 1.3.1-5
- Enforce that Pygments requires Python 2.4 or later via an explicit BR
- Minor tweaks to spec file
- Deliver html and reST doc files to specifically named directories
- Align description with that of http://pygments.org/
- Add %%check section for Python2 and add BR on python-nose

* Fri Apr 23 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-4
- switched with_python3 back to 1

* Fri Apr 23 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.1-3
- add python3 subpackage (BZ#537244), ignoring soft-dep on imaging for now

* Sat Apr 13 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-2
- added python-imaging as a dependency per BZ#581663.

* Sat Mar  6 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-1
- Updated for release.

* Tue Sep 29 2009 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.1.1-1
- Updated for release.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.0-3
- Updated for release.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0-2
- Rebuild for Python 2.6

* Fri Nov 27 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.0-1
- Updated for upstream 1.0.

* Sun Sep 14 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.11.1-1
- Updated for upstream 0.11.

* Mon Jul 21 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.10-1
- Updated for upstream 0.10.

* Thu Nov 29 2007 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.9-2
- Added python-setuptools as a Requires per bz#403601.

* Mon Nov 12 2007 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.9-1
- Updated for upstream 0.9.

* Thu Aug 17 2007 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.8.1-2
- Removed the dos2unix build dependency.

* Thu Jun 28 2007 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.8.1-1
- Initial packaging for Fedora.
