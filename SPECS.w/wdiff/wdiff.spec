Name:           wdiff
Version:	1.2.2
Release:	2%{?dist}
Summary:        A front-end to GNU diff
Summary(zh_CN.UTF-8): GNU diff 的前端

Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License:        GPLv3+
URL:            http://www.gnu.org/software/%{name}/
Source0:        http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  automake
BuildRequires:  gettext-devel
BuildRequires:  libtool  
BuildRequires:  texinfo  

Requires(post): info
Requires(preun): info

#https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = 30.5.2012

%description
`wdiff' is a front-end to GNU `diff'.  It compares two files, finding
which words have been deleted or added to the first in order to create
the second.  It has many output formats and interacts well with
terminals and pagers (notably with `less').  `wdiff' is particularly
useful when two texts differ only by a few words and paragraphs have
been refilled.

%description -l zh_CN.UTF-8
GNU diff 的前端。

%prep
%setup -q -n %{name}-%{version}
iconv --from=ISO-8859-1 --to=UTF-8 ChangeLog > ChangeLog.new && \
touch -r ChangeLog ChangeLog.new && \
mv ChangeLog.new ChangeLog

%build
%configure --enable-experimental="mdiff wdiff2 unify" 
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
find $RPM_BUILD_ROOT -type f -name '*gnulib.mo' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name}

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc NEWS  README TODO  ChangeLog  AUTHORS
%{_bindir}/*
%{_mandir}/man1/*.1.gz
%{_infodir}/%{name}.info.gz


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 1.2.2-2
- 为 Magic 3.0 重建

* Mon Oct 19 2015 Liu Di <liudidi@gmail.com> - 1.2.2-1
- 更新到 1.2.2

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.2.1-3
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 1.2.1-1
- New release 

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 1.1.2-1
- New release and fixed no bundled library issue

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 16 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 1.1.0-1
- New release

* Thu Oct 20 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 1.0.1-1
- New release

* Thu Sep 8 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 1.0.0-1
- New release

* Fri Mar 4 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.6.5-5
- Fix change log issue 

* Tue Mar 1 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.6.5-4
- Add find language tag

* Tue Mar 1 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.6.5-3
- Removed unnecessary -gnulib translation files.
- Rpmlint warning fixed for ChangeLog not utf8 file.
- Adding %%doc files

* Tue Mar 1 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.6.5-2
- Fix license,buildroot issue. Add find language tag.

* Tue Mar 1 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.6.5-1
- Initial version of the package
