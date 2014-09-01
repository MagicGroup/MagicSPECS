Name:           maven-shared-jar
Version:        1.1
Release:        9%{?dist}
# Maven-shared defines maven-shared-jar version as 1.1
Epoch:          1
Summary:        Maven JAR Utilities
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-shared-jar
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-collections:commons-collections)
BuildRequires:  mvn(org.apache.bcel:bcel)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-digest)


Obsoletes:      maven-shared-jar < %{epoch}:%{version}-%{release} 
Provides:       maven-shared-jar = %{epoch}:%{version}-%{release}

%description
Utilities that help identify the contents of a JAR, including Java class
analysis and Maven metadata analysis.

This is a replacement package for maven-shared-jar

%package javadoc
Summary:        Javadoc for %{name}
    
%description javadoc
API documentation for %{name}.


%prep
%setup -q

%pom_add_dep org.codehaus.plexus:plexus-container-default

find -type f -iname '*.jar' -delete

# Replace plexus-maven-plugin with plexus-component-metadata
find -name 'pom.xml' -exec sed \
    -i 's/<artifactId>plexus-maven-plugin<\/artifactId>/<artifactId>plexus-component-metadata<\/artifactId>/' '{}' ';'
find -name 'pom.xml' -exec sed \
    -i 's/<goal>descriptor<\/goal>/<goal>generate-metadata<\/goal>/' '{}' ';'

%build
# Tests require the jars that were removed
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 1:1.1-9
- 为 Magic 3.0 重建

* Fri Aug  1 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-8
- Fix build-requires on maven-shared

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:1.1-6
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 05 2013 Michal Srb <msrb@redhat.com> - 1:1.1-5
- Adapt to current guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:1.1-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan 23 2013 Tomas Radej <tradej@redhat.com> - 1:1.1-2
- Removed jars and skipped tests

* Tue Jan 15 2013 Tomas Radej <tradej@redhat.com> - 1:1.1-1
- Initial version

