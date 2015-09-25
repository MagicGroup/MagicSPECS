%global snapshot 20101120svn7

Name:           xqc
Version:        1.0
Release:        0.9.%{snapshot}%{?dist}
Summary:        C/C++ API for interfacing with XQuery processors

Group:          Development/Libraries
License:        BSD
URL:            http://xqc.sourceforge.net

# snapshot archive created from upstream revision 7 with:
# svn export https://xqc.svn.sourceforge.net/svnroot/xqc/trunk/xqc xqc 
# tar czf xqc.tar.gz xqc
Source0:        xqc.tar.gz
Source1:        http://downloads.sourceforge.net/%{name}/intro.pdf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  doxygen

%description
The goal of the XQC project is to create standardized C/C++ APIs for 
interfacing with XQuery processors. They should provide mechanisms to compile 
and execute XQueries, manage contexts, and provide a basic interface for 
the XQuery Data Model.


%prep
%setup -q -n %{name}
cp %{SOURCE1} .

%build
%configure
make %{?_smp_mflags}
cd docs
doxygen Doxyfile.xqc


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE.txt intro.pdf examples/ docs/xqc/
%{_includedir}/xqc.h
%exclude %{_includedir}/xqc++.hpp


%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.9.20101120svn7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.20101120svn7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.7.20101120svn7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.20101120svn7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.5.20101120svn7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.4.20101120svn7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.3.20101120svn7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0-0.2.20101120svn7
- added SVN revision number to release tag

* Sat Nov 20 2010 Martin Gieseking <martin.gieseking@uos.de> 1.0-0.1.20101120svn
- initial package

