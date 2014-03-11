%define python_sitelib %(%{__python} -c "from distutils import sysconfig; print sysconfig.get_python_lib()")
%define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')

Name: obexftp
Summary: Tool to access devices via the OBEX protocol
Group: Applications/File
Version: 0.23
Release: 13%{?dist}
License: GPLv2+
URL: http://openobex.triq.net/
Source: http://triq.net/obexftp/%{name}-%{version}.tar.bz2
Patch0: %{name}-norpath.patch
Patch1: %{name}-perl.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)
BuildRequires: bluez-libs-devel
BuildRequires: gettext-devel
BuildRequires: libtool
BuildRequires: openobex-devel >= 1.2
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: python-devel
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: tcl-devel

%description
The overall goal of this project is to make mobile devices featuring the OBEX
protocol and adhering to the OBEX FTP standard accessible by an open source
implementation. The common usage for ObexFTP is to access your mobile phones
memory to store and retrieve e.g. your phonebook, logos, ringtones, music,
pictures and alike.

%package -n python-%{name}
Summary: Python library to access devices via the OBEX protocol
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description -n python-%{name}
The overall goal of this project is to make mobile devices featuring the OBEX
protocol and adhering to the OBEX FTP standard accessible by an open source
implementation. The common usage for ObexFTP is to access your mobile phones
memory to store and retrieve e.g. your phonebook, logos, ringtones, music,
pictures and alike.

%package -n perl-%{name}
Summary: Perl library to access devices via the OBEX protocol
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-%{name}
The overall goal of this project is to make mobile devices featuring the OBEX
protocol and adhering to the OBEX FTP standard accessible by an open source
implementation. The common usage for ObexFTP is to access your mobile phones
memory to store and retrieve e.g. your phonebook, logos, ringtones, music,
pictures and alike.

%package -n ruby-%{name}
Summary: Ruby library to access devices via the OBEX protocol
Group: Development/Libraries
Requires: ruby(release)
Requires: %{name} = %{version}-%{release}

%description -n ruby-%{name}
The overall goal of this project is to make mobile devices featuring the OBEX
protocol and adhering to the OBEX FTP standard accessible by an open source
implementation. The common usage for ObexFTP is to access your mobile phones
memory to store and retrieve e.g. your phonebook, logos, ringtones, music,
pictures and alike.

%package libs
Summary: Shared libraries for %{name}
Group: System Environment/Libraries
Obsoletes: %{name} < 0.23-0.1

%description libs
The overall goal of this project is to make mobile devices featuring the OBEX
protocol and adhering to the OBEX FTP standard accessible by an open source
implementation. The common usage for ObexFTP is to access your mobile phones
memory to store and retrieve e.g. your phonebook, logos, ringtones, music,
pictures and alike.

%package devel
Summary: Header files and libraries for %{name}
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: openobex-devel >= 1.2
Requires: pkgconfig

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q
%patch0 -p1 -b .norpath
%patch1 -p1 -b .p

%build
autoreconf -f -i
%configure --disable-static --disable-dependency-tracking --disable-rpath
# fix for Ruby 1.9
sed -i 's|RSTRING(argv\[0\])->len|RSTRING_LEN(argv[0])|' swig/ruby/ruby_wrap.c
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
# ruby_headers= added to workaround bug in Ruby.
# https://bugzilla.redhat.com/show_bug.cgi?id=921650
%{__make} DESTDIR=%{buildroot} RUBYARCHDIR=%{buildroot}%{ruby_vendorarchdir} ruby_headers= install

%{__rm} %{buildroot}%{_libdir}/*.la
%{__rm} %{buildroot}%{perl_archlib}/perllocal.pod
%{__rm} -f %{buildroot}%{perl_vendorarch}/*/OBEXFTP/{.packlist,OBEXFTP.bs}

chmod 755 %{buildroot}%{perl_vendorarch}/*/OBEXFTP/OBEXFTP.so
chmod 755 %{buildroot}%{python_sitearch}/obexftp/_obexftp.so

%clean
%{__rm} -rf %{buildroot}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%{_mandir}/man1/obexftp.1*
%{_mandir}/man1/obexftpd.1*
%{_bindir}/obexftp
%{_bindir}/obexftpd

%files libs
%defattr(-, root, root, -)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, -)
%{_includedir}/bfb/
%{_includedir}/multicobex/
%{_includedir}/obexftp/
%{_libdir}/*.so
%{_libdir}/pkgconfig/obexftp.pc

%files -n python-%{name}
%defattr(-, root, root, -)
%dir %{python_sitearch}/obexftp
%{python_sitearch}/obexftp/_obexftp.so*
%{python_sitearch}/obexftp/__init__.py*
%if 0%{?fedora} >= 9
%{python_sitearch}/*.egg-info
%endif

%files -n perl-%{name}
%defattr(-, root, root, -)
%{perl_vendorarch}/OBEXFTP.pm
%dir %{perl_vendorarch}/*/OBEXFTP
%{perl_vendorarch}/*/OBEXFTP/OBEXFTP.so

%files -n ruby-%{name}
%defattr(-, root, root, -)
%{ruby_vendorarchdir}/obexftp.so

%changelog
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
