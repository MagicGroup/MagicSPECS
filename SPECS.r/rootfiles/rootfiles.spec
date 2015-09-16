Summary: The basic required files for the root user's directory.
Summary(zh_CN.UTF-8): root 用户目录的基本需要文件
Name: rootfiles
Version: 8.1
Release: 5%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: dot-bashrc
Source1: dot-bash_profile
Source2: dot-bash_logout
Source3: dot-tcshrc
Source4: dot-cshrc

BuildRoot: %{_tmppath}/%{name}%{name}-root
BuildArchitectures: noarch

%description
The rootfiles package contains basic required files that are placed
in the root user's account.  These files are basically the same
as those in /etc/skel, which are placed in regular
users' home directories.

%description -l zh_CN.UTF-8
rootfiles包包含了在root账户里放置的基本需求文件。
这个文件和有/etc/skel中的一样，它们会放在普通用户的目录。

%prep

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/root

for file in %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} ; do 
  f=`basename $file`
  install -m 644 $file $RPM_BUILD_ROOT/root/${f/dot-/.}
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) /root/.[A-Za-z]*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 8.1-5
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 8.1-4
- 为 Magic 3.0 重建

* Sat Feb 04 2012 Liu Di <liudidi@gmail.com> - 8.1-3
- 为 Magic 3.0 重建

* Tue Jan 09 2007 Liu Di <liudidi@gamil.com> - 8-2mgc
- rebuild for Magic

* Wed Sep 22 2004 Bill Nottingham <notting@redhat.com> 8-1
- sync files with current /etc/skel stuff
- remove Xresources (#75666)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 7.2-5
- rebuild 

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jul  5 2001 Preston Brown <pbrown@redhat.com> 7.2-1
- /sbin stuff out of PATH, moved into /etc/profile

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Preston Brown <pbrown@redhat.com>
- fix .tcshrc

* Mon Jul  3 2000 Jakub Jelinek <jakub@redhat.com>
- don't assume ASCII ordering in glob pattern

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- rebuild
- fix some path stuff (#11191)

* Tue Apr 18 2000 Bill Nottingham <notting@redhat.com>
- mv .Xdefaults -> .Xresources (#10623)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- add %clean (#719)

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Wed Oct  9 1998 Bill Nottingham <notting@redhat.com>
- remove /root from %files (it's in filesystem)

* Sun Aug 23 1998 Jeff Johnson <jbj@redhat.com>
- portability fix for .cshrc (problem #235)
- change version to be same as release.

* Tue Sep 09 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

* Thu Mar 20 1997 Erik Troan <ewt@redhat.com>
- Removed .Xclients and .Xsession from package, added %pre to back up old
  .Xclients if necessary.
