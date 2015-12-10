Name:           maven-release
Version:        2.2.1
Release:        16%{?dist}
Summary:        Release a project updating the POM and tagging in the SCM
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-release-plugin/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/release/%{name}/%{version}/%{name}-%{version}-source-release.zip
# Remove deps needed for tests, till jmock gets packaged
Patch1:         002-mavenrelease-fixbuild.patch
Patch2:         003-fixing-migration-to-component-metadata.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1015123
Patch3:         %{name}-ftbfs.patch

BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  maven-local
BuildRequires:  maven-scm
BuildRequires:  maven-antrun-plugin
BuildRequires:  maven-source-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  modello
BuildRequires:  plexus-containers-component-metadata
BuildRequires:  plexus-utils
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  jaxen

%description
This plugin is used to release a project with Maven, saving a lot of 
repetitive, manual work. Releasing a project is made in two steps: 
prepare and perform.

%package manager
Summary:        Release a project updating the POM and tagging in the SCM

%description manager
This package contains %{name}-manager needed by %{name}-plugin.

%package plugin
Summary:        Release a project updating the POM and tagging in the SCM

%description plugin
This plugin is used to release a project with Maven, saving a lot of
repetitive, manual work. Releasing a project is made in two steps:
prepare and perform.

%package javadoc
Summary:        Javadoc for %{name}
Provides:       %{name}-manager-javadoc = %{version}-%{release}
Obsoletes:      %{name}-manager-javadoc <= 2.0-1
Provides:       %{name}-plugin-javadoc = %{version}-%{release}
Obsoletes:      %{name}-plugin-javadoc <= 2.0-1

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1

cat > README << EOT
%{name}-%{version}

This plugin is used to release a project with Maven, saving a lot of
repetitive, manual work. Releasing a project is made in two steps:
prepare and perform.
EOT


%build

%mvn_file :%{name}-manager %{name}-manager
%mvn_file :%{name}-plugin %{name}-plugin
%mvn_package :%{name}-manager manager
%mvn_package :%{name}-plugin plugin
# Skip tests because we don't have dependencies (jmock)
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE README

%files manager -f .mfiles-manager
%doc LICENSE NOTICE

%files plugin -f .mfiles-plugin
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 2.2.1-16
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.2.1-15
- 为 Magic 3.0 重建

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 2.2.1-14
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Michal Srb <msrb@redhat.com> - 2.2.1-12
- Rebuild to regenerate auto-requires

* Wed Mar 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-11
- Add missing BR on modello
- Resolves: rhbz#1077909

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-10
- Use Requires: java-headless rebuild (#1067528)

* Wed Jan 08 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.2.1-10
- fix rhbz#1015123

* Mon Aug 12 2013 gil cattaneo <puntogil@libero.it> 2.2.1-9
- fix rhbz#984875, rhbz#992200
- fix some rpmlint problems
- update to current packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.1-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Sep 17 2012 Jaromir Capik <jcapik@redhat.com> - 2.2.1-5
- Fixing incomplete migration to component metadata

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-4
- Remove BR: maven-scm-test

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-1
- Update to latest upstream release.
- Adapt to current guidelines.

* Tue Jul 26 2011 Guido Grazioli <guido.grazioli@gmail.com> - 2.2-3
- Reinclude maven-scm-test in BRs

* Tue Jul 26 2011 Guido Grazioli <guido.grazioli@gmail.com> - 2.2-2
- Import patch provided by Jaromír Cápík (#725088)

* Mon Jul 18 2011 Guido Grazioli <guido.grazioli@gmail.com> - 2.2-1
- Update to 2.2
- Update to current guidelines
- Build with maven 3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 3 2011 Alexander Kurtakov <akurtako@redhat.com> 2.0-2
- Drop tomcat5 BRs.
- Drop versioned jars.

* Mon Sep 13 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-1
- Update to upstream 2.0

* Sat Sep 11 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.4
- Fix build requires
- Use javadoc:aggregate goal

* Tue May 25 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.3
- Fix build requires

* Mon May 10 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.2
- Fix release tag
- Better macro usage

* Mon Apr 26 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.1
- Install maven-release-parent pom in dedicated package
- Patch maven-release-plugin to skip helpmojo goal
- Patch to skip tests depending on (unpackaged) jmock

* Fri Apr 16 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn
- Initial packaging
