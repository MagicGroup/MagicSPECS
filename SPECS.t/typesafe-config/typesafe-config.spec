%if 0%{?fedora} >= 21
%global java_pkg java-headless
%else
%global java_pkg java
%endif

Name:          typesafe-config
Version:       1.2.0
Release:       4%{?dist}
Summary:       Configuration library for JVM languages
License:       ASL 2.0
URL:           https://github.com/typesafehub/config/
Source0:       https://github.com/typesafehub/config/archive/v%{version}.tar.gz
BuildRequires: java-devel
BuildRequires: javapackages-tools
BuildRequires: sbt

Requires:      %{java_pkg}
Requires:      javapackages-tools
BuildArch:     noarch

%description
Configuration library for JVM languages.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n config-%{version}

rm -f project/plugins.sbt

sed -i -e '/SbtOsgi/d' project/Build.scala
sed -i -e '/OsgiKeys/d' project/Build.scala
sed -i -e 's/osgiSettings [+][+]//g' project/Build.scala
sed -i -e '/override val settings/d' project/Build.scala

sed -i -e '/de.johoop/d' config/build.sbt
sed -i -e '/JacocoPlugin/d' config/build.sbt
sed -i -e '/findbugs/,+2d' config/build.sbt
sed -i -e '/jacoco/,+2d' config/build.sbt

sed -i -e '/% "test"$/,+2d' config/build.sbt

sed -i -e '/com.typesafe.sbt/d' build.sbt
sed -i -e '/SbtGit/,+2d' build.sbt
sed -i -e '/useGpg/,+2d' build.sbt
sed -i -e '/publishSigned/,+2d' build.sbt
sed -i -e '/publishLocalSigned/,+2d' build.sbt

sed -i -e 's/2[.]10[.][0-2]/2.10.3/' build.sbt

sed -i -e 's/Some("1[.]6")/Some("1.7")/' project/JavaVersionCheck.scala

for buildsbt in $(find . -name build.sbt) ; do
    (echo ; echo ; echo 'version := "%{version}"'; echo) >> $buildsbt
done

# missing test deps
rm -rf config/src/test

cp -r /usr/share/sbt/ivy-local .
mkdir boot


%build
export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local

#sbt package "set publishTo in Global := Some(Resolver.file(\"published\", file(\"published\"))(Resolver.ivyStylePatterns) ivys \"$(pwd)/published/[organization]/[module]/[revision]/ivy.xml\" artifacts \"$(pwd)/published/[organization]/[module]/[revision]/[artifact]-[revision].[ext]\")" publish makePom
sbt package makePom deliverLocal doc

%install

mkdir -p %{buildroot}%{_javadir}
cp -p config/target/config-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 config/target/config-%{version}.pom %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp config/target/api/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE-2.0.txt NEWS.md README.md

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE-2.0.txt

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1.2.0-4
- 为 Magic 3.0 重建

* Wed Aug 13 2014 Liu Di <liudidi@gmail.com> - 1.2.0-3
- 为 Magic 3.0 重建

* Mon Feb 24 2014 William Benton <willb@redhat.com> 1.2.0-2
- updated to use sbt build

* Tue Feb 04 2014 gil cattaneo <puntogil@libero.it> 1.2.0-1
- initial rpm
