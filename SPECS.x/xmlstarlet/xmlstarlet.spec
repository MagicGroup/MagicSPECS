Name: xmlstarlet
Version:	1.6.1
Release:	3%{?dist}
Summary: Command Line XML Toolkit
Summary(zh_CN.UTF-8): 命令行的 XML 工具
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
License: MIT
URL: http://xmlstar.sourceforge.net/
Source0: http://downloads.sourceforge.net/xmlstar/%{name}-%{version}.tar.gz

# https://sourceforge.net/p/xmlstar/bugs/109/
Patch0: xmlstarlet-1.6.1-nogit.patch

# http://sourceforge.net/tracker/?func=detail&aid=3266898&group_id=66612&atid=515106
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: xmlto automake autoconf libxslt-devel
BuildRequires: libxml2-devel >= 2.6.23

%description
XMLStarlet is a set of command line utilities which can be used
to transform, query, validate, and edit XML documents and files
using simple set of shell commands in similar way it is done for
plain text files using UNIX grep, sed, awk, diff, patch, join, etc
commands.
%description -l zh_CN.UTF-8
命令行的 XML 工具，可以传输，查询，校验和编辑 XML 文档。

%prep
%setup -q
%patch0 -p1 -b .nogit


%build
autoreconf -i
%configure --disable-static-libs --with-libxml-include-prefix=%{_includedir}/libxml2 --docdir=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}} # --libdir=%{_libdir}
make %{?_smp_mflags}


%install
rm -fr %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT
# Avoid name kluGroup(zh_CN.UTF-8):ing in autotools
mv $RPM_BUILD_ROOT%{_bindir}/xml $RPM_BUILD_ROOT%{_bindir}/xmlstarlet


%check
make check


%clean
rm -fr %{buildroot}


%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README Copyright TODO 
%{_mandir}/man1/xmlstarlet.1*
%{_bindir}/xmlstarlet
%{_docdir}/%{name}-%{version}/*

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.6.1-3
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 1.6.1-2
- 更新到 1.6.1

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.3.1-3
- 为 Magic 3.0 重建

* Wed Feb 15 2012 Paul W. Frields <stickster@gmail.com> - 1.3.1-2
- Fix build with configure flag

* Wed Feb 15 2012 Paul W. Frields <stickster@gmail.com> - 1.3.1-1
- Update to upstream 1.3.1 (#782066)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct  3 2011 Paul W. Frields <stickster@gmail.com> - 1.3.0-1
- Update to upstream 1.3.0

* Fri Aug 26 2011 Paul W. Frields <stickster@gmail.com> - 1.2.1-1
- Update to upstream 1.2.1

* Sun Apr 10 2011 Paul W. Frields <stickster@gmail.com> - 1.1.0-1
- Update to upstream 1.1.0

* Thu Apr 07 2011 Dan Horák <dan[at]danny.cz> - 1.0.6-2
- fix build on 64-bit big-endians

* Sat Mar 26 2011 Paul W. Frields <stickster@gmail.com> - 1.0.6-1
- Update to upstream 1.0.6
- Drop obsolete patch

* Thu Feb 17 2011 Paul W. Frields <stickster@gmail.com> - 1.0.5-1
- Update to upstream 1.0.5
- Update libxml2 requirement
- Drop unnecessary patch, naming issue fixed upstream

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Paul W. Frields <stickster@gmail.com> - 1.0.4-1
- Update to new upstream 1.0.4
- Drop patches for fixed upstream issues

* Fri Dec 17 2010 Paul W. Frields <stickster@gmail.com> - 1.0.3-1
- Update to new upstream 1.0.3
- Add %%check section for validation testing

* Mon Nov  1 2010 Paul W. Frields <stickster@gmail.com> - 1.0.2-1
- Update to new upstream 1.0.2

* Sun Jan 10 2010 Paul W. Frields <stickster@gmail.com> - 1.0.1-9
- Correct source URL

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Mar 21 2008 Paul W. Frields <stickster@gmail.com> - 1.0.1-6
- Rebuild to use FORTIFY_SOURCE correctly

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-5
- Autorebuild for GCC 4.3

* Sat Sep  2 2006 Paul W. Frields <stickster@gmail.com> - 1.0.1-4
- Bump release for FC6 mass rebuild

* Fri Feb 17 2006 Paul W. Frields <stickster@gmail.com> - 1.0.1-3
- FESCo mandated rebuild

* Wed Nov 23 2005 Paul W. Frields <stickster@gmail.com> - 1.0.1-2
- Minor changes per review

* Tue Nov 22 2005 Paul W. Frields <stickster@gmail.com> - 1.0.1-1.2
- Improve patching to conquer inconsistent naming

* Tue Nov 22 2005 Paul W. Frields <stickster@gmail.com> - 1.0.1-1.1
- Initial RPM version


