%global project   felix
%global bundle    org.apache.felix.gogo.runtime

%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package %{project}-gogo-runtime}

Name:           %{?scl_prefix}%{project}-gogo-runtime
Version:        0.12.1
Release:        1%{?dist}
Summary:        Community OSGi R4 Service Platform Implementation - Basic Commands
License:        ASL 2.0
URL:            http://felix.apache.org/site/apache-felix-gogo.html

Source0:        http://www.mirrorservice.org/sites/ftp.apache.org//felix/org.apache.felix.gogo.runtime-%{version}-project.tar.gz 

# Typecast an Event constructor call with java.util.Properties to 
# java.util.Dictionary because the call to the constructor with Properties
# was ambiguous.
Patch1:         %{pkg_name}-dictionary.patch
# Changed path to DEPENDENCIES, LICENSE and NOTICE from META-INF to root dir
Patch2:         %{pkg_name}-bundle-resources.patch
# Removed failing thread IO test
Patch3:         %{pkg_name}-deleted-io-test.patch
# Removed relativePath to parent pom
Patch4:         %{pkg_name}-parent.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:gogo-parent:pom:)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(org.mockito:mockito-all)
BuildRequires:  mvn(org.osgi:org.osgi.compendium)
BuildRequires:  mvn(org.osgi:org.osgi.core)

%{?scl:BuildRequires:	  %{?scl_prefix}build}

%{?scl:Requires: %scl_runtime}

%description
Apache Felix is a community effort to implement the OSGi R4 Service Platform
and other interesting OSGi-related technologies under the Apache license. The
OSGi specifications originally targeted embedded devices and home services
gateways, but they are ideally suited for any project interested in the
principles of modularity, component-orientation, and/or service-orientation.
OSGi technology combines aspects of these aforementioned principles to define a
dynamic service deployment framework that is amenable to remote management.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{bundle}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%mvn_file : %{project}/%{name}

%build
%{?scl:%scl_maven_opts}
%mvn_build

%install
%mvn_install


%files -f .mfiles
%dir %{_javadir}/%{project}
%doc DEPENDENCIES LICENSE NOTICE 

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Thu Jul 3 2014 Alexander Kurtakov <akurtako@redhat.com> 0.12.1-1
- Update to upstream 0.12.1.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.10.0-11
- Use Requires: java-headless rebuild (#1067528)

* Tue Aug 06 2013 Michal Srb <msrb@redhat.com> - 0.10.0-10
- Adapt to current guidelines
- Install NOTICE file with javadoc subpackage

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.10.0-8
- Initial SCLization.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.10.0-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 18 2012 Tomas Radej <tradej@redhat.com> - 0.10.0-4
- Changed jar path

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Tomas Radej <tradej@redhat.com> - 0.10.0-2
- Repackaged, minor changes

* Mon Nov 07 2011 Tomas Radej <tradej@redhat.com> - 0.10.0-1
- Initial packaging
