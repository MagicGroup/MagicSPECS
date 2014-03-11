Name:		libspotify
Version:	12.1.51
Release:	3%{?dist}
Summary:	Official Spotify API
Group:		Development/Libraries
License:	Redistributable, no modification permitted
URL:		http://developer.spotify.com/en/libspotify/overview/
Source0:	http://developer.spotify.com/download/libspotify/libspotify-%{version}-Linux-i686-release.tar.gz
Source1:	http://developer.spotify.com/download/libspotify/libspotify-%{version}-Linux-x86_64-release.tar.gz
Source2:        http://developer.spotify.com/download/libspotify/libspotify-%{version}-Linux-armv5-release.tar.gz
Source3:        http://developer.spotify.com/download/libspotify/libspotify-%{version}-Linux-armv6-release.tar.gz
Source4:        http://developer.spotify.com/download/libspotify/libspotify-%{version}-Linux-armv7-release.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
ExclusiveArch:	i686 x86_64 armv5tel armv6l armv7l

%description
libspotify is the official Spotify API.  Applications can use this API to play
music using a user's Spotify account, provided that the user has a Spotify
Premium Account.

%package devel
Summary:	Development files for official Spotify API
Requires:	libspotify = %{version}-%{release}

%description devel
This contains the files needed to develop using libspotify

%prep
%ifarch i686
%setup -q -b 0 -n %{name}-%{version}-Linux-i686-release
%endif
%ifarch x86_64
%setup -q -b 1 -n %{name}-%{version}-Linux-x86_64-release
# There must be a prettier way of doing this
sed -i s/"\/lib\/"/"\/lib64\/"/g Makefile
sed -i s/"\/lib$"/"\/lib64"/g Makefile
sed -i s/"\/lib "/"\/lib64 "/g Makefile
%endif
%ifarch armv5tel
%setup -q -b 2 -n %{name}-%{version}-Linux-armv5-release
%endif
%ifarch armv6l
%setup -q -b 3 -n %{name}-%{version}-Linux-armv6-release
%endif
%ifarch armv7l
%setup -q -b 4 -n %{name}-%{version}-Linux-armv7-release
%endif
%ifnarch i686 x86_64 armv5tel armv6l armv7l
echo "This cpu architecture is not supported"
exit 1
%endif
cat Makefile | grep -v ldconfig > Makefile.new
rm -f Makefile
mv Makefile.new Makefile

%install
rm -rf $RPM_BUILD_ROOT
%ifnarch i686 x86_64 armv5tel armv6l armv7l
echo "This cpu architecture is not supported"
exit 1
%endif
make install prefix=$RPM_BUILD_ROOT/usr
ls -l ./
cd $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cat libspotify.pc | grep -v "^prefix=" > libspotify.pc.new
echo "prefix=/usr" > libspotify.pc
cat libspotify.pc.new >> libspotify.pc
rm -f libspotify.pc.new
%ifarch x86_64
sed -i s/"\/lib"/"\/lib64"/g libspotify.pc
%endif
chmod 644 $RPM_BUILD_ROOT%{_includedir}/libspotify/*
magic_rpm_clean.sh

%build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README licenses.xhtml
%{_libdir}/libspotify.so.*

%files devel
%defattr(-,root,root,-)
%doc LICENSE README licenses.xhtml
%{_includedir}/*
%{_libdir}/libspotify.so
%{_libdir}/pkgconfig/*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 12.1.51-3
- 为 Magic 3.0 重建

* Wed Jul 11 2012 Jonathan Dieter <jdieter@gmail.com> - 12.1.51-2
- Add in armv5, armv6 and armv7

* Thu Jun 28 2012 Jonathan Dieter <jdieter@gmail.com> - 12.1.51-1
- Update to 12.1.51

* Mon Mar 26 2012 Jonathan Dieter <jdieter@gmail.com> - 10.1.16-3
- Change license
- Add empty build section to make rpmlint happy

* Mon Jan 23 2012 Jonathan Dieter <jdieter@gmail.com> - 10.1.16-2
- Add documentation to both main and devel package
- Only prep tarball that we're going to use when building

* Wed Jan  4 2012 Jonathan Dieter <jdieter@gmail.com> - 10.1.16-1
- Initial release
