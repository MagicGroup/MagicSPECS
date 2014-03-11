%{!?python:%define python python}
%{!?python_sitearch: %define python_sitearch %(%{python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Experimental Twisted Web Server Framework
Name: %{python}-twisted-web2
Version: 8.1.0
Release: 12%{?dist}
License: MIT
Group: Development/Libraries
URL: http://twistedmatrix.com/trac/wiki/TwistedWeb2
Source: http://tmrc.mit.edu/mirror/twisted/Web2/8.1/TwistedWeb2-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: %{python}-twisted-core >= 8.1.0
BuildRequires: %{python}-twisted-core >= 8.1.0
BuildRequires: %{python}-devel
# Files are noarch, but we need to install in sitearch for things to work, as
# all the rest of Twisted is in sitearch
#BuildArch: noarch
# Because of the above, disable generating an empty debuginfo package
%define debug_package %{nil}

%description
Twisted.Web2 is an experimental web server built with Twisted. Useful Web2
functionality will be backported to TwistedWeb until TwistedWeb is as
featureful as Web2, then Web2 will be abandoned. 


%prep
%setup -q -n TwistedWeb2-%{version}


%build
%{python} setup.py build


%install
%{__rm} -rf %{buildroot}
%{python} setup.py install \
    -O1 --skip-build --root %{buildroot} \
    --install-purelib %{python_sitearch}
# See if there's any egg-info
if [ -f %{buildroot}%{python_sitearch}/Twisted*.egg-info ]; then
    echo %{buildroot}%{python_sitearch}/Twisted*.egg-info |
        %{__sed} -e 's|^%{buildroot}||'
fi > egg-info


%clean
%{__rm} -rf %{buildroot}


%post
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%postun
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi


%files -f egg-info
%defattr(-,root,root,-)
%doc LICENSE NEWS README doc/*
%{python_sitearch}/twisted/plugins/twisted_web2.py*
%{python_sitearch}/twisted/web2/


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 8.1.0-12
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 8.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-5
- Introduce python macro for parallel installable versions.
- Add calls to twisted-dropin-cache and make sure they don't ever fail.
- Minor spec file updates.

* Tue Aug 19 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-4
- Use --install-purelib option instead of manually moving the installed files.
- Fix description.
- Include doc/ directory, although it would fit best in a "devel" package.
- Require python-twisted-core >= 8.1.0 to get ServiceMaker.

* Wed Jul 30 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-2
- Update to 8.1.0 again, as the downgrade didn't fix the problem.

* Wed Jul 16 2008 Matthias Saou <http://freshrpms.net/> 0.2.0-2
- Downgrade to 0.2.0 as elisa doesn't work with 8.1.0.
- Include Debian's patch, as it changes quite a bit of code.

* Tue Jul 15 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-0.1
- Initial RPM release.

