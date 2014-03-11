Name:           edje
Version:        1.7.9
Release:        1%{?dist}
License:        GPLv2+ and BSD
Summary:        Abstract GUI layout and animation object library
Url:            http://www.enlightenment.org
Group:          System Environment/Libraries
Source:         http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2

BuildRequires: doxygen
BuildRequires: embryo
BuildRequires: embryo-devel
BuildRequires: ecore-devel
BuildRequires: eet-devel
BuildRequires: fontconfig-devel
BuildRequires: evas-devel
BuildRequires: libeina-devel
BuildRequires: evas-devel
BuildRequires: lua-devel
BuildRequires: intltool pkgconfig automake autoconf gettext libtool glib2-devel 

%description
Abstract GUI layout and animation object library.

%package devel
Summary:        Edje headers, documentation and test programs
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers,  test programs and documentation for edje.

%prep
%setup -q

%build
%configure --disable-static --disable-doc
make %{?_smp_mflags} V=1

sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

#Temporarily disable doc due to size
#make doc %{?_smp_mflags}

%install
%make_install 
find %{buildroot}%{_libdir} -name '*.la' -exec rm -r {} +

#comment out for now for size
# remove unfinished manpages
#find doc/man/man3 -size -100c -delete
#for l in todo %{name}.dox; do
#    rm -f doc/man/man3/$l.3
#done
#mkdir -p %{buildroot}%{_mandir}/man3
#install -Dpm0644 doc/man/man3/* %{buildroot}%{_mandir}/man3
#mv  %{buildroot}%{_mandir}/man3/authors.3 %{buildroot}%{_mandir}/man3/edje-authors.3

%post
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%files
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/edje*
%{_datadir}/mime/packages/edje.xml
%{_libdir}/edje
%{_libdir}/libedje.so.1*
%{_bindir}/inkscape2edc

%files devel
#Commented out for size, will fix before import
#{_mandir}/man3/*
%{_libdir}/libedje.so
%{_libdir}/pkgconfig/edje.pc
%{_datadir}/edje
%{_includedir}/edje-1


%changelog
* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.9-1
- Update to 1.7.9

* Sat Aug 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-3
- Bump release

* Sat Aug 24 2013 Dan Mashal <dan.msahal@fedoraproject.org> 1.7.8-2
- Update BRs and license
- Rework spec for emotion
- Get rid of utils package

* Sun Aug 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-1
- Update to 1.7.8

* Sat Aug 17 2013 Rex Dieter <rdieter@fedoraproject.org> 1.7.7-5
- tighten build deps
- -devel: drop extraneous deps, %%files
- drop unneccessary rpath hacks


* Fri Aug 16 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-4
- Update BRs and sort them alphabetically 
- Fixed dir ownership again

* Thu Aug 15 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-3
- Update license
- Own /usr/share/mime/packages
- Update BR's

* Wed Jun 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-2
- Fix directory ownership
- Add update-mime-db scriptlets

* Mon Jun 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-1
- Update to latest upstream release
- Update BR's and devel isa bits

* Fri Dec 28 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1
- initial spec. some changes from Terje Rosten <terje.rosten@ntnu.no> 

