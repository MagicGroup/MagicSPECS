Name:           itstool
Version:        2.0.2
Release:        1%{?dist}
Summary:        ITS-based XML translation tool
Summary(zh_CN.UTF-8): 基于 ITS 的 XML 翻译工具

Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:        GPLv3+
URL:            http://itstool.org/
Source0:        http://files.itstool.org/itstool/%{name}-%{version}.tar.bz2

BuildArch:      noarch
Requires:       libxml2-python

%description
ITS Tool allows you to translate XML documents with PO files, using rules from
the W3C Internationalization Tag Set (ITS) to determine what to translate and
how to separate it into PO file messages.

%description -l zh_CN.UTF-8
ITS 工具允许你使用 PO 文件翻译 XML 文档，使用 W3C 的标准 国际化标签集（ITS）来
检测需要翻译什么和怎么在 PO 文件中分隔信息。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%files
%doc COPYING COPYING.GPL3 NEWS
%{_bindir}/itstool
%{_datadir}/itstool
%doc %{_mandir}/man1/itstool.1.gz

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.0-2
- 为 Magic 3.0 重建

* Mon Jul 02 2012 Kalev Lember <kalevlember@gmail.com> 1.2.0-1
- Update to 1.2.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> 1.1.2-1
- Update to itstool 1.1.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 19 2011 Shaun McCance <shaunm@gnome.org> 1.1.1-1
- Update to itstool 1.1.1

* Sun Aug 07 2011 Rahul Sundaram <sundaram@fedoraproject.org> 1.1.0-2
- Add requires on libxml2-python since itstool uses it
- Drop redundant defattr
- Add NEWS to doc

* Mon Jun 27 2011 Shaun McCance <shaunm@gnome.org> 1.1.0-1
- Update to itstool 1.1.0

* Sun May 8 2011 Shaun McCance <shaunm@gnome.org> 1.0.1-1
- Initial packaging
