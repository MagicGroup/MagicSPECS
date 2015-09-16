Name:           shtool
Version:        2.0.8
Release:        17%{?dist}
Summary:        A portable shell tool

License:        GPLv2+
URL:            http://www.gnu.org/software/shtool/
Source0:        ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl-podlators

%description
GNU shtool is a compilation of small but very stable and portable
shell scripts into a single shell tool. All ingredients were in
successful use over many years in various free software projects.
The compiled shtool program is intended to be used inside the source
tree of other free software packages. There it can overtake various
(usually non-portable) tasks related to the building and installation
of such a package. It especially can replace the old mkdir.sh,
install.sh and related scripts. 

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

%check
make check

%files
%doc AUTHORS ChangeLog COPYING NEWS RATIONAL README THANKS VERSION
%{_mandir}/man*/%{name}*.*
%{_bindir}/%{name}
%{_bindir}/%{name}ize
%{_datadir}/%{name}/
%{_datadir}/aclocal/%{name}.m4

%changelog
* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 2.0.8-17
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.8-15
- Spec file updated

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.0.8-12
- Perl 5.18 rebuild

* Sat Feb 23 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.8-11
- Spec file updated

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.8-7
- Rebuilt

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.8-5
- Rebuilt

* Sat Feb 27 2010 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.8-4
- Rebuilt

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 08 2009 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.8-2
- Added test suite

* Sat Dec 27 2008 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.8-1
- Initial spec for Fedora
