#global posttag .final.0

Name:		    scons
Version:	2.4.0
Release:	1%{?dist}
Summary:	    An Open Source software construction tool
Summary(zh_CN.UTF-8): 开源软件的构建工具
Group:		    Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:	    MIT
URL:		    http://www.scons.org
Source:		    http://downloads.sourceforge.net/scons/scons-%{version}%{?posttag}.tar.gz
BuildRoot:	    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	    noarch

BuildRequires:	python2-devel

%description
SCons is an Open Source software construction tool--that is, a build
tool; an improved substitute for the classic Make utility; a better way
to build software.  SCons is based on the design which won the Software
Carpentry build tool design competition in August 2000.

SCons "configuration files" are Python scripts, eliminating the need
to learn a new build tool syntax.  SCons maintains a global view of
all dependencies in a tree, and can scan source (or other) files for
implicit dependencies, such as files specified on #include lines.  SCons
uses MD5 signatures to rebuild only when the contents of a file have
really changed, not just when the timestamp has been touched.  SCons
supports side-by-side variant builds, and is easily extended with user-
defined Builder and/or Scanner objects.

%description -l zh_CN.UTF-8
开源软件的构建工具，

%prep

%setup -q -n %{name}-%{version}%{?posttag}
sed -i 's|/usr/bin/env python|/usr/bin/python|' script/*
# Convert to utf-8
for file in *.txt; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --root=%{buildroot} \
    --no-version-script \
	--standalone-lib \
    --install-scripts=%{_bindir} \
    --install-data=%{_datadir}
 
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES.txt LICENSE.txt README.txt RELEASE.txt
%{_bindir}/*
%{_prefix}/lib/scons
%{_mandir}/man?/*

%changelog
* Sat Sep 26 2015 Liu Di <liudidi@gmail.com> - 2.4.0-1
- 更新到 2.4.0

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 2.3.1-3
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.1-1
- Update to new upstream version 2.3.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 09 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.0-1
- Update to new upstream version 2.3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 29 2012 Fabian Affolter <mail@fabian-affolter.ch> - 2.2.0-1
- Update to new upstream version 2.2.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 10 2011 Fabian Affolter <mail@fabian-affolter.ch> - 2.1.0-1
- Update to new upstream version 2.1.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 23 2010 Chen Lei <supercyper@163.com> - 2.0.1-1
- new release 2.0.1

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.0-2.final.0
- recompiling .py files against Python 2.7 (rhbz#623357)

* Thu Jul 08 2010 Chen Lei <supercyper@163.com> - 2.0.0-1.final.0
- new release 2.0.0.final.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 25 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.2.0-1
- Update to 1.2.0 to fix problems with Python 2.6 (#475903)
  (currently causing broken deps with other packages)

* Thu Dec 18 2008 Gerard Milmeister <gemi@bluewin.ch> - 1.1.0-1
- new release 1.1.0

* Fri Sep  5 2008 Gerard Milmeister <gemi@bluewin.ch> - 1.0.0-1.d20080826
- new release 1.0.0

* Sun Aug  3 2008 Gerard Milmeister <gemi@bluewin.ch> - 0.98.5-1
- new release 0.98.5

* Sun Jun  1 2008 Gerard Milmeister <gemi@bluewin.ch> - 0.98.4-2
- added buildreq sed

* Sat May 31 2008 Gerard Milmeister <gemi@bluewin.ch> - 0.98.4-1
- new release 0.98.4

* Sun May  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 0.98.3-2
- changed shebang line of scripts

* Sun May  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 0.98.3-1
- new release 0.98.3

* Sat Apr 19 2008 Gerard Milmeister <gemi@bluewin.ch> - 0.98.1-1
- new release 0.98.1

* Sat Apr  5 2008 Gerard Milmeister <gemi@bluewin.ch> - 0.98-1
- new release 0.98

* Mon May 21 2007 Gerard Milmeister <gemi@bluewin.ch> - 0.97-1
- new version 0.97

* Thu May 10 2007 Gerard Milmeister <gemi@bluewin.ch> - 0.96.96-1
- new version 0.96.96

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.96.1-3
- Rebuild for FE6

* Sat Jun 18 2005 Gerard Milmeister <gemi@bluewin.ch> - 0.96.1-1
- New Version 0.96.1

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Jan 25 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 0.96-4
- Place libs in {_prefix}/lib/ and not in {libdir}; fixes x86_64 problems
- Adjust minor bits to be in sync with python-spec-template
