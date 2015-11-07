Name:           shared-desktop-ontologies
Version:        0.11.0
Release:        4%{?dist}
Summary:        Shared ontologies needed for semantic environments
Summary(zh_CN.UTF-8): 语义环境的共享本体

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
# see LICENSE.README
License:        (BSD or CC-BY) and CC-BY and W3C
URL:            http://oscaf.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/oscaf/shared-desktop-ontologies/%{version}/shared-desktop-ontologies-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  cmake >= 2.6.0
BuildRequires:  pkgconfig


%description
The vision of the Social Semantic Desktop defines a user’s personal
information environment as a source and end-point of the Semantic Web:
Knowledge workers comprehensively express their information and data
with respect to their own conceptualizations.

Semantic Web languages and protocols are used to formalize these
conceptualizations and for coordinating local and global information
access. The Resource Description Framework serves as a common data
representation format. With a particular focus on addressing certain
limitations of RDF, a novel representational language akin to RDF and
the Web Ontology Language, plus a number of other high-level
ontologies were created.

Together, they provide a means to build the semantic bridges necessary
for data exchange and application integration on distributed social
semantic desktops. Although initially designed to fulfill requirements
for the Nepomuk project, these ontologies are useful for the semantic
web community in general.

%description -l zh_CN.UTF-8
语义环境的共享本体。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       cmake
Requires:       %{name} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries
and header files for developing applications
that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%check
# verify pkg-config version (notoriously wrong in recent releases)
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig
test "$(pkg-config --modversion shared-desktop-ontologies)" = "%{version}"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS README
%doc LICENSE.README
%doc LICENSE.BSD LICENSE.CC-BY LICENSE.DCMI LICENSE.w3c
%{_datadir}/ontology/

%files devel
%defattr(-,root,root,-)
%{_datadir}/cmake/SharedDesktopOntologies/
%{_datadir}/pkgconfig/shared-desktop-ontologies.pc


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.11.0-4
- 为 Magic 3.0 重建

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 0.11.0-3
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Rex Dieter <rdieter@fedoraproject.org> 0.11.0-1
- 0.11.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.0-2
- 0.10.0

* Fri Feb 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-1
- 0.9.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-1
- 0.8.1

* Thu Sep 01 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-1
- 0.8.0

* Fri Jul 22 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.1-2
- 0.7.1

* Tue May 31 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.0-2
- rebuild

* Mon May 16 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.0-1
- 0.7.0
- License: (BSD or CC-BY) and CC-BY and W3C

* Sun Feb 27 2011 Rex Dieter <rdieter@fedoraproject.org> 0.6.0-1
- 0.6.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.5-1
- 0.5

* Thu May 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4-1
- 0.4

* Wed Apr 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.3-2
- %%check: verify pkg-config --modversion sanity

* Wed Mar 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.3-1
- 0.3

* Sun Dec  6 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 0.2-3
- Add -devel package and move CMake and pkgconfig files there

* Sun Dec  6 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 0.2-2
- Fix license tag

* Sat Dec  5 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 0.2-1
- Initial release
