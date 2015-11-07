
Name:           xfconf
Version:	4.12.0
Release:        4%{?dist}
Summary:        Hierarchical configuration system for Xfce
Summary(zh_CN.UTF-8): Xfce 下的分类配置系统

Group:          System Environment/Base
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2
URL:            http://www.xfce.org/
#VCS git:git://git.xfce.org/xfce/xfconf
%global xfceversion %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(libxfce4util-1.0) >= %{xfceversion}
BuildRequires:  pkgconfig(dbus-1) >= 1.1.0
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.84
BuildRequires:  perl(ExtUtils::Depends)
BuildRequires:  perl(ExtUtils::PkgConfig)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Glib)
BuildRequires:  perl(Glib::MakeHelper)
BuildRequires:  gettext
BuildRequires:  intltool

Requires:       dbus-x11

Obsoletes:      libxfce4mcs < 4.4.3-3

%description
Xfconf is a hierarchical (tree-like) configuration system where the
immediate child nodes of the root are called "channels".  All settings
beneath the channel nodes are called "properties."

%description -l zh_CN.UTF-8
Xfce 下的分类配置系统。

%package        devel
Summary:        Development tools for xfconf
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       dbus-devel
Requires:       dbus-glib-devel
Requires:       glib2-devel
Obsoletes:      libxfce4mcs-devel < 4.4.3-3
Obsoletes:      xfce-mcs-manager-devel < 4.4.3-3

%description devel
This package includes the libraries and header files you will need
to compile applications for xfconf.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package perl
Summary:        Perl modules for xfconf
Summary(zh_CN.UTF-8): %{name} 的 Perl 模块
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
This package includes the perl modules and files you will need to 
interact with xfconf using perl. 

%description perl -l zh_CN.UTF-8
%{name} 的 Perl 模块。

%prep
%setup -q

%build
%configure --disable-static --with-perl-options=INSTALLDIRS="vendor"
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

# remove unneeded la files. 
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
# remove perl temp file
rm -f $RPM_BUILD_ROOT/%{perl_archlib}/perllocal.pod
# remove unneeded dynloader bootstrap file
rm -f $RPM_BUILD_ROOT/%{perl_vendorarch}/auto/Xfce4/Xfconf/Xfconf.bs
# remove .packlist files. 
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
# fix permissions on the .so file
chmod 755 $RPM_BUILD_ROOT/%{perl_vendorarch}/auto/Xfce4/Xfconf/Xfconf.so
# kevin identified the issue - fixes wrong library permissions
chmod 755 $RPM_BUILD_ROOT/%{_libdir}/*.so
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS TODO COPYING
%{_libdir}/lib*.so.*
%{_bindir}/xfconf-query
%{_libdir}/xfce4/xfconf/
%{_datadir}/dbus-1/services/org.xfce.Xfconf.service

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/xfconf-0

%files perl
%defattr(-,root,root,-)
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Xfce4
%{_mandir}/man3/*.3*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 4.12.0-4
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 4.12.0-3
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 4.12.0-2
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 4.12.0-1
- 更新到 4.12.0

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 4.10.0-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.10.0-4
- 为 Magic 3.0 重建

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 4.10.0-2
- Perl 5.16 rebuild

* Sat Apr 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Make build verbose
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.1-1
- Update to 4.9.1 (Xfce 4.10pre2)

* Sun Apr 01 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.0-1
- Update to 4.9.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Kevin Fenzi <kevin@scrye.com> - 4.8.1-1
- Update to 4.8.1

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 4.8.0-4
- Perl mass rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.8.0-3
- Perl mass rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0 final. 

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Fri Dec 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4
- Fix directory ownership

* Sun Sep 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3

* Mon Aug 23 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-3
- Remove unneeded gtk-doc dep. Fixes bug #604423

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.6.2-2
- Mass rebuild with perl-5.12.0

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-1
- Update to 4.6.2

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4.6.1-5
- rebuild against perl 5.10.1

* Tue Oct 20 2009 Orion Poplawski <orion@cora.nwra.com> - 4.6.1-4
- Add BR perl(ExtUtils::MakeMaker) and perl(Glib::MakeHelper)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-2
- Require dbus-x11 (#505499)

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Mon Mar 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.0-2
- Fix directory ownership problems
- Move gtk-doc into devel package and mark it %%doc
- Make devel package require gtk-doc

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Thu Jan 22 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.5.93-3
- Let xfce4-settings Obsolete mcs manager and plugin packages

* Thu Jan 22 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.5.93-2
- Add Obsoletes for mcs devel package

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Fri Jan 02 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.92-4
- Add Obsoletes for mcs packages

* Mon Dec 22 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-3
- Fixes for review ( bug 477732 )

* Mon Dec 22 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-2
- Add gettext BuildRequires

* Sun Dec 21 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Initial version for Fedora
