Name:           sombok
Version:        2.3.1
Release:        1%{?dist}
Summary:        Unicode Text Segmentation Package

Group:          System Environment/Libraries
License:        GPLv2+ or Artistic clarified
URL:            http://sf.net/projects/linefold/
Source0:        http://downloads.sourceforge.net/linefold/%{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# libthai is available only in Fedora and EL6
%if 0%{?rhel} > 5 || 0%{?fedora}
BuildRequires:  libthai-devel
%endif

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool


%description
Sombok library package performs Line Breaking Algorithm described in Unicode
Standards Annex #14 (UAX #14). East_Asian_Width informative properties defined
by Annex #11 (UAX #11) may be concerned to determine breaking positions. This
package also implements "default" Grapheme Cluster segmentation described in
Annex #29 (UAX #29).


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
autoreconf -vif
%configure --disable-static  --disable-doc
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog ChangeLog.REL1 COPYING NEWS README README.ja_JP
%{_libdir}/libsombok.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/sombok*.h
%{_libdir}/libsombok.so
%{_libdir}/pkgconfig/sombok.pc


%changelog
* Sun Sep 29 2013 Xavier Bachelot <xavier@bachelot.org> 2.3.1-1
- Update to 2.3.1.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Xavier Bachelot <xavier@bachelot.org> 2.2.1-1
- Update to 2.2.1.
- Update License: to GPLv2+ or Artistic clarified. 

* Thu Mar 01 2012 Xavier Bachelot <xavier@bachelot.org> 2.1.1-1
- Update to 2.1.1.

* Sat Feb 04 2012 Xavier Bachelot <xavier@bachelot.org> 2.1.0-1
- Update to 2.1.0.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Xavier Bachelot <xavier@bachelot.org> 2.0.6-1
- Update to 2.0.6.

* Tue Jul 26 2011 Xavier Bachelot <xavier@bachelot.org> 2.0.5-2
- Fix conditional BuildRequires on libthai-devel.
- Fix description.
- Fix Requires in the devel subpackage.
- Be more specific on filenames in the %%files' sections.

* Tue May 17 2011 Xavier Bachelot <xavier@bachelot.org> 2.0.5-1
- Initial Fedora release.
