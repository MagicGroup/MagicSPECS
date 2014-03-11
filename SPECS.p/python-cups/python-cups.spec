%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

Summary:       Python bindings for CUPS
Name:          python-cups
Version:       1.9.62
Release:       2%{?dist}
URL:           http://cyberelk.net/tim/software/pycups/
Source:        http://cyberelk.net/tim/data/pycups/pycups-%{version}.tar.bz2
License:       GPLv2+
Group:         Development/Languages
BuildRequires: cups-devel
BuildRequires: python2-devel
BuildRequires: epydoc

%description
This package provides Python bindings for the CUPS API,
known as pycups. It was written for use with
system-config-printer, but can be put to other uses as well.

%package doc
Summary:       Documentation for python-cups
Group:         Documentation

%description doc
Documentation for python-cups.

%prep
%setup -q -n pycups-%{version}

%build
make CFLAGS="%{optflags} -fno-strict-aliasing"
make doc

%install
make install DESTDIR="%{buildroot}"

%files
%doc COPYING ChangeLog README NEWS TODO
%{python_sitearch}/cups.so
%{python_sitearch}/pycups*.egg-info
%{_rpmconfigdir}/fileattrs/psdriver.attr
%{_rpmconfigdir}/postscriptdriver.prov

%files doc
%doc examples html

%changelog
* Thu Sep 27 2012 Jiri Popelka <jpopelka@redhat.com> - 1.9.62-2
- Remove unused statements.

* Wed Aug  1 2012 Tim Waugh <twaugh@redhat.com> - 1.9.62-1
- 1.9.62, including fixes for building against newer versions of CUPS.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Tim Waugh <twaugh@redhat.com> - 1.9.61-2
- Apply upstream patch to fix crash on loading invalid PPDs (bug #811159).

* Tue Mar  6 2012 Tim Waugh <twaugh@redhat.com> - 1.9.61-1
- 1.9.61, fixing ref-counting bugs (bug #800143).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Tim Waugh <twaugh@redhat.com> - 1.9.60-1
- 1.9.60.  Constants from CUPS 1.5.0.

* Mon Oct  3 2011 Tim Waugh <twaugh@redhat.com> - 1.9.59-1
- 1.9.59.  Fixes auth loops with CUPS 1.5.0 (bug #734247).

* Thu Jun  9 2011 Tim Waugh <twaugh@redhat.com> - 1.9.57-1
- 1.9.57.  Fixes rpm provides script (bug #712027).

* Sun Mar 20 2011 Tim Waugh <twaugh@redhat.com> - 1.9.55-1
- 1.9.55.  Support for IPP "resolution" type.

* Wed Feb 23 2011 Tim Waugh <twaugh@redhat.com> - 1.9.54-1
- 1.9.54.  The rpm hook is now upstream.

* Wed Feb 23 2011 Tim Waugh <twaugh@redhat.com> - 1.9.53-5
- Use rpmconfigdir macro throughout.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Tim Waugh <twaugh@redhat.com> - 1.9.53-3
- Fixed typo in psdriver.attr that prevented PPD files from being
  scanned when generating postscriptdriver tags.

* Thu Jan 20 2011 Tim Waugh <twaugh@redhat.com> - 1.9.53-2
- Moved postscriptdriver RPM tagging machinery here.  Fixed
  leading/trailing whitespace in tags as well.

* Wed Dec 15 2010 Tim Waugh <twaugh@redhat.com> - 1.9.53-1
- 1.9.53 fixing a thread-local storage issue (bug #662805).

* Wed Nov 17 2010 Jiri Popelka <jpopelka@redhat.com> - 1.9.52-2
- Fixed rpmlint errors/warnings (#648986)
- doc subpackage

* Mon Nov 01 2010 Jiri Popelka <jpopelka@redhat.com> - 1.9.52-1
- Initial RPM spec file
