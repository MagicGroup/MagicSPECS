Name: apache-mina
Version: 2.0.7
Release: 3%{?dist}
Summary: Apache MINA
Group: Development/Libraries
License: ASL 2.0
URL: http://mina.apache.org
Source0: http://mina.apache.org/dyn/closer.cgi/mina/%{version}/%{name}-%{version}-src.tar.gz
BuildArch: noarch

BuildRequires: maven-local

BuildRequires: apache-commons-lang
BuildRequires: easymock
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-shared
BuildRequires: maven-site-plugin
BuildRequires: maven-surefire-plugin


%description
Apache MINA is a network application framework which helps users develop high
performance and high scalability network applications easily. It provides an
abstract event-driven asynchronous API over various transports such as TCP/IP
and UDP/IP via Java NIO.


%package javadoc
Summary: API documentation for %{name}
Group: Documentation


%description javadoc
This package provides %{name}.


%prep

# Extract the source:
%setup -q

# In the tarball distributed by Apache the source code is inside the src
# directory, but our build tools expect the POM files in the current directory,
# so in order to simplify things we move everything to the top level before
# starting the build:
mv src/* .

# The modules use "bundle" packaging which doesn't work correctly with xmvn
# automatic dependency generation, in order to avoid that we change that to
# "jar":
sed -i \
    -e 's|<packaging>bundle</packaging>|<packaging>jar</packaging>|g' \
    -e 's|<type>bundle</type>|<type>jar</type>|g' \
    $(find . -name pom.xml)

# Disable the plugins that we don't need:
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-bundle-plugin

# Disable the modules that we can't currently build:
%pom_disable_module mina-legal
%pom_disable_module mina-transport-apr
%pom_disable_module mina-integration-beans
%pom_disable_module mina-integration-xbean
%pom_disable_module mina-integration-ognl
%pom_disable_module mina-integration-jmx
%pom_disable_module mina-example


%build

# The tests are disabled because they require EasyMock version 2 and we only
# have version 3:
%mvn_build -f


%install
%mvn_install


%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE.txt
%doc NOTICE.txt


%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt
%doc NOTICE.txt


%changelog
* Fri Aug 15 2014 Liu Di <liudidi@gmail.com> - 2.0.7-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 30 2013 Juan Hernandez <juan.hernandez@redhat.com> 2.0.7-1
- Update to upstream 2.0.7
- Build with xmvn

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Orion Poplawski <orion@cora.nwra.com> - 2.0.4-7
- Own the jar directory, use .mfiles
- Add BR/Requires on mvn(org.easymock:easymockclassextension)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.0.4-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jul 24 2012 Juan Hernandez <juan.hernandez@redhat.com> - 2.0.4-4
- Add pmd build time requirement

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.0.4-2
- Use the complete URL of the source code tarball

* Sun Feb 12 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.0.4-1
- Initial packaging

