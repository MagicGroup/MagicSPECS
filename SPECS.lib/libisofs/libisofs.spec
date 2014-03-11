Summary:	Library to create ISO 9660 disk images
Name:		libisofs
Version:	1.1.6
Release:	2%{?dist}
License:	GPLv2
Group:		System Environment/Libraries
URL:		http://libburnia-project.org/
Source:		http://files.libburnia-project.org/releases/%{name}-%{version}.tar.gz
Patch0:		libisofs-0.6.16-multilib.patch
BuildRequires:	libacl-devel, zlib-devel, doxygen, graphviz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Libisofs is a library to create an ISO-9660 filesystem and supports
extensions like RockRidge or Joliet. It is also a full featured
ISO-9660 editor, allowing you to modify an ISO image or multisession
disc, including file addition or removal, change of file names and
attributes etc. It supports the extension AAIP which allows to store
ACLs and xattr in ISO-9660 filesystems as well. As it is linked with
zlib, it supports zisofs compression, too.

%package devel
Summary:	Development files for libisofs
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The libisofs-devel package contains libraries and header files for
developing applications that use libisofs.

%prep
%setup -q
%patch0 -p1 -b .multilib

%build
%configure --disable-static
make %{?_smp_mflags}
doxygen doc/doxygen.conf

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT README
%{_libdir}/%{name}*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}*.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.6-2
- 为 Magic 3.0 重建

* Sat Oct 08 2011 Robert Scheck <robert@fedoraproject.org> 1.1.6-1
- Upgrade to 1.1.6

* Sun Sep 18 2011 Robert Scheck <robert@fedoraproject.org> 1.1.4-1
- Upgrade to 1.1.4

* Sun Jul 10 2011 Robert Scheck <robert@fedoraproject.org> 1.1.2-1
- Upgrade to 1.1.2

* Tue May 17 2011 Robert Scheck <robert@fedoraproject.org> 1.0.8-1
- Upgrade to 1.0.8

* Sun Apr 10 2011 Robert Scheck <robert@fedoraproject.org> 1.0.6-1
- Upgrade to 1.0.6

* Tue Mar 15 2011 Robert Scheck <robert@fedoraproject.org> 1.0.4-1
- Upgrade to 1.0.4

* Mon Feb 28 2011 Robert Scheck <robert@fedoraproject.org> 1.0.2-1
- Upgrade to 1.0.2

* Thu Feb 17 2011 Honza Horak <hhorak@redhat.com> - 1.0.0-1
- Update to upstream 1.0.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Robert Scheck <robert@fedoraproject.org> 0.6.40-1
- Upgrade to 0.6.40

* Sun Oct 31 2010 Robert Scheck <robert@fedoraproject.org> 0.6.38-1
- Upgrade to 0.6.38

* Sun Jul 04 2010 Robert Scheck <robert@fedoraproject.org> 0.6.34-1
- Upgrade to 0.6.34

* Fri May 14 2010 Robert Scheck <robert@fedoraproject.org> 0.6.32-1
- Upgrade to 0.6.32

* Sat Apr 17 2010 Robert Scheck <robert@fedoraproject.org> 0.6.30-1
- Upgrade to 0.6.30

* Tue Feb 16 2010 Robert Scheck <robert@fedoraproject.org> 0.6.28-1
- Upgrade to 0.6.28

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Robert Scheck <robert@fedoraproject.org> 0.6.20-1
- Upgrade to 0.6.20

* Tue Mar 17 2009 Robert Scheck <robert@fedoraproject.org> 0.6.16-1
- Upgrade to 0.6.16
- Several spec file cleanups and solved the multilib issues

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Denis Leroy <denis@poolshark.org> - 0.6.12-1
- Update to 0.6.12 upstream version

* Wed Aug  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.6-2
- fix license tag

* Wed Jun 11 2008 Denis Leroy <denis@poolshark.org> - 0.6.6-1
- Update to upstream 0.6.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.8-3
- Autorebuild for GCC 4.3

* Wed Oct 10 2007 Jesse Keating <jkeating@redhat.com> - 0.2.8-2
- Rebuild for BuildID

* Fri Aug 10 2007 Denis Leroy <denis@poolshark.org> - 0.2.8-1
- Update to 0.2.8
- Fixed Source URL

* Mon Jan 08 2007 Jesse Keating <jkeating@redhat.com> - 0.2.4-2
- Move html docs to -devel
- Change urls to new upstream location

* Wed Jan 03 2007 Jesse Keating <jkeating@redhat.com> - 0.2.4-1
- New upstream release to fix some issues

* Tue Jan 02 2007 Jesse Keating <jkeating@redhat.com> - 0.2.3-2
- Fix some issues brought up during review

* Tue Jan 02 2007 Jesse Keating <jkeating@redhat.com> - 0.2.3-1
- Initial release split off of libburn package.
- Disable docs for now, will be fixed in future upstream release
