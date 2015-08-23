%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

Summary:       Python bindings for CUPS
Name:          python-cups
Version:       1.9.72
Release:       3%{?dist}
URL:           http://cyberelk.net/tim/software/pycups/
Source:        http://cyberelk.net/tim/data/pycups/pycups-%{version}.tar.bz2
License:       GPLv2+
Group:         Development/Languages
BuildRequires: cups-devel
BuildRequires: python2-devel python3-devel
BuildRequires: epydoc

%description
This package provides Python bindings for CUPS API,
known as pycups. It was written for use with
system-config-printer, but can be put to other uses as well.

%package -n python3-cups
Summary:       Python3 bindings for CUPS API, known as pycups.
Group:         Development/Languages

%description -n python3-cups
This package provides Python bindings for CUPS API,
known as pycups. It was written for use with
system-config-printer, but can be put to other uses as well.

This is a ported release for python 3

%package doc
Summary:       Documentation for python-cups
Group:         Documentation

%description doc
Documentation for python-cups.

%prep
%setup -q -n pycups-%{version}

rm -rf %{py3dir}
cp -a . %{py3dir}

%build
make CFLAGS="%{optflags} -fno-strict-aliasing"
make doc

pushd %{py3dir}
%py3_build
popd


%install
make install DESTDIR="%{buildroot}"

pushd %{py3dir}
%py3_install
chmod 755 %{buildroot}%{python3_sitearch}/cups*.so
popd



%files
%doc COPYING README NEWS TODO
%{python_sitearch}/cups.so
%{python_sitearch}/pycups*.egg-info

%files -n python3-cups
%doc COPYING README NEWS
%{python3_sitearch}/cups.cpython-3*.so
%{python3_sitearch}/pycups*.egg-info
%{_rpmconfigdir}/fileattrs/psdriver.attr
%{_rpmconfigdir}/postscriptdriver.prov

%files doc
%doc examples html

%changelog
* Tue Aug 11 2015 Jiri Popelka <jpopelka@redhat.com> - 1.9.72-3
- %%py3_build && %%py3_install

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 10 2015 Tim Waugh <twaugh@redhat.com> - 1.9.72-1
- Latest upstream release.

* Thu Jan 15 2015 Tim Waugh <twaugh@redhat.com> - 1.9.70-3
- Only ship the postscriptdriver rpm-provides script in python3-cups
  as it is a python3 script.

* Mon Jan 12 2015 Tim Waugh <twaugh@redhat.com> - 1.9.70-2
- Fixes for IPP constants (bug #1181043, bug #1181055).

* Tue Dec 23 2014 Tim Waugh <twaugh@redhat.com> - 1.9.70-1
- 1.9.70.

* Sat Dec 13 2014 Tim Waugh <twaugh@redhat.com> - 1.9.69-2
- Fixed password_callback so it obtains UTF-8 password correctly
  (bug #1155469).

* Thu Dec  4 2014 Tim Waugh <twaugh@redhat.com> - 1.9.69-1
- 1.9.69.

* Mon Oct  6 2014 Tim Waugh <twaugh@redhat.com> - 1.9.68-1
- 1.9.68.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 20 2014 Tim Waugh <twaugh@redhat.com> - 1.9.67-1
- 1.9.67, fixing a Connection.getFile crash.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.66-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.9.66-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Nov 27 2013 Jiri Popelka <jpopelka@redhat.com> - 1.9.66-1
- 1.9.66 - Python 3 support.

* Wed Nov 27 2013 Tim Waugh <twaugh@redhat.com> - 1.9.65-1
- 1.9.65.

* Wed Jul 31 2013 Jiri Popelka <jpopelka@redhat.com> - 1.9.63-4
- Fix getting of booleans.

* Fri Apr 12 2013 Tim Waugh <twaugh@redhat.com> - 1.9.63-3
- Propagate UTF-8 decoding errors.

* Thu Apr 11 2013 Tim Waugh <twaugh@redhat.com> - 1.9.63-2
- Encode generated URIs correctly (bug #950162).

* Wed Mar 20 2013 Tim Waugh <twaugh@redhat.com> - 1.9.63-1
- 1.9.63.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

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
