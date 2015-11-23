Name:           maven-site-plugin
Version:        3.4
Release:        4%{?dist}
Summary:        Maven Site Plugin
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-site-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
BuildArch:      noarch

Patch0:         0001-Port-to-jetty-9.patch
Patch1:         0001-Fix-jetty-dependencies.patch
# Jetty is needed only in interactive mode of maven-site-plugin. Change
# dependency scope from compile to provided to reduce dependency bloat.
Patch2:         %{name}-jetty-provided.patch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-decoration-model)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-integration-tools)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-logging-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-xdoc)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-xhtml)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-markdown)
BuildRequires:  mvn(org.apache.maven:maven-archiver)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.apache.maven:maven-settings-builder)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-exec)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  mvn(org.apache.velocity:velocity)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-i18n)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus-velocity)
BuildRequires:  mvn(org.eclipse.jetty:jetty-server)
BuildRequires:  mvn(org.eclipse.jetty:jetty-servlet)
BuildRequires:  mvn(org.eclipse.jetty:jetty-util)
BuildRequires:  mvn(org.eclipse.jetty:jetty-webapp)

%description
The Maven Site Plugin is a plugin that generates a site for the current project.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2

%build
# skipping tests because we need to fix them first for jetty update
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Michael Simacek <msimacek@redhat.com> - 3.4-3
- Add BR doxia-module-markdown

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4-2
- Remove legacy Obsoletes/Provides for maven2 plugin

* Sun Jul 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4-1
- Update to upstream version 3.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.3-4
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3-3
- Fix unowned directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3-1
- Update to upstream version 3.3

* Fri Mar  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-4
- Merge branch 'port-to-jetty-9' into master

* Tue Feb 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-3
- Change jetty dependency scope to provided

* Mon Feb 25 2013 Michal Srb <msrb@redhat.com> - 3.2-3
- Port to jetty 9.0.0

* Thu Feb 07 2013 Michal Srb <msrb@redhat.com> - 3.2-2
- Migrate from maven-doxia to doxia subpackages

* Thu Jan 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-1
- Update to upstream version 3.2
- Build with xmvn

* Tue Oct 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-3
- Don't require full jetty, only minimal set of subpackages

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-1
- Updatw to upstream 3.1

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 3.0-5
- BR/R servlet 3.

* Thu Jan 26 2012 Alexander Kurtakov <akurtako@redhat.com> 3.0-4
- Add BR/R on jetty-parent.

* Thu Jan 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-3
- Port for jetty 8.1.0
- Small spec cleanups

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 Alexander Kurtakov <akurtako@redhat.com> 3.0-1
- Update to upstream 3.0 release.

* Thu Jul 21 2011 Jaromir Capik <jcapik@redhat.com> - 2.3-3
- Removal of plexus-maven-plugin dependency (not needed)

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3-2
- Add several missing things to (Build)Requires
- Fix build for maven3-only buildroot

* Wed May 25 2011 Alexander Kurtakov <akurtako@redhat.com> 2.3-1
- Update to new upstream version.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2-1
- Update to new upstream version.

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1-3
- Requires maven-doxia-tools.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1-2
- Fix requires.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1-1
- Initial package.
