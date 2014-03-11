Name:                   libconfig
Summary:                C/C++ configuration file library
Version:                1.4.9
Release:                1%{?dist}
License:                LGPLv2+
Group:                  System Environment/Libraries
Source0:                http://www.hyperrealm.com/libconfig/libconfig-%{version}.tar.gz
URL:                    http://www.hyperrealm.com/libconfig/
BuildRequires:          texinfo-tex
BuildRequires:		bison, flex

%description
Libconfig is a simple library for manipulating structured configuration
files. This file format is more compact and more readable than XML. And
unlike XML, it is type-aware, so it is not necessary to do string parsing
in application code.

%package devel
Summary:                Development files for libconfig
Group:                  Development/Libraries
Requires:               %{name} = %{version}-%{release}
Requires:               pkgconfig
Requires(post):         /sbin/install-info
Requires(preun):        /sbin/install-info

%description devel
Development libraries and headers for developing software against
libconfig.

%prep
%setup -q
iconv -f iso-8859-1 -t utf-8 -o AUTHORS{.utf8,}
mv AUTHORS{.utf8,}

%build
%configure --disable-static
make %{?_smp_mflags}
#make pdf

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir
# Prevent multilib conflicts
#sed -i '/^\/CreationDate/d' $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}/libconfig.pdf
#sed -i '/^\/ModDate/d' $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}/libconfig.pdf
#sed -i '/^\/ID /d' $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}/libconfig.pdf

%post -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%postun -p /sbin/ldconfig

%preun devel
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libconfig*.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/libconfig*
%{_libdir}/libconfig*.so
%{_libdir}/pkgconfig/libconfig*.pc
#%{_defaultdocdir}/%{name}/
%{_infodir}/libconfig.info*

%changelog
* Mon Oct  1 2012 Tom Callaway <spot@fedoraproject.org> - 1.4.9-1
- update to 1.4.9

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.4.8-1
- update to 1.4.8

* Wed Mar 23 2011 Tom Callaway <spot@fedoraproject.org> - 1.4.7-1
- update to 1.4.7

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.6-1
- Update to 1.4.6
- Install libconfig_tests
- Fix rpmlint warnings

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May  5 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4.5-1
- update to 1.4.5

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.2-1
- update to 1.3.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.1-2
- prevent multilib conflicts with the generated pdf

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.1-1
- update to 1.3.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-2
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-1
- bump to 1.2.1

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-4
- nuke %%{_infodir}/dir, we handle it in %%post

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-3
- move all docs to devel
- move scriptlets around to match
- move requires around to match

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-2
- BR: texinfo-tex (not Requires)

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-1
- Initial package for Fedora
