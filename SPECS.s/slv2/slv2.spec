Name:			slv2
Summary:		LV2 host library
Summary(zh_CN.UTF-8): 	LV2 主机库
Version:		0.6.6
Release:		12%{?dist}
License:		GPLv2+
Group:			System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0:		http://download.drobilla.net/%{name}-%{version}.tar.bz2
# Remove dates from html doc files RHBZ#566345
Patch0:			%{name}-no-date-on-docs.patch
URL:			http://drobilla.net/software/slv2/
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:		doxygen
BuildRequires:		lv2core-devel
BuildRequires:		python
BuildRequires:		redland-devel
BuildRequires:		jack-audio-connection-kit-devel
# To provide a clean upgrade path from PlanetCCRMA:
Obsoletes:		%{name}-examples < 0.6
Provides:		%{name}-examples = %{version}-%{release}

%description
SLV2 is a library to make the use of LV2 plugins as simple as possible for 
applications. It is written in standard C using the Redland RDF toolkit. The 
Data (RDF) and code (shared library) functionality in SLV2 is strictly
separated so it is simple to control where each is used (e.g. it is possible
to discover/investigate plugins and related data without loading any shared 
libraries, avoiding the associated risks).
%description -l zh_CN.UTF-8
LV2 主机库。

%package devel
Summary:	Development libraries and headers for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	lv2core-devel 
Requires:	redland-devel
Requires:	pkgconfig
Requires:	%{name} = %{version}-%{release}

%description devel
SLV2 is a library to make the use of LV2 plugins as simple as possible for
applications. It is written in standard C using the Redland RDF toolkit. The
Data (RDF) and code (shared library) functionality in SLV2 is strictly
separated so it is simple to control where each is used (e.g. it is possible
to discover/investigate plugins and related data without loading any shared
libraries, avoiding the associated risks).

This package contains the headers and development libraries for SLV2.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q 
%patch0 -p1 -b .nodates

# Fix possible multilib issues
sed -i 's|/lib/|/%{_lib}/|g' src/world.c
sed -i "s|/lib'|/%{_lib}'|" autowaf.py

# Remove unnecessary flags
sed -i 's|@REDLAND.*@||' slv2.pc.in
# Fix CFLAGS issue in slv2->redland->rasqal dependency chain
echo "Requires.private: redland" >> slv2.pc.in

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
./waf configure --prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--htmldir=%{_docdir}/%{name}-devel-%{version} \
	--build-docs
./waf build -v %{?_smp_mflags}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} ./waf install
chmod +x %{buildroot}%{_libdir}/lib%{name}.so*
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/lv2*
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_docdir}/%{name}-devel-%{version}
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so
%{_mandir}/man3/*%{name}*

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.6.6-12
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.6.6-11
- 为 Magic 3.0 重建

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 0.6.6-10
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.6.6-9
- 为 Magic 3.0 重建

* Mon Feb 06 2012 Liu Di <liudidi@gmail.com> - 0.6.6-8
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 01 2010 Dan Horák <dan[at]danny.cz> - 0.6.6-6
- Fix CFLAGS issue in slv2->redland->rasqal dependency chain

* Fri Feb 19 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.6.6-5
- Remove dates from html doc files RHBZ#566345

* Sun Jan 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.6.6-4
- rebuild (redland)

* Sun Jan 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.6.6-3
- rebuild (rasqal/redland)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.6.6-1
- Version update: 0.6.6
- Add Obsoletes/Provides to slv2-examples

* Tue May 05 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.6.4-1
- Version update: 0.6.4
- Drop plugininstance patch (upstreamed)

* Wed Apr 08 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.6.2-3
- Change CCFLAGS to CFLAGS

* Sat Mar 28 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.6.2-2
- Remove redland flags from the .pc file
- Change CPPFLAGS to CXXFLAGS
- Move API documentation to the -devel package

* Thu Mar 26 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.6.2-1
- Initial build
