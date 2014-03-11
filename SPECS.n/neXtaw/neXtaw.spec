Summary:        Modified version of the Athena Widgets with N*XTSTEP appearance
Name:           neXtaw
Version:        0.15.1
Release:        16%{?dist}

URL:            http://siag.nu/neXtaw/
Source0:        http://siag.nu/pub/neXtaw/%{name}-%{version}.tar.gz
License:        MIT
Group:          System Environment/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  libXext-devel
BuildRequires:  libXt-devel
BuildRequires:  libXmu-devel

%description
neXtaw is a replacement library for the Athena (libXaw) widget set. It
is based on Xaw3d, by Kaleb Keithley and is almost 100% backward
compatible with it. Its goal is to try to emulate the look and feel of
the N*XTSTEP GUI.

%package        devel
Summary:        Development files for the neXtaw library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libXmu-devel
Requires:       libXt-devel

%description devel
neXtaw is a replacement library for the Athena (libXaw) widget set. It
is based on Xaw3d, by Kaleb Keithley and is almost 100% backward
compatible with it. Its goal is to try to emulate the look and feel of
the N*XTSTEP GUI. This package contains the development files of the
neXtaw library.


%prep
%setup -q
f=README ; iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f


%build
%configure --disable-static --disable-dependency-tracking \
    --x-libraries=%{_libdir}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __docs
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
cp -a doc __docs
rm __docs/{Makefile*,TODO,app-defaults/Makefile*}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO __docs/*
%{_libdir}/libneXtaw.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/neXtaw/
%{_libdir}/libneXtaw.so


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.15.1-16
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 0.15.1-15
- 为 Magic 3.0 重建

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  9 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.15.1-12
- Include more docs, convert README to UTF-8.

* Mon Aug  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.15.1-11
- License: MIT

* Mon Aug 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.15.1-10
- Rebuild.

* Sun Jun  4 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.15.1-9
- Fix linkage on lib64 archs.
- Drop static lib build option.

* Mon Feb 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.15.1-8
- Rebuild.

* Fri Nov 11 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.15.1-7
- Adapt to modular X11 packaging.
- Don't ship static libraries by default.
- Build with dependency tracking disabled.
- Use "rm" instead of %%exclude.
- Specfile cleanups.

* Sat Jun 25 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.15.1-6
- Rebuild.

* Sun Jun 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.15.1-5
- Require X devel in -devel.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.15.1-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.15.1-2
- rebuilt

* Thu Oct  2 2003 Dams <anvil[AT]livna.org> 0:0.15.1-0.fdr.1
- Updated to 0.15.1
- Removed marker after scriptlets

* Tue Sep  2 2003 Dams <anvil[AT]livna.org> 0:0.15.0-0.fdr.1
- Updated to 0.15.0

* Thu May  8 2003 Dams <anvil[AT]livna.org> 0:0.14.0-0.fdr.3
- Modified BuildRoot
- Modified defattr
- Added doc files
- Buildroot -> RPM_BUILD_ROOT
- Added post/postun scriptlets
- Exclude ".la" files.
- Added missing epoch in -devel Requires.
- Added missing BuildRequires

* Mon Mar 31 2003 Dams <anvil[AT]livna.org> 0:0.14.0-0.fdr.2
- Added Epoch

* Tue Mar 25 2003 Dams <anvil[AT]livna.org> 0.fdr.1
- modified spec according to fedora template

* Sat Feb 22 2003 Dams <anvil[AT]livna.org>
- Initial build.
