Name:           maven-script-interpreter
Version:        1.1
Release:        7%{?dist}
Summary:        Maven Script Interpreter
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-script-interpreter/
Source0:        http://central.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.beanshell:bsh)
BuildRequires:  mvn(org.codehaus.groovy:groovy)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)


%description
This component provides some utilities to interpret/execute some scripts for
various implementations: Groovy or BeanShell.


%package javadoc
Summary:        Javadoc for %{name}
    
%description javadoc
API documentation for %{name}.


%prep
%setup -q

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc DEPENDENCIES LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.1-7
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.1-6
- 为 Magic 3.0 重建

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-5
- Fix build-requires on parent POM

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-3
- Use Requires: java-headless rebuild (#1067528)

* Mon Sep 02 2013 Michal Srb <msrb@redhat.com> - 1.1-2
- Fix BR

* Mon Sep 02 2013 Michal Srb <msrb@redhat.com> - 1.1-1
- Update to upstream version 1.1

* Mon Aug 05 2013 Michal Srb <msrb@redhat.com> - 1.0-5
- Adapt to current guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jul 24 2012 Tomas Radej <tradej@redhat.com> - 1.0-1
- Initial version

