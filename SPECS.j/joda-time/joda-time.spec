%global tzversion tzdata2013g

Name:             joda-time
Version:          2.3
Release:          5.%{tzversion}%{?dist}
Summary:          Java date and time API

License:          ASL 2.0
URL:              http://joda-time.sourceforge.net
Source0:          http://downloads.sourceforge.net/%{name}/%{name}-%{version}-dist.tar.gz
Source1:          ftp://ftp.iana.org/tz/releases/%{tzversion}.tar.gz
BuildArch:        noarch

BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    maven-local
BuildRequires:    joda-convert
BuildRequires:    exec-maven-plugin


%description
Joda-Time provides a quality replacement for the Java date and time classes. The
design allows for multiple calendar systems, while still providing a simple API.
The 'default' calendar is the ISO8601 standard which is used by XML. The
Gregorian, Julian, Buddhist, Coptic, Ethiopic and Islamic systems are also
included, and we welcome further additions. Supporting classes include time
zone, duration, format and parsing.


%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' NOTICE.txt
sed -i 's/\r//' RELEASE-NOTES.txt

# all java binaries must be removed from the sources
find . -name '*.jar' -exec rm -f '{}' \;

# replace internal tzdata
rm -f src/main/java/org/joda/time/tz/src/*
tar -xzf %{SOURCE1} -C src/main/java/org/joda/time/tz/src/

# compat filename
%mvn_file : %{name}

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt RELEASE-NOTES.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.3-5.tzdata2013g
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.3-4.tzdata2013g
- 为 Magic 3.0 重建

* Tue Aug 12 2014 Liu Di <liudidi@gmail.com> - 2.3-3.tzdata2013g
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2.tzdata2013g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 16 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3-1.tzdata2013g
- Update to latest upstream and tzdata2013g

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2.tzdata2013c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun  5 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-1.tzdata2013c
- Update to latest upstream and tzdata
- Install NOTICE.txt

* Tue Jun  4 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-5.tzdata2012h
- Enable testsuite
- Update to lates packaging guidelines

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4.tzdata2012h
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.1-3.tzdata2012h
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 1 2012 Chris Spike <spike@fedoraproject.org> 2.1-2.tzdata2012h
- New tzdata (2012h)

* Sat Oct 20 2012 Chris Spike <spike@fedoraproject.org> 2.1-1.tzdata2012g
- Updated to 2.1
- New tzdata (2012g)
- Updated spec file according to latest java packaging guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-8.tzdata2011f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-7.tzdata2011f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 1.6.2-6.tzdata2011f
- Adapt to current guidelines.

* Fri Apr 15 2011 Chris Spike <spike@fedoraproject.org> 1.6.2-5.tzdata2011f
- New tzdata (2011f)
- Fixed build for maven 3
- Cleaned up BRs

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-4.tzdata2010n
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Chris Spike <spike@fedoraproject.org> 1.6.2-3.tzdata2010n
- New tzdata (2010n)

* Thu Sep 23 2010 Chris Spike <spike@fedoraproject.org> 1.6.2-2.tzdata2010l
- Ignore test failures (tests fail in koji)

* Thu Sep 23 2010 Chris Spike <spike@fedoraproject.org> 1.6.2-1.tzdata2010l
- New upstream version (1.6.2)
- Removed dependency on main package for -javadoc subpackage
- Replaced summary with latest version
- Switched from ant to maven (no build.xml any more)
- Added patch to remove maven toolchain from pom.xml

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3.tzdata2008i
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2.tzdata2008i
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Conrad Meyer <konrad@tylerc.org> - 1.6-1.tzdata2008i
- New upstream version (1.6).

* Fri Oct 31 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-10.tzdata2008i
- New tzdata.

* Mon Oct 13 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-7.tzdata2008g
- New tzdata (2008g).

* Sat Aug 23 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-7.tzdata2008e
- New version with new tzdata (2008e).

* Sat Jul 19 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-7.tzdata2008d
- New version with new tzdata (2008d).

* Mon Jun 9 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-6.tzdata2008c
- New version with new tzdata (2008c).

* Sun Apr 6 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-5.tzdata2008b
- Don't compile GCJ bits yet as we hit some GCJ bug.

* Sat Apr 5 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-4.tzdata2008b
- Update to tzdata2008b.
- Use unversioned jar.
- Some small things to comply with Java Packaging Guidelines.
- GCJ support.

* Mon Mar 17 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-3.tzdata2008a
- Many small changes from bz# 436239 comment 6.
- Change -javadocs to -javadoc in accordance with java packaging
  guidelines draft.

* Sun Mar 16 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-2
- Use system junit via Mamoru Tasaka's patch.

* Mon Mar 3 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-1
- Initial package.
