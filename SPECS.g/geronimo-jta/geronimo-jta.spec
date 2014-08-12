%global spec_name geronimo-jta_1.1_spec

Name:		geronimo-jta
Version:	1.1.1
Release:	17%{?dist}
Summary:	J2EE JTA v1.1 API

Group:		Development/Libraries
License:	ASL 2.0
URL:		http://geronimo.apache.org/
# svn export http://svn.apache.org/repos/asf/geronimo/specs/tags/%{spec_name}-%{version}/
Source0:	%{spec_name}-%{version}.tar.bz

BuildArch:	noarch

# This pulls in almost all of the required java and maven stuff
BuildRequires:  maven-local
BuildRequires:	geronimo-parent-poms
BuildRequires:	maven-resources-plugin

# Ensure a smooth transition from geronimo-specs
Provides:	jta = %{version}-%{release}
Obsoletes:	geronimo-specs <= 1.0-3.3
Obsoletes:	geronimo-specs-compat <= 1.0-3.3

%description
Java Transaction API (JTA) specifies standard Java interfaces between a
transaction manager and the parties involved in a distributed transaction
system: the resource manager, the application server, and the transactional
applications.

%package javadoc
Summary:	API documentation for %{name}
Group:		Documentation
BuildArch:	noarch

%description javadoc
%{summary}.

%prep
%setup -q -n %{spec_name}-%{version}


%build
%mvn_file  : %{name} %{spec_name} jta
%mvn_alias : javax.transaction:jta
%mvn_alias : org.eclipse.jetty.orbit:javax.transaction
%mvn_build -f

%install
%mvn_install

%pre javadoc
# workaround for rpm bug, can be removed in F-20
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-16
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.1-14
- Add depmap for org.eclipse.jetty.orbit
- Resolves: rhbz#917622

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1.1-12
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 1.1.1-11
- Build with xmvn

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-8
- Build with Maven 3
- Fix packaging problems

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 12 2010 Alexander Kurtakov <akurtako@redhat.com> 1.1.1-6
- Add javax.transaction:jta depmap.

* Fri Apr  2 2010 Mary Ellen Foster <mefoster at gmail.com> 1.1.1-5
- Add the *correct* version to the geronimo-specs Obsoletes line
- Also Obsolete geronimo-specs-compat

* Tue Mar 16 2010 Mary Ellen Foster <mefoster at gmail.com> 1.1.1-4
- Don't require geronimo-parent-poms at runtime

* Wed Feb 10 2010 Mary Ellen Foster <mefoster at gmail.com> 1.1.1-3
- Add a version to the geronimo-specs Obsoletes line

* Wed Feb 10 2010 Mary Ellen Foster <mefoster at gmail.com> 1.1.1-2
- Clean up provides list, and obsolete geronimo-specs
- Change summary and javadoc description

* Wed Feb  3 2010 Mary Ellen Foster <mefoster at gmail.com> 1.1.1-1
- Initial package
