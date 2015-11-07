Name:           fcgi
Version:        2.4.0
Release:        21%{?dist}
Summary:        FastCGI development kit
Summary(zh_CN.UTF-8): FastCGI 开发包

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/库
License:        OML
URL:            http://www.fastcgi.com/#TheDevKit
Source0:        http://fastcgi.com/dist/fcgi-%{version}.tar.gz
Source1:        fcgi-autogen.sh
Patch0:         fcgi-2.4.0-autotools.patch
# Patch0 created with Source1 after patching Patch1 and Patch2
Patch1:         fcgi-2.4.0-configure.in.patch
Patch2:         fcgi-2.4.0-Makefile.am-CPPFLAGS.patch
Patch3:         fcgi-2.4.0-gcc44_fixes.patch

%description
FastCGI is a language independent, scalable, open extension to CGI that
provides high performance without the limitations of server specific APIs.

%description -l zh_CN.UTF-8
FastCGI 开发包

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8 
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1
%patch3 -p1 -b .gcc44_fixes

# remove DOS End Of Line Encoding
sed -i 's/\r//' doc/fastcgi-prog-guide/ch2c.htm
# fix file permissions
chmod a-x include/fcgios.h libfcgi/os_unix.c


%build
%configure
# does not build with parallel make flags
make


%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/libfcgi{++,}.{l,}a
install -p -m 0644 -D doc/cgi-fcgi.1 $RPM_BUILD_ROOT%{_mandir}/man1/cgi-fcgi.1
for manpage in doc/*.3
do
install -p -m 0644 -D $manpage $RPM_BUILD_ROOT%{_mandir}/man3/$(basename $manpage)
done
rm -f -- doc/*.1
rm -f -- doc/*.3


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_bindir}/cgi-fcgi
%{_libdir}/libfcgi.so.*
%{_libdir}/libfcgi++.so.*
%{_mandir}/man1/*
%defattr(0644,root,root,0755)
%doc LICENSE.TERMS README


%files devel
%{_includedir}/*
%{_libdir}/libfcgi.so
%{_libdir}/libfcgi++.so
%{_mandir}/man3/*
%defattr(0644,root,root,0755)
%doc doc/


%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.4.0-21
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.4.0-20
- 为 Magic 3.0 重建

* Sun Nov 04 2012 Liu Di <liudidi@gmail.com> - 2.4.0-19
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 09 2011 Iain Arnell <iarnell@gmail.com> 2.4.0-17
- drop perl sub-package; it's been replaced by perl-FCGI (rhbz#736612)

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.4.0-16
- Perl mass rebuild & clean spec & clean Makefile.PL

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.4.0-14
- Mass rebuild with perl-5.12.0

* Sun May 16 2010 Till Maas <opensource@till.name> - 2.4.0-13
- Fix license tag. It's OML instead of BSD

* Mon Jan 18 2010 Chris Weyl <cweyl@alumni.drew.edu> - 2.4.0-12
- drop perl .so provides filtering, as it may have multiarch rpm implications

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.4.0-11
- rebuild against perl 5.10.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 01 2009 Chris Weyl <cweyl@alumni.drew.edu> - 2.4.0-9
- Stripping bad provides of private Perl extension libs

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Till Maas <opensource@till.name> - 2.4.0-7
- Add missing #include <cstdio> to make it compile with gcc 4.4

* Tue Oct 14 2008 Chris Weyl <cweyl@alumni.drew.edu> - 2.4.0-6
- package up the perl bindings in their own subpackage

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.4.0-5
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Till Maas <opensource till name> - 2.4.0-4
- bump release for rebuild

* Tue Jul 11 2007 Till Maas <opensource till name> - 2.4.0-3
- remove parallel make flags

* Tue Apr 17 2007 Till Maas <opensource till name> - 2.4.0-2
- add some documentation
- add mkdir ${RPM_BUILD_ROOT} to %%install
- install man-pages

* Mon Mar 5 2007 Till Maas <opensource till name> - 2.4.0-1
- Initial spec for fedora
