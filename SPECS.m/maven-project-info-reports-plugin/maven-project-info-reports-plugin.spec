Name:           maven-project-info-reports-plugin
Version:        2.7
Release:        7%{?dist}
Summary:        Maven Project Info Reports Plugin
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-project-info-reports-plugin/
BuildArch:      noarch

Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch0:         0001-Update-to-Doxia-1.6.patch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-validator:commons-validator)
BuildRequires:  mvn(joda-time:joda-time)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-decoration-model)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-logging-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-xhtml)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven:maven-repository-metadata)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jarsigner-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-impl)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-api)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-manager-plexus)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-provider-cvs-commons)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-provider-cvsexe)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-provider-git-commons)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-provider-gitexe)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-provider-hg)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-provider-perforce)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-provider-starteam)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-provider-svn-commons)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-provider-svnexe)
BuildRequires:  mvn(org.apache.maven.shared:maven-dependency-tree)
BuildRequires:  mvn(org.apache.maven.shared:maven-doxia-tools)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-jar)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-file)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-http-lightweight)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-ssh)
BuildRequires:  mvn(org.codehaus.mojo:keytool-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-i18n)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

%description
The Maven Project Info Reports Plugin is a plugin 
that generates standard reports for the specified project.
  

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.


%prep
%setup -q -c
mv %{name}-%{version}/* .
%patch0 -p1
# removed cvsjava provider since we don't support it anymore
%pom_remove_dep :maven-scm-provider-cvsjava

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles

%files javadoc -f .mfiles-javadoc

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 2.7-7
- 为 Magic 3.0 重建

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-6
- Port to Doxia 1.6

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-4
- Update to current packaging guidelines

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.7-3
- Use Requires: java-headless rebuild (#1067528)

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-2
- Migrate to Wagon subpackages

* Mon Jul 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-1
- Update to upstream version 2.7
- Don't install artifacts in local repository

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-5
- Remove dependencies with test scope

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-4
- Add missing Requires on doxia packages
- Resolves: rhbz#909250

* Fri Feb 08 2013 Michal Srb <msrb@redhat.com> - 2.6-3
- Migrate from maven-doxia to doxia subpackages (Resolves: #909250)
- Add BR on maven-local

* Tue Dec 11 2012 Michal Srb <msrb@redhat.com> - 2.6-2
- Migrated to plexus-containers-container-default (Resolves: #878559)
- Removed build dependency on netbeans-cvsclient

* Mon Oct 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-1
- Update to upstream version 2.6

* Tue Sep 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.1-1
- Update to upstream version 2.5.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4-6
- Remove cvsjava support (still can use cvsexe)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 5 2011 Alexander Kurtakov <akurtako@redhat.com> 2.4-4
- One more missing R - joda-time.

* Mon Sep 5 2011 Alexander Kurtakov <akurtako@redhat.com> 2.4-3
- Requires maven-scm.

* Mon Sep 5 2011 Alexander Kurtakov <akurtako@redhat.com> 2.4-2
- Add missing R.

* Mon May 30 2011 Alexander Kurtakov <akurtako@redhat.com> 2.4-1
- Update to upstream version 2.4.

* Mon May 23 2011 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-1
- UPdate to upstream version 2.3.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 9 2010 Chris Spike <chris.spike@arcor.de> 2.2-5
- Removed obsolete patch
- tomcat5 -> tomcat6 BRs/Rs

* Tue Oct 26 2010 akurtakov <akurtakov@redhat.com> 2.2-4
- Fix apache-commons-validator BR/R.

* Thu Sep 09 2010 Hui Wang <huwang@redhat.com> - 2.2-3
- Add missing BR netbeans-cvsclient

* Mon Jun 07 2010 Hui Wang <huwang@redhat.com> - 2.2-2
- Added missing requires

* Thu Jun 02 2010 Hui Wang <huwang@redhat.com> - 2.2-1
- Initial version of the package
