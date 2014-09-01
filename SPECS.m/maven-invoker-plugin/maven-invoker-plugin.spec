Name:           maven-invoker-plugin
Version:        1.8
Release:        13%{?dist}
Summary:        Maven Invoker Plugin
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-invoker-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
Patch0:         pom-xml.patch
BuildArch: noarch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven.plugin-testing:maven-plugin-testing-harness)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-impl)
BuildRequires:  mvn(org.apache.maven.shared:maven-invoker)
BuildRequires:  mvn(org.apache.maven.shared:maven-script-interpreter)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.beanshell:bsh)
BuildRequires:  mvn(org.codehaus.groovy:groovy)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-i18n)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

Provides:       maven2-plugin-invoker = 1:%{version}-%{release}
Obsoletes:      maven2-plugin-invoker <= 0:2.0.8

%description
The Maven Invoker Plugin is used to run a set of Maven projects. The plugin 
can determine whether each project execution is successful, and optionally 
can verify the output generated from a given project execution.
  

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q 
%patch0

%build
%mvn_build -f 

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 1.8-13
- 为 Magic 3.0 重建

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-12
- Fix build-requires on parent POM

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-10
- Add missing BR on modello
- Resolves: rhbz#1077914

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.8-9
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-8
- Update to current packaging guidelines

* Mon Aug 12 2013 Alexander Kurtakov <akurtako@redhat.com> 1.8-7
- Build with xmvn.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-5
- Fix Requires and BuildRequires on Doxia; resolves: rhbz#950061
- Remove unneeded BR

* Sat Feb 16 2013 Michal Srb <msrb@redhat.com> - 1.8-4
- Migrate from maven-doxia to doxia subpackages (Resolves: #909238)
- Remove unnecessary BR on maven-doxia-tools

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.8-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jan 18 2013 Weinan Li <weli@redhat.com> 1.8-1
- Upgrade to 1.8

* Fri Jan 4 2013 David Xie <david.scriptfan@gmail.com> 1.7-2
- Add LICENSE and NOTICE files.

* Tue Oct 23 2012 Alexander Kurtakov <akurtako@redhat.com> 1.7-1
- Update to latest upstream.

* Tue Aug 21 2012 Tomas Radej <tradej@redhat.com> - 1.6-1
- Updated to v1.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 9 2011 Alexander Kurtakov <akurtako@redhat.com> 1.5-5
- Build with maven 3.x.
- Use upstream source.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 Weinan Li <weli@redhat.com> -1.5-3
- R: maven-shared-invoker
- R: maven-shared-reporting-api
- R: maven-shared-reporting-impl
- Remove BR: maven2-plugin-changes
- Add BR: maven-shared-invoker

* Mon Jun 7 2010 Weinan Li <weli@redhat.com> - 1.5-2
- Fix incoherent version in changelog
- BR: maven-javadoc-plugin

* Thu Jun 3 2010 Weinan Li <weli@redhat.com> - 1.5-1
- Initial Package
