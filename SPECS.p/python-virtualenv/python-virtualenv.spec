# sitelib for noarch packages
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python2_version: %global python2_version %(%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])")}
%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-virtualenv
Version:        13.1.2
Release:        1%{?dist}
Summary:        Tool to create isolated Python environments

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/virtualenv
Source0:        http://pypi.python.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

%if 0%{?fedora}
BuildRequires:  python-sphinx
%endif

%if 0%{?with_python3}
BuildRequires:  python3-devel

%if 0%{?fedora}
BuildRequires:  python3-sphinx
%endif

%endif # with_python3

Requires:       python-setuptools
Requires:       python2-devel

%description
virtualenv is a tool to create isolated Python environments. virtualenv
is a successor to workingenv, and an extension of virtual-python. It is
written by Ian Bicking, and sponsored by the Open Planning Project. It is
licensed under an MIT-style permissive license.

%if 0%{?with_python3}
%package -n     python3-virtualenv
Summary:        Tool to create isolated Python environments

Requires:       python3-setuptools
Requires:       python3-devel

%description -n python3-virtualenv
virtualenv is a tool to create isolated Python environments. virtualenv
is a successor to workingenv, and an extension of virtual-python. It is
written by Ian Bicking, and sponsored by the Open Planning Project. It is
licensed under an MIT-style permissive license
%endif # with_python3


%prep
%setup -q -n virtualenv-%{version}
%{__sed} -i -e "1s|#!/usr/bin/env python||" virtualenv.py 

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
# Build code
%{__python2} setup.py build

# Build docs on Fedora
%if 0%{?fedora} > 0
%{__python2} setup.py build_sphinx
rm -f build/sphinx/html/.buildinfo
%endif

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build

# Build docs on Fedora
%if 0%{?fedora} > 0
%{__python3} setup.py build_sphinx
rm -f build/sphinx/html/.buildinfo
%endif

popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
# rename binaries to use python3
mv %{buildroot}/%{_bindir}/virtualenv %{buildroot}/%{_bindir}/py3-virtualenv
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT

%files
%doc docs/*rst PKG-INFO AUTHORS.txt LICENSE.txt
# Include sphinx docs on Fedora
%if 0%{?fedora} > 0
%doc build/sphinx/*
%endif

%{python2_sitelib}/*
%{_bindir}/virtualenv
%{_bindir}/virtualenv-%{python2_version}

%if 0%{?with_python3}
%files -n python3-virtualenv
%doc docs/*rst PKG-INFO AUTHORS.txt LICENSE.txt
# Include sphinx docs on Fedora
%if 0%{?fedora} > 0
%doc build/sphinx/*
%endif
%{_bindir}/py3-virtualenv
%{_bindir}/virtualenv-%{python3_version}
%{python3_sitelib}/*
%endif



%changelog
* Mon Aug 24 2015 Steve Milner <smilner@redhat.com> - 13.1.2-1
- Update for upstream release.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 16 2015 Matej Stuchlik <mstuchli@redhat.com> - 12.0.7-1
- Update to 12.0.7

* Thu Jan 15 2015 Matthias Runge <mrunge@redhat.com> - 1.11.6-2
- add a python3-package, thanks to Matej Stuchlik (rhbz#1179150)

* Wed Jul 09 2014 Matthias Runge <mrunge@redhat.com> - 1.11.6-1
- update to 1.11.6:
  Upstream updated setuptools to 3.6, updated pip to 1.5.6

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.10.1-1
- Upstream upgraded pip to v1.4.1
- Upstream upgraded setuptools to v0.9.8 (fixes CVE-2013-1633)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.1-1
- Update to upstream 1.9.1 because of security issues with the bundled
  python-pip in older releases.  This is just a quick fix until a
  python-virtualenv maintainer can unbundle the python-pip package
  see: https://bugzilla.redhat.com/show_bug.cgi?id=749378

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Steve Milner <me@stevemilner.org> - 1.7.2-1
- Update for upstream bug fixes.
- Added path for versioned binary.
- Patch no longer required.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.7.1.2-1
- Update for upstream bug fixes.
- Added patch for sphinx building

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.7-1
- Update for https://bugzilla.redhat.com/show_bug.cgi?id=769067

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 16 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.5.1-1
- Added _weakrefset requirement for Python 2.7.1.
- Add support for PyPy.
- Uses a proper temporary dir when installing environment requirements.
- Add --prompt option to be able to override the default prompt prefix.
- Add fish and csh activate scripts.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul  7 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.8-3
- Fixed EPEL installation issue from BZ#611536

* Tue Jun  8 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.8-2
- Only replace the python shebang on the first line (Robert Buchholz)

* Fri Apr 28 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.8-1
- update pip to 0.7
- move regen-docs into bin/
- Fix #31, make activate_this.py work on Windows (use Lib/site-packages)
unset PYTHONHOME envioronment variable -- first step towards fixing the PYTHONHOME issue; see e.g. https://bugs.launchpad.net/virtualenv/+bug/290844
- unset PYTHONHOME in the (Unix) activate script (and reset it in deactivate())
- use the activate.sh in virtualenv.py via running bin/rebuild-script.py
- add warning message if PYTHONHOME is set

* Fri Apr 2 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.6-1
- allow script creation without setuptools
- fix problem with --relocate when bin/ has subdirs (fixes #12)
- Allow more flexible .pth file fixup
- make nt a required module, along with posix. it may not be a builtin module on jython
- don't mess with PEP 302-supplied __file__, from CPython, and merge in a small startup optimization for Jython, from Jython

* Tue Dec 22 2009 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.3-1
- Updated for upstream release.

* Thu Nov 12 2009 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.2-1
- Updated for upstream release.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.3-1
- Updated for upstream release.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 25 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.2-1
- Updated for upstream release.

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.1-4
- Rebuild for Python 2.6

* Mon Dec  1 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-3
- Added missing dependencies.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.1-2
- Rebuild for Python 2.6

* Fri Nov 28 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-1
- Updated for upstream release

* Sun Sep 28 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3-1
- Updated for upstream release

* Sat Aug 30 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.2-1
- Updated for upstream release

* Fri Aug 29 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.1-3
- Updated from review notes

* Thu Aug 28 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.1-2
- Updated from review notes

* Tue Aug 26 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.1-1
- Initial Version
