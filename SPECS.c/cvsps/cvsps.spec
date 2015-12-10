%global prever  b1

Name:           cvsps
Version:        2.2
Release:        0.13.%{prever}%{?dist}
Summary:        Patchset tool for CVS
Summary(zh_CN.UTF-8): CVS 用的补丁工具集

Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:        GPL+
URL:            http://www.cobite.com/cvsps/
Source0:        http://www.cobite.com/cvsps/%{name}-%{version}%{prever}.tar.gz
# https://bugzilla.redhat.com/516083
Patch0:         %{name}-2.2b1-dynamic-logbuf.patch
Patch1:         %{name}-2.2b1-man.patch
Patch2:         %{name}-2.2b1-bufferoverflow.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  zlib-devel
# Strictly speaking, requires cvs only with --no-cvs-direct (which is
# the default as of 2.2b1), but this shouldn't be a problem on systems
# where cvsps will be installed.
Requires: cvs

%description
CVSps is a program for generating 'patchset' information from a CVS
repository.  A patchset in this case is defined as a set of changes
made to a collection of files, and all committed at the same time
(using a single 'cvs commit' command).  This information is valuable
to seeing the big picture of the evolution of a cvs project.  While
cvs tracks revision information, it is often difficult to see what
changes were committed 'atomically' to the repository.

%description -l zh_CN.UTF-8
CVS 用的补丁工具集。

%prep
%setup -q -n %{name}-%{version}%{prever}
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
CFLAGS="$RPM_OPT_FLAGS -DLINUX" make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGELOG COPYING README merge_utils.sh
%{_bindir}/cvsps
%{_mandir}/man1/cvsps.1*


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.2-0.13.b1
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.2-0.12.b1
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.2-0.10.b1
- 为 Magic 3.0 重建

* Mon Feb 14 2011 Honza Horak <hhorak@redhat.com> - 2.2-0.8.b1
- Patch to fix buffer overflow.
- https://bugzilla.redhat.com/show_bug.cgi?id=576076

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 18 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.2-0.6.b1
- Patch to fix man page formatting errors.

* Tue Dec 22 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.2-0.5.b1
- Build with -DLINUX to fix --cvs-direct on 64-bit platforms (#539765).
- Use patch instead of sed for man page fixes.

* Thu Aug  6 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.2-0.4.b1
- Apply David D. Kilzer's dynamic log buffer allocation patch (#516083,
  Andreas Schwab).
- Use %%global instead of %%define.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-0.3.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jun 14 2008 Ville Skyttä <ville.skytta@iki.fi> - 2.2-0.1.b1
- 2.2b1.

* Sat Feb  9 2008 Ville Skyttä <ville.skytta@iki.fi> - 2.1-6
- Change cvs dependency to a Requires(hint).
- Fix typo in man page.

* Thu Aug 16 2007 Ville Skyttä <ville.skytta@iki.fi> - 2.1-5
- License: GPL+

* Tue Aug 29 2006 Ville Skyttä <ville.skytta@iki.fi> - 2.1-4
- Rebuild.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta@iki.fi> - 2.1-3
- Rebuild.

* Fri May 27 2005 Ville Skyttä <ville.skytta@iki.fi> - 2.1-2
- 2.1.

* Sun Mar 20 2005 Ville Skyttä <ville.skytta@iki.fi> - 2.0-0.2.rc1
- Drop 0.fdr and Epoch: 0.

* Sun Sep 14 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:2.0-0.fdr.0.2.rc1
- Remove #---- section markers.

* Fri Jul  4 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:2.0-0.fdr.0.1.rc1
- First build.
