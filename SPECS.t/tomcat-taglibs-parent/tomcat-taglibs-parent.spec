Name:           tomcat-taglibs-parent
Version:        3
Release:        4%{?dist}
Summary:        Apache Taglibs Parent

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://tomcat.apache.org/taglibs/
Source0:        http://svn.apache.org/repos/asf/tomcat/taglibs/taglibs-parent/tags/taglibs-parent-3/pom.xml
BuildArch: noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

%description
Apache Taglibs Parent pom used for building purposes.

%prep
%setup -q -c -T
cp -p %{SOURCE0} .

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_mavenpomdir}/%{name}

%changelog
* Thu Nov 19 2015 Liu Di <liudidi@gmail.com> - 3-4
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 4 2015 Alexander Kurtakov <akurtako@redhat.com> 3-2
- Fix review issues.

* Wed Mar 4 2015 Alexander Kurtakov <akurtako@redhat.com> 3-1
- Initial package.
