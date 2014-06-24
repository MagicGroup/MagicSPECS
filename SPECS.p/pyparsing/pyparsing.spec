%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

Name:           pyparsing
Version:        1.5.6
Release:        7%{?dist}
Summary:        An object-oriented approach to text processing
Group:          Development/Libraries
License:        MIT
URL:            http://pyparsing.wikispaces.com/
Source0:        http://downloads.sourceforge.net/pyparsing/pyparsing-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  dos2unix
BuildRequires:  glibc-common

%if 0%{?with_python3}
BuildRequires: python3-devel
%endif # if with_python3

%description
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

%package doc
Summary:        Documentation for pyparsing
Group:          Development/Libraries

%description doc
The package contains documentation for pyparsing.

%if 0%{?with_python3}
%package -n python3-pyparsing
Summary:        An object-oriented approach to text processing (Python 3 version)
Group:          Development/Libraries

%description -n python3-pyparsing
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

This is the Python 3 version.
%endif # if with_python3

%prep
%setup -q
mv docs/pyparsingClassDiagram.PNG docs/pyparsingClassDiagram.png
rm docs/pyparsingClassDiagram.JPG
dos2unix -k CHANGES LICENSE
dos2unix -k docs/examples/*
dos2unix -k docs/htmldoc/epydoc*
for f in CHANGES docs/examples/{holaMundo.py,mozillaCalendarParser.py} ; do
    mv $f $f.iso88591
    iconv -f ISO-8859-1 -t UTF-8 -o $f $f.iso88591
    touch -r $f.iso88591 $f
    rm -f $f.iso88591
done

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}

# Install python 3 first, so that python 2 gets precedence:
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES README LICENSE
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%{python_sitelib}/pyparsing*egg-info
%endif
%{python_sitelib}/pyparsing.py*

%if 0%{?with_python3}
%files -n python3-pyparsing
%defattr(-,root,root,-)
%doc CHANGES README LICENSE
%{python3_sitelib}/pyparsing*egg-info
%{python3_sitelib}/pyparsing.py*
%endif # with_python3
%if ( 0%{?fedora} >= 15 || 0%{?rhel} >= 7 ) && 0%{?with_python3}
%{python3_sitelib}/__pycache__/pyparsing*
%endif # pycache

%files doc
%defattr(-,root,root,-)
%doc CHANGES README LICENSE docs/*

%changelog
* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 1.5.6-7
- 为 Magic 3.0 重建

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 1.5.6-6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 1.5.6-5
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 David Malcolm <dmalcolm@redhat.com> - 1.5.6-2
- fix __pycache__ conditional on RHEL

* Fri Jul  1 2011 José Matos <jamatos@fedoraproject.org> - 1.5.6-1
- New upstream version.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 21 2010 Terje Rosten <terje.rosten@ntnu.no> - 1.5.5-1
- 1.5.5
- use buildroot macro
- fix wrong file end of line encoding
- convert files to utf-8
- doc subpackage
- python3 subpackage
- rpmlint clean

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 16 2010 Dan Horák <dan[at]danny.cz> - 1.5.0-6
- include egginfo on EL >= 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.5.0-3
- Rebuild for Python 2.6

* Mon Aug  4 2008 José Matos <jamatos[AT]fc.up.pt> - 1.5.0-2
- respun (now with the right sources)

* Mon Aug  4 2008 José Matos <jamatos[AT]fc.up.pt> - 1.5.0-1
- new upstream release.

* Tue Apr  1 2008 José Matos <jamatos[AT]fc.up.pt> - 1.4.11-1
- New upstream version, add egg-info for F9+.

* Wed Aug 29 2007 José Matos <jamatos[AT]fc.up.pt> - 1.4.7-1
- New upstream version.

* Sat Apr 21 2007 José Matos <jamatos[AT]fc.up.pt> - 1.4.6-1
- New upstream version.

* Mon Dec 11 2006 José Matos <jamatos[AT]fc.up.pt> - 1.4.4-1
- New upstream version.

* Mon Sep 11 2006 José Matos <jamatos[AT]fc.up.pt> - 1.4.3-1
- New version.

* Wed Aug  3 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.3-1
- Initial RPM release
