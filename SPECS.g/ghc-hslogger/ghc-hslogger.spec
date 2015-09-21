# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name hslogger

Name:           ghc-%{pkg_name}
Version:        1.2.6
Release:        3%{?dist}
Summary:        Versatile logging framework

License:        BSD
Url:            https://hackage.haskell.org/package/%{pkg_name}
Source0:        https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-unix-devel
# End cabal-rpm deps

%description
Hslogger is a logging framework for Haskell, roughly similar to Python's
logging module.

hslogger lets each log message have a priority and source be associated with
it. The programmer can then define global handlers that route or filter
messages based on the priority and source. hslogger also has a syslog handler
built in.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
%ghc_lib_install


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE


%files devel -f %{name}-devel.files


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.2.6-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Jens Petersen <petersen@redhat.com> - 1.2.6-1
- update to 1.2.6

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Jens Petersen <petersen@redhat.com> - 1.2.1-4
- update to cblrpm-0.8.11

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 05 2013 Jens Petersen <petersen@redhat.com> - 1.2.1-1
- update to 1.2.1
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 1.1.5-7
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.1.5-5
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.1.5-4
- rebuild

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 1.1.5-3
- add license to ghc_files

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 1.1.5-2
- update to cabal2spec-0.25.2

* Sun Jan 01 2012 Bruno Wolff III <bruno@wolff.to> - 1.1.5-1.4
- Rebuild for libHSnetwork update so that test hegdewars can be built

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.5-1.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.5-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.1.5-1.1
- rebuild with new gmp

* Sat Aug 27 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.5-1
- package update to 1.1.5
- upgrade to cabal2spec 0.24
- license change from LGPLv2 to BSD

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 1.1.4-2
- BR ghc-Cabal-devel instead of ghc-prof (cabal2spec-0.23.2)

* Fri Mar 11 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.4-1
- upgrade to hslogger-1.1.4

* Fri Mar 11 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.3-5
- Rebuild for ghc-7.0.2

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.3-4
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 1.1.3-3
- rebuild for haskell-platform-2011.1 updates
- bump network dependency for haskell-platform-2011.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 1 2011 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.1.3-1
- upstream package update to 1.1.3

* Thu Jan 6 2011 Lakshmi Narasimhan <lakshminaras2002@gmail.com> - 1.1.0-6
- rebuild for new ghc changes
- updating to cabal2spec-0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 1.1.0-5
- rebuild

* Sun Nov 28 2010 Lakshmi Narasimhan <lakshminaras2002@gmail.com> - 1.1.0-4
- Rebuilding for ghc7

* Fri Sep 3 2010 Lakshmi Narasimhan <lakshminaras2002@gmail.com> - 1.1.0-3
- Modified the way COPYING is put into the package, using mkdir and install commands
- Added explicit permissions in install command as the COPYING file in package had execute permissions

* Wed Sep 1 2010 Lakshmi Narasimhan <lakshminaras2002@gmail.com> - 1.1.0-2
- Added COPYING to the list of files to be included in the doc folder.
- The presence of doc directive wipes out COPYRIGHT from BUILD directory. COPYRIGHT would have been copied during cabal install. Hence it has to be included explicitly in .files. If this problem was not there, only COPYING need to put.

* Thu Aug 26 2010 Lakshmi Narasimhan <lakshminaras2002@gmail.com> - 1.1.0-1
- source package updated from 1.0.10 to 1.1.0

* Tue Aug 24 2010 Lakshmi Narasimhan <lakshminaras2002@gmail.com> - 1.0.10-3
- updated using cabal2spec-0.22.2 and ghc-rpm-macros-0.8.1
- corrected LICENSE string to LGPLv2+

* Sat Jul  3 2010 Lakshmi Narasimhan <lakshminaras2002@gmail.com> - 1.0.10-2
- updated using cabal2spec-0.22.1
- Updated to use ghc_lib_package, ghc_lib_build, ghc_lib_install macros instead of cabal macros

* Tue May 25 2010 Lakshmi Narasimhan <lakshminaras2002@gmail.com> - 1.0.10-1
- initial packaging for Fedora automatically generated by cabal2spec-0.21.3
