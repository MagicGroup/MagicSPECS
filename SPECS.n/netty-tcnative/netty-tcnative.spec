%global namedreltag .Fork2
%global namedversion %{version}%{?namedreltag}

Name:           netty-tcnative
Version:        1.1.30
Release:        2%{?dist}
Summary:        Fork of Tomcat Native with improved OpenSSL and mavenized build
License:        ASL 2.0
URL:            https://github.com/netty/netty/wiki/Forked-Tomcat-Native
Source0:        https://github.com/netty/netty-tcnative/archive/%{name}-%{namedversion}.tar.gz
Source1:        CheckLibrary.java
Patch1:         fixLibNames.patch.in
Patch2:         i388aprFix.patch

BuildRequires:  maven-local
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  glibc-devel
BuildRequires:  apr-devel
BuildRequires:  openssl-devel
BuildRequires:  maven-hawtjni-plugin
#parent pom is needed
BuildRequires:  netty
BuildRequires: mvn(kr.motd.maven:os-maven-plugin)


%description
netty-tcnative is a fork of Tomcat Native. It includes a set of changes
contributed by Twitter, Inc, such as:
 *  Simplified distribution and linkage of native library
 *  Complete mavenization of the project
 *  Improved OpenSSL support
To minimize the maintenance burden, we create a dedicated branch for each stable
upstream release and apply our own changes on top of it, while keeping the
number of maintained branches to minimum


%package javadoc
Summary:   API documentation for %{name}
Group:     Documentation
BuildArch: noarch

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{name}-%{namedversion}
patch=`mktemp`
sed "s;@PATH@;%{_libdir}/%{name};g" < %{PATCH1} > $patch
patch -p1 < $patch
%patch2 -p1


%build
%mvn_build -f

%install
%mvn_install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/
cp target/native-build/target/lib/lib%{name}-%{namedversion}.so $RPM_BUILD_ROOT%{_libdir}/%{name}/lib%{name}.so


%check
javac -d . -cp $RPM_BUILD_ROOT%{_jnidir}/%{name}/%{name}.jar %{SOURCE1}
#don't know how to test load(path) without more and more patching, however the test class can be used for manual testing
#java -cp .:$RPM_BUILD_ROOT%%{_jnidir}/%%{name}/%%{name}.jar CheckLibrary


%files -f .mfiles
%dir %{_libdir}/%{name}
%dir %{_jnidir}/%{name}
%dir %{_mavenpomdir}/%{name}
%{_libdir}/%{name}/lib%{name}.so

%files javadoc -f .mfiles-javadoc

%changelog
* Mon Jul 13 2015 Jiri Vanek <jvanek@redhat.com> - 1.1.30-2
- adapted to parent pom, enabled kr.motd.maven:os-maven-plugin and added buildrequires dependence 

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 18 2015 Jiri Vanek <jvanek@redhat.com> - 1.1.30-1
- removed manual requires

* Thu Jan 29 2015 Jiri Vanek <jvanek@redhat.com> - 1.1.30-0
- initial build
