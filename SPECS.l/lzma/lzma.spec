Summary: 	LZMA utils
Name: 		lzma
Version: 	4.32.7
Release: 	11%{?dist}
License: 	GPLv2+
Group:		Applications/File
Source0:	http://tukaani.org/%{name}/%{name}-%{version}.tar.lzma
URL:		http://tukaani.org/%{name}/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	%{name}-libs	= %{version}-%{release}

%description
LZMA provides very high compression ratio and fast decompression. The
core of the LZMA utils is Igor Pavlov's LZMA SDK containing the actual
LZMA encoder/decoder. LZMA utils add a few scripts which provide
gzip-like command line interface and a couple of other LZMA related
tools. 

%package 	libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	LGPLv2+

%description 	libs
Libraries for decoding LZMA compression.

%package 	devel
Summary:	Devel libraries & headers for liblzmadec
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name}-libs	= %{version}-%{release}

%description  devel
Devel libraries & headers for liblzmadec.

%prep
%setup -q  -n %{name}-%{version}

%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
rm -f %{buildroot}/%{_libdir}/*.a
rm -f %{buildroot}/%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README THANKS COPYING.* ChangeLog AUTHORS
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%doc COPYING.*
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32.7-7
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.32.7-4
- Use lzma compressed upstream tarball.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Tue Aug 04 2008 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.7-1
- Switch to version 4.32.7

* Sat Feb 09 2008 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.5-1
- Switch to version 4.32.5

* Sat Oct 27 2007 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.2-2
- Forgot to upload new sources, bumping...

* Sat Oct 27 2007 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.2-1
- 'make tag' problems, bumping...

* Sat Oct 27 2007 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.2-0
- Switch to version 4.32.2

* Tue Aug 7 2007 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.0-0.6.beta5
- More clean-up in spec and use beta5 release

* Tue Aug 7 2007 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.0-0.5.beta3
- More clean-up in spec

* Thu Jul 25 2007 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.0-0.4.beta3
- Add COPYING, remove *.a and *.la file, make description shorter

* Thu Jul 19 2007 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.0-0.3.beta3
- Add dist and _smp_mflags

* Tue Jul 17 2007 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.0-0.2.beta3
- Clean-up in spec.

* Sun Jul 15 2007 Per Patrice Bouchand <patrice.bouchand.fedora<at>gmail.com> 4.32.0-0.1.beta3
- Initial Fedora release (inspired by mandriva spec)

