%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           pyflakes
Version:        0.5.0
Release:        4%{?dist}
Summary:        A Lint-like tool for Python

Group:          Development/Languages
License:        MIT
URL:            https://launchpad.net/pyflakes

Source0:        http://pypi.python.org/packages/source/p/pyflakes/pyflakes-%{version}.tar.gz
Patch0:         http://ftp.debian.org/debian/pool/main/p/pyflakes/pyflakes_0.4.0-1.diff.gz
Patch1:         pyflakes-0.5.0-nullbytes-691164.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-twisted-core

%description
PyFlakes is a Lint-like tool for Python, like PyChecker. It is focused
on identifying common errors quickly without executing Python
code. Its primary advantage over PyChecker is that it is fast. You
don't have to sit around for minutes waiting for the checker to run;
it runs on most large projects in only a few seconds.

%prep
%setup -q
%patch0 -p1
%{__patch} -p1 -s -F 0 -i debian/patches/always_close_fd.diff
%patch1 -p1

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -Dpm 644 debian/pyflakes.1 %{buildroot}%{_mandir}/man1/pyflakes.1

%check
trial pyflakes/test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE NEWS.txt PKG-INFO
%{_bindir}/pyflakes
%{python_sitelib}/pyflakes*
%exclude %{python_sitelib}/pyflakes/test/
%{_mandir}/man1/pyflakes.1*

%changelog
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep  5 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.5.0-2
- Bring back null byte input traceback patch.
- Include LICENSE and NEWS.txt in docs.

* Sun Sep  4 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.0-1
- Update to 0.5.0
- Remove patches that no longer apply

* Mon Apr  4 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.4.0-5
- Avoid traceback on input with null bytes (#691164).

* Sun Feb 13 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.4.0-4
- Backport upstream changes for set and dict comprehension support (#677032).
- Add man page and file descriptor close patch from Debian.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Mar 19 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.4.0-1
- Update to 0.4.0.

* Wed Nov  4 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.3.0-1
- Update to 0.3.0 (#533015).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.1-4
- Rebuild for Python 2.6

* Sat Dec  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.2.1-3
- Correctly identify the license

* Sat Dec  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.2.1-2
- Revert to released tarball

* Fri Dec  8 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.2.1-1.10526svn
- Fix version number

* Fri Dec  8 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-1.10526svn
- Fix up versioning

* Tue Dec  5 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-0.1.10526
- First version for Fedora Extras
