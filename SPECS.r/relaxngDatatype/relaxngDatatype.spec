Name:           relaxngDatatype
Version:        1.0
Release:        12.5%{?dist}
Summary:        RELAX NG Datatype API
License:        BSD
URL:            https://sourceforge.net/projects/relaxng
# wget http://netcologne.dl.sourceforge.net/project/relaxng/datatype%20%28java%29/Ver.%{version}/%{name}-%{version}.zip
Source0:        http://netcologne.dl.sourceforge.net/project/relaxng/datatype%20%28java%29/Ver.%{version}/%{name}-%{version}.zip
Source1:        http://repo1.maven.org/maven2/%{name}/%{name}/20020414/%{name}-20020414.pom
Patch0:         %{name}-compressjar.patch

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6

%description
RELAX NG is a public space for test cases and other ancillary software
related to the construction of the RELAX NG language and its
implementations.

%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
This package provides %{name}.

%prep
%setup -q
%patch0 -p0
sed -i s/// copying.txt doc/stylesheet.css

%build
ant -Dbuild.sysclasspath=only

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 %{name}.jar $RPM_BUILD_ROOT%{_javadir}/

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Workaround for RPM bug (symlink was changed to directory).
# TODO: Remove this in F-22
%pretrans javadoc -p <lua>
dir = "%{_javadocdir}/%{name}"
dummy = posix.readlink(dir) and os.remove(dir)

%files -f .mfiles
%doc copying.txt

%files javadoc
%doc copying.txt
%doc %{_javadocdir}/%{name}

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-11.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-10.5
- Install license file with javadoc package
- Convert versioned javadoc to versionless
- Update to current packaging guidelines
- Remove msv provides and obsoletes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Michal Srb <msrb@redhat.com> - 1.0-9.4
- Source0 is now URL (Resolves: #875884)

* Fri Nov  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-8.4
- Add maven POM

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar  8 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.0-5.3
- Added missing Requires: jpackage-utils (%%{_javadir} and %%{_javadocdir})

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-3.2
- drop repotag

* Mon Feb 12 2007 Andrew Overholt <overholt@redhat.com> 1.0-3jpp.1
- Fixed issues for Fedora-ization
- Add patch to compress the main jar

* Tue Apr 11 2006 Ralph Apel <r.apel@r-apel.de>- 0:1.0-3jpp
- First JPP-1.7 release

* Wed Aug 25 2004 Fernando Nasser <fnasser@redhat.com>- 0:1.0-2jpp
- Require Ant > 1.6
- Rebuild with Ant 1.6.2

* Tue Jul 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-1jpp
- First JPackage build from sources

