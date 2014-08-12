Name:           exec-maven-plugin
Version:        1.3.2
Release:        1%{?dist}
Summary:        Exec Maven Plugin

License:        ASL 2.0
URL:            http://mojo.codehaus.org/exec-maven-plugin
Source0:        http://repo1.maven.org/maven2/org/codehaus/mojo/exec-maven-plugin/%{version}/exec-maven-plugin-%{version}-source-release.zip
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.commons:commons-exec)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven:maven-toolchain)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.codehaus.mojo:mojo-parent:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

Obsoletes:      maven-plugin-exec < %{version}-%{release}
Provides:       maven-plugin-exec = %{version}-%{release}

%description
A plugin to allow execution of system and Java programs.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n exec-maven-plugin-%{version}

sed -i 's/\r$//' LICENSE.txt
find . -name *.jar -delete

%pom_remove_plugin :animal-sniffer-maven-plugin

%build
# tests are disabled, see: rhbz#1095077
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Wed Jul 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.2-1
- Update to upstream version 1.3.2

* Mon Jun 09 2014 Michal Srb <msrb@redhat.com> - 1.3.1-1
- Update to upstream version 1.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Michal Srb <msrb@redhat.com> - 1.3-2
- Fix license tag

* Wed May 07 2014 Michal Srb <msrb@redhat.com> - 1.3-1
- Update to upstream version 1.3

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-13
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun  5 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-11
- Clean up BuildRequires

* Thu Feb 14 2013 Michal Srb <msrb@redhat.com> - 1.2.1-10
- Disable animal-sniffer plugin

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2.1-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jan 11 2013 Michal Srb <msrb@redhat.com> - 1.2.1-7
- Fixed rpmlint warnings
- Remove bundled JAR files before building the package

* Wed Jan 09 2013 Michal Srb <msrb@redhat.com> - 1.2.1-6
- maven-plugin-exec renamed (Resolves: #893451)
- Migrated to xmvn

* Wed Nov 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.1-5
- Fix license tag
- Install license files
- Resolves: rhbz#880290

* Wed Nov 28 2012 Tomas Radej <tradej@redhat.com> - 1.2.1-4
- Removed (B)R on plexus-container-default

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 6 2011 Alexander Kurtakov <akurtako@redhat.com> 1.2.1-1
- Update to latest upstream.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 11 2009 Alexander Kurtakov <akurtako@gmail.com> 1.1-1
- Initial package.
