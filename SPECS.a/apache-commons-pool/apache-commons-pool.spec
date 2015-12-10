%global base_name       pool
%global short_name      commons-%{base_name}

Name:             apache-%{short_name}
Version:          1.6
Release:          12%{?dist}
Summary:          Apache Commons Pool Package
License:          ASL 2.0
URL:              http://commons.apache.org/%{base_name}/
Source0:          http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
BuildArch:        noarch

BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    maven-local

# This should go away with F-17
Provides:         jakarta-%{short_name} = 0:%{version}-%{release}
Obsoletes:        jakarta-%{short_name} < 0:1.3-14
Obsoletes:        jakarta-%{short_name}-tomcat5 < 0:1.3-14
Obsoletes:        jakarta-%{short_name}-manual < 0:1.3-14

%description
The goal of Pool package is it to create and maintain an object (instance)
pooling package to be distributed under the ASF license. The package should
support a variety of pool implementations, but encourage support of an
interface that makes these implementations interchangeable.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src

%mvn_alias : org.apache.commons:%{short_name}
%mvn_file : %{name} %{short_name}

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc README.txt LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.6-12
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.6-11
- 为 Magic 3.0 重建

* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 1.6-10
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.6-8
- Use Requires: java-headless rebuild (#1067528)

* Thu Aug  8 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.6-7
- Update to latest packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Mat Booth <fedora@matbooth.co.uk> - 1.6-5
- Add missing BuildRequires maven-local

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-3
- Install NOTICE file with javadoc package

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Alexander Kurtakov <akurtako@redhat.com> 1.6-1
- Update to latest release - 1.6.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Alexander Kurtakov <akurtako@redhat.com> 1.5.7-1
- Update to latest version (1.5.7).

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 1.5.6-2
- Adapt to current guidelines.

* Fri Apr 15 2011 Chris Spike <spike@fedoraproject.org> 1.5.6-1
- Updated to 1.5.6
- Fixed build for maven 3

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 9 2010 Chris Spike <spike@fedoraproject.org> 1.5.5-4
- Removed maven* BRs in favour of apache-commons-parent
- Added deprecated groupId to depmap for compatibility reasons

* Mon Oct 18 2010 Chris Spike <spike@fedoraproject.org> 1.5.5-3
- Removed Epoch

* Tue Oct 5 2010 Chris Spike <spike@fedoraproject.org> 1.5.5-2
- Consistently using 'buildroot' macro instead of 'RPM_BUILD_ROOT' now

* Fri Oct 1 2010 Chris Spike <spike@fedoraproject.org> 1.5.5-1
- Rename and rebase from jakarta-commons-pool
