Name:          jts
Version:       1.13
Release:       2%{?dist}
Summary:       Java Topology Suite
License:       LGPLv2+
URL:           http://sourceforge.net/projects/jts-topo-suite
# sh jts-create-tarball.sh < VERSION >
Source0:       %{name}-%{version}.tar.xz
Source1:       %{name}-create-tarball.sh

BuildRequires: maven-local
BuildRequires: maven-plugin-build-helper

BuildArch:     noarch

%description
The JTS Topology Suite is an API for modelling and
manipulating 2-dimensional linear geometry. It provides
numerous geometric predicates and functions. JTS
conforms to the Simple Features Specification for
SQL published by the Open GIS Consortium.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

%pom_remove_plugin :maven-source-plugin
%pom_xpath_remove "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"

%pom_add_plugin org.apache.maven.plugins:maven-jar-plugin . "
<configuration>
  <archive>
    <manifestFile>java/src/MANIFEST.MF</manifestFile>
  </archive>
</configuration>"

sed -i "s,59 Temple Place,51 Franklin Street,;s,Suite 330,Fifth Floor,;s,02111-1307,02110-1301," doc/LICENSE.txt $(find . -type f -name "*.java")
sed -i 's/\r//' doc/LICENSE.txt

%build

%mvn_file : %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc doc/LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc doc/LICENSE.txt

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 26 2013 gil cattaneo <puntogil@libero.it> 1.13-1
- initial rpm