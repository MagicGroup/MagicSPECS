# Filter private shared library provides
%filter_provides_in %{python_sitearch}/pyalsa/.*\.so$
%filter_setup

Summary:	Python binding for the ALSA library
Name:		python-alsa
Version:	1.0.24
Release:	3%{?dist}
License:	LGPLv2+
Group:		Development/Languages
Source0:	ftp://ftp.alsa-project.org/pub/pyalsa/pyalsa-%{version}.tar.bz2
URL:		http://www.alsa-project.org/
BuildRequires:	alsa-lib-devel >= %{version}
BuildRequires:	python-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Python binding for the ALSA library.

%prep
%setup -q -n pyalsa-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
	
%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{python_sitearch}/*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0.24-3
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Liu Di <liudidi@gmail.com> - 1.0.24-2
- 为 Magic 3.0 重建

* Tue Mar 29 2011 Robin Lee <cheeselee@fedoraproject.org> - 1.0.24-1
- Update to 1.0.24 (#674260)
- Filter private shared library provides
- Clean up unused definitions

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.22-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.22-1.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jan 25 2010 Andy Shevchenko <andy@smile.org.ua> - 1.0.22-1
- update to release 1.0.22 (should fix bug #558229)

* Sat Sep 05 2009 Andy Shevchenko <andy@smile.org.ua> - 1.0.21-1
- update to release 1.0.21

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Andy Shevchenko <andy@smile.org.ua> - 1.0.20-1
- update to release 1.0.20

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.17-2
- Rebuild for Python 2.6

* Fri Jul 25 2008 Andy Shevchenko <andy@smile.org.ua> - 1.0.17-1
- update to release 1.0.17

* Sun May 04 2008 Andy Shevchenko <andy@smile.org.ua> - 1.0.16-1
- update to release 1.0.16

* Wed Feb 20 2008 Jesse Keating <jkeating@redhat.com> - 1.0.15-3
- Rebuild for GCC 4.3

* Fri Jan 04 2008 Andy Shevchenko <andy@smile.org.ua> 1.0.15-2
- include egg-info to the files: catched from rawhide mass rebuild
  (http://sunsite.mff.cuni.cz/rawhide20071220-gcc43/fails-even-with-41/python-alsa-1.0.15-1.fc8.log)

* Wed Oct 17 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-1
- update to relase 1.0.15

* Sun Oct 14 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-0.4.rc2
- require at least ALSA 1.0.15

* Fri Oct 12 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-0.3.rc2
- don't put executable files to the documentation

* Thu Oct 11 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-0.2.rc2
- prepare to include to the Fedora
  (https://bugzilla.redhat.com/show_bug.cgi?id=327351)

* Wed Oct 10 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-0.1.rc2
- initial build
