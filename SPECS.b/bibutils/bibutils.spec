Name:           bibutils
Version:        5.0
Release:        6%{?dist}
Summary:        Bibliography conversion tools
License:        GPLv2
URL:            http://sourceforge.net/p/bibutils/home/Bibutils/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{version}_src.tgz
Patch0:         bibutils-5.0-install-LIBTARGETIN.patch

BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl

%description
The bibutils package converts between various bibliography
formats using a common MODS-format XML intermediate.


%package libs
Summary:        Bibutils library
License:        GPL+

%description libs
Bibutils library.


%package devel
Summary:        Development files for bibutils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
License:        GPL+

%description devel
Bibutils development files.


%prep
%setup -q -n %{name}_%{version}
%patch0 -p1 -b .orig


%build
./configure --install-dir %{buildroot}%{_bindir} --install-lib %{buildroot}%{_libdir} --dynamic
make DISTRO_CFLAGS="%{optflags}"

xsltproc -o bibutils.1 --nonet %{_datadir}/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl bibutils.dbk


%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir}
make install

mkdir -p %{buildroot}%{_includedir}/%{name}
cp -p lib/*.h %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_libdir}/pkgconfig 
cp -p lib/%{name}.pc %{buildroot}%{_libdir}/pkgconfig
sed -i -e 's!\\!!g' -e 's!libdir=${prefix}/lib!libdir=%{_libdir}!' -e 's!${includedir}!${includedir}/%{name}!' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
mkdir -p %{buildroot}%{_mandir}/man1
cp -p %{name}.1 %{buildroot}%{_mandir}/man1

for i in $(cd %{buildroot}%{_bindir}; ls *); do
  ln -s bibutils.1 %{buildroot}%{_mandir}/man1/$i.1
done


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc Copying ChangeLog
%{_bindir}/*
%{_mandir}/man1/*.1*


%files libs
%{_libdir}/libbibutils.so.*


%files devel
%{_includedir}/%{name}
%{_libdir}/libbibutils.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 5.0-6
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 5.0-5
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 5.0-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun  5 2013 Jens Petersen <petersen@redhat.com> - 5.0-1
- update to 5.0

* Mon Jan 28 2013 Jens Petersen <petersen@redhat.com> - 4.17-1
- update to 4.17
- patch and use upstream's Makefile

* Thu Jan 10 2013 Jens Petersen <petersen@redhat.com> - 4.16-1
- update to 4.16
- update License to only GPLv2
- no longer needs csh to build

* Thu Oct  4 2012 Jens Petersen <petersen@redhat.com> - 4.15-4
- tcsh provides csh so no need to patch configure for tcsh
- change license to GPL+ for the code and GPLv2 for the manpage

* Tue Oct  2 2012 Jens Petersen <petersen@redhat.com> - 4.15-3
- improve summary and description (#861922)
- build and install docbook manpage which is GPLv2+ (#861922)
- use _isa (#861922)

* Tue Oct  2 2012 Jens Petersen <petersen@redhat.com> - 4.15-2
- BR tcsh

* Mon Oct  1 2012 Jens Petersen <petersen@redhat.com> - 4.15-1
- initial packaging
