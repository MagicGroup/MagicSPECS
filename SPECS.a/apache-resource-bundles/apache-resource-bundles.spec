%global jar_version 1.4
%global lh_version 1.1
%global id_version 1.1

Name:		apache-resource-bundles
Version:	2
Release:	13%{?dist}
Summary:	Apache Resource Bundles

Group:		Development/Libraries
License:	ASL 2.0
URL:		http://repo1.maven.org/maven2/org/apache/apache-resource-bundles/
Source0:	http://repo1.maven.org/maven2/org/apache/%{name}/%{version}/%{name}-%{version}.pom
Source1:	http://repo1.maven.org/maven2/org/apache/apache-jar-resource-bundle/%{jar_version}/apache-jar-resource-bundle-%{jar_version}-sources.jar
Source2:	http://repo1.maven.org/maven2/org/apache/apache-jar-resource-bundle/%{jar_version}/apache-jar-resource-bundle-%{jar_version}.pom
Source3:	http://repo1.maven.org/maven2/org/apache/apache-license-header-resource-bundle/%{lh_version}/apache-license-header-resource-bundle-%{lh_version}-sources.jar
Source4:	http://repo1.maven.org/maven2/org/apache/apache-license-header-resource-bundle/%{lh_version}/apache-license-header-resource-bundle-%{lh_version}.pom
Source5:	http://repo1.maven.org/maven2/org/apache/apache-incubator-disclaimer-resource-bundle/%{id_version}/apache-incubator-disclaimer-resource-bundle-%{id_version}-sources.jar
Source6:	http://repo1.maven.org/maven2/org/apache/apache-incubator-disclaimer-resource-bundle/%{id_version}/apache-incubator-disclaimer-resource-bundle-%{id_version}.pom

BuildRequires:	maven-local
BuildRequires:	maven-compiler-plugin
BuildRequires:	maven-install-plugin
BuildRequires:	maven-jar-plugin
BuildRequires:	maven-remote-resources-plugin
BuildRequires:	maven-resources-plugin
BuildRequires:	maven-surefire-plugin
BuildRequires:  maven-site-plugin

BuildArch:	noarch

%description
An archive which contains templates for generating the necessary license files
and notices for all Apache releases.

%prep
%setup -c -T
cp %SOURCE0 ./pom.xml

# jar
mkdir -p apache-jar-resource-bundle
pushd apache-jar-resource-bundle
jar xvf %SOURCE1
cp %SOURCE2 ./pom.xml
mkdir -p src/main/resources
mv META-INF src/main/resources
popd

# license-header
mkdir -p apache-license-header-resource-bundle
pushd apache-license-header-resource-bundle
jar xvf %SOURCE3
cp %SOURCE4 ./pom.xml
mkdir -p src/main/resources
mv META-INF src/main/resources
popd

# incubator-disclaimer
mkdir -p apache-incubator-disclaimer-resource-bundle
pushd apache-incubator-disclaimer-resource-bundle
jar xvf %SOURCE5
cp %SOURCE6 ./pom.xml
mkdir -p src/main/resources
mv META-INF src/main/resources
popd


%build
%mvn_file :apache-jar-resource-bundle apache-resource-bundles/jar
%mvn_file :apache-license-header-resource-bundle apache-resource-bundles/license-header
%mvn_file :apache-incubator-disclaimer-resource-bundle apache-resource-bundles/incubator-disclaimer
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}

%changelog
* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2-13
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2-12
- Fix unowned directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan 16 2013 Michal Srb <msrb@redhat.com> - 2-9
- Build with xmvn

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2-5
- Fix pom file names and add_to_maven_depmap calls (Resolves rhbz#655790)

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 2-4
- Add maven-site-plugin BR.
- Use newer names of maven plugins.

* Mon Feb  1 2010 Mary Ellen Foster <mefoster at gmail.com> 2-3
- Fix license 

* Tue Jan 19 2010 Mary Ellen Foster <mefoster at gmail.com> 2-2
- Add plugin dependencies from POMs
- Fix description
- Remove maven-release plugin (not on Fedora yet)

* Mon Jan 18 2010 Mary Ellen Foster <mefoster at gmail.com> 2-1
- Initial package
