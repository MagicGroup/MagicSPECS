Name:           plexus-containers
Version:        1.6
Release:        4%{?dist}
Summary:        Containers for Plexus
License:        ASL 2.0 and MIT
URL:            https://github.com/codehaus-plexus/plexus-containers
BuildArch:      noarch

Source0:        https://github.com/sonatype/%{name}/archive/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  maven-invoker-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-shared-invoker
BuildRequires:  maven-release
BuildRequires:  maven-plugin-plugin
BuildRequires:  plexus-classworlds >= 2.5
BuildRequires:  plexus-utils
BuildRequires:  plexus-cli
BuildRequires:  xbean >= 3.14
BuildRequires:  guava
BuildRequires:  objectweb-asm >= 5.0.2
BuildRequires:  qdox >= 2.0


%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package component-metadata
Summary:        Component metadata from %{name}

%description component-metadata
%{summary}.

%package component-javadoc
Summary:        Javadoc component from %{name}

%description component-javadoc
%{summary}.

%package component-annotations
Summary:        Component API from %{name}

%description component-annotations
%{summary}.

%package container-default
Summary:        Default Container from %{name}
Obsoletes:      plexus-container-default < 1.0-1
Provides:       plexus-containers-component-api = %{version}-%{release}

%description container-default
%{summary}.

%package javadoc
Summary:        API documentation for all plexus-containers packages
Group:          Documentation
Provides:       %{name}-component-annotations-javadoc = %{version}-%{release}
Obsoletes:      %{name}-component-annotations-javadoc < %{version}-%{release}
Provides:       %{name}-component-javadoc-javadoc = %{version}-%{release}
Obsoletes:      %{name}-component-javadoc-javadoc < %{version}-%{release}
Provides:       %{name}-component-metadata-javadoc = %{version}-%{release}
Obsoletes:      %{name}-component-metadata-javadoc < %{version}-%{release}
Provides:       %{name}-container-default-javadoc = %{version}-%{release}
Obsoletes:      %{name}-container-default-javadoc < %{version}-%{release}

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{name}-%{version}

# For Maven 3 compat
%pom_add_dep org.apache.maven:maven-core plexus-component-metadata

# ASM dependency was changed to "provided" in XBean 4.x, so we need to provide ASM
%pom_add_dep org.ow2.asm:asm:5.0.3:runtime plexus-container-default
%pom_add_dep org.ow2.asm:asm-commons:5.0.3:runtime plexus-container-default

%pom_remove_dep com.sun:tools plexus-component-javadoc
%pom_add_dep com.sun:tools plexus-component-javadoc

# Generate OSGI info
%pom_xpath_inject "pom:project" "
    <packaging>bundle</packaging>
    <build>
      <plugins>
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <configuration>
            <instructions>
              <_nouses>true</_nouses>
              <Export-Package>org.codehaus.plexus.component.annotations.*</Export-Package>
            </instructions>
          </configuration>
        </plugin>
      </plugins>
    </build>" plexus-component-annotations

# to prevent ant from failing
mkdir -p plexus-component-annotations/src/test/java

# integration tests fix
sed -i "s|<version>2.3</version>|<version> %{javadoc_plugin_version}</version>|" plexus-component-javadoc/src/it/basic/pom.xml

# plexus-component-api has been merged into plexus-container-default
%mvn_alias ":plexus-container-default" "org.codehaus.plexus:containers-component-api"

# keep compat symlink for maven's sake
%mvn_file ":plexus-component-annotations" %{name}/plexus-component-annotations plexus/containers-component-annotations

%build
%mvn_build -f -s

%install
%mvn_install


# plexus-containers pom goes into main package
%files -f .mfiles-plexus-containers
%files component-annotations -f .mfiles-plexus-component-annotations
%files container-default -f .mfiles-plexus-container-default
%files component-metadata -f .mfiles-plexus-component-metadata
%files component-javadoc -f .mfiles-plexus-component-javadoc

%files javadoc -f .mfiles-javadoc

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-3
- Update upstream URL

* Thu Feb  5 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-2
- Add runtime dependenty on ASM5

* Mon Oct 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-1
- Update to upstream version 1.6

* Mon Oct  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.5-20
- Obsolete plexus-container-default

* Wed Sep 24 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.5-19
- Remove verioned build-requires on maven-javadoc-plugin

* Fri Jul 04 2014 Mat Booth <mat.booth@redhat.com> - 1.5.5-18
- Port to lastest objectweb-asm

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Michal Srb <msrb@redhat.com> - 1.5.5-16
- Drop empty .mfiles

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-15
- Use Requires: java-headless rebuild (#1067528)

* Thu Dec  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.5-14
- Update to Plexus Classworlds 2.5, resolves: rhbz#1015124
- Require xbean >= 3.14, resolves: rhbz#1038607

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.5-12
- Generate OSGi metadata
- Resolves: rhbz#987116
- Bump maven-javadoc-plugin version to 2.9.1

* Fri Mar 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5.5-11
- Correctly place plexus-containers POM in the main package

* Thu Mar 21 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-11
- Add compat symlinks to keep Maven working

* Wed Mar 20 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-10
- Update to latest packaging guidelines
- Remove several unneeded buildrequires

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.5.5-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Nov 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-7
- Fix license tag (Plexus license was replaced by MIT some time ago)
- Update javadoc plugin BR version

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> - 1.5.5-5
- Resolves rhbz#791339
- Applied fix from Omair Majid <omajid at redhat dot com> to build with Java 7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-3
- Fix maven3 build
- Use new add_maven_depmap macro

* Mon Feb 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-2
- Remove unneeded env var definitions

* Fri Feb 25 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-1
- Update to latest upstream
- Remove obsolete patches
- Use maven 3 to build
- Packaging fixes
- Versionless jars & javadocs

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.4-4
- Add plexus-cli to component-metadata Requires

* Wed Sep  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.4-3
- Use javadoc:aggregate
- Merge javadoc subpackages into one -javadoc

* Thu Jul 15 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.4-2
- Fix maven depmaps

* Tue Jul 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.4-1
- Version bump
- Add new sub-packages
- Cleanups

* Thu Aug 20 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.1.a34.7
- Clean up javadoc post/postun
- Build with ant
- Remove gcj support
- Clean up groups

* Fri May 15 2009 Fernando Nasser <fnasser@redhat.com> 1.0-0.1.a34.6
- Fix license

* Tue Apr 28 2009 Yong Yang <yyang@redhat.com> 1.0-0.1.a34.5
- Add BRs maven2-plugin-surfire*, maven-doxia*
- Merge from RHEL-4-EP-5 1.0-0.1.a34.2, add plexus-containers-sourcetarget.patch
- Rebuild with new maven2 2.0.8 built in non-bootstrap mode

* Mon Mar 16 2009 Yong Yang <yyang@redhat.com> 1.0-0.1.a34.4
- rebuild with new maven2 2.0.8 built in bootstrap mode

* Wed Feb 04 2009 Yong Yang <yyang@redhat.com> - 1.0-0.1.a34.3
- re-build with maven

* Wed Feb 04 2009 Yong Yang <yyang@redhat.com> - 1.0-0.1.a34.2
- fix bulding with ant
- temporarily buid with ant

* Wed Jan 14 2009 Yong Yang <yyang@redhat.com> - 1.0-0.1.a34.1jpp.2
- re-build with maven
- disabled assert in plexus-container-default/.../UriConverter.java???

* Tue Jan 13 2009 Yong Yang <yyang@redhat.com> - 1.0-0.1.a34.1jpp.1
- Imported into devel from dbhole's maven 2.0.8 packages

* Tue Apr 08 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a34.0jpp.1
- Initial build with original base spec from JPackage
