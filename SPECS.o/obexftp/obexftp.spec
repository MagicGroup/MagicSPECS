Name:           obexftp
Version:        0.24
Release:        3%{?dist}
Summary:        Tool to access devices via the OBEX protocol
License:        GPLv2+
URL:            https://gitorious.org/obexftp
Source0:        http://download.sourceforge.net/openobex/%{name}-%{version}-Source.tar.gz
Patch0:         %{name}-norpath.patch
# From upstream git, fixes fuse apps not being installed
Patch1:         %{name}-0.24-fuse.patch
# From OpenSUSE, thanks: fix pkgconfig to require bluez not bluetooth
Patch2:         %{name}-pkgconfig_requires.patch
# From OpenSUSE, thanks: fix python install path
Patch3:         %{name}-0.24-fix-absurd-install-path.patch
BuildRequires:  asciidoc
BuildRequires:  bluez-libs-devel
BuildRequires:  cmake
BuildRequires:  fuse-devel
BuildRequires:  gettext-devel
BuildRequires:  openobex-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  python-devel
BuildRequires:  ruby
BuildRequires:  ruby-devel
BuildRequires:  swig
BuildRequires:  tcl-devel
BuildRequires:  xmlto

%description
The overall goal of this project is to make mobile devices featuring the OBEX
protocol and adhering to the OBEX FTP standard accessible by an open source
implementation. The common usage for ObexFTP is to access your mobile phones
memory to store and retrieve e.g. your phonebook, logos, ringtones, music,
pictures and alike.

%package -n     python-%{name}
Summary:        Python library to access devices via the OBEX protocol
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python-%{name}
The overall goal of this project is to make mobile devices featuring the OBEX
protocol and adhering to the OBEX FTP standard accessible by an open source
implementation. The common usage for ObexFTP is to access your mobile phones
memory to store and retrieve e.g. your phonebook, logos, ringtones, music,
pictures and alike.

%package -n     perl-%{name}
Summary:        Perl library to access devices via the OBEX protocol
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-%{name}
The overall goal of this project is to make mobile devices featuring the OBEX
protocol and adhering to the OBEX FTP standard accessible by an open source
implementation. The common usage for ObexFTP is to access your mobile phones
memory to store and retrieve e.g. your phonebook, logos, ringtones, music,
pictures and alike.

%package -n     ruby-%{name}
Summary:        Ruby library to access devices via the OBEX protocol
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ruby(release)

%description -n ruby-%{name}
The overall goal of this project is to make mobile devices featuring the OBEX
protocol and adhering to the OBEX FTP standard accessible by an open source
implementation. The common usage for ObexFTP is to access your mobile phones
memory to store and retrieve e.g. your phonebook, logos, ringtones, music,
pictures and alike.

%package        libs
Summary:        %{name} Shared libraries
Obsoletes:      %{name} < 0.23-0.1

%description    libs
This package contains shared libraries of provided by %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       openobex-devel%{?_isa}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{name}-%{version}-Source
%patch0 -p1 -b .norpath
%patch1 -p1 -b .fuse
%patch2 -p1 -b .pkgconfig
%patch3 -p1 -b .pythonpath

%build
%cmake
# 'all' doesn't include doc, it seems - thanks, SUSE.
make %{?_smp_mflags} all doc

%install
make DESTDIR=%{buildroot} RUBYARCHDIR=%{buildroot}%{ruby_vendorarchdir} install

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/obexftp
%{_bindir}/obexftpd
%{_bindir}/obexautofs
%{_bindir}/obexfs
%{_mandir}/man1/obexftp.1*
%{_mandir}/man1/obexftpd.1*

%files libs
%{_libdir}/*.so.*

%files devel
%{_includedir}/bfb/
%{_includedir}/multicobex/
%{_includedir}/obexftp/
%{_libdir}/*.so
%{_libdir}/pkgconfig/obexftp.pc

%files -n python-%{name}
%{python_sitearch}/_obexftp.so*
%{python_sitearch}/obexftp.py*

%files -n perl-%{name}
%{perl_vendorarch}/OBEXFTP.pm
%dir %{perl_vendorarch}/*/OBEXFTP
%{perl_vendorarch}/*/OBEXFTP/OBEXFTP.so

%files -n ruby-%{name}
%{ruby_vendorarchdir}/obexftp.so

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Vít Ondruch <vondruch@redhat.com> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Fri Jan 10 2014 Adam Williamson <awilliam@redhat.com> - 0.24-1
- new upstream release 0.24
- convert to new cmake build system
- drop cruft and now-unnecessary workarounds/fixes from spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.23-14
- Perl 5.18 rebuild

* Fri Mar 22 2013 Vít Ondruch <vondruch@redhat.com> - 0.23-13
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.23-10
- Perl 5.16 rebuild

* Wed Feb 08 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.23-9
- Rebuilt for Ruby 1.9.3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.23-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Feb 28 2009 Dominik Mierzejewski <rpm@greysector.net> - 0.23-1
- updated to 0.23 release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.23-0.3.alpha
- Rebuild for Python 2.6

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.23-0.2.alpha
- Rebuild

* Mon Aug 18 2008 Dominik Mierzejewski <rpm@greysector.net> - 0.23-0.1.alpha
- updated to 0.23-alpha
- split libs into separate subpackage for multilib

* Sun Jun 15 2008 Dominik Mierzejewski <rpm@greysector.net> - 0.22-0.10.uctest
- latest test release, with iconv support
- fix rpmlint warning

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-0.9.rc9
Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.22-0.8.rc9
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Dominik Mierzejewski <rpm@greysector.net> - 0.22-0.7.rc9
- include python egg-info in the file list

* Tue Jan 01 2008 Dominik Mierzejewski <rpm@greysector.net> - 0.22-0.6.rc9
- updated to 0.22-rc9

* Thu Sep 06 2007 Dominik Mierzejewski <rpm@greysector.net> - 0.22-0.5.rc7
- updated to 0.22-rc7
- added pkgconfig file
- make perl BR more specific

* Mon Aug 27 2007 Dominik Mierzejewski <rpm@greysector.net> - 0.22-0.4.rc6
- rebuilt for BuildID
- updated license tag

* Mon Aug 06 2007 Dominik Mierzejewski <rpm@greysector.net> - 0.22-0.3.rc6
- updated to 0.22-rc6
- added ruby bindings (patch by Andy Shevchenko)
- dropped upstreamed patch
- added missing BRs for F7+

* Mon Mar 26 2007 Dominik Mierzejewski <rpm@greysector.net> - 0.22-0.2.pre4
- fix segfault in obexftpd (patch by Jan Kratochvil), closes (#230991)

* Fri Mar 23 2007 Dominik Mierzejewski <rpm@greysector.net> - 0.22-0.1.pre4
- updated to 0.22-pre4
- updated patches

* Fri Jan 26 2007 Dominik Mierzejewski <rpm@greysector.net> - 0.20-3
- add missing disttag

* Thu Jan 25 2007 Dominik Mierzejewski <rpm@greysector.net> - 0.20-2
- added missing defattr
- require openobex-devel > 1.2
- added missing MODULE_COMPAT Requires: to perl subpackage
- renamed subpackages to perl/python-obexftp
- fixed rpaths

* Mon Jan 01 2007 Dominik Mierzejewski <rpm@greysector.net> - 0.20-1
- updated to 0.20

* Sun Jan 29 2006 Dag Wieers <dag@wieers.com> - 0.18-1
- Initial package. (using DAR)
