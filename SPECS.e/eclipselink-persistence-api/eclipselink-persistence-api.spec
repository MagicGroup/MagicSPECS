%global oname javax.persistence
%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}
Name:          eclipselink-persistence-api
Version:       2.0.5
Release:       3%{?dist}
Summary:       JPA 2.0 Spec OSGi Bundle
License:       EPL and ASL 2.0
URL:           http://www.eclipse.org/eclipselink/
#Source0:       https://github.com/eclipse/javax.persistence/archive/2.0.5.v201212031355.tar.gz
Source0:       http://maven.eclipse.org/nexus/content/repositories/build/org/eclipse/persistence/%{oname}/%{namedversion}/%{oname}-%{namedversion}-sources.jar
Source1:       http://maven.eclipse.org/nexus/content/repositories/build/org/eclipse/persistence/%{oname}/%{namedversion}/%{oname}-%{namedversion}.pom
# add org.eclipse.osgi as build dep
# add maven-bundle-plugin conf
Patch0:        %{name}-2.0.5-build.patch

BuildRequires: java-devel

BuildRequires: mvn(org.eclipse.osgi:org.eclipse.osgi)

BuildRequires: maven-local
BuildRequires: maven-plugin-bundle

BuildArch:     noarch

%description
EclipseLink definition of the Java Persistence 2.0 API.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -c

# fixing incomplete source directory structure
mkdir -p src/main/java
mv org src/main/java/
mv javax src/main/java/

mkdir src/main/resources
cp -p *.html src/main/resources/

# clone source directory structure
find src/main/java/ -type d | while read dirname ; do
  newdirname=`echo $dirname | sed "s:src/main/java:src/main/resources:g"`
  mkdir -p $newdirname
done

# copy everything except *.java sources
find src/main/java/ -type f | grep -v "\.java" | while read cpfrom ; do
  cpto=`echo $cpfrom | sed "s:src/main/java:src/main/resources:g"`
  cp $cpfrom $cpto
done

cp -p %{SOURCE1} pom.xml
%patch0 -p0

# fix non ASCII chars
for s in src/main/java/javax/persistence/EntityManager.java\
  src/main/java/javax/persistence/MapsId.java;do
  native2ascii -encoding UTF8 ${s} ${s}
done

%build

%mvn_file :%{oname} %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc *.html

%files javadoc -f .mfiles-javadoc
%doc license.html

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.0.5-2
- Use Requires: java-headless rebuild (#1067528)

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 2.0.5-1
- update to 2.0.5

* Mon Jul 16 2012 gil cattaneo <puntogil@libero.it> 2.0.4-1
- initial rpm