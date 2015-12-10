%if 0%{?fedora}
%bcond_without extensions
%endif

%global short_name guice

Name:           google-%{short_name}
Version:        3.2.2
Release:        4%{?dist}
Summary:        Lightweight dependency injection framework for Java 5 and above
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/sonatype/sisu-%{short_name}
# ./create-tarball.sh %%{version}
Source0:        %{name}-%{version}.tar.xz
Source1:        create-tarball.sh
BuildArch:      noarch

BuildRequires:  maven-local >= 3.2.4-2
BuildRequires:  maven-remote-resources-plugin
BuildRequires:  munge-maven-plugin
BuildRequires:  apache-resource-bundles
BuildRequires:  aopalliance
BuildRequires:  atinject
BuildRequires:  cglib
BuildRequires:  guava
BuildRequires:  slf4j

%if %{with extensions}
BuildRequires:  hibernate-jpa-2.0-api
BuildRequires:  springframework-beans
BuildRequires:  tomcat-servlet-3.0-api
%endif

# Test dependencies:
%if 0
BuildRequires:  maven-surefire-provider-testng
BuildRequires:  aqute-bnd
BuildRequires:  atinject-tck
BuildRequires:  easymock2
BuildRequires:  felix-framework
BuildRequires:  hibernate3-entitymanager
BuildRequires:  mvn(org.hsqldb:hsqldb-j5)
BuildRequires:  testng
%endif

Provides:       %{short_name} = %{version}-%{release}

%description
Put simply, Guice alleviates the need for factories and the use of new
in your Java code. Think of Guice's @Inject as the new new. You will
still need to write factories in some cases, but your code will not
depend directly on them. Your code will be easier to change, unit test
and reuse in other contexts.

Guice embraces Java's type safe nature, especially when it comes to
features introduced in Java 5 such as generics and annotations. You
might think of Guice as filling in missing features for core
Java. Ideally, the language itself would provide most of the same
features, but until such a language comes along, we have Guice.

Guice helps you design better APIs, and the Guice API itself sets a
good example. Guice is not a kitchen sink. We justify each feature
with at least three use cases. When in doubt, we leave it out. We
build general functionality which enables you to extend Guice rather
than adding every feature to the core framework.

%package -n %{short_name}-parent
Summary:        Guice parent POM

%description -n %{short_name}-parent
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides parent POM for Guice modules.

%if %{with extensions}

%package -n %{short_name}-assistedinject
Summary:        AssistedInject extension module for Guice

%description -n %{short_name}-assistedinject
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides AssistedInject module for Guice.

%package -n %{short_name}-extensions
Summary:        Extensions for Guice

%description -n %{short_name}-extensions
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides extensions POM for Guice.

%package -n %{short_name}-grapher
Summary:        Grapher extension module for Guice

%description -n %{short_name}-grapher
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Grapher module for Guice.

%package -n %{short_name}-jmx
Summary:        JMX extension module for Guice

%description -n %{short_name}-jmx
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JMX module for Guice.

%package -n %{short_name}-jndi
Summary:        JNDI extension module for Guice

%description -n %{short_name}-jndi
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JNDI module for Guice.

%package -n %{short_name}-multibindings
Summary:        MultiBindings extension module for Guice

%description -n %{short_name}-multibindings
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides MultiBindings module for Guice.

%package -n %{short_name}-persist
Summary:        Persist extension module for Guice

%description -n %{short_name}-persist
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Persist module for Guice.

%package -n %{short_name}-servlet
Summary:        Servlet extension module for Guice

%description -n %{short_name}-servlet
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Servlet module for Guice.

%package -n %{short_name}-spring
Summary:        Spring extension module for Guice

%description -n %{short_name}-spring
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Spring module for Guice.

%package -n %{short_name}-testlib
Summary:        TestLib extension module for Guice

%description -n %{short_name}-testlib
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides TestLib module for Guice.

%package -n %{short_name}-throwingproviders
Summary:        ThrowingProviders extension module for Guice

%description -n %{short_name}-throwingproviders
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides ThrowingProviders module for Guice.

%endif # with extensions

%package javadoc
Summary:        API documentation for Guice
Group:          Documentation
Provides:       %{short_name}-javadoc = %{version}-%{release}

%description javadoc
This package provides %{summary}.


%prep
%setup -q -n %{name}-%{version}

# We don't have struts2 in Fedora yet.
%pom_disable_module struts2 extensions

# Remove additional build profiles, which we don't use anyways
# and which are only pulling additional dependencies.
%pom_xpath_remove "pom:profile[pom:id='guice.with.jarjar']" core

# Animal sniffer is only causing problems. Disable it for now.
%pom_remove_plugin :animal-sniffer-maven-plugin core
%pom_remove_plugin :animal-sniffer-maven-plugin extensions

# We don't have the custom doclet used by upstream. Remove
# maven-javadoc-plugin to generate javadocs with default style.
%pom_remove_plugin :maven-javadoc-plugin

%pom_remove_dep javax.persistence:persistence-api extensions/persist
%pom_add_dep org.hibernate.javax.persistence:hibernate-jpa-2.0-api extensions/persist

# remove test dependency to make sure we don't produce requires
# see #1007498
%pom_remove_dep :guava-testlib extensions
%pom_xpath_remove "pom:dependency[pom:classifier[text()='tests']]" extensions

# Don't try to build extension modules unless they are needed
%if %{without extensions}
%pom_disable_module extensions
%endif


%build
%if %{with extensions}
%mvn_alias ":guice-{assistedinject,grapher,jmx,jndi,multibindings,persist,\
servlet,spring,throwingproviders}" "com.google.inject.extensions:guice-@1"
%endif # with extensions

%mvn_package :::no_aop: sisu-guice

%mvn_file  ":guice-{*}"  %{short_name}/guice-@1
%mvn_file  ":sisu-guice" %{short_name}/%{name} %{name}
%mvn_alias ":sisu-guice" "com.google.inject:guice"
# Skip tests because of missing dependency (hsqldb-j5).
%mvn_build -f -s

%install
%mvn_install

%files -f .mfiles-sisu-guice
%dir %{_javadir}/%{short_name}

%files -n %{short_name}-parent -f .mfiles-guice-parent
%doc COPYING

%if %{with extensions}
%files -n %{short_name}-assistedinject -f .mfiles-guice-assistedinject
%files -n %{short_name}-extensions -f .mfiles-extensions-parent
%files -n %{short_name}-grapher -f .mfiles-guice-grapher
%files -n %{short_name}-jmx -f .mfiles-guice-jmx
%files -n %{short_name}-jndi -f .mfiles-guice-jndi
%files -n %{short_name}-multibindings -f .mfiles-guice-multibindings
%files -n %{short_name}-persist -f .mfiles-guice-persist
%files -n %{short_name}-servlet -f .mfiles-guice-servlet
%files -n %{short_name}-spring -f .mfiles-guice-spring
%files -n %{short_name}-testlib -f .mfiles-guice-testlib
%files -n %{short_name}-throwingproviders -f .mfiles-guice-throwingproviders
%endif # with extensions

%files javadoc -f .mfiles-javadoc
%doc COPYING


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.2.2-4
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 3.2.2-3
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 3.2.2-2
- 为 Magic 3.0 重建

* Fri Jun  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.2-1
- Update to upstream version 3.2.2

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-2
- Rebuild to regenerate Maven auto-requires

* Wed Apr 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-1
- Update to upstream version 3.2.1
- Add testlib subpackage

* Tue Mar  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.10-3
- Fix directory ownership

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.10-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.10-2
- Fix unowned directory

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.10-1
- Update to upstream version 3.1.10

* Mon Jan 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.9-1
- Update to upstream version 3.1.9

* Mon Nov 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.8-1
- Update to upstream version 3.1.8

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-10
- Rebuild to regenerate broken POMs
- Related: rhbz#1021484

* Fri Oct 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-9
- Don't force generation of pom.properties

* Wed Sep 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-8
- Install no_aop artifact after javapackages update

* Thu Sep 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.3-7
- Remove dependency on tests from runtime
- Related: rhbz#1007498

* Tue Sep 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-6
- Install no_aop artifact
- Resolves: rhbz#1006491

* Wed Sep  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-5
- Enable pom.properties
- Resolves: rhbz#1004360

* Wed Aug 07 2013 Michal Srb <msrb@redhat.com> - 3.1.3-4
- Add create-tarball.sh script to SRPM

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 24 2013 Michal Srb <msrb@redhat.com> - 3.1.3-2
- Revert update to 3.1.4 (uses asm4)

* Thu Mar 14 2013 Michal Srb <msrb@redhat.com> - 3.1.3-1
- Update to upstream version 3.1.3
- Remove bundled JARs from tarball

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.1.2-11
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 31 2013 Michal Srb <msrb@redhat.com> - 3.1.2-10
- Remove all requires
- Correct usage of xmvn's macros

* Mon Jan 28 2013 Michal Srb <msrb@redhat.com> - 3.1.2-9
- Build with xmvn

* Fri Nov 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-8
- Remove README

* Fri Nov 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-7
- Repackage tarball

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-6
- Don't try to build extension modules unless they are needed

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-5
- Conditionalize %%install section too

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-4
- Conditionally disable extensions

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-3
- Update to new add_maven_depmap macro

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.2-2
- Use new generated maven filelist feature from javapackages-tools

* Fri Oct  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-1
- Complete rewrite of the spec file
- New upstream, to ease future maintenance
- Build with maven instead of ant
- Split into multiple subpackages

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.7.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.6.rc2
- Temporary fix for maven buildroots

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.5.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.4.rc2
- Build with aqute-bnd (#745176)
- Use new maven macros
- Few packaging tweaks

* Tue May 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.3.rc2
- Add cglib and atinject to R

* Thu May 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.2.rc2
- Remove test and missing deps from pom.xml

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.1.rc2
- Update to 3.0rc2
- Changes according to new guidelines (versionless jars & javadocs)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4.1219svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-3.1219svn
- Add java-devel >= 1:1.6.0 to BR

* Wed Oct 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-2.1219svn
- Moved munge repacking to prep
- Added -Dversion to change generated manifest version
- Removed http part of URL

* Thu Oct  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-1.1219svn
- Initial version of the package
