Name:           nifticlib
Version:        2.0.0
Release:        5%{?dist}
Summary:        A set of i/o libraries for reading and writing files in the nifti-1 data format

License:        Public Domain
URL:            http://niftilib.sourceforge.net/
Source0:        http://downloads.sourceforge.net/niftilib/%{name}-%{version}.tar.gz

BuildRequires:  zlib-devel doxygen cmake
#Requires:       

%description
Nifticlib is a set of C i/o libraries for reading and writing files in
the nifti-1 data format. nifti-1 is a binary file format for storing
medical image data, e.g. magnetic resonance image (MRI) and functional
MRI (fMRI) brain images.

%package devel
Summary: Libraries and header files for nifticlib development
Requires: %{name} = %{version}-%{release}

%description devel
The nifticlib-devel package contains the header files and libraries
necessary for developing programs that make use of the nifticlib library.

%package docs
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}

%description docs
The package contains documentation and example files for %{name}.

%prep
%setup -q
sed -i "s|csh|$SHELL|" Makefile

%build
# make the doc
make doc %{?_smp_mflags}

# cmake replaces the original makefile so I call it after generating my docs
%cmake -DBUILD_SHARED_LIBS=ON .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

## hack to get this to work for x86_64
%if "%{_lib}" == "lib64" 
    install -p -d $RPM_BUILD_ROOT/%{_libdir}/
    mv -v $RPM_BUILD_ROOT/usr/lib/* $RPM_BUILD_ROOT/%{_libdir}/
    rm -rvf $RPM_BUILD_ROOT/usr/lib/
%endif

install -p -d $RPM_BUILD_ROOT/%{_docdir}/%{name}/docs/
install -p -d $RPM_BUILD_ROOT/%{_docdir}/%{name}/examples/

# remove extra files
rm -fv docs/html/installdox
rm -fv docs/html/Doxy*
cp -av docs/* $RPM_BUILD_ROOT/%{_docdir}/%{name}/docs/
cp -av examples/* $RPM_BUILD_ROOT/%{_docdir}/%{name}/examples/

%files
%defattr(-,root,root,-)
%doc README LICENSE Updates.txt
%{_bindir}/*
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/nifti/

%files docs
%defattr(-,root,root,-)
%{_docdir}/%{name}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 06 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.0.0-3
- spec bump for gcc 4.7 rebuild

* Tue Jul 26 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.0.0-2
- Correct source URL

* Fri Jun 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.0.0-1
- initial rpm build
- based on the spec built by Andy Loening <loening at alum dot mit dot edu> in the source tar
