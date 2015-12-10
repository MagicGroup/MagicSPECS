%global namewithoutpythonprefix %(echo %{name} | sed 's/^python-//')

Name:           python-pydns
Version:        2.3.6
Release:        6%{?dist}
Summary:        Python module for DNS (Domain Name Service)
Summary(zh_CN.UTF-8): DNS 的 Python 模块

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        Python
URL:            http://pydns.sourceforge.net/
Source0:        http://download.sourceforge.net/pydns/pydns-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

%description
This is a another release of the pydns code, as originally written by
Guido van Rossum, and with a hopefully nicer API bolted over the
top of it by Anthony Baxter <anthony@interlink.com.au>.

This package contains a module (dnslib) that implements a DNS
(Domain Name Server) client, plus additional modules that define some
symbolic constants used by DNS (dnstype, dnsclass, dnsopcode).

%description -l zh_CN.UTF-8
DNS 的 Python 模块。

%prep
%setup -q -n %{namewithoutpythonprefix}-%{version}

# Some files are latin-1 encoded but are incorrectly labelled as UTF-8 by
# upstream (see rhbz:620265)
#
# Convert them to actually be UTF-8, preserving the (now-correct) encoding
# declaration (preserving timestamps):
for file in DNS/Lib.py DNS/Type.py ; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
magic_rpm_clean.sh

%files
%defattr(-,root,root,-)
%doc CREDITS.txt PKG-INFO README-guido.txt README.txt
%dir %{python_sitelib}/DNS
%{python_sitelib}/DNS/*.py*
%{python_sitelib}/pydns-%{version}-py*.egg-info

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.3.6-6
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.3.6-5
- 为 Magic 3.0 重建

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 2.3.6-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Adam Williamson <awilliam@redhat.com> - 2.3.6-1
- update to latest upstream, modernize spec

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug  1 2010 David Malcolm <dmalcolm@redhat.com> - 2.3.3-6
- fix encoding issues (rhbz 620265)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.3.3-2
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.3-1
- fix license tag
- update to 2.3.3

* Sun Jan 21 2007 Sean Reifschneider <jafo@tummy.com> 2.3.0-5
- Adding encoding of the Python files.

* Thu Aug 31 2006 Sean Reifschneider <jafo@tummy.com> 2.3.0-4
- Fixing .spec file changelog entries.

* Wed Aug 30 2006 Sean Reifschneider <jafo@tummy.com> 2.3.0-3
- Changes based on Kevin Fenzi's review.

* Wed Aug 30 2006 Sean Reifschneider <jafo@tummy.com> 2.3.0-2
- Changes based on Kevin Fenzi's review.

* Tue Aug 29 2006 Sean Reifschneider <jafo@tummy.com> 2.3.0-1
- Initial RPM spec file.
