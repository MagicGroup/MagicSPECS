Name:           apache-ivy
Version:        2.3.0
Release:        10%{?dist}
Summary:        Java-based dependency manager

License:        ASL 2.0
URL:            http://ant.apache.org/ivy/
Source0:        http://www.apache.org/dist/ant/ivy/%{version}/%{name}-%{version}-src.tar.gz
BuildArch:      noarch

# Non-upstreamable.  Add /etc/ivy/ivysettings.xml at the end list of
# settings files Ivy tries to load.  This file will be used only as
# last resort, when no other setting files exist.
Patch0:         %{name}-global-settings.patch

Provides:       ivy = %{version}-%{release}

BuildRequires:  ant
BuildRequires:  ant-contrib
BuildRequires:  ant-testutil
BuildRequires:  apache-commons-vfs
BuildRequires:  bouncycastle
BuildRequires:  bouncycastle-pg
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  jsch
BuildRequires:  jakarta-oro
BuildRequires:  ivy-local >= 3.5.0-2
BuildRequires:  maven-local

%description
Apache Ivy is a tool for managing (recording, tracking, resolving and
reporting) project dependencies.  It is designed as process agnostic and is
not tied to any methodology or structure. while available as a standalone
tool, Apache Ivy works particularly well with Apache Ant providing a number
of powerful Ant tasks ranging from dependency resolution to dependency
reporting and publication.

%package javadoc
Summary:        API Documentation for ivy
Group:          Development/Tools

%description javadoc
JavaDoc documentation for %{name}

%prep
%setup -q
%patch0

# Fix messed-up encodings
for F in RELEASE_NOTES README LICENSE NOTICE CHANGES.txt
do
        sed 's/\r//' $F |iconv -f iso8859-1 -t utf8 >$F.utf8
        touch -r $F $F.utf8
        mv $F.utf8 $F
done
# ant-trax has been obsoleted, use main ant package
sed -i s/ant-trax/ant/ ivy.xml

# Fedora bouncycastle packages provide -jdk16 artifacts only
sed -i /bouncycastle/s/jdk14/jdk16/ ivy.xml

# Port from commons-vfs 1.x to 2.x
sed -i "s/commons.vfs/&2/" src/java/org/apache/ivy/plugins/repository/vfs/*

# Remove prebuilt documentation
rm -rf doc build/doc

%build
%ant -Divy.mode=local -Dtarget.ivy.bundle.version=%{version} -Dtarget.ivy.bundle.version.qualifier= -Dtarget.ivy.version=%{version} jar javadoc


%install
%mvn_file : %{name} ivy
%mvn_artifact ivy.xml build/artifact/jars/ivy.jar
sed -i "/rawPom/{p;s//effectivePom/g}" .xmvn-reactor
%mvn_install -J build/doc/reports/api

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "ivy" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{name}

%files -f .mfiles
%{_sysconfdir}/ant.d/%{name}
%doc LICENSE NOTICE RELEASE_NOTES CHANGES.txt README

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.3.0-10
- 为 Magic 3.0 重建

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-9
- BuildRequire ivy-local >= 3.5.0-2

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-8
- Build with ivy-local
- Add patch for global settings

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.0-7
- Remove prebuilt documentation in %%prep
- Install NOTICE file with javadoc subpackage

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.0-6
- Restore PGP signing ability
- Remove unneeded R

* Thu Dec 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-5
- Enable VFS resolver

* Wed Dec  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4
- Install POM files, resolves: rhbz#1032258
- Remove explicit requires; auto-requires are in effect now

* Fri Nov  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-3
- Add Maven depmap

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 1 2013 Alexander Kurtakov <akurtako@redhat.com> 2.3.0-1
- Update to latest upstream.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-5
- Fix osgi metadata.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-2
- Fix ant integration.

* Fri Feb 25 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-1
- Update to 2.2.0.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 09 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.0-1
- Initial Fedora packaging
