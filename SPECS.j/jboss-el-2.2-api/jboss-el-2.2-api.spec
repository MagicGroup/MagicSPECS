%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:         jboss-el-2.2-api
Version:      1.0.2
Release:      2%{?dist}
Summary:      Expression Language 2.2 API
License:      CDDL or GPLv2 with exceptions
URL:          http://www.jboss.org

Source0:      https://github.com/jboss/jboss-el-api_spec/archive/%{namedversion}.tar.gz

BuildRequires: jboss-parent
BuildRequires: maven-local
BuildRequires: maven-compiler-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin

BuildArch: noarch

%description
Expression Language 2.2 API classes.

%package javadoc
Summary: Javadocs for %{name}

%description javadoc	
This package contains the API documentation for %{name}.

%prep
%setup -q -n jboss-el-api_spec-%{namedversion}

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE
%doc README

%files javadoc -f .mfiles-javadoc
%doc LICENSE
%doc README

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 09 2013 Marek Goldmann <mgoldman@redhat.com> - 1.0.2-1
- Upstream release 1.0.2.Final
- New guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.7.20120212git2fabd8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.6.20120212git2fabd8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.1-0.5.20120212git2fabd8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jul 24 2012 Juan Hernandez <juan.hernandez@redhat.com> - 1.0.1-0.4.20120212git2fabd8
- Added maven-enforcer-plugin build time dependency

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.3.20120212git2fabd8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Marek Goldmann <mgoldman@redhat.com> 1.0.1-0.2.20120212git2fabd8
- Added additional POM mapping: javax.el:el-api

* Mon Mar 12 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.0.1-0.1.20120212git2fabd8
- Packaging after license cleanup upstream

* Fri Feb 24 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.0.0-2
- Cleanup of the spec file

* Wed Feb 1 2012 Marek Goldmann <mgoldman@redhat.com> 1.0.0-1
- Initial packaging

