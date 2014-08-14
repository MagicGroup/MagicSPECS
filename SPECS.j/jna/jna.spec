Name:           jna
Version:        4.1.0
Release:        4%{?dist}
Summary:        Pure Java access to native libraries

Group:          Development/Libraries
License:        LGPLv2+
URL:            https://jna.dev.java.net/
# The source for this package was pulled from upstream's vcs. Use the
# following commands to generate the tarball:
#   https://github.com/twall/jna/tarball/%{version}
#   tar xzf twall-jna-%{version}*.tar.gz
#   mv twall-jna-* jna-%{version}
#   rm -rf jna-%{version}/{dist/*,www}
#   tar cjf ~/rpm/SOURCES/jna-%{version}.tar.gz jna-%{version}
Source0:        https://github.com/twall/jna/archive/%{name}-%{version}.tar.gz
Source1:	package-list
Patch0:         jna-3.5.0-build.patch
# This patch is Fedora-specific for now until we get the huge
# JNI library location mess sorted upstream
Patch1:         jna-4.0.0-loadlibrary.patch
# The X11 tests currently segfault; overall I think the X11 JNA stuff is just a 
# Really Bad Idea, for relying on AWT internals, using the X11 API at all,
# and using a complex API like X11 through JNA just increases the potential
# for problems.
Patch2:         jna-4.0.0-tests-headless.patch
# Build using GCJ javadoc
Patch3:         jna-3.5.2-gcj-javadoc.patch
# junit cames from rpm
Patch4:         jna-4.1.0-junit.patch
Patch6:         jna-4.0.0-ffi.patch
Patch7:         jna-4.0.0-fix-native-test.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# We manually require libffi because find-requires doesn't work
# inside jars.
Requires:       java, jpackage-utils, libffi
Requires(post):	jpackage-utils
Requires(postun): jpackage-utils
BuildRequires:  java-devel, jpackage-utils, libffi-devel
BuildRequires:  ant, ant-junit, junit
%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires:	ant-nodeps, ant-trax
%endif
BuildRequires:  libX11-devel, libXt-devel
# for ExclusiveArch see bug: 468831 640005 548099
%if 0%{?fedora} < 10 && 0%{?rhel} < 6
ExclusiveArch: %{ix86} x86_64
%endif


%description
JNA provides Java programs easy access to native shared libraries
(DLLs on Windows) without writing anything but Java code. JNA's
design aims to provide native access in a natural way with a
minimum of effort. No boilerplate or generated code is required.
While some attention is paid to performance, correctness and ease
of use take priority.


%package        javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
%if 0%{?fedora} || 0%{?rhel} > 5
BuildArch:      noarch
%endif


%description    javadoc
This package contains the javadocs for %{name}.


%package        contrib
Summary:        Contrib for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-examples
%if 0%{?fedora} || 0%{?rhel} > 5
BuildArch:      noarch
%endif


%description    contrib
This package contains the contributed examples for %{name}.


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .
%patch0 -p1 -b .build
%patch1 -p1 -b .loadlib
sed -i 's|@JNIPATH@|%{_libdir}/%{name}|' src/com/sun/jna/Native.java
%patch2 -p1 -b .tests-headless
chmod -Rf a+rX,u+w,g-w,o-w .
%patch3 -p0 -b .gcj-javadoc
%patch4 -p1 -b .junit
%patch6 -p1 -b .ffi
%patch7 -p1

# all java binaries must be removed from the sources
#find . -name '*.jar' -delete
rm lib/junit.jar
find . -name '*.class' -delete

# remove internal copy of libffi
rm -rf native/libffi

# clean LICENSE.txt
sed -i 's/\r//' LICENSE

chmod -c 0644 LICENSE OTHERS CHANGES.md


%build
# We pass -Ddynlink.native which comes from our patch because
# upstream doesn't want to default to dynamic linking.
#ant -Dcflags_extra.native="%{optflags}" -Ddynlink.native=true native compile javadoc jar contrib-jars
ant -Dcflags_extra.native="%{optflags}" -Ddynlink.native=true native dist
# remove compiled contribs
find contrib -name build -exec rm -rf {} \; || :

%install
rm -rf %{buildroot}

# jars
install -D -m 644 build/%{name}-min.jar %{buildroot}%{_javadir}/%{name}.jar
install -d -m 755 %{buildroot}%{_javadir}/%{name}
find contrib -name '*.jar' -exec cp {} %{buildroot}%{_javadir}/%{name}/ \;
# NOTE: JNA has highly custom code to look for native jars in this
# directory.  Since this roughly matches the jpackage guidelines,
# we'll leave it unchanged.
install -d -m 755 %{buildroot}%{_libdir}/%{name}
install -m 755 build/native*/libjnidispatch*.so %{buildroot}%{_libdir}/%{name}/

%if 0%{?fedora} >= 9 || 0%{?rhel} > 5
# install maven pom file
install -Dm 644 pom-%{name}.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
install -Dm 644 pom-%{name}-platform.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-platform.pom

# ... and maven depmap
%if 0%{?fedora} >= 9
%add_maven_depmap JPP-%{name}.pom %{name}.jar
%add_maven_depmap JPP.%{name}-%{name}-platform.pom -f platform %{name}/%{name}-platform.jar -a "net.java.dev.jna:platform"
%else
%add_to_maven_depmap net.java.dev.jna jna-platform %{version} JPP jna-platform
mv %{buildroot}%{_mavendepmapfragdir}/%{name} %{buildroot}%{_mavendepmapfragdir}/%{name}-platform
%add_to_maven_depmap net.java.dev.jna %{name} %{version} JPP %{name}
%endif
%endif

# javadocs
install -p -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -a doc/javadoc/* %{buildroot}%{_javadocdir}/%{name}


#%if 0%{?rhel} >= 6 || 0%{?fedora} >= 9
#%if 0%{?fedora} >= 9
#%ifnarch ppc s390 s390x
#%check
#ant -Dcflags_extra.native="%{optflags}" -Ddynlink.native=true -Dnomixedjar.native=true test
#%endif
#%endif


%clean
rm -rf %{buildroot}


%if 0%{?rhel} > 5
%post
%update_maven_depmap

%postun
%update_maven_depmap

%post contrib
%update_maven_depmap

%postun contrib
%update_maven_depmap
%endif


%files
%defattr(-,root,root,-)
%doc LICENSE OTHERS README.md CHANGES.md TODO
%{_libdir}/%{name}
%{_javadir}/%{name}.jar
%if 0%{?fedora} >= 9 || 0%{?rhel} > 5
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%endif


%files javadoc
%defattr(-,root,root,-)
%doc LICENSE
%{_javadocdir}/%{name}


%files contrib
%defattr(-,root,root,-)
%{_javadir}/%{name}
%if 0%{?fedora} >= 9 || 0%{?rhel} > 5
%{_mavenpomdir}/JPP.%{name}-%{name}-platform.pom
%{_mavendepmapfragdir}/%{name}-platform
%endif


%changelog
* Fri Jan 10 2014 Roland Grunberg <rgrunber@redhat.com> - 4.0.0-4
- fix updated depmap

* Fri Jan 10 2014 Roland Grunberg <rgrunber@redhat.com> - 4.0.0-3
- Update depmap calls and fix tests compilation issue.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul  6 2013 Levente Farkas <lfarkas@lfarkas.org> - 4.0-1
- Update to 4.0

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.5.2-2
- Fix ant-trax and ant-nodeps BR on RHEL

* Thu Apr 25 2013 Levente Farkas <lfarkas@lfarkas.org> - 3.5.2-1
- Update to 3.5.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Levente Farkas <lfarkas@lfarkas.org> - 3.4.0-4
- fix #833786 by Mary Ellen Foster 

* Wed Mar 14 2012 Juan Hernandez <juan.hernandez@redhat.com> - 3.4.0-3
- Generate correctly the maven dependencies map (#)

* Sun Mar 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.4.0-2
- Don't strip binaries too early, build with $RPM_LD_FLAGS (#802020).

* Wed Mar  7 2012 Levente Farkas <lfarkas@lfarkas.org> - 3.4.0-1
- Update to 3.4.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.2.7-11
- Drop dependency on main package from -javadoc.
- Add license to -javadoc, and OTHERS and TODO to main package docs.
- Install javadocs and jars unversioned.
- Fix release-notes.html permissions.
- Make -javadoc and -contrib noarch where available.

* Fri Dec  3 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-10
- fix pom file name #655810
- disable check everywhere since it seems to always fail in mock

* Fri Nov  5 2010 Dan Horák <dan[at]danny.cz> - 3.2.7-9
- exclude checks on s390(x)

* Tue Oct 12 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-8
- exclude check on ppc

* Fri Oct  8 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-7
- fix excludearch condition

* Wed Oct  6 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-6
- readd excludearch for old release fix #548099

* Fri Oct 01 2010 Dennis Gilmore <dennis@ausil.us> - 3.2.7-5.1
- remove the ExcludeArch it makes no sense

* Sun Aug  1 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-5
- reenable test and clean up contrib files

* Tue Jul 27 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-4
- add Obsoletes for jna-examples

* Sat Jul 24 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-3
- upstream 64bit fixes

* Fri Jul 23 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-2
- Temporary hack for 64bit build

* Thu Jul 22 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-1
- Rebase on upstream 3.2.7

* Wed Jul 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-6
- Add maven depmap

* Thu Apr 22 2010 Colin Walters <walters@verbum.org> - 3.2.4-5
- Add patches to make the build happen with gcj

* Wed Apr 21 2010 Colin Walters <walters@verbum.org> - 3.2.4-4
- Fix the build by removing upstream's hardcoded md5

* Thu Dec 17 2009 Levente Farkas <lfarkas@lfarkas.org> - 3.2.4-3
- add proper ExclusiveArch

* Thu Dec 17 2009 Alexander Kurtakov <akurtako@redhat.com> 3.2.4-2
- Comment rhel ExclusiveArchs - not correct applies on Fedora.

* Sat Nov 14 2009 Levente Farkas <lfarkas@lfarkas.org> - 3.2.4-1
- Rebase on upstream 3.2.4

* Thu Oct 29 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.9-6
- Add examples subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Colin Walters <walters@redhat.com> - 3.0.9-3
- Add patch to allow opening current process

* Sun Nov 30 2008 Colin Walters <walters@redhat.com> - 3.0.9-2
- Fix library mapping, remove upstreamed patches

* Fri Oct 31 2008 Colin Walters <walters@redhat.com> - 3.0.9-1
- Rebase on upstream 3.0.9

* Tue Oct 14 2008 Colin Walters <walters@redhat.com> - 3.0.4-10.svn729
- Add patch to support String[] returns

* Wed Oct 01 2008 Colin Walters <walters@redhat.com> - 3.0.4-9.svn729
- Add new patch to support NativeMapped[] which I want

* Wed Oct 01 2008 Colin Walters <walters@redhat.com> - 3.0.4-8.svn729
- Update to svn r729
- drop upstreamed typemapper patch

* Thu Sep 18 2008 Colin Walters <walters@redhat.com> - 3.0.4-7.svn700
- Add patch to make typemapper always accessible
- Add patch to skip cracktastic X11 test bits which currently fail

* Tue Sep 09 2008 Colin Walters <walters@redhat.com> - 3.0.4-5.svn700
- Update to upstream SVN r700; drop all now upstreamed patches

* Sat Sep 06 2008 Colin Walters <walters@redhat.com> - 3.0.4-3.svn630
- A few more patches for JGIR

* Thu Sep 04 2008 Colin Walters <walters@redhat.com> - 3.0.4-2.svn630
- Add two (sent upstream) patches that I need for JGIR

* Thu Jul 31 2008 Colin Walters <walters@redhat.com> - 3.0.4-1.svn630
- New upstream version, drop upstreamed patch parts
- New patch jna-3.0.4-nomixedjar.patch which ensures that we don't
  include the .so in the .jar

* Fri Apr 04 2008 Colin Walters <walters@redhat.com> - 3.0.2-7
- Add patch to use JPackage-compatible JNI library path
- Do build debuginfo package
- Refactor build patch greatly so it's hopefully upstreamable
- Install .so directly to JNI directory, rather than inside jar
- Clean up Requires/BuildRequires (thanks Mamoru Tasaka)

* Sun Mar 30 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-6
- -javadocs should be -javadoc.
- %%files section cleaned a bit.

* Mon Mar 17 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-5
- -javadocs package should be in group "Documentation".

* Mon Mar 17 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-4
- License should be LGPLv2+, not GPLv2+.
- Several minor fixes.
- Fix Requires in javadoc package.

* Sun Mar 16 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-3
- Don't use internal libffi.

* Thu Mar 6 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-2
- Don't pull in jars from the web.

* Mon Mar 3 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-1
- Initial package.
