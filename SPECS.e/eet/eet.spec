Name:           eet
Version:        1.7.9
Release:        1%{?dist}
Summary:        Library for speedy data storage, retrieval, and compression
Group:          System Environment/Libraries
License:        GPLv2+ and BSD
URL:            http://web.enlightenment.org/p.php?p=about/efl/eet
Source0:        http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
BuildRequires:  libjpeg-devel zlib-devel chrpath doxygen 
BuildRequires:  libeina-devel
BuildRequires:  openssl-devel

%description
Eet is a tiny library designed to write an arbitary set of chunks of
data to a file and optionally compress each chunk (very much like a
zip file) and allow fast random-access reading of the file later
on. It does not do zip as a zip itself has more complexity than is
needed, and it was much simpler to implement this once here.

It also can encode and decode data structures in memory, as well as
image data for saving to eet files or sending across the network to
other machines, or just writing to arbitary files on the system. All
data is encoded in a platform independent way and can be written and
read by any architecture.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-static --disable-doc
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
#chrpath --delete %{buildroot}%{_bindir}/%{name}
find %{buildroot} -name '*.la' -delete
#chrpath --delete %{buildroot}%{_libdir}/libeet.so.%{version}

# remove unfinished manpages
# find doc/man/man3 -size -100c -delete

# for l in todo %%{name}.dox
# do
#  rm -f doc/man/man3/$l.3
# done 

#chmod -x doc/html/*

# mkdir -p %%{buildroot}%%{_mandir}/man3
# install -Dpm0644 doc/man/man3/* %%{buildroot}%%{_mandir}/man3

# Rename overly generic manpage
# mv %%{buildrooti}%%{_mandir}/man3/deprecated.3 %%{buildroot}%%{_mandir}/man3/eet-deprecated.3

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/%{name}
%{_libdir}/*.so.*

%files devel
#%doc doc/html/*
# %%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/eet/

%changelog
* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Thu Aug 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-3
- Update license

* Sun Aug 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-2
- Bump version

* Sat Aug 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-1
- Update to 1.7.8
- Disable docs
- Remove unneeded BR's

* Tue Jun  4 2013 Tom Callaway <spot@fedoraproject.org> - 1.7.7-1
- update to 1.7.7

* Fri Apr 19 2013 Tom Callaway <spot@fedoraproject.org> - 1.7.6-1
- update to 1.7.6

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.7.4-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 27 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1
- update to 1.7.4
- silence rpmlint warnings

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.6.1-2
- rebuild against new libjpeg

* Thu Aug  2 2012 Tom Callaway <spot@fedoraproject.org> - 1.6.1-1
- update to 1.6.1

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for glibc bug#747377

* Thu Jul 14 2011 Tom Callaway <spot@fedoraproject.org> - 1.4.1-2
- resolve manpage conflict due to generic naming (bz678782)

* Thu Jul 14 2011 Tom Callaway <spot@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Thomas Janssen <thomasj@fedoraproject.org> 1.4.0-1
- final 1.4.0 release

* Wed Dec 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.4.0-0.1.beta3
- beta 3 release

* Tue Nov 16 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.4.0-0.1.beta2
- beta 2 release

* Fri Nov 05 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.4.0-0.1.beta1
- beta 1 release

* Fri Jul 02 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.3.2-1
- eet 1.3.2

* Fri Jun 11 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.3.0-1
- eet 1.3.0

* Fri Feb 12 2010 Thomas Janssen <thomasj@fedoraproject.org> - 1.2.3-1
- new upstream source 1.2.3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 1.1.0-1
- New upstream snapshot

* Mon May 19 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 1.0.1-1
- New upstream snapshot

* Thu Apr 24 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 1.0.0-1
- New upstream release, eet is out of beta now
- Fixed pkg-config file

* Sat Apr 19 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.99900-4
- Added workaround for bug in eet.pc. Proper fix is commited upstream

* Sat Apr 19 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.99900-3
- Cleaned up documentation installation
- Removed unneded dependency on zlib-devel from eet-devel

* Sat Apr 19 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.99900-2
- Fixed timestamp of source tarball
- Preserve timestamps of installed files
- Added pkgconfig to -devel dependencies
- Added html docs

* Thu Apr 10 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.99900-1
- Initial specfile for Eet
