%{!?python:%define python python}
%{!?python_sitearch: %define python_sitearch %(%{python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           %{python}-twisted-runner
Version:        12.2.0
Release:        2%{?dist}
Summary:        Twisted Runner process management library and inetd replacement
License:        MIT
URL:            http://www.twistedmatrix.com/trac/wiki/TwistedRunner
Source0:        http://twistedmatrix.com/Releases/Runner/12.2/TwistedRunner-%{version}.tar.bz2
BuildRequires:  %{python}-twisted-core >= %{version}
BuildRequires:  %{python}-devel
Requires:       %{python}-twisted-core >= %{version}

%description
Twisted is an event-based framework for internet applications.

Twisted Runner contains code useful for persistent process management
with Python and Twisted, and has an almost full replacement for inetd.

%prep
%setup -q -n TwistedRunner-%{version}

%build
CFLAGS="%{optflags}" %{python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Don't package C files
rm $RPM_BUILD_ROOT%{python_sitearch}/twisted/runner/portmap.c

# Fix permissions of shared objects to pacify rpmlint
chmod 0755 $RPM_BUILD_ROOT%{python_sitearch}/twisted/runner/portmap.so

# See if there's any egg-info
if [ -f $RPM_BUILD_ROOT%{python_sitearch}/Twisted*.egg-info ]; then
    echo $RPM_BUILD_ROOT%{python_sitearch}/Twisted*.egg-info |
        sed -e "s|^$RPM_BUILD_ROOT||"
fi > egg-info

%files -f egg-info
%doc LICENSE NEWS README
%{python_sitearch}/twisted/plugins/twisted_runner.py*
%{python_sitearch}/twisted/runner/

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 12.2.0-2
- 为 Magic 3.0 重建

* Mon Sep 03 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.2.0-1
- Updated to 12.2.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.1.0-1
- Updated to 12.1.0

* Sun Feb 12 2012 Julian Sikorski <belegdol@fedoraproject.org> - 12.0.0-1
- Updated to 12.0.0

* Sat Jan 07 2012 Julian Sikorski <belegdol@fedoraproject.org> - 11.1.0-2
- Rebuilt for gcc-4.7

* Fri Nov 18 2011 Julian Sikorski <belegdol@fedoraproject.org> - 11.1.0-1
- Updated to 11.1.0
- Dropped obsolete Group, Buildroot, %%clean and %%defattr

* Sat Apr 30 2011 Julian Sikorski <belegdol@fedoraproject.org> - 11.0.0-1
- Updated to 11.0.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 10.2.0-1
- Updated to 10.2.0

* Wed Sep 29 2010 jkeating - 10.1.0-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 10.1.0-1
- Updated to 10.1.0
- Switched to macros for versioned dependencies
- Added the runner plugin

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 8.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matthias Saou <http://freshrpms.net/> 8.2.0-1
- Update to 8.2.0.
- Change back spec cosmetic details from Paul's to Thomas' preference.

* Tue Dec 23 2008 Matthias Saou <http://freshrpms.net/> 8.0.0-2
- Update to 8.0.0.
- Merge back changes from Paul Howarth.

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.0-8
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.0-7
- Rebuild for Python 2.6

* Fri Mar 07 2008 Jesse Keating <jkeating@redhat.com> - 0.2.0-6
- Fix the egg issue, drop the pyver stuff.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.0-5
- Autorebuild for GCC 4.3

* Wed Dec 27 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- add LICENSE and NEWS

* Wed Nov 01 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.0-3
- remove .c file

* Tue Sep 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.0-2
- no longer ghost .pyo files

* Wed Jun 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2.0-1
- new release
- remove noarch

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-2
- disttag

* Fri Mar 25 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-1
- final release

* Wed Mar 16 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-0.1.a3
- upstream release

* Sat Mar 12 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-0.1.a2
- prerelease; FE versioning

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-1
- prep for split

